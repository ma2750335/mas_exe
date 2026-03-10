import bk_test
import mas
class mas_client(mas):
    def __init__(self, toggle=True, log=print):
        super().__init__()    

def main(account=123, password="", server="", toggle=True,log=print,symbol=""):
    try:
        mas_c = mas_client(toggle=False, log=print)
        params = {
            "account": account,
            "password": password,
            "server": server
        }
        mas_c.login(params)
        connection = mas_c.connection
        all_code = connection.all_code
        
        if symbol:
            symbol = symbol
        else:
            symbol = bk_test.get_symbol()
        candidates = [code for code in all_code if code.startswith(symbol)]
        if not candidates:
            return None
        candidates.sort(key=lambda x: (len(x), x))
        return candidates[0]
        
            
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    main()
