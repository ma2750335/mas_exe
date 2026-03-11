import mas
import pandas as pd
from datetime import datetime, timedelta
from mas.enum.env_setting import env_type
import json


class mas_client(mas):
    def __init__(self, toggle, log=print, backtest_log=None):
        super().__init__()
        self.close_prices = []  # 儲存收盤價
        self.hold = False       # 是否持倉
        self.last_signal = 0    # 上一次訊號（避免重複進場）
        self.toggle = toggle    # 切換回測與真實交易
        self.order_id = None    # 持倉單order_id
        self.symbol = None      # 商品代碼
        self.volume = 1         # 手續
        self.is_data_recovery = False  # 歷史資料回補
        self.data_recovery_datetime = None  # 歷史資料最後一天回補日
        self.log = log
        self.backtest_log = backtest_log  # 回測 Log callback

    def receive_bars(self, symbol, data, is_end):
        # 每次收到新的 bar，新增收盤價
        self.close_prices.append(data['close'])

        # 在執行檔的部分，判斷回補歷史資料，不進場
        if env_type.exe.value:
            if (self.data_recovery_datetime is not None) and (data['time'].date() <= datetime.strptime(self.data_recovery_datetime, "%Y-%m-%d").date()):
                self.is_data_recovery = True
            else:
                self.is_data_recovery = False

        # 若資料筆數少於10，跳過
        if len(self.close_prices) < 10:
            return

        close_series = pd.Series(self.close_prices[:-1])
        # 計算最近5MA 和 10MA
        ma5 = close_series[-5:].mean()
        ma10 = close_series[-10:].mean()

        current_signal = 1 if ma5 > ma10 else -1
        signal_label = "多方" if current_signal == 1 else "空方"

        # 判斷是否為回補資料
        if not self.is_data_recovery:
            # 回測 Log：市價訊號
            if self.backtest_log:
                bar_time = data['time'].strftime(
                    "%Y-%m-%d %H:%M") if hasattr(data['time'], 'strftime') else str(data['time'])
                self.backtest_log(
                    f"💹 Market Price | {self.symbol} | {bar_time} | close={data['close']:.5f} | MA5={ma5:.5f} | MA10={ma10:.5f} | {signal_label}")

            if not self.hold:
                # 黃金交叉，進場做多
                self.order_id = mas_c.send_order({
                    "symbol": self.symbol,
                    "order_type": "buy",
                    "volume": self.volume,
                    "backtest_toggle": self.toggle
                })
                if env_type.exe.value:
                    self.log(f"Order Open, Order ID: {self.order_id}")
                # 回測 Log：進場
                if self.backtest_log:
                    bar_time = data['time'].strftime(
                        "%Y-%m-%d %H:%M") if hasattr(data['time'], 'strftime') else str(data['time'])
                    self.backtest_log(
                        f"📈 Open Order | {self.symbol} | {bar_time} | close={data['close']:.5f} | OrderID={self.order_id}")
                self.hold = True
            elif self.hold:
                # 死亡交叉，平倉
                mas_c.send_order({
                    "symbol": self.symbol,
                    "order_type": "sell",
                    "volume": self.volume,
                    "order_id": self.order_id,
                    "backtest_toggle": self.toggle
                })
                if env_type.exe.value:
                    self.log(f"Order Close, Order ID: {self.order_id}")
                # 回測 Log：出場
                if self.backtest_log:
                    bar_time = data['time'].strftime(
                        "%Y-%m-%d %H:%M") if hasattr(data['time'], 'strftime') else str(data['time'])
                    self.backtest_log(
                        f"📉 Close Order | {self.symbol} | {bar_time} | close={data['close']:.5f} | OrderID={self.order_id}")
                self.hold = False

        # 更新最近一次的訊號
        self.last_signal = current_signal
        if is_end and self.toggle:
            data = self.generate_data_report()
            data['data']['data_source'] = ""
            if isinstance(data, dict) and 'data' in data:
                print(json.dumps(data.get('data'), ensure_ascii=False))


mas_c = mas_client(toggle=True, log=print)
timeframe = "M1"
symbol = "GOLD_"
volume = float(1)


def get_symbol():
    return symbol


def main(account=123, password="", server="", symbol="",  capital=10000, volume=1, toggle=True, log=print, backtest_log=None):
    # 初始化物件
    mas_c.toggle = toggle
    mas_c.log = log
    mas_c.backtest_log = backtest_log
    # 登入 MT5
    params = {
        "account": account,
        "password": password,
        "server": server
    }
    success = mas_c.login(params)
    mas_c.symbol = symbol
    mas_c.volume = volume
    mas_c.capital = capital

    # 判斷是否開啟程式前，已經進場
    if env_type.exe.value:
        positions = mas_c.get_positions({"symbol": mas_c.symbol})
        for position in positions:
            p_order_id = position['order_id']
            p_symbol = position['symbol']
            p_volume = position['volume']
            if p_symbol == mas_c.symbol and mas_c.volume == p_volume:
                mas_c.hold = True
                mas_c.order_id = p_order_id

    # 若真實交易，請根據所有策略，判斷出需取策略所需要之最大裸K數量，並帶入至kbar
    if toggle == False:
        kbar = 10
        yesterday_str = (datetime.today() - timedelta(days=3)
                         ).strftime("%Y-%m-%d")
        params = {
            "symbol": mas_c.symbol,
            "from": mas_c.get_start_date(yesterday_str, timeframe, kbar),
            "to": yesterday_str,
            "timeframe": timeframe,
            "backtest_toggle": True
        }
        mas_c.data_recovery_datetime = yesterday_str
        mas_c.subscribe_bars(params)
    # 啟動回測
    params = {
        "symbol": mas_c.symbol,
        "from": '2020-01-01',
        "to": '2024-12-31',
        "timeframe": timeframe,
        "capital": mas_c.capital,
        "backtest_toggle": mas_c.toggle
    }
    mas_c.subscribe_bars(params)


def stop_main():
    params = {
        "symbol": symbol,
        "timeframe": timeframe,
    }
    mas_c.unsubscribe_bars(params)


if __name__ == "__main__":
    main()
