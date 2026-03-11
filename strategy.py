import bk_test

def main(account=123, password="", server="",symbol="", capital=10000, volume=1, toggle=True,log=print, backtest_log=None):
    try:
        bk_test.main(account=account,password=password,server=server,symbol=symbol,capital=capital,volume=volume,toggle=toggle,log=log,backtest_log=backtest_log)
        return {
            'status': True
        }
    except Exception as e:
        return {
            'status': False,
            'error': str(e)
        }
def stop_main():
    bk_test.stop_main()

if __name__ == "__main__":
    main()
