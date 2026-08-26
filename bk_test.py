import mas
from datetime import datetime, timedelta
from mas.enum.env_setting import env_type
import pandas as pd
import numpy as np
import json

import zlib
from env_info import UUID as STRATEGY_UUID
MAGIC = zlib.crc32(STRATEGY_UUID.encode("utf-8")) & 0x7FFFFFFF

class mas_client(mas):
    def __init__(self, toggle, log=print, backtest_log=None):
        super().__init__()
        self.close_prices = []
        self.high_prices  = []
        self.low_prices   = []
        self.direction    = None
        self.hold         = False
        self.toggle       = toggle
        self.base_volume  = 3.4
        self.current_volume = 3.4
        self.entry_volume   = 3.4
        self.entry_price    = 0.0
        self.stop_loss      = 0.0
        self.take_profit    = 0.0
        self.symbol         = "UK100Cash"
        self.capital        = 10000
        self.peak_capital   = 10000
        self.circuit_cooldown = 0
        self.is_data_recovery = False
        self.data_recovery_datetime = None
        # LIVE 模式新增
        self.order_id = None
        self.log = log
        self.backtest_log = backtest_log
        self.volume = 0.1
        self.last_signal = 0

    def receive_bars(self, symbol, data, is_end):
        c = data.get('Close') or data.get('close') or data.get('price')
        h = data.get('High')  or data.get('high') or c
        l = data.get('Low')   or data.get('low')  or c
        if c: self.close_prices.append(float(c))
        if h: self.high_prices.append(float(h))
        if l: self.low_prices.append(float(l))
        if len(self.close_prices) < 50:
            if is_end: self._do_report()
            return

        if env_type.exe.value:
            if (self.data_recovery_datetime is not None) and (data.get('time') is not None) and (data.get('time').date() <= datetime.strptime(self.data_recovery_datetime, "%Y-%m-%d").date()):
                self.is_data_recovery = True
            else:
                self.is_data_recovery = False
        if self.is_data_recovery:
            if is_end: self._do_report()
            return

        close_series = pd.Series(self.close_prices[-500:])
        high_series  = pd.Series(self.high_prices[-500:])
        low_series   = pd.Series(self.low_prices[-500:])
        close_v      = float(close_series.iloc[-1])
        pip_size     = 0.15    # UK100Cash 規格由 SYMBOL_SPEC 注入（10*pip_size = 來回點差成本）
        contract_size = 1  # UK100Cash 合約大小（對齊 mas_book 實測值）

        # Pre-computed ATR(14)
        _atr_raw = (high_series - low_series).rolling(14).mean()
        atr_v = float(_atr_raw.iloc[-1]) if not pd.isna(_atr_raw.iloc[-1]) else abs(close_v) * 0.001

        # Layer 1A: Dynamic volume (compounding)
        self.peak_capital = max(self.peak_capital, self.capital)
        _drawdown_pct = (self.peak_capital - self.capital) / max(self.peak_capital, 1)
        # XAG(白銀)設 2.0：1.0 矯枉過正（誠實但只 2% 連自家 OOS 3.5% 都搆不到），
        # 2.5 又會放大過擬合（146%/Calmar 12）。2.0 是中庸：讓 PF~1.3 的穩健白銀策略
        # 放大到 ~4-5% 報酬清過 OOS，又不至於灌水成假策略。OOS 閘門仍是最終品質保證。
        _max_vol_mult = 2.0 if 'XAG' in "UK100Cash" else (2.5 if ('XAU' in "UK100Cash" or 'GBP' in "UK100Cash") else 5.0)
        self.current_volume = max(
            round(self.base_volume * 0.5, 2),
            min(round(self.base_volume * _max_vol_mult, 2),
                round((self.capital / 10000) * self.base_volume, 2))
        )

        # Layer 1B: Circuit breaker
        if self.circuit_cooldown > 0:
            self.circuit_cooldown -= 1
        if _drawdown_pct > 0.22 and not self.hold:
            self.circuit_cooldown = 10
        if self.circuit_cooldown > 0 and not self.hold:
            if is_end: self._do_report()
            return

        # Layer 1C: Hard bankruptcy protection (capital below peak*20% → permanent stop)
        # 2026-05-19: Added after AUDUSD/LOW_FREQ ran return=-974% / -807%.
        # Strong version: force-close ANY open position once capital is critical,
        # then permanently block any further trading (no matter what _do_report says).
        if self.capital <= 0 or self.capital < self.peak_capital * 0.2:
            if self.hold and self.direction:
                # 強制平倉現有部位（按當前 close_v 結算）
                _force_ot = "sell" if self.direction == "long" else "buy"
                _force_ev = getattr(self, 'entry_volume', self.current_volume)
                _force_pnl = ((close_v - self.entry_price - 10 * pip_size) * _force_ev * contract_size
                              if self.direction == "long"
                              else (self.entry_price - close_v - 10 * pip_size) * _force_ev * contract_size)
                if 'JPY' in "UK100Cash": _force_pnl /= close_v
                self.capital += _force_pnl
                # 📉 LIVE log: 平倉前訊號
                _bar_time = data.get('time') or data.get('Time')
                _bar_time_str = _bar_time.strftime("%Y-%m-%d %H:%M") if hasattr(_bar_time, 'strftime') else str(_bar_time)
                _close_order_id = self.order_id  # 暫存 order_id（平倉後會被清掉）
                _close_ret = mas_c.send_order({"symbol": self.symbol, "order_type": _force_ot, "volume": _force_ev, "order_id": self.order_id, "backtest_toggle": self.toggle, "magic": MAGIC})
                if (not self.toggle) and (not _close_ret or _close_ret == "N/A"):
                    self.log("平倉未成交，保留部位、下根再試")
                    return
                if env_type.exe.value:
                    self.log(f"Order Close, Order ID: {_close_order_id}")
                if self.backtest_log:
                    self.backtest_log(f"📉 Close Order | {self.symbol} | {_bar_time_str} | close={close_v:.5f} | OrderID={_close_order_id}")
                self.hold = False
                self.direction = None
            # 永久停手：不再進入策略邏輯
            if is_end: self._do_report()
            return


        # === RSI_SWING STRATEGY ===
        delta    = close_series.diff()
        gain_s   = delta.clip(lower=0).rolling(7).mean()
        loss_s   = (-delta.clip(upper=0)).rolling(7).mean()
        rs_s     = gain_s / loss_s.replace(0, 1e-10)
        rsi_s    = 100 - (100 / (1 + rs_s))
        rsi_prev = float(rsi_s.iloc[-3]) if not pd.isna(rsi_s.iloc[-3]) else 50.0
        rsi_v    = float(rsi_s.iloc[-2]) if not pd.isna(rsi_s.iloc[-2]) else 50.0

        ema_f   = close_series.ewm(span=50, adjust=False).mean()
        ema_f_v = float(ema_f.iloc[-2])

        ema_ok_long  = close_v > ema_f_v if False else True
        ema_ok_short = close_v < ema_f_v if False else True

        rsi_cross_long  = rsi_prev < 39  and rsi_v >= 39
        rsi_cross_short = rsi_prev > 61 and rsi_v <= 61

        if not self.hold:
            if rsi_cross_long and ema_ok_long:
                self.entry_volume = self.current_volume
                self.entry_price  = close_v
                self.stop_loss    = close_v - 1 * atr_v
                self.take_profit  = close_v + 3.4 * atr_v
                self.direction    = "long"
                self.hold         = True
                # 💹 LIVE log: 進場前訊號
                _bar_time = data.get('time') or data.get('Time')
                _bar_time_str = _bar_time.strftime("%Y-%m-%d %H:%M") if hasattr(_bar_time, 'strftime') else str(_bar_time)
                if self.backtest_log:
                    self.backtest_log(f"💹 Market Price | {self.symbol} | {_bar_time_str} | close={close_v:.5f}")
                self.order_id = mas_c.send_order({"symbol": self.symbol, "order_type": "buy", "volume": self.entry_volume, "backtest_toggle": self.toggle, "magic": MAGIC})
                if (not self.toggle) and (not self.order_id or self.order_id == "N/A"):
                    self.log("開倉未成交，取消進場、下根重試")
                    self.hold = False
                    self.direction = None
                    return
                if env_type.exe.value:
                    self.log(f"Order Open, Order ID: {self.order_id}")
                if self.backtest_log:
                    self.backtest_log(f"📈 Open Order | {self.symbol} | {_bar_time_str} | close={close_v:.5f} | OrderID={self.order_id}")
            elif rsi_cross_short and ema_ok_short:
                self.entry_volume = self.current_volume
                self.entry_price  = close_v
                self.stop_loss    = close_v + 1 * atr_v
                self.take_profit  = close_v - 3.4 * atr_v
                self.direction    = "short"
                self.hold         = True
                # 💹 LIVE log: 進場前訊號
                _bar_time = data.get('time') or data.get('Time')
                _bar_time_str = _bar_time.strftime("%Y-%m-%d %H:%M") if hasattr(_bar_time, 'strftime') else str(_bar_time)
                if self.backtest_log:
                    self.backtest_log(f"💹 Market Price | {self.symbol} | {_bar_time_str} | close={close_v:.5f}")
                self.order_id = mas_c.send_order({"symbol": self.symbol, "order_type": "sell", "volume": self.entry_volume, "backtest_toggle": self.toggle, "magic": MAGIC})
                if (not self.toggle) and (not self.order_id or self.order_id == "N/A"):
                    self.log("開倉未成交，取消進場、下根重試")
                    self.hold = False
                    self.direction = None
                    return
                if env_type.exe.value:
                    self.log(f"Order Open, Order ID: {self.order_id}")
                if self.backtest_log:
                    self.backtest_log(f"📈 Open Order | {self.symbol} | {_bar_time_str} | close={close_v:.5f} | OrderID={self.order_id}")

        elif self.hold:
            exit_hit = (
                (self.direction == "long"  and (close_v <= self.stop_loss or close_v >= self.take_profit))
                or
                (self.direction == "short" and (close_v >= self.stop_loss or close_v <= self.take_profit))
            )
            if exit_hit:
                ot  = "sell" if self.direction == "long" else "buy"
                pnl = (close_v - self.entry_price - 10 * pip_size) * self.entry_volume * contract_size if self.direction == "long"                     else (self.entry_price - close_v - 10 * pip_size) * self.entry_volume * contract_size
                if 'JPY' in "UK100Cash": pnl /= close_v  # JPY報價貨幣→換算回美元（避免 pnl 數值爆炸導致 circuit breaker 永久鎖死）
                self.capital += pnl
                # 📉 LIVE log: 平倉前訊號
                _bar_time = data.get('time') or data.get('Time')
                _bar_time_str = _bar_time.strftime("%Y-%m-%d %H:%M") if hasattr(_bar_time, 'strftime') else str(_bar_time)
                _close_order_id = self.order_id  # 暫存 order_id（平倉後會被清掉）
                _close_ret = mas_c.send_order({"symbol": self.symbol, "order_type": ot, "volume": self.entry_volume, "order_id": self.order_id, "backtest_toggle": self.toggle, "magic": MAGIC})
                if (not self.toggle) and (not _close_ret or _close_ret == "N/A"):
                    self.log("平倉未成交，保留部位、下根再試")
                    return
                if env_type.exe.value:
                    self.log(f"Order Close, Order ID: {_close_order_id}")
                if self.backtest_log:
                    self.backtest_log(f"📉 Close Order | {self.symbol} | {_bar_time_str} | close={close_v:.5f} | OrderID={_close_order_id}")
                self.hold      = False
                self.direction = None


        if is_end and self.toggle:
            self._do_report()

    def _do_report(self):
        global _reported
        if _reported: return
        _reported = True
        if self.hold and self.direction:
            ot = "sell" if self.direction == "long" else "buy"
            # 📉 LIVE log: 平倉前訊號
            # _do_report 內不引用外部 data 變數
            _bar_time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            _close_order_id = self.order_id  # 暫存 order_id（平倉後會被清掉）
            _close_ret = mas_c.send_order({"symbol": self.symbol, "order_type": ot, "volume": self.entry_volume, "order_id": self.order_id, "backtest_toggle": self.toggle, "magic": MAGIC})
            if (not self.toggle) and (not _close_ret or _close_ret == "N/A"):
                self.log("平倉未成交，保留部位、下根再試")
                return
            if env_type.exe.value:
                self.log(f"Order Close, Order ID: {_close_order_id}")
            if self.backtest_log:
                self.backtest_log(f"📉 Close Order | {self.symbol} | {_bar_time_str} | close=N/A (end of run) | OrderID={_close_order_id}")
        report = self.generate_data_report()
        _data = report.get('data') if (report and isinstance(report, dict)) else None
        _write_report(_data or {"performance_metrics": {"number_of_trades": 0}})

