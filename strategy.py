import bk_test

def main(account=123, password="", server="",symbol="", toggle=True,log=print, backtest_log=None):
    try:
        bk_test.main(account=account,password=password,server=server,symbol=symbol,toggle=toggle,log=log,backtest_log=backtest_log)
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
