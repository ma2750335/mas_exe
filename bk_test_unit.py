from mas.mas import MAS
import pandas as pd

class mas(MAS):
    def __init__(self, toggle):
        super().__init__()
        self.data_buffer = pd.DataFrame()  # 初始化資料緩衝區
        self.hold = False  # 是否持倉
        self.last_signal = 0  # 上一次訊號
        self.toggle = toggle

    def receive_bars(self, symbol, data, is_end):
        if not self.hold:
            self.order_id = self.send_order({
                "symbol": "EURUSD",
                "order_type": "sell",
                "volume": 0.1,
                "backtest_toggle": self.toggle 
            })
            self.hold = True
        else:
            self.send_order({
                "symbol": "EURUSD",
                "order_type": "buy",
                "order_id":self.order_id,
                "volume": 0.1,
                "backtest_toggle": self.toggle 
            })
            self.hold = False

mas_c = mas(toggle=True)

def main(account=6246796, password="ltfxtwx2", server="OANDA-Demo-1", toggle=True):
    mas_c.toggle = toggle
    params = {
        "account": account,
        "password": password,
        "server": server
    }
    success = mas_c.login(params)

    params = {
        "symbol": "EURUSD",
        "from": '2020-01-01',
        "to": '2024-12-31',
        "timeframe": "M1",
        "backtest_toggle": mas_c.toggle
    }
    mas_c.subscribe_bars(params)

def stop_main():
    params = {
        "symbol": "EURUSD",
        "timeframe": "M1",
    }
    mas_c.unsubscribe_bars(params)
    mas_c.stop_all_subscriptions()

if __name__ == "__main__":
    main()