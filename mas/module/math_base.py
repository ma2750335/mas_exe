from decimal import Decimal


def _get_decimal_nub(price: float) -> int:
    """
    根據價格的小數位數計算精度倍率（decimal_nub）。

    例如：
    - 1.10001（5 位小數）→ 100000
    - 1915.51（2 位小數）→ 100
    - 100（整數）→ 1

    Args:
        price (float): 參考價格。

    Returns:
        int: 小數精度對應的倍率（1、10、100、1000、10000 或 100000）。

    Calculate the decimal precision multiplier (decimal_nub) based on a price value.

    Examples:
    - 1.10001 (5 decimal places) → 100000
    - 1915.51 (2 decimal places) → 100
    - 100 (integer) → 1

    Args:
        price (float): Reference price value.

    Returns:
        int: Decimal precision multiplier (1, 10, 100, 1000, 10000, or 100000).
    """
    d = Decimal(str(price)).normalize()
    decimal_places = -d.as_tuple().exponent if d.as_tuple().exponent < 0 else 0
    if decimal_places > 4:
        return 100000
    if decimal_places == 4:
        return 10000
    elif decimal_places == 3:
        return 1000
    elif decimal_places == 2:
        return 100
    elif decimal_places == 1:
        return 10
    else:
        return 1


def get_spread_fee_for_tick(df):
    """
    根據 Tick 資料計算點差費用與價格精度（decimal_nub），用於後續交易損益估算。

    將 ask - bid 的差值作為 spread，並計算加權後的平均 spread 作為 fee。
    同時計算標的價格的小數點精度，轉換為 decimal_nub（如 100000、100、1）。

    過濾規則：移除 ask < bid（無效報價）或 bid/ask 為 NaN 的列。

    Args:
        df (pd.DataFrame): 必填，含有欄位 ['bid', 'ask', 'last'] 的 Tick 資料。

    Returns:
        dict: 回傳點差參數，包含：
            - decimal_nub (int): 精度倍率，根據 last 價格的小數位數計算。
            - fee (float): 計算後的平均點差費用（四捨五入至小數點後 1 位）。

    Raises:
        ValueError: 若過濾後的資料為空（所有列均無效），則拋出此例外。

    Estimate spread fee and price precision (decimal_nub) based on Tick data.

    Calculates the spread as (ask - bid), then derives a weighted average spread as the fee.
    Also determines the decimal precision from the 'last' price to get the corresponding multiplier.

    Filtering rules: rows where ask < bid or bid/ask is NaN are excluded.

    Args:
        df (pd.DataFrame): Required. Tick DataFrame with columns ['bid', 'ask', 'last'].

    Returns:
        dict: Spread fee configuration with:
            - decimal_nub (int): Decimal multiplier derived from the price precision.
            - fee (float): Estimated average spread fee, rounded to 1 decimal place.

    Raises:
        ValueError: If no valid rows remain after filtering (all rows are invalid).
    """
    df = df.copy()
    df = df[(df["ask"] >= df["bid"]) & df["bid"].notna() & df["ask"].notna()]
    df["spread"] = df["ask"] - df["bid"]

    if df.empty:
        raise ValueError("no spread data")

    fee = (df["spread"].mean() + 0.25 * df["spread"].std()) / 2
    price = df["last"].iloc[0]

    return {
        "decimal_nub": _get_decimal_nub(price),
        "fee": round(fee, 1)
    }


def get_spread_fee(df):
    """
    根據 Bar 資料計算點差費用與價格精度（decimal_nub），用於後續交易損益估算。

    此函式預期傳入資料中已包含 spread 欄位，會計算加權後的平均 spread 作為 fee，
    並依據 close 價格的小數位數估算 decimal_nub（精度倍率）。

    Args:
        df (pd.DataFrame): 必填，包含 'spread' 與 'close' 欄位的 Bar 資料。
                           資料不可為空（否則拋出 IndexError）。

    Returns:
        dict: 回傳點差參數，包含：
            - decimal_nub (int): 精度倍率，根據 close 價格的小數位數決定。
            - fee (float): 平均點差費用（加權後，四捨五入至小數點後 1 位）。

    Raises:
        IndexError: 若 df 為空，無法讀取第一列 close 價格。

    Estimate spread fee and price precision (decimal_nub) based on Bar (candlestick) data.

    Assumes the input DataFrame already contains a 'spread' column.
    Calculates the weighted average spread as the fee and determines decimal precision
    from the 'close' price to get the corresponding multiplier.

    Args:
        df (pd.DataFrame): Required. Bar data containing 'spread' and 'close' columns.
                           Must not be empty (raises IndexError otherwise).

    Returns:
        dict: Spread fee configuration including:
            - decimal_nub (int): Decimal multiplier derived from the price precision.
            - fee (float): Estimated average spread fee, rounded to 1 decimal place.

    Raises:
        IndexError: If df is empty and the first 'close' row cannot be accessed.
    """
    if df.empty:
        raise ValueError("no spread data")

    fee = (df['spread'].mean() + 0.25 * df['spread'].std()) / 2
    price = df['close'].iloc[0]

    return {
        "decimal_nub": _get_decimal_nub(price),
        "fee": round(fee, 1)
    }
