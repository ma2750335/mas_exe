# -*- coding: utf-8 -*-
"""
diag_close.py — 直接探測「精靈 exe 平倉為什麼失敗」+ 順手平掉卡單

背景：精靈 LIVE 在 MT5 hedge 帳戶送出平倉後，部位沒被平掉。liveCode + library
      的平倉請求看起來都對（action=DEAL、position=ticket、type=反向），但 exe 是
      視窗程式、library 的失敗訊息只印到隱藏 console，所以看不到真正的 retcode。

這支腳本繞過 exe，直接用 MetaTrader5 對「你終端機現在登入的那個 demo」做平倉探測：
  - 接上正在跑的 MT5 終端機（已登入就不用帳密）
  - 列出所有持倉
  - 對每一筆，用跟 library 相同的平倉請求去送，且 IOC→FOK→RETURN 三種 filling 各試
  - 把每次 retcode + comment 印出來 → 一翻兩瞪眼

⚠️ 這會對 demo 帳戶送出真正的平倉單（demo 安全；而且這些就是你要清掉的卡單）。
用法（在你剛剛跑 bk_test.py 的同一個 python 環境）：
    python diag_close.py
若終端機沒登入，填下面 ACCOUNT/PASSWORD/SERVER 再跑。
"""
import MetaTrader5 as mt5

# 只有在「MT5 終端機沒登入」時才會用到；終端機已登入就留空也沒差
ACCOUNT  = 0                  # ← 沒登入才填 demo 帳號（已登入終端機則免）
PASSWORD = ""                 # ← 終端機已登入就不用填；沒登入才填 demo 密碼
SERVER   = ""                 # ← 沒登入才填，如 "XMGlobal-MT5 7"

DO_CLOSE = True               # True=真的送平倉單（demo）；改 False 只看持倉不動作

# ── 連線 ──
if not mt5.initialize():
    print("❌ initialize 失敗:", mt5.last_error()); raise SystemExit

ai = mt5.account_info()
if ai is None:
    # 終端機沒登入 → 用帳密登入
    if not mt5.login(ACCOUNT, password=PASSWORD, server=SERVER):
        print("❌ login 失敗:", mt5.last_error()); mt5.shutdown(); raise SystemExit
    ai = mt5.account_info()

print(f"✅ 連上帳戶 {ai.login} @ {ai.server}  balance={ai.balance} equity={ai.equity}")
print(f"   交易允許(terminal)={mt5.terminal_info().trade_allowed}  "
      f"交易允許(account)={ai.trade_allowed}")   # 若是 False，平倉一定被退（AutoTrading 沒開）

positions = mt5.positions_get()
if positions is None:
    print("positions_get 回 None:", mt5.last_error()); positions = []
print(f"\n📋 目前持倉 {len(positions)} 筆：")
for p in positions:
    side = "SELL" if p.type == mt5.ORDER_TYPE_SELL else "BUY"
    print(f"  ticket={p.ticket}  {p.symbol}  {side}  vol={p.volume}  open={p.price_open}  pnl={p.profit}")

if not DO_CLOSE:
    print("\n(DO_CLOSE=False，只列出不平倉)"); mt5.shutdown(); raise SystemExit

FILLINGS = [("IOC", mt5.ORDER_FILLING_IOC),       # ← library 現在寫死用這個
            ("FOK", mt5.ORDER_FILLING_FOK),
            ("RETURN", mt5.ORDER_FILLING_RETURN)]

for p in positions:
    print(f"\n──── 平倉 ticket={p.ticket} {p.symbol} vol={p.volume} ────")
    si = mt5.symbol_info(p.symbol)
    # filling_mode 是 bitmask：bit0(1)=FOK 支援、bit1(2)=IOC 支援
    print(f"  symbol.filling_mode bitmask={si.filling_mode}  (1=支援FOK, 2=支援IOC, 3=兩者都支援)")
    close_type = mt5.ORDER_TYPE_BUY if p.type == mt5.ORDER_TYPE_SELL else mt5.ORDER_TYPE_SELL
    done = False
    for name, fmode in FILLINGS:
        tick = mt5.symbol_info_tick(p.symbol)
        price = tick.ask if close_type == mt5.ORDER_TYPE_BUY else tick.bid
        req = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": p.symbol,
            "volume": p.volume,
            "type": close_type,
            "position": p.ticket,     # ← 關鍵：指定要平的部位（hedge 帳戶平倉靠這個）
            "price": price,
            "deviation": 100,         # 比 library 的 10 寬很多，排除黃金滑價問題
            "magic": 123456,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": fmode,
        }
        r = mt5.order_send(req)
        rc = getattr(r, "retcode", None)
        cm = getattr(r, "comment", None)
        print(f"  [{name:6}] retcode={rc}  comment={cm}")
        if rc == mt5.TRADE_RETCODE_DONE:
            print(f"  ✅ 用 ORDER_FILLING_{name} 成功平掉！→ 這就是 library 該改的 filling mode")
            done = True
            break
    if not done:
        print(f"  ❌ 三種 filling 都沒成功 — 上面的 retcode/comment 就是真正原因")
        print(f"     （常見：10027=AutoTrading沒開, 10018=市場關閉, 10030=filling不支援, "
              f"10004/10021=requote/沒報價=滑價）")

mt5.shutdown()
print("\n完成。把整段輸出貼給我，我就能定位真因。")
