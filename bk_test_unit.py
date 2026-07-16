from mas.mas import MAS
import pandas as pd
import zlib
from env_info import UUID as STRATEGY_UUID
MAGIC = zlib.crc32(STRATEGY_UUID.encode("utf-8")) & 0x7FFFFFFF

class mas(MAS):
    def __init__(self, toggle):
        super().__init__()
        self.data_buffer = pd.DataFrame()  # 初始化資料緩衝區
        self.hold = False  # 是否持倉
        self.last_signal = 0  # 上一次訊號
        self.toggle = toggle
        self.order_id = None  # 持倉單order_id

    def receive_bars(self, symbol, data, is_end):
        if not self.hold:
            self.log(f"Order Open, Order ID: {self.order_id}")
            self.order_id = self.send_order({
                "symbol": self.symbol,
                "order_type": "sell",
                "volume": 0.1,
                "magic": MAGIC,
                "backtest_toggle": self.toggle 
            })
            self.hold = True
        else:
            self.log(f"Order Close, Order ID: {self.order_id}")
            self.send_order({
                "symbol": self.symbol,
                "order_type": "buy",
                "order_id":self.order_id,
                "volume": 0.1,
                "magic": MAGIC,
                "backtest_toggle": self.toggle 
            })
            self.hold = False

mas_c = mas(toggle=True)

def main(account=123, password="", server="", symbol="",  capital=10000, volume=1, toggle=True, log=print, backtest_log=None):
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
    positions = mas_c.get_positions({"symbol": mas_c.symbol})
    print("positions:", positions)
    for position in positions:
        print("position:", position)
        if position.get('magic') == MAGIC and position['symbol'] == mas_c.symbol:
            mas_c.hold = True
            mas_c.order_id = position['order_id']
            print("hold = True, order_id:", mas_c.order_id)

    params = {
        "symbol": mas_c.symbol,
        "from": '2020-01-01',
        "to": '2024-12-31',
        "timeframe": "M1",
        "backtest_toggle": mas_c.toggle
    }
    mas_c.subscribe_bars(params)

def stop_main():
    params = {
        "symbol": mas_c.symbol,
        "timeframe": "M1",
    }
    mas_c.unsubscribe_bars(params)
    mas_c.stop_all_subscriptions()

if __name__ == "__main__":
    main(account=167152989, password="Mas29188910@", server="XMGlobal-MT5 2", symbol="EURUSD",  capital=10000, volume=1, toggle=False, log=print, backtest_log=None)