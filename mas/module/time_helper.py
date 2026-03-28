from datetime import datetime, timedelta


def normalize_datetime_params(params: dict) -> dict:
    """
    將字典中的 'from' 與 'to' 日期字串標準化為 datetime 物件。

    支援格式包括：
    - 'YYYY-MM-DD'
    - 'YYYY-MM-DD HH:MM:SS'
    並會自動將 'to' 日期補上當日最後一秒（23:59:59），以利涵蓋整日資料區間。

    Args:
        params (dict): 包含 'from' 和 'to' 欄位的查詢參數字典，可為 datetime 或字串格式。

    Returns:
        dict: 處理後的參數字典，'from' 與 'to' 欄位皆為 datetime 物件。

    Normalize 'from' and 'to' datetime parameters in a dictionary.

    Supports the following formats:
    - 'YYYY-MM-DD'
    - 'YYYY-MM-DD HH:MM:SS'
    Automatically appends 23:59:59 to the 'to' date to ensure full-day coverage.

    Args:
        params (dict): Dictionary containing 'from' and 'to' keys. Values can be strings or datetime objects.

    Returns:
        dict: Dictionary with 'from' and 'to' fields converted to datetime objects.
    """
    def parse(val, is_to=False):
        if isinstance(val, str):
            try:
                dt = datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                dt = datetime.strptime(val, "%Y-%m-%d")
                if is_to:
                    dt = dt.replace(hour=23, minute=59, second=59)
                else:
                    dt = dt.replace(hour=0, minute=0, second=0)
            return dt
        return val

    params["from"] = parse(params.get("from"), is_to=False)
    params["to"] = parse(params.get("to"), is_to=True)
    return params


def get_start_date(to_date: str, timeframe: str, kbar_num: int) -> str:
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
    if timeframe != "D1":
            to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")
            start_date = to_date_obj - timedelta(days=4)
    else:
        # 計算總共要回推幾天（以週為單位）
        weeks = kbar_num // 5
        if kbar_num % 5 != 0:
            weeks += 1
        delta_days = weeks * 7

        # 計算日期
        to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")
        start_date = to_date_obj - timedelta(days=delta_days)

    return start_date.strftime("%Y-%m-%d")
