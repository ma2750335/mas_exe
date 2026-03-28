from mas.connection.connection import ConnectionManager
from mas.market_data.market_data_manager import MarketDataManager
from mas.history.history_data_manager import HistoryDataManager
from mas.trade.trade_manager import TradeManager
from mas.account.account_manager import AccountManager
from mas.receive.receive_manage import ReceiveManager
from mas.provider.data_provider import DataProvider
from mas.virtual.virtual_trade import VirtualTradeManager
from mas.clinet.client_post import ClientPost
from mas.lang.i18n_strings import set_lang as _set_lang
from mas.module.time_helper import get_start_date as _get_start_date
import os
import sys


class MAS:
    """主交易管理類別，整合所有交易、回測、帳戶、報表等模組功能。"""

    def __init__(self):
        """
        初始化 MAS 類別，建立各子模組的實例，包含歷史資料、實盤資料、虛擬交易、帳戶管理等。

        此類別為整體系統的核心中樞，負責整合所有元件模組（如 MT5 連線、下單、歷史資料、即時市場資料、報表產出等），
        並可透過 `self.provider` 統一操作數據訂閱與交易操作。

        Args:
            無

        Returns:
            無

        Initialize the MAS class and instantiate all internal components, including 
        history, market, virtual trade, account, and reporting modules.

        This serves as the central hub of the system, integrating MT5 connectivity, 
        order management, historical data retrieval, real-time data streaming, and reporting.
        The `self.provider` object provides a unified interface to interact with market or backtest data.

        Args:
            None

        Returns:
            None
        """
        self.clientpost = ClientPost(
            os.path.dirname(os.path.abspath(sys.argv[0]))
        )
        self.connection = ConnectionManager()
        self.receiver = ReceiveManager(
            clientpost=self.clientpost,
            owner=self
        )
        self.virtual_trade = VirtualTradeManager(receiver=self.receiver)
        self.trade = TradeManager(
            receiver=self.receiver,
            connection=self.connection
        )
        self.market = MarketDataManager(
            receiver=self.receiver,
            connection=self.connection
        )
        self.history = HistoryDataManager(
            receiver=self.receiver,
            virtual_trade=self.virtual_trade,
            connection=self.connection,
            clientpost=self.clientpost
        )
        self.provider = DataProvider(
            market=self.market,
            history=self.history,
            virtual_trade=self.virtual_trade,
            trade=self.trade,
            receiver=self.receiver,
            clientpost=self.clientpost
        )
        self.account = AccountManager(
            connection=self.connection
        )

    # --- 登入 ---

    def login(self, params: dict) -> bool:
        """
        登入 MT5 平台。

        Args:
            params (dict): 包含登入必要參數：
                - login (int): 登入帳號
                - password (str): 登入密碼
                - server (str): 伺服器名稱
                - timeout (int, optional): 登入逾時時間，預設為 6000 毫秒

        Returns:
            bool: 登入成功回傳 True，否則回傳 False。

        Login to the MT5 platform.

        Args:
            params (dict): Contains the required login fields:
                - login (int): MT5 account number
                - password (str): Account password
                - server (str): Server name
                - timeout (int, optional): Timeout in milliseconds, default is 6000

        Returns:
            bool: Returns True if login is successful, otherwise False.
        """
        return self.connection.login(params)

    # --- 交易相關 ---

    def send_order(self, params: dict) -> str:
        """
        發出一筆交易訂單（支援市價單與掛單類型）。

        Args:
            params (dict): 包含以下欄位的下單參數：
                - symbol (str): 商品代碼。
                - order_type (str): 訂單型別，如 "buy", "sell", "buy_limit", "sell_stop" 等。
                - volume (float): 下單數量（手數）。
                - price (float, optional): 掛單價格（僅限限價單/停損單）。
                - sl (float, optional): 停損價格。
                - tp (float, optional): 停利價格。
                - stoplimit (float, optional): 停損限價價格。
                - deviation (int, optional): 可容許滑價（預設 10）。
                - magic (int, optional): EA 標記碼（預設 123456）。
                - comment (str, optional): 訂單備註（預設 "MAS Order"）。
                - type_time (enum, optional): 有效時間類型（預設 GTC）。
                - expiration (datetime, optional): 訂單過期時間（若適用）。
                - type_filling (enum, optional): 撮合方式（預設 FOK）。
                - order_id (int, optional): 修改訂單時用的原始訂單號。
                - position_by (int, optional): 關聯部位標記。

        Returns:
            str: 成功下單後的訂單代碼（order_id）。若失敗則回傳空字串。

        Submit a trade order (supports both market and pending types).

        Args:
            params (dict): Order parameters including:
                - symbol (str): Instrument symbol.
                - order_type (str): Type of order, e.g., "buy", "sell", "buy_limit", "sell_stop", etc.
                - volume (float): Lot size of the order.
                - price (float, optional): Entry price for pending orders.
                - sl (float, optional): Stop loss price.
                - tp (float, optional): Take profit price.
                - stoplimit (float, optional): Stop limit price.
                - deviation (int, optional): Slippage allowed (default: 10).
                - magic (int, optional): Expert Advisor ID (default: 123456).
                - comment (str, optional): Order comment (default: "MAS Order").
                - type_time (enum, optional): Order time type (default: GTC).
                - expiration (datetime, optional): Expiration time if applicable.
                - type_filling (enum, optional): Order filling type (default: FOK).
                - order_id (int, optional): Used for modifying existing orders.
                - position_by (int, optional): Linked position identifier.

        Returns:
            str: Order ID if the order is successfully sent. Returns empty string on failure.
        """
        return self.provider.send_order(params)

    def modify_order(self, params: dict) -> bool:
        """
        修改一筆未成交的掛單（限價單、停損單等）。

        Args:
            params (dict): 修改參數，需包含以下欄位：
                - order_id (str): 要修改的訂單代碼。
                - price (float): 新的掛單價格。
                - sl (float, optional): 新的停損價格。
                - tp (float, optional): 新的停利價格。
                - stoplimit (float, optional): 停損限價價格（若有）。
                - expiration (datetime, optional): 訂單有效期限（若 applicable）。
                - comment (str, optional): 修改備註（預設為 "Modified by MAS"）。

        Returns:
            bool: 若修改成功則回傳 True，否則回傳 False。

        Modify a pending order (limit/stop type) before it gets executed.

        Args:
            params (dict): Parameters for modification, must include:
                - order_id (str): The ID of the order to be modified.
                - price (float): New entry price.
                - sl (float, optional): New stop loss price.
                - tp (float, optional): New take profit price.
                - stoplimit (float, optional): Stop-limit trigger price if applicable.
                - expiration (datetime, optional): Order expiration time.
                - comment (str, optional): Comment for the modification (default: "Modified by MAS").

        Returns:
            bool: Returns True if the modification was successful; otherwise False.
        """
        return self.trade.modify_order(params)

    def cancel_order(self, params: dict) -> bool:
        """
        取消一筆尚未成交的掛單（限價單、停損單等）。

        Args:
            params (dict): 取消參數，需包含以下欄位：
                - order_id (str): 欲取消的訂單代碼。

        Returns:
            bool: 若取消成功則回傳 True，否則 False。

        Cancel a pending order (e.g., limit or stop order) that has not yet been executed.

        Args:
            params (dict): Parameters for cancellation, must include:
                - order_id (str): The ID of the order to be cancelled.

        Returns:
            bool: Returns True if the order was successfully cancelled; otherwise False.
        """
        return self.trade.cancel_order(params)

    def receive_order_status(self, order_id: str, status_data: dict) -> None:
        """
        接收訂單狀態更新的推播事件，通常來自實盤或回測引擎。

        Args:
            order_id (str): 訂單代碼。
            status_data (dict): 訂單狀態資料，內容包含：
                - status (int): 狀態代碼（例如：成功、失敗、自定義碼）。
                - retcode (int): MT5 原始回傳碼。
                - message (str): 狀態描述文字。
                - request (dict): 原始下單請求內容。
                - action (str, optional): 狀態所屬的操作類型（如 modify/cancel 等）。

        Receive push notification of order status updates, typically from live trading or backtesting engine.

        Args:
            order_id (str): The ID of the order.
            status_data (dict): Order status payload, may include:
                - status (int): Status code (e.g., success, failure, or custom code).
                - retcode (int): MT5 return code.
                - message (str): Human-readable status description.
                - request (dict): The original order request.
                - action (str, optional): Operation type related to the status (e.g., modify/cancel).
        """
        pass

    def receive_order_execution(self, order_id: str, execution_data: dict) -> None:
        """
        接收訂單成交推播資訊，包含成交價格、時間與方向等細節。

        Args:
            order_id (str): 訂單代碼。
            execution_data (dict): 成交資訊，包含以下欄位：
                - price (float): 成交價格。
                - volume (float): 成交數量。
                - symbol (str): 商品代碼。
                - time (datetime): 成交時間。
                - type (str): 成交方向（例如 'buy', 'sell' 等）。

        Receive execution notification of an order, including fill price, time, direction, etc.

        Args:
            order_id (str): The order ID.
            execution_data (dict): Execution detail including:
                - price (float): Execution price.
                - volume (float): Executed volume.
                - symbol (str): Instrument symbol.
                - time (datetime): Time of execution.
                - type (str): Trade direction (e.g., 'buy', 'sell').
        """
        pass

    # --- 歷史資料&市場資料 ---
    def subscribe_ticks(self, params: dict) -> None:
        """
        訂閱即時 Tick 資料，或回測模式下的歷史Tick。

        Args:
            params (dict): 查詢參數，需包含以下欄位：
                - symbol (str): 商品代碼。
                - interval_ms (int, optional): 非必填，每筆資料推播間隔時間（單位：毫秒）。
                - backtest_toggle (bool): 是否啟用回測模式。

        Returns:
            None

        Subscribe to real-time tick data, or simulate tick stream in backtest mode.

        Args:
            params (dict): Parameters include:
                - symbol (str): Instrument symbol.
                - interval_ms (int, optional): Optional. Interval in milliseconds between tick push.
                - backtest_toggle (bool): Toggle for backtest mode.

        Returns:
            None
        """
        return self.provider.subscribe_ticks(params)

    def unsubscribe_ticks(self, params: dict) -> None:
        """
        取消 Tick 資料訂閱。

        Args:
            params (dict): 查詢參數，需包含以下欄位：
                - symbol (str): 商品代碼。

        Returns:
            None

        Unsubscribe from tick data stream.

        Args:
            params (dict): Parameters include:
                - symbol (str): Instrument symbol.

        Returns:
            None
        """
        return self.provider.unsubscribe_ticks(params)

    def subscribe_bars(self, params: dict) -> None:
        """
        訂閱即時 Bar 資料或回測模式下的歷史 Bar。

        Args:
            params (dict): 訂閱參數，需包含以下欄位：
                - symbol (str): 商品代碼。
                - timeframe (str): K 線週期，例如 "M1", "H1"。
                - interval_ms (int, optional): 資料輪詢間隔（毫秒），預設為 1000。
                - backtest_toggle (bool, optional): 是否為回測模式。

        Returns:
            None

        Subscribe to real-time bar data or stream historical bars in backtest mode.

        Args:
            params (dict): Subscription parameters include:
                - symbol (str): Instrument symbol.
                - timeframe (str): K-line timeframe, e.g., "M1", "H1".
                - interval_ms (int, optional): Polling interval in milliseconds. Default is 1000.
                - backtest_toggle (bool, optional): Whether to use backtest mode.

        Returns:
            None
        """
        return self.provider.subscribe_bars(params)

    def unsubscribe_bars(self, params: dict) -> None:
        """
        取消 Bar 資料訂閱。

        Args:
            params (dict): 取消參數，需包含以下欄位：
                - symbol (str): 商品代碼。
                - timeframe (str): K 線週期，例如 "M1", "H1"。

        Returns:
            None

        Unsubscribe from real-time or backtest bar data stream.

        Args:
            params (dict): Unsubscription parameters include:
                - symbol (str): Instrument symbol.
                - timeframe (str): K-line timeframe, e.g., "M1", "H1".

        Returns:
            None
        """
        return self.provider.unsubscribe_bars(params)

    def stop_all_subscriptions(self):
        """
        停止所有 Tick 與 Bar 資料訂閱。

        Args:
            無需參數。

        Returns:
            None

        Stop all active subscriptions including Tick and Bar streams.

        Args:
            No arguments required.

        Returns:
            None
        """
        return self.market.stop_all_subscriptions()

    def receive_ticks(self, symbol: str, data: dict, is_end: bool = False) -> None:
        """
        接收 Tick 推播資料。

        Args:
            symbol (str): 商品代碼。
            data (dict): Tick 結構內容。
            is_end (bool): 是否為最後一筆（預設為 False）。

        Returns:
            None

        Receive tick data push, typically used to override strategy logic.

        Args:
            symbol (str): Symbol code.
            data (dict): Tick data structure.
            is_end (bool): Indicates whether it is the last tick (default: False).

        Returns:
            None
        """
        return self.receiver.on_tick(symbol, data, is_end)

    def receive_bars(self, symbol: str, data: dict, is_end: bool = False) -> None:
        """
        接收 Bar 推播資料。

        Args:
            symbol (str): 商品代碼。
            data (dict): Bar 結構內容。
            is_end (bool): 是否為最後一筆（預設為 False）。

        Returns:
            None

        Receive bar (candlestick) data push, typically used for strategy computation.

        Args:
            symbol (str): Symbol code.
            data (dict): Bar data structure.
            is_end (bool): Indicates whether it is the last bar (default: False).

        Returns:
            None
        """
        return self.receiver.on_bar(symbol, data, is_end)

    # --- MT5 連線管理 ---

    def initialize_mt5(self) -> bool:
        """
        初始化 MT5 環境並連線。

        Returns:
            bool: 初始化成功回傳 True，否則 False。

        Initialize and connect to the MT5 environment.

        Returns:
            bool: Returns True if initialization is successful; otherwise, False.
        """
        return self.connection.initialize_mt5()

    def shutdown_mt5(self) -> None:
        """
        關閉 MT5 平台。

        Returns:
            None

        Shutdown the MT5 platform.

        Returns:
            None
        """
        return self.connection.shutdown_mt5()

    def check_connection(self) -> bool:
        """
        檢查 MT5 是否仍保持連線。

        Returns:
            bool: 若仍保持連線則回傳 True，否則 False。

        Check if MT5 is still connected.

        Returns:
            bool: Returns True if connected; otherwise, False.
        """
        return self.connection.check_connection()

    def reconnect_mt5(self) -> bool:
        """
        重新連線 MT5（如中斷後自動重連）。

        Returns:
            bool: 重新連線成功回傳 True，否則 False。

        Reconnect to MT5 (e.g., after disconnection).

        Returns:
            bool: Returns True if reconnection is successful; otherwise, False.
        """
        return self.connection.reconnect_mt5()

    # --- 帳戶與持倉管理 ---

    def get_account_info(self) -> dict:
        """
        查詢 MT5 帳戶資訊。

        Returns:
            dict: 帳戶基本資訊。

        Retrieve MT5 account information.

        Returns:
            dict: Basic account information.
        """
        return self.account.get_account_info()

    def get_positions(self, params: dict = {}) -> list:
        """
        查詢當前所有未平倉部位，可依商品代碼、群組或單號過濾。

        Args:
            params (dict): 查詢參數，支援以下欄位：
                - symbol (str): 非必填，指定商品代碼。
                - group (str): 非必填，指定商品群組。
                - ticket (int): 非必填，指定部位單號。

        Returns:
            list[dict]: 每筆為完整的部位資訊。若查無資料則回傳空列表。

        Retrieve current open positions, with optional filters by symbol, group, or ticket.

        Args:
            params (dict): Query parameters. Supported keys:
                - symbol (str): Optional. Specify instrument symbol.
                - group (str): Optional. Filter by symbol group.
                - ticket (int): Optional. Specify position ticket.

        Returns:
            list[dict]: Each item represents a full position record. Returns an empty list if no data is found.
        """
        return self.account.get_positions(params)

    def switch_account(self, params: dict) -> bool:
        """
        切換 MT5 登入帳戶。

        Args:
            params (dict): 需包含 account, password, server。

        Returns:
            bool: 切換成功回傳 True，否則 False。

        Switch to a different MT5 account.

        Args:
            params (dict): Must include account, password, server.

        Returns:
            bool: True if switch succeeded, otherwise False.
        """
        return self.connection.switch_account(params)

    def get_version(self) -> dict:
        """
        取得 MT5 終端版本資訊。

        Returns:
            dict: 包含 version, build, release_date 的版本字典。

        Get MT5 terminal version info.

        Returns:
            dict: Contains version, build, release_date.
        """
        return self.connection.get_version()

    def get_symbols(self, params: dict = {}) -> list:
        """
        取得 MT5 所有可用商品清單，可依 group 過濾。

        Args:
            params (dict): 可選 group (str)。

        Returns:
            list[dict]: 商品資訊列表。

        Get all available MT5 symbols, optionally filtered by group.

        Args:
            params (dict): Optional group (str).

        Returns:
            list[dict]: List of symbol info dicts.
        """
        return self.connection.get_symbols(params)

    def get_symbols_total(self) -> int:
        """
        取得 MT5 商品總數。

        Returns:
            int: 商品總數。

        Get total count of available MT5 symbols.

        Returns:
            int: Total symbol count.
        """
        return self.connection.get_symbols_total()

    def get_pending_orders(self, params: dict = {}) -> list:
        """
        查詢當前掛單（Pending Orders）。

        Args:
            params (dict): 可選 symbol, group, ticket。

        Returns:
            list[dict]: 掛單列表。

        Retrieve current pending orders.

        Args:
            params (dict): Optional symbol, group, ticket.

        Returns:
            list[dict]: List of pending order records.
        """
        return self.account.get_pending_orders(params)

    def get_orders_total(self) -> int:
        """
        取得當前掛單總數。

        Returns:
            int: 掛單數量。

        Get the total count of current pending orders.

        Returns:
            int: Pending order count.
        """
        return self.account.get_orders_total()

    def get_history_orders(self, params: dict = {}) -> list:
        """
        查詢歷史掛單紀錄（History Orders）。

        Args:
            params (dict): 可選 from, to, symbol, ticket, position。

        Returns:
            list[dict]: 歷史掛單列表。

        Retrieve historical order records.

        Args:
            params (dict): Optional from, to, symbol, ticket, position.

        Returns:
            list[dict]: List of historical order records.
        """
        return self.account.get_history_orders(params)

    def get_history_orders_total(self, params: dict = {}) -> int:
        """
        查詢指定時間區間內的歷史掛單總數。

        Args:
            params (dict): 可選 from, to。

        Returns:
            int: 歷史掛單總數。

        Get total historical order count in given time range.

        Args:
            params (dict): Optional from, to.

        Returns:
            int: Total historical order count.
        """
        return self.account.get_history_orders_total(params)

    def modify_position_sltp(self, params: dict) -> bool:
        """
        修改持倉的 SL/TP。

        Args:
            params (dict): 需包含 position_id，以及 sl 或 tp（至少一個）。

        Returns:
            bool: 成功回傳 True，否則 False。

        Modify SL/TP of an open position.

        Args:
            params (dict): Must include position_id, and at least sl or tp.

        Returns:
            bool: True if modification succeeded, otherwise False.
        """
        return self.trade.modify_position_sltp(params)

    def order_check(self, params: dict) -> dict:
        """
        預先檢查訂單是否可以執行（不實際下單）。

        Args:
            params (dict): 同 send_order 參數，必填 symbol, order_type, volume。

        Returns:
            dict: 檢查結果。

        Pre-check whether an order can be executed without placing it.

        Args:
            params (dict): Same as send_order; symbol, order_type, volume required.

        Returns:
            dict: Order check result.
        """
        return self.trade.order_check(params)

    def calc_order_margin(self, params: dict) -> float:
        """
        計算指定訂單所需保證金。

        Args:
            params (dict): 需包含 action, symbol, volume, price。

        Returns:
            float: 保證金金額，失敗回傳 -1.0。

        Calculate required margin for an order.

        Args:
            params (dict): Must include action, symbol, volume, price.

        Returns:
            float: Required margin, -1.0 on failure.
        """
        return self.trade.calc_order_margin(params)

    def calc_order_profit(self, params: dict) -> float:
        """
        計算指定訂單的預計損益。

        Args:
            params (dict): 需包含 action, symbol, volume, price_open, price_close。

        Returns:
            float: 預計損益，失敗回傳 -1.0。

        Calculate estimated profit/loss for an order.

        Args:
            params (dict): Must include action, symbol, volume, price_open, price_close.

        Returns:
            float: Estimated profit/loss, -1.0 on failure.
        """
        return self.trade.calc_order_profit(params)

    def subscribe_market_book(self, params: dict) -> bool:
        """
        訂閱指定商品的市場深度（DOM）。

        Args:
            params (dict): 需包含 symbol。

        Returns:
            bool: 成功回傳 True，否則 False。

        Subscribe to market depth (DOM) for a symbol.

        Args:
            params (dict): Must include symbol.

        Returns:
            bool: True if subscription succeeded, otherwise False.
        """
        return self.market.subscribe_market_book(params)

    def get_market_book(self, params: dict) -> list:
        """
        取得指定商品的市場深度快照。

        Args:
            params (dict): 需包含 symbol。

        Returns:
            list[dict]: 市場深度列表，失敗回傳空列表。

        Get market depth snapshot for a symbol.

        Args:
            params (dict): Must include symbol.

        Returns:
            list[dict]: Market depth entries, empty list on failure.
        """
        return self.market.get_market_book(params)

    def unsubscribe_market_book(self, params: dict) -> bool:
        """
        取消指定商品的市場深度訂閱。

        Args:
            params (dict): 需包含 symbol。

        Returns:
            bool: 成功回傳 True，否則 False。

        Unsubscribe from market depth for a symbol.

        Args:
            params (dict): Must include symbol.

        Returns:
            bool: True if release succeeded, otherwise False.
        """
        return self.market.unsubscribe_market_book(params)

    def get_bars_from_pos(self, params: dict):
        """
        從指定位置取得固定數量的 K 線資料。

        Args:
            params (dict): 需包含 symbol, timeframe, count，可選 start_pos（預設 0）。

        Returns:
            pd.DataFrame: K 線資料。

        Get a fixed number of bars starting from a given position index.

        Args:
            params (dict): Must include symbol, timeframe, count. Optional start_pos.

        Returns:
            pd.DataFrame: Bar data.
        """
        return self.history.get_bars_from_pos(params)

    def get_order_history(self, params: dict) -> list:
        """
        查詢歷史成交紀錄（Deal History），可依商品與時間區間過濾。

        Args:
            params (dict): 查詢參數，支援以下欄位：
                - symbol (str): 非必填，指定商品。
                - from (datetime/str): 起始時間，預設為 2000-01-01。
                - to (datetime/str): 結束時間，預設為當下時間。
                - ticket (int): 非必填，指定某張訂單的成交紀錄。
                - position (int): 非必填，指定某張部位的成交紀錄。

        Returns:
            list[dict]: 每筆為完整的成交紀錄。若查無資料則回傳空列表。

        Retrieve historical deal records, with optional filters by symbol, time range, ticket, or position.

        Args:
            params (dict): Query parameters. Supported keys:
                - symbol (str): Optional. Specify instrument symbol.
                - from (datetime/str): Start time. Default is 2000-01-01.
                - to (datetime/str): End time. Default is now.
                - ticket (int): Optional. Filter by order ticket.
                - position (int): Optional. Filter by position ID.

        Returns:
            list[dict]: Each item represents a complete deal record. Returns an empty list if no data is found.
        """
        return self.account.get_order_history(params)

    # --- 報表統計 ---
    def generate_data_report(self) -> dict:
        """
        根據交易紀錄產生完整績效報表資料（含 KPI 指標、年化報酬、回撤等）。

        Returns:
            dict: 包含完整統計資料的績效報表結構。

        Generate full performance data report based on trading records.
        Includes KPIs, annual returns, drawdowns, and source data.

        Returns:
            dict: Dictionary containing full statistical results.
        """
        return self.clientpost.gen_data_report()

    def generate_kpi_report(self) -> dict:
        """
        產生 KPI HTML 報表（勝率、獲利因子、最大回撤等），自動存成檔案。

        Returns:
            dict: 回傳報表產出狀態。

        Generate KPI report in HTML format, including win rate, profit factor, and drawdown.
        The report is saved to a file.

        Returns:
            dict: Report generation status.
        """
        return self.clientpost.gen_kpi_report()

    def generate_trade_chart(self):
        """
        根據交易紀錄產出圖表化報表（進出場點、K線、資金變化），並儲存為 HTML。

        Returns:
            dict: 報表產出狀態。

        Generate interactive trade chart with entry/exit points, candlestick, and capital curve.
        Output is saved as an HTML file.

        Returns:
            dict: Report generation status.
        """
        return self.clientpost.gen_trade_report()

    def set_lang(self, lang="en"):
        """
        設定系統預設語言，影響所有訊息顯示與國際化翻譯（i18n）內容。


        Args:
            lang (str): 語言代碼，支援以下選項：
                - 'en': 英文
                - 'zh-tw': 繁體中文
                - 'zh-cn': 簡體中文
                預設為 'en'。

        Returns:
            None: 僅設定內部語言狀態，無回傳值。

        Set the default language for system messages and internationalized (i18n) strings.

        Args:
            lang (str): Language code. Supported values:
                - 'en': English
                - 'zh-tw': Traditional Chinese
                - 'zh-cn': Simplified Chinese
                Default is 'en'.

        Returns:
            None: This method updates internal language state and returns nothing.
        """
        _set_lang(lang)

    def get_start_date(self, to_date: str, timeframe: str, kbar_num: int) -> str:
        """
        根據結束日期與K棒數量，計算回測所需的起始日期（僅支援 D1 週期）。

        以每週 5 個交易日為計算基準，向前推算足夠的日曆週數，以確保涵蓋所需的 K 棒數。

        Args:
            to_date (str): 結束日期，格式為 'YYYY-MM-DD'。
            timeframe (str): 時間週期，目前僅支援 'D1'（日線）。
            kbar_num (int): 所需的 K 棒數量（以交易日計算）。

        Returns:
            str: 計算出的起始日期，格式為 'YYYY-MM-DD'。

        Raises:
            ValueError: 若 timeframe 不為 'D1' 則拋出例外。

        Calculate the backtest start date based on the end date and required K-bar count.
        Only D1 (daily) timeframe is currently supported.

        Uses 5 trading days per week as the baseline, and advances by whole weeks to ensure
        the required number of bars is covered.

        Args:
            to_date (str): End date in 'YYYY-MM-DD' format.
            timeframe (str): Timeframe string; only 'D1' (daily) is currently supported.
            kbar_num (int): Required number of K-bars (counted in trading days).

        Returns:
            str: Calculated start date in 'YYYY-MM-DD' format.

        Raises:
            ValueError: Raised if timeframe is not 'D1'.
        """
        return _get_start_date(to_date, timeframe, kbar_num)
