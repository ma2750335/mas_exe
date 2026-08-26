# -*- coding: utf-8 -*-
"""
test_open_close.py — 最小平倉測試：開倉 → 等 60 秒 → 平倉 → 驗證部位真的消失

目的：把策略邏輯全部拿掉，只留「開→等→平」，而且走「跟精靈 exe 完全相同的
      library 路徑」(mas_c.send_order)，最後用 MT5 直接看部位在不在 →
      精準回答「精靈那條平倉路徑到底有沒有真的平掉」。

  - 開倉：mas_c.send_order(order_type=buy)              ← 跟精靈一樣
  - 平倉：mas_c.send_order(order_type=sell, order_id=…) ← 跟精靈一樣（帶 order_id）
  - 驗證：mt5.positions_get()                           ← 直接看 ground truth

用法（跟 bk_test.py / diag_close.py 同一個 python 環境，MT5 終端機開著並登入 demo）：
    python test_open_close.py

⚠️ 會對 demo 帳戶送出真實的開倉/平倉單（demo 安全）。
"""
import time
import MetaTrader5 as mt5
import mas

# ════════════ 設定 ════════════
SYMBOL    = "GOLD_"          # ← 必須填「broker 實際代碼」(XM 黃金=GOLD_)，不是 XAUUSD
DIRECTION = "buy"            # 開倉方向：buy / sell
VOLUME    = 0.01             # 手數（demo 測試用小一點）
WAIT_SEC  = 60              # 開倉後等幾秒才平（題目要的 1 分鐘）

# 只有「MT5 終端機沒登入」時才會用到；已登入就不用管
ACCOUNT  = 0                  # 沒登入才填 demo 帳號（已登入終端機則免）
PASSWORD = ""
SERVER   = ""                 # 沒登入才填，如 "XMGlobal-MT5 7"
# ══════════════════════════════


class _tester(mas):
    def __init__(self):
        super().__init__()


mas_c = _tester()


def positions_on(sym):
    ps = mt5.positions_get(symbol=sym) or []
    return {p.ticket: p for p in ps}


def fmt(p):
    return f"ticket={p.ticket} {'SELL' if p.type == mt5.ORDER_TYPE_SELL else 'BUY'} vol={p.volume} open={p.price_open} pnl={p.profit}"


# ── 連線（已登入的終端機直接接上，不用帳密）──
if not mt5.initialize():
    print("❌ initialize 失敗:", mt5.last_error()); raise SystemExit
if mt5.account_info() is None:
    if not mt5.login(ACCOUNT, password=PASSWORD, server=SERVER):
        print("❌ login 失敗:", mt5.last_error()); mt5.shutdown(); raise SystemExit

ai = mt5.account_info()
print(f"✅ 連上 {ai.login} @ {ai.server}  "
      f"trade_allowed(terminal)={mt5.terminal_info().trade_allowed} (account)={ai.trade_allowed}")
if not mt5.terminal_info().trade_allowed:
    print("⚠️ AutoTrading 沒開（terminal trade_allowed=False）→ 開/平倉都會被退。請先在 MT5 按工具列那顆 AutoTrading。")

# ── 1) 開倉（走 library，跟精靈一樣）──
print(f"\n[1] 開倉 {DIRECTION} {SYMBOL} {VOLUME} …")
before = positions_on(SYMBOL)
oid = mas_c.send_order({"symbol": SYMBOL, "order_type": DIRECTION, "volume": VOLUME, "backtest_toggle": False})
print(f"    send_order 回傳 order_id = {oid!r}")
time.sleep(2)
after_open = positions_on(SYMBOL)
new_tickets = set(after_open) - set(before)
if new_tickets:
    for t in new_tickets:
        print(f"    ✅ 新開部位：{fmt(after_open[t])}")
else:
    print("    ❌ 沒有新增部位 → 開倉就失敗了（看上面 library 印的錯誤）。停。")
    mt5.shutdown(); raise SystemExit

# ── 2) 等 1 分鐘 ──
print(f"\n[2] 等 {WAIT_SEC} 秒後平倉 …")
time.sleep(WAIT_SEC)

# ── 3) 平倉（走 library，帶 order_id，跟精靈一字不差）──
close_dir = "sell" if DIRECTION == "buy" else "buy"
print(f"\n[3] 平倉 {close_dir} {SYMBOL} {VOLUME} order_id={oid} …")
ret = mas_c.send_order({"symbol": SYMBOL, "order_type": close_dir, "volume": VOLUME,
                        "order_id": oid, "backtest_toggle": False})
print(f"    平倉 send_order 回傳 = {ret!r}")
time.sleep(2)

# ── 4) 驗證：MT5 直接看部位還在不在 ──
after_close = positions_on(SYMBOL)
still_open = [t for t in new_tickets if t in after_close]

print("\n══════════════ 結果 ══════════════")
if not still_open:
    print(f"✅✅ 真的平掉了！開的部位 {new_tickets} 已不在持倉 → 精靈的 library 平倉路徑【沒問題】。")
else:
    print(f"❌❌ 沒平掉！部位還在 → 這就是精靈的 bug（送了帶 order_id 的平倉、但部位沒消失）：")
    for t in still_open:
        print(f"    {fmt(after_close[t])}")
    print("   → 對照 diag_close.py（raw MT5 能不能平）就能判斷：")
    print("      • diag_close 能平、這支不能 → bug 在 library 的 send_order")
    print("      • 兩支都不能平 → 是帳戶/環境（AutoTrading、filling、市場關閉…）")
print("══════════════════════════════════")

mt5.shutdown()
print("\n把整段輸出貼給我。")
