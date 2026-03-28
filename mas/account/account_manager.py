import MetaTrader5 as mt5
from datetime import datetime
from mas.module.time_helper import normalize_datetime_params
from mas.module.base import clean_symbol
from mas.connection.connection import ConnectionManager
from mas.lang.i18n_strings import get_text, AccountText


class AccountManager:
    def __init__(self, connection: ConnectionManager):
        """
        初始化 AccountManager 實例，並注入連線管理器。

        Args:
            connection (ConnectionManager): 來自 mas.connection.connection 模組的連線管理器，用於處理與後端服務的連線。

        Initialize an instance of AccountManager with a connection manager.

        Args:
            connection (ConnectionManager): Connection manager from mas.connection.connection,
                                            used to handle connections to backend services.
        """
        self.connection = connection

    def init_mt5(self):
        """
        初始化 MetaTrader 5 (MT5) 交易終端。

        Args:
            無

        Returns:
            無。若初始化失敗，將拋出 RuntimeError 異常。

        Initialize the MetaTrader 5 (MT5) trading terminal.

        Args:
            None

        Returns:
            None. Raises RuntimeError if initialization fails.
        """

        if not mt5.initialize():
            raise RuntimeError("MT5 initialization failed. Please ensure the terminal is running.")

    def get_account_info(self) -> dict:
        """
        查詢 MT5 帳戶基本資訊。

        Args:
            無

        Returns:
            dict: 成功時回傳包含帳戶資訊dict，欄位包含 login、balance、equity、margin、leverage 等。
                  若查詢失敗，則回傳 {"error": "查詢帳戶資訊失敗"}。

        Retrieve basic account information from MT5.

        Args:
            None

        Returns:
            dict: If successful, returns a dictionary containing account details such as login, balance,
                  equity, margin, leverage, etc. If retrieval fails, returns {"error": "Failed to retrieve account info"}.
        """

        self.init_mt5()

        info = mt5.account_info()
        if info is None:
            return {"error": "查詢帳戶資訊失敗"}

        return {
            "login": info.login,
            "trade_mode": info.trade_mode,
            "leverage": info.leverage,
            "limit_orders": info.limit_orders,
            "margin_so_mode": info.margin_so_mode,
            "trade_allowed": info.trade_allowed,
            "trade_expert": info.trade_expert,
            "margin_mode": info.margin_mode,
            "currency_digits": info.currency_digits,
            "fifo_close": info.fifo_close,
            "balance": info.balance,
            "credit": info.credit,
            "profit": info.profit,
            "equity": info.equity,
            "margin": info.margin,
            "margin_free": info.margin_free,
            "margin_level": info.margin_level,
            "margin_so_call": info.margin_so_call,
            "margin_so_so": info.margin_so_so,
            "margin_initial": info.margin_initial,
            "margin_maintenance": info.margin_maintenance,
            "assets": info.assets,
            "liabilities": info.liabilities,
            "commission_blocked": info.commission_blocked,
            "name": info.name,
            "server": info.server,
            "currency": info.currency,
            "company": info.company
        }

    def get_positions(self, params: dict = {}) -> list:
        """
        查詢目前持倉部位（Position），可依據商品、群組或持倉單號過濾查詢。

        Args:
            params (dict): 查詢參數，可包含以下欄位：
                - symbol (str): 非必填，指定商品代碼。
                - group (str): 非必填，指定商品群組。
                - ticket (int): 非必填，指定持倉單號（優先順序低於 symbol 與 group）。

        Returns:
            list[dict]: 每筆為完整的部位資訊，若無資料則回傳空列表。

        Retrieve current open positions, with optional filters by symbol, group, or ticket.

        Args:
            params (dict): Query parameters. Supported keys:
                - symbol (str): Optional. Specify instrument symbol.
                - group (str): Optional. Filter by symbol group.
                - ticket (int): Optional. Specify position ticket (lower priority than symbol or group).

        Returns:
            list[dict]: Each item represents a full position record. Returns an empty list if no data is found.
        """
        symbol = params.get("symbol", "")
        group = params.get("group", "")
        ticket = params.get("ticket", "")

        if not symbol == "":
            symbol = self.connection.find_symbol(symbol)
        if not group == "":
            group = self.connection.find_symbol(group)
            
        if symbol:
            positions = mt5.positions_get(symbol=symbol)
        elif group:
            positions = mt5.positions_get(group=group)
        elif ticket:
            positions = mt5.positions_get(ticket=ticket)
        else:
            positions = mt5.positions_get()

        if positions is None:
            return []

        result = []
        for p in positions:
            result.append({
                "order_id": p.ticket, 
                "ticket": p.ticket,
                "symbol": clean_symbol(p.symbol),
                "type": p.type,
                "magic": p.magic,
                "identifier": p.identifier,
                "reason": p.reason,
                "volume": p.volume,
                "price_open": p.price_open,
                "sl": p.sl,
                "tp": p.tp,
                "price_current": p.price_current,
                "swap": p.swap,
                "profit": p.profit,
                "comment": p.comment,
                "external_id": p.external_id,
                "time": datetime.fromtimestamp(p.time),
                "time_msc": p.time_msc,
                "time_update": datetime.fromtimestamp(p.time_update),
                "time_update_msc": p.time_update_msc
            })

        return result

    def get_order_history(self, params: dict = {}) -> list:
        """
        查詢歷史成交紀錄（Deal History）。

        Args:
            params (dict): 查詢參數，可包含以下欄位：
                - symbol (str): 非必填，指定商品代碼。
                - from (datetime | str): 非必填，起始時間，預設為 2000-01-01。
                - to (datetime | str): 非必填，結束時間，預設為現在時間。
                - ticket (int): 非必填，指定某張訂單的成交紀錄。
                - position (int): 非必填，指定某張部位的成交紀錄。

        Returns:
            list[dict]: 每筆為完整的成交紀錄。若查無資料則回傳空列表。

        Retrieve historical deal records (Deal History) from MT5.

        Args:
            params (dict): Query parameters. Supported keys:
                - symbol (str): Optional. Specify instrument symbol.
                - from (datetime | str): Optional. Start datetime (default is 2000-01-01).
                - to (datetime | str): Optional. End datetime (default is current time).
                - ticket (int): Optional. Specify a ticket to filter by order.
                - position (int): Optional. Specify a position ID to filter by deal.

        Returns:
            list[dict]: Each item is a full deal record. Returns an empty list if no data is found.
        """
        if params.get("from") is not None and params.get("to") is not None:
            params = normalize_datetime_params(params)
        date_from = params.get("from", datetime(2000, 1, 1,0,0,1))
        date_to = params.get("to", datetime.now())
        symbol = params.get("symbol")
        ticket = params.get("ticket")
        position = params.get("position")
        if ticket != None:
            deals = mt5.history_deals_get(
                ticket=ticket,
            )
        elif position != None:
            deals = mt5.history_deals_get(
                position=position,
            )
        else:
            if symbol != None:
                real_symbol = self.connection.find_symbol(symbol)
                deals = mt5.history_deals_get(
                    date_from,
                    date_to,
                    group=real_symbol,
                    # ticket=ticket,
                    # position=position,
                )
            else:
                deals = mt5.history_deals_get(
                    date_from,
                    date_to,
                )

        if deals is None:
            return []

        result = []
        for d in deals:
            result.append({
                "ticket": d.ticket,
                "order": d.order,
                "position_id": d.position_id,
                "symbol": d.symbol,
                "type": d.type,
                "entry": d.entry,
                "reason": d.reason,
                "volume": d.volume,
                "price": d.price,
                "commission": d.commission,
                "swap": d.swap,
                "fee": d.fee,
                "profit": d.profit,
                "comment": d.comment,
                "external_id": d.external_id,
                "time": datetime.fromtimestamp(d.time),
                "time_msc": d.time_msc
            })

        return result

    def get_pending_orders(self, params: dict = {}) -> list:
        """
        查詢當前所有掛單（Pending Orders），可依商品、群組或單號過濾。

        Args:
            params (dict): 查詢參數，可包含 symbol、group、ticket。

        Returns:
            list[dict]: 每筆為掛單資訊，若無資料則回傳空列表。

        Retrieve current pending orders, optionally filtered by symbol, group, or ticket.

        Args:
            params (dict): Supported keys: symbol, group, ticket.

        Returns:
            list[dict]: Each item is a pending order record. Returns empty list if no data.
        """
        try:
            symbol = params.get("symbol", "")
            group = params.get("group", "")
            ticket = params.get("ticket")

            if symbol:
                real_symbol = self.connection.find_symbol(symbol)
                orders = mt5.orders_get(symbol=real_symbol)
            elif group:
                orders = mt5.orders_get(group=group)
            elif ticket:
                orders = mt5.orders_get(ticket=int(ticket))
            else:
                orders = mt5.orders_get()

            if orders is None:
                return []

            result = []
            for o in orders:
                result.append({
                    "ticket": o.ticket,
                    "symbol": clean_symbol(o.symbol),
                    "type": o.type,
                    "volume_initial": o.volume_initial,
                    "volume_current": o.volume_current,
                    "price_open": o.price_open,
                    "sl": o.sl,
                    "tp": o.tp,
                    "price_current": o.price_current,
                    "price_stoplimit": o.price_stoplimit,
                    "comment": o.comment,
                    "magic": o.magic,
                    "reason": o.reason,
                    "time_setup": datetime.fromtimestamp(o.time_setup),
                    "time_expiration": datetime.fromtimestamp(o.time_expiration) if o.time_expiration else None,
                    "time_done": datetime.fromtimestamp(o.time_done) if o.time_done else None,
                })
            return result
        except Exception as e:
            print(get_text(AccountText.GET_PENDING_ORDERS_ERROR, msg=str(e)))
            return []

    def get_orders_total(self) -> int:
        """
        取得當前掛單總數。

        Returns:
            int: 掛單數量，失敗時回傳 0。

        Get the total number of current pending orders.

        Returns:
            int: Number of pending orders, 0 on failure.
        """
        try:
            total = mt5.orders_total()
            return total if total is not None else 0
        except Exception as e:
            print(get_text(AccountText.GET_ORDERS_TOTAL_ERROR, msg=str(e)))
            return 0

    def get_history_orders(self, params: dict = {}) -> list:
        """
        查詢歷史掛單紀錄（History Orders），可依時間區間、商品或單號過濾。

        Args:
            params (dict): 查詢參數，可包含 from、to、symbol、ticket、position。

        Returns:
            list[dict]: 每筆為歷史掛單資訊，若無資料則回傳空列表。

        Retrieve historical order records with optional filters.

        Args:
            params (dict): Supported keys: from, to, symbol, ticket, position.

        Returns:
            list[dict]: Each item is a historical order record. Returns empty list if no data.
        """
        try:
            if params.get("from") is not None and params.get("to") is not None:
                params = normalize_datetime_params(params)
            date_from = params.get("from", datetime(2000, 1, 1, 0, 0, 1))
            date_to = params.get("to", datetime.now())
            symbol = params.get("symbol")
            ticket = params.get("ticket")
            position = params.get("position")

            if ticket is not None:
                orders = mt5.history_orders_get(ticket=int(ticket))
            elif position is not None:
                orders = mt5.history_orders_get(position=int(position))
            elif symbol is not None:
                real_symbol = self.connection.find_symbol(symbol)
                orders = mt5.history_orders_get(date_from, date_to, group=real_symbol)
            else:
                orders = mt5.history_orders_get(date_from, date_to)

            if orders is None:
                return []

            result = []
            for o in orders:
                result.append({
                    "ticket": o.ticket,
                    "symbol": clean_symbol(o.symbol),
                    "type": o.type,
                    "volume_initial": o.volume_initial,
                    "volume_current": o.volume_current,
                    "price_open": o.price_open,
                    "sl": o.sl,
                    "tp": o.tp,
                    "price_current": o.price_current,
                    "price_stoplimit": o.price_stoplimit,
                    "comment": o.comment,
                    "magic": o.magic,
                    "reason": o.reason,
                    "state": o.state,
                    "time_setup": datetime.fromtimestamp(o.time_setup),
                    "time_expiration": datetime.fromtimestamp(o.time_expiration) if o.time_expiration else None,
                    "time_done": datetime.fromtimestamp(o.time_done) if o.time_done else None,
                })
            return result
        except Exception as e:
            print(get_text(AccountText.GET_HISTORY_ORDERS_ERROR, msg=str(e)))
            return []

    def get_history_orders_total(self, params: dict = {}) -> int:
        """
        查詢指定時間區間內的歷史掛單總數。

        Args:
            params (dict): 查詢參數，可包含 from（起始時間）與 to（結束時間）。

        Returns:
            int: 歷史掛單總數，失敗時回傳 0。

        Get total number of historical orders in the given time range.

        Args:
            params (dict): Supported keys: from, to.

        Returns:
            int: Total historical order count, 0 on failure.
        """
        try:
            if params.get("from") is not None and params.get("to") is not None:
                params = normalize_datetime_params(params)
            date_from = params.get("from", datetime(2000, 1, 1, 0, 0, 1))
            date_to = params.get("to", datetime.now())
            total = mt5.history_orders_total(date_from, date_to)
            return total if total is not None else 0
        except Exception as e:
            print(get_text(AccountText.GET_HISTORY_ORDERS_TOTAL_ERROR, msg=str(e)))
            return 0