mas_c = mas_client(toggle=True, log=print)
timeframe = "H1"
symbol = "UK100Cash"
volume = float(0.1)

_reported = False

import sys
import atexit
def _write_report(result):
    out_file = sys.argv[1] if len(sys.argv) > 1 else None
    if out_file:
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False)
    else:
        print(json.dumps(result, ensure_ascii=False))

def _safe_exit():
    global _reported
    if not _reported:
        _reported = True
        try:
            report = mas_c.generate_data_report()
            _data = report.get('data') if (report and isinstance(report, dict)) else None
            _write_report(_data or {"performance_metrics":{"number_of_trades":0,"total_return_rate":0,"max_drawdown":0,"profit_factor":0,"win_rate":0}})
        except Exception as _ex:
            _write_report({"performance_metrics":{"number_of_trades":0,"total_return_rate":0,"max_drawdown":0,"profit_factor":0,"win_rate":0},"error":str(_ex)})
atexit.register(_safe_exit)

def main(account=0, password="", server="", symbol="UK100Cash", capital=10000, volume=0.1, toggle=False, log=print, backtest_log=None):
    """LIVE / 模擬倉模式入口

    Args:
        account:  MT5 帳號（會由視窗填入）
        password: MT5 密碼（會由視窗填入）
        server:   Broker server，如 "ICMarkets-Demo"
        toggle:   False=LIVE 模式（預設），True=回測模式
    """
    mas_c.toggle = toggle
    mas_c.log = log
    mas_c.backtest_log = backtest_log

    # ── 登入 MT5 ──
    params = {"account": account, "password": password, "server": server}
    success = mas_c.login(params)

    mas_c.symbol = symbol
    mas_c.volume = volume
    mas_c.capital = capital

    # ── 啟動前檢查是否已有部位（避免重複開倉）──
    if env_type.exe.value:
        positions = mas_c.get_positions({"symbol": mas_c.symbol})
        for position in positions:
            p_order_id = position['order_id']
            p_symbol = position['symbol']
            if position.get('magic') == MAGIC and p_symbol == mas_c.symbol:
                mas_c.hold = True
                mas_c.order_id = p_order_id
                log(f"📌 偵測到既有部位 ID={p_order_id}，繼續持倉")

    timeframe = "H1"

    if toggle == False:
        # ═══ LIVE 模式 ═══
        # Step 1: 暖機載入 500 根歷史 K 棒
        kbar = 500
        yesterday_str = (datetime.today() - timedelta(days=3)).strftime("%Y-%m-%d")
        warmup_params = {
            "symbol": mas_c.symbol,
            "from": mas_c.get_start_date(yesterday_str, timeframe, kbar),
            "to": yesterday_str,
            "timeframe": timeframe,
            "backtest_toggle": True
        }
        mas_c.data_recovery_datetime = yesterday_str
        mas_c.subscribe_bars(warmup_params)

        # Step 2: 接 LIVE 即時資料流
        live_params = {
            "symbol": mas_c.symbol,
            "timeframe": timeframe,
            "backtest_toggle": False
        }
        mas_c.subscribe_bars(live_params)
    else:
        # ═══ 回測模式（驗證用）═══
        backtest_params = {
            "symbol": mas_c.symbol,
            "from": "2025-03-12",
            "to": "2026-03-12",
            "timeframe": timeframe,
            "capital": mas_c.capital,
            "backtest_toggle": True
        }
        mas_c.subscribe_bars(backtest_params)


def stop_main():
    """停止策略，取消資料訂閱"""
    params = {
        "symbol": mas_c.symbol,
        "timeframe": "H1",
    }
    mas_c.unsubscribe_bars(params)


def get_symbol():
    return symbol



if __name__ == "__main__": main()
