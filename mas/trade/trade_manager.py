import MetaTrader5 as mt5
from datetime import datetime
from mas.receive.receive_manage import ReceiveManager
from mas.connection.connection import ConnectionManager
from mas.lang.i18n_strings import get_text, TradeText

class TradeManager:
    def __init__(self, receiver: ReceiveManager, connection: ConnectionManager):
        """
        初始化即時行情訂閱器，設定資料接收器與 MT5 連線管理器。

        此類別負責管理 Tick 與 Bar 的訂閱、取消與推送資料流程，並由 receiver 回傳給上層接收模組。

        Args:
            receiver (ReceiveManager): 用於接收 Tick 或 Bar 訊號的資料接收管理器。
            connection (ConnectionManager): MT5 連線控制器，用於查詢商品代碼與執行 API 操作。

        Returns:
            None

        Initialize real-time market subscription manager with receiver and MT5 connection manager.

        This class manages the lifecycle of tick/bar subscriptions, including push and unsubscribe logic,
        and delegates all received data to the provided receiver.

        Args:
            receiver (ReceiveManager): Receiver module to handle tick/bar events.
            connection (ConnectionManager): MT5 connection handler for symbol lookup and data queries.

        Returns:
            None
        """
        self.receiver = receiver
        self.connection = connection

    def send_order(self, params: dict) -> str:
        """
        發送交易訂單至 MT5，支援市價單、限價單與停損單等多種類型，並處理回報與訂單狀態。

        此函式會：
        - 驗證基本參數（商品、方向、手數）
        - 初始化 MT5 並確認登入狀態
        - 取得最新 Tick 價格（Bid/Ask）
        - 將訂單參數轉換為 MT5 API 格式，發送至交易伺服器
        - 回傳訂單編號並推播訂單狀態與成交資訊

        Args:
            params (dict): 下單參數字典，支援欄位如下：
                - symbol (str): 商品代碼（必填）
                - order_type (str): 訂單類型，例如 buy、sell、buy_limit、sell_stop 等（必填）
                - volume (float): 下單手數（必填）
                - price (float): 訂單價格（限價與停損單需填）
                - sl (float): 停損價（非必填）
                - tp (float): 停利價（非必填）
                - stoplimit (float): 二段觸價（限於 stop_limit 類型，非必填）
                - deviation (int): 最大滑價，預設 10
                - magic (int): EA 編號，預設 123456
                - comment (str): 訂單備註，預設 "MAS Order"
                - type_time (int): 時效類型，預設 mt5.ORDER_TIME_GTC
                - expiration (datetime): 到期時間（若為 GTT 類型才需填）
                - type_filling (int): 撮合方式，預設 mt5.ORDER_FILLING_IOC
                - order_id (int/str): 修改單用 position ID（非必填）
                - position_by (int): 多單關聯 ID（非必填）

        Returns:
            str: 訂單編號（若下單失敗則回傳空字串）

        Submit a trading order to MT5, supporting market, limit, and stop orders with full parameter control.

        This method:
        - Validates basic parameters (symbol, direction, volume)
        - Initializes MT5 and confirms login status
        - Gets current tick price (Bid/Ask)
        - Translates input into MT5 order request
        - Submits the order and pushes result status and execution report

        Args:
            params (dict): Dictionary of order parameters:
                - symbol (str): Instrument code (required)
                - order_type (str): Order type (e.g., buy, sell, buy_limit, sell_stop) (required)
                - volume (float): Order volume (required)
                - price (float): Price (for pending orders)
                - sl (float): Stop loss (optional)
                - tp (float): Take profit (optional)
                - stoplimit (float): Second trigger price for stop_limit orders (optional)
                - deviation (int): Max slippage (default: 10)
                - magic (int): EA identifier (default: 123456)
                - comment (str): Order comment (default: "MAS Order")
                - type_time (int): Time-in-force type (default: mt5.ORDER_TIME_GTC)
                - expiration (datetime): Expiry time (for GTT orders)
                - type_filling (int): Order fill mode (default: mt5.ORDER_FILLING_IOC)
                - order_id (int/str): Existing position ID to modify (optional)
                - position_by (int): Related order ID (optional)

        Returns:
            str: Order ID. Empty string if submission failed.
        """
        symbol = params.get("symbol")
        order_type = params.get("order_type")
        volume = float(params.get("volume"))
        price = params.get("price")
        sl = params.get("sl")
        tp = params.get("tp")
        stoplimit = params.get("stoplimit")
        deviation = params.get("deviation", 10)
        magic = params.get("magic", 123456)
        comment = params.get("comment", "MAS Order")
        type_time = params.get("type_time", mt5.ORDER_TIME_GTC)
        expiration = params.get("expiration")
        type_filling = params.get("type_filling", mt5.ORDER_FILLING_IOC)
        position = params.get("order_id")
        position_by = params.get("position_by")

        if isinstance(position, str):
            position = int(position)

        if not all([symbol, order_type, volume]):
            print(get_text(TradeText.MISSING_ORDER_PARAMS))
            return ""

        if not mt5.initialize():
            print(get_text(TradeText.INIT_FAILED))
            return ""

        if not mt5.account_info():
            print(get_text(TradeText.NOT_LOGGED_IN))
            return ""

        real_symbol = self.connection.find_symbol(symbol)
        symbol_info = mt5.symbol_info(real_symbol)
        if not symbol_info or not symbol_info.visible:
            mt5.symbol_select(real_symbol, True)

        tick = mt5.symbol_info_tick(real_symbol)
        if not tick:
            print(get_text(TradeText.NO_TICK_INFO))
            return ""

        ask = tick.ask
        bid = tick.bid

        # 型別轉換
        order_type_map = {
            "buy": mt5.ORDER_TYPE_BUY,
            "sell": mt5.ORDER_TYPE_SELL,
            "buy_limit": mt5.ORDER_TYPE_BUY_LIMIT,
            "sell_limit": mt5.ORDER_TYPE_SELL_LIMIT,
            "buy_stop": mt5.ORDER_TYPE_BUY_STOP,
            "sell_stop": mt5.ORDER_TYPE_SELL_STOP,
            "buy_stop_limit": mt5.ORDER_TYPE_BUY_STOP_LIMIT,
            "sell_stop_limit": mt5.ORDER_TYPE_SELL_STOP_LIMIT
        }
        mt5_type = order_type_map.get(order_type.lower())
        if mt5_type is None:
            print(get_text(TradeText.UNSUPPORTED_ORDER_TYPE, order_type=order_type))
            return ""

        is_market = order_type.lower() in ["buy", "sell"]
        order_price = price if not is_market else (
            ask if "buy" in order_type else bid)

        # 建構下單請求
        request = {
            "action": mt5.TRADE_ACTION_DEAL if is_market else mt5.TRADE_ACTION_PENDING,
            "symbol": real_symbol,
            "volume": volume,
            "type": mt5_type,
            "price": order_price,
            "sl": sl,
            "tp": tp,
            "stoplimit": stoplimit,
            "deviation": deviation,
            "magic": magic,
            "comment": comment,
            "type_time": type_time,
            "expiration": expiration,
            "type_filling": type_filling,
            "position": position,
            "position_by": position_by
        }
        request = {k: v for k, v in request.items() if v is not None}
        result = mt5.order_send(request)
        order_id = str(result.order) if result and result.order else "N/A"

        self.receiver.on_order_status(order_id, {
            "status": result.retcode if result else "N/A",
            "retcode": getattr(result, 'retcode', 'N/A'),
            "message": getattr(result, 'comment', 'unknown'),
            "request": request
        })

        if result and result.retcode == mt5.TRADE_RETCODE_DONE:
            self.receiver.on_order_execution(order_id, {
                "price": result.price,
                "volume": result.volume,
                "symbol": symbol,
                "time": datetime.now(),
                "type": order_type
            })
        else:
            print(get_text(TradeText.ORDER_FAILED, msg=getattr(result, 'comment', 'Exception error')))

        return order_id

    def modify_order(self, params: dict) -> bool:
        """
        修改已送出的 MT5 訂單參數（價格、停損、停利、到期日等）。

        此函式支援：
        - 修改掛單價格
        - 調整停損與停利價
        - 更新 stoplimit 與 expiration 時間（若為 GTT 類型）
        - 回報修改結果，並將狀態推播至 receiver

        Args:
            params (dict): 修改參數字典，需包含以下欄位：
                - order_id (int/str): 訂單編號（必填）
                - price (float): 新價格（必填）
                - sl (float): 停損價（非必填）
                - tp (float): 停利價（非必填）
                - stoplimit (float): 二段觸價（非必填）
                - expiration (datetime): 到期時間（非必填）
                - comment (str): 修改備註，預設為 "Modified by MAS"

        Returns:
            bool: 是否修改成功

        Modify existing pending MT5 order parameters, including price, SL/TP, expiration.

        This method supports:
        - Changing price of pending orders
        - Adjusting SL (stop loss) and TP (take profit)
        - Updating stoplimit and expiration (for GTT types)
        - Reporting the result and pushing status to receiver

        Args:
            params (dict): Dictionary of modification parameters:
                - order_id (int/str): Order ID to modify (required)
                - price (float): New order price (required)
                - sl (float): Stop loss price (optional)
                - tp (float): Take profit price (optional)
                - stoplimit (float): Second trigger price (optional)
                - expiration (datetime): Expiration datetime (optional)
                - comment (str): Modification note, default to "Modified by MAS"

        Returns:
            bool: True if modification succeeded, otherwise False.
        """ 
        order_id = params.get("order_id")
        price = params.get("price")
        sl = params.get("sl")
        tp = params.get("tp")
        stoplimit = params.get("stoplimit")
        expiration = params.get("expiration")
        comment = params.get("comment", "Modified by MAS")

        if not order_id or price is None:
            print(get_text(TradeText.MODIFY_MISSING_PARAMS))
            return False

        try:
            request = {
                "action": mt5.TRADE_ACTION_MODIFY,
                "order": int(order_id),
                "price": price,
                "comment": comment
            }

            if sl is not None:
                request["sl"] = sl
            if tp is not None:
                request["tp"] = tp
            if stoplimit is not None:
                request["stoplimit"] = stoplimit
            if expiration is not None:
                request["expiration"] = expiration

            result = mt5.order_send(request)

            if result is None:
                print(get_text(TradeText.MODIFY_NO_RESPONSE))
                return False

            order_status = {
                "status": result.retcode,
                "retcode": result.retcode,
                "message": result.comment,
                "request": request,
                "action": "modify"
            }

            self.receiver.on_order_status(order_id, order_status)

            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print(get_text(TradeText.MODIFY_FAILED, msg=result.comment))
                return False

            print(get_text(TradeText.MODIFY_SUCCESS, msg=result.comment))
            return True

        except Exception as e:
            print(get_text(TradeText.EXCEPTION_ERROR, error=str(e)))
            return False

    def cancel_order(self, params: dict) -> bool:
        """
        取消尚未成交的 MT5 掛單（Pending Order），適用於限價單、停損單等未成交訂單。

        此函式會：
        - 檢查參數是否合法（需提供 order_id）
        - 呼叫 MT5 的 `TRADE_ACTION_REMOVE` 執行取消
        - 將結果推播給 receiver 並列印狀態
        - 處理失敗情況與例外錯誤

        Args:
            params (dict): 取消參數字典：
                - order_id (int/str): 欲取消之掛單編號（必填）
                - comment (str): 備註文字，預設為 "Cancel by MAS"

        Returns:
            bool: 是否取消成功

        Cancel a pending MT5 order (limit/stop types) that has not yet been executed.

        This function:
        - Validates input (requires `order_id`)
        - Submits a `TRADE_ACTION_REMOVE` request to MT5
        - Pushes cancellation result to receiver
        - Handles response or exceptions if any occur

        Args:
            params (dict): Dictionary of cancellation parameters:
                - order_id (int/str): The pending order ID to cancel (required)
                - comment (str): Optional remark, default is "Cancel by MAS"

        Returns:
            bool: True if cancellation succeeded, otherwise False.
        """

        order_id = params.get("order_id")
        comment = params.get("comment", "Cancel by MAS")

        if not order_id:
            print(get_text(TradeText.CANCEL_MISSING_ORDER_ID))
            return False

        try:
            request = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": int(order_id),
                "comment": comment
            }

            result = mt5.order_send(request)

            if result is None:
                print(get_text(TradeText.CANCEL_NO_RESPONSE))
                return False

            self.receiver.on_order_status(order_id, {
                "status": result.retcode,
                "retcode": result.retcode,
                "message": result.comment,
                "request": request,
                "action": "cancel"
            })

            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print(get_text(TradeText.CANCEL_FAILED, msg=result.comment))
                return False

            print(get_text(TradeText.CANCEL_SUCCESS, order_id=order_id))
            return True

        except Exception as e:
            print(get_text(TradeText.EXCEPTION_ERROR, error=str(e)))
            return False

    def modify_position_sltp(self, params: dict) -> bool:
        """
        修改持倉部位的停損（SL）與停利（TP）價格。

        Args:
            params (dict): 修改參數：
                - position_id (int/str): 持倉部位 ID（必填）
                - sl (float): 停損價（與 tp 至少提供一個）
                - tp (float): 停利價（與 sl 至少提供一個）

        Returns:
            bool: 修改成功回傳 True，否則 False。

        Modify SL (stop loss) and TP (take profit) for an open position.

        Args:
            params (dict): Must include position_id and at least sl or tp.

        Returns:
            bool: True if modification succeeded, otherwise False.
        """
        position_id = params.get("position_id")
        sl = params.get("sl")
        tp = params.get("tp")

        if not position_id or (sl is None and tp is None):
            print(get_text(TradeText.SLTP_MISSING_PARAMS))
            return False

        try:
            request = {
                "action": mt5.TRADE_ACTION_SLTP,
                "position": int(position_id),
            }
            if sl is not None:
                request["sl"] = sl
            if tp is not None:
                request["tp"] = tp

            result = mt5.order_send(request)
            if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
                msg = getattr(result, "comment", "no response") if result else "no response"
                print(get_text(TradeText.SLTP_FAILED, msg=msg))
                return False

            print(get_text(TradeText.SLTP_SUCCESS, order_id=position_id))
            return True
        except Exception as e:
            print(get_text(TradeText.EXCEPTION_ERROR, error=str(e)))
            return False

    def order_check(self, params: dict) -> dict:
        """
        預先檢查訂單是否可以執行（無實際下單），回傳保證金與帳戶狀態。

        Args:
            params (dict): 下單參數（同 send_order），必填 symbol, order_type, volume。

        Returns:
            dict: 檢查結果包含 retcode, balance, equity, margin 等，失敗回傳空字典。

        Pre-check whether an order can be executed without actually placing it.

        Args:
            params (dict): Same fields as send_order; symbol, order_type, volume required.

        Returns:
            dict: Check result with retcode, balance, equity, margin, etc. Empty dict on failure.
        """
        symbol = params.get("symbol")
        order_type = params.get("order_type")
        volume = params.get("volume")

        if not all([symbol, order_type, volume]):
            print(get_text(TradeText.ORDER_CHECK_MISSING_PARAMS))
            return {}

        try:
            order_type_map = {
                "buy": mt5.ORDER_TYPE_BUY,
                "sell": mt5.ORDER_TYPE_SELL,
                "buy_limit": mt5.ORDER_TYPE_BUY_LIMIT,
                "sell_limit": mt5.ORDER_TYPE_SELL_LIMIT,
                "buy_stop": mt5.ORDER_TYPE_BUY_STOP,
                "sell_stop": mt5.ORDER_TYPE_SELL_STOP,
            }
            mt5_type = order_type_map.get(order_type.lower())
            real_symbol = self.connection.find_symbol(symbol)
            tick = mt5.symbol_info_tick(real_symbol)
            price = tick.ask if "buy" in order_type.lower() else tick.bid

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": real_symbol,
                "volume": float(volume),
                "type": mt5_type,
                "price": price,
                "deviation": params.get("deviation", 10),
                "magic": params.get("magic", 123456),
                "comment": params.get("comment", "MAS Check"),
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            result = mt5.order_check(request)
            if result is None:
                print(get_text(TradeText.ORDER_CHECK_FAIL, msg="no response"))
                return {}

            return {
                "retcode": result.retcode,
                "balance": result.balance,
                "equity": result.equity,
                "profit": result.profit,
                "margin": result.margin,
                "margin_free": result.margin_free,
                "margin_level": result.margin_level,
                "comment": result.comment,
            }
        except Exception as e:
            print(get_text(TradeText.ORDER_CHECK_FAIL, msg=str(e)))
            return {}

    def calc_order_margin(self, params: dict) -> float:
        """
        計算指定訂單所需的保證金。

        Args:
            params (dict): 計算參數：action (buy/sell), symbol, volume, price。

        Returns:
            float: 所需保證金，失敗回傳 -1.0。

        Calculate the required margin for a specific order.

        Args:
            params (dict): action (buy/sell), symbol, volume, price.

        Returns:
            float: Required margin, or -1.0 on failure.
        """
        action = params.get("action")
        symbol = params.get("symbol")
        volume = params.get("volume")
        price = params.get("price")

        if not all([action, symbol, volume, price]):
            print(get_text(TradeText.CALC_MARGIN_MISSING_PARAMS))
            return -1.0

        try:
            action_map = {"buy": mt5.ORDER_TYPE_BUY, "sell": mt5.ORDER_TYPE_SELL}
            mt5_action = action_map.get(action.lower(), mt5.ORDER_TYPE_BUY)
            real_symbol = self.connection.find_symbol(symbol)
            margin = mt5.order_calc_margin(mt5_action, real_symbol, float(volume), float(price))
            if margin is None:
                print(get_text(TradeText.CALC_MARGIN_FAIL, msg="no response"))
                return -1.0
            return margin
        except Exception as e:
            print(get_text(TradeText.CALC_MARGIN_FAIL, msg=str(e)))
            return -1.0

    def calc_order_profit(self, params: dict) -> float:
        """
        計算指定訂單的預計損益。

        Args:
            params (dict): 計算參數：action (buy/sell), symbol, volume, price_open, price_close。

        Returns:
            float: 預計損益，失敗回傳 -1.0。

        Calculate the estimated profit/loss for a specific order.

        Args:
            params (dict): action (buy/sell), symbol, volume, price_open, price_close.

        Returns:
            float: Estimated profit/loss, or -1.0 on failure.
        """
        action = params.get("action")
        symbol = params.get("symbol")
        volume = params.get("volume")
        price_open = params.get("price_open")
        price_close = params.get("price_close")

        if not all([action, symbol, volume, price_open, price_close]):
            print(get_text(TradeText.CALC_PROFIT_MISSING_PARAMS))
            return -1.0

        try:
            action_map = {"buy": mt5.ORDER_TYPE_BUY, "sell": mt5.ORDER_TYPE_SELL}
            mt5_action = action_map.get(action.lower(), mt5.ORDER_TYPE_BUY)
            real_symbol = self.connection.find_symbol(symbol)
            profit = mt5.order_calc_profit(mt5_action, real_symbol, float(volume), float(price_open), float(price_close))
            if profit is None:
                print(get_text(TradeText.CALC_PROFIT_FAIL, msg="no response"))
                return -1.0
            return profit
        except Exception as e:
            print(get_text(TradeText.CALC_PROFIT_FAIL, msg=str(e)))
            return -1.0
