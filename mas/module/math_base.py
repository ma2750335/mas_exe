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



# ── 窗內完全沒有點差資料時的退路值 ──
#   單位＝DB `spread` 欄位的原始點數（與 decimal_nub 同一個刻度）。
#   取自各商品自己的歷史中位數（只算 spread>0 的 K 棒），2026-08-07 量測。
#   重新產生：SELECT code, spread FROM fxpriceddata_h1 WHERE spread>0  → 取各 code 的中位數
#            （H1 與 D1 不同時取較大者，偏保守）
#
#   ⚠️ 這是估計值、不是真實歷史點差。舊年份的實際點差普遍比現在寬，所以這組數字偏樂觀；
#      但比原本「spread=0 就當成免費交易」正確太多——實測 OILCash 的 D1 資料有 79% 是 0
#      （2010~2022 整段沒有點差），5 支 OILCash D1 菁英的訓練窗有 61% 不付成本、
#      錨點窗 100% 不付成本，等於在無摩擦市場裡驗證策略。
#
#   ⚠️ SymbolSettingEnum 那張表不能拿來當退路：它沒有 OILCash/NGASCash/指數/加密貨幣
#      （正是零點差最嚴重的那批），而且查無時回傳 fee=0.0＝又變回免費交易。
_FALLBACK_SPREAD = {
    "XAUUSD": 37.0,   "XAGUSD": 43.0,   "OILCash": 3.0,    "BRENTCash": 3.0,
    "NGASCash": 16.0, "HGCOP-SEP26": 74.0,
    "GER40Cash": 200.0, "UK100Cash": 220.0, "US30Cash": 400.0, "US500Cash": 70.0,
    "US100Cash": 220.0, "JP225Cash": 8.0,
    "BTCUSD": 6000.0, "ETHUSD": 335.0,
    "USDJPY": 22.0, "AUDUSD": 16.0, "USDCAD": 18.0, "USDCHF": 23.0, "NZDUSD": 25.0,
}


# ── 報價刻度（decimal_nub）：**每個商品一個定值**，不要每個回測窗各自推 ──
#   2026-08-18 實測：DB 裡有 6 個商品的報價精度**跨年不一致**（資料源本身的斷層）——
#     US100Cash 2011-15=10 → 2016+=100      US500Cash 2018=10、其餘 100
#     GER40Cash 2011-16=10 → 2017=100 → 2018=10 → 2019+=100
#     UK100Cash 2011-14=10 → 2015+=100      XAGUSD 2010-11=100 → 2012+=1000
#     US30Cash  三種都有 [1, 10, 100]
#   刻度是成本的分母（cost = fee*2/decimal_nub），所以窗落在哪一段年份，
#   同一支策略的交易成本就差一個數量級：
#     GER40Cash D1 深史2016 窗 刻度10 → 來回成本 0.392%
#     GER40Cash D1 訓練窗    刻度100 → 來回成本 0.008%   ＝ 49 倍
#   那個窗會刷掉所有策略 → 深史檢查（過半數為正）被廢掉一半效力。
#   而且是**會走動的地雷**：窗隨日曆前進，明年深史窗換成 2017/2018 又會踩到。
#
#   ⚠️ 2026-08-07 的 _infer_decimal_nub 修的是「同一窗內會亂跳」（尾隨 0 的問題），
#      修不到這一種——那是資料本身不同年份精度就不同，推得再準也只是忠實反映斷層。
#      唯一正解是釘死成常數。
#
#   取值＝各商品全歷史（D1/H1/M15/M5 四個週期取最大）推出的刻度。
#   已驗證 23 個商品**全歷史推出的值 == 最近 3000 根推出的值**，
#   所以釘死不改變現行（近期資料）的行為，只把舊年份的窗拉回同一把尺。
#   重新產生：server/scratch/_nuball.py
_SYMBOL_NUB = {
    "XAUUSD": 100,      "XAGUSD": 1000,     "OILCash": 100,     "BRENTCash": 100,
    "NGASCash": 1000,   "HGCOP-SEP26": 10000,
    "US100Cash": 100,   "US500Cash": 100,   "GER40Cash": 100,   "UK100Cash": 100,
    "US30Cash": 100,    "JP225Cash": 1,     "Nvidia_turbo": 100,
    "BTCUSD": 100,      "ETHUSD": 100,
    "USDJPY": 1000,
    "EURUSD": 100000,   "GBPUSD": 100000,   "EURGBP": 100000,   "USDCAD": 100000,
    "USDCHF": 100000,   "AUDUSD": 100000,   "NZDUSD": 100000,
}


def _resolve_decimal_nub(prices, symbol=None):
    """有 symbol 就用釘死的刻度；查無（含上線時的券商代碼如 GOLD_）才退回推算。

    上線（MT5）走的是 get_spread_fee_for_tick / get_spread_fee(rates)，都**不傳 symbol**，
    所以行為完全不變——而且上線拿到的是當期報價、推算本來就正確，
    與本表的值一致（已逐商品驗證）。釘死只作用在回測（history_data_db 會傳 canonical code）。
    """
    if symbol:
        pinned = _SYMBOL_NUB.get(symbol)
        if pinned:
            return pinned
    return _infer_decimal_nub(prices)


def _infer_decimal_nub(prices) -> int:
    """從整段價格序列推報價精度（刻度倍率），取「最大小數位數」。

    ⚠️ 不可只看單一價格（原本是 df['close'].iloc[0] / df['last'].iloc[0]）：
       浮點數的尾隨 0 在 str() 時會消失——
         DB 1.14380 → float → "1.1438"  → 判 4 位 → 刻度 10000（正解 100000）
         DB 3312.80 → float → "3312.8"  → 判 1 位 → 刻度 10   （正解 100）
         DB 71.00   → float → "71.0"    → 判 0 位 → 刻度 1    （正解 100）
       2026-08-07 實測：掃 60 個不同起始日，同商品同週期會推出 1/10/100 三種刻度，
       交易成本因此相差 10~98 倍。回測窗只要位移一週，成本就可能差一個數量級——
       這正是「同一支策略窗位移就翻盤」的來源之一（40 支 ACTIVE 菁英裡，
       有 12 支的兩個錨點窗只差 3 週、刻度就差 10 倍）。

       尾隨 0 只會讓位數變少、不會變多 → 取整窗最大值必然收斂到真實報價精度。
       實測 8 組商品×週期全部 60/60 收斂到唯一正確值。
    """
    best = 0
    for v in list(prices)[:2000]:   # 取樣 2000 根足夠收斂，避免大窗變慢
        try:
            d = Decimal(str(float(v))).normalize()
        except Exception:
            continue
        places = -d.as_tuple().exponent if d.as_tuple().exponent < 0 else 0
        if places > best:
            best = places
            if best >= 5:
                break
    return 10 ** min(best, 5) if best > 0 else 1

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

    return {
        "decimal_nub": _infer_decimal_nub(df["last"]),
        "fee": round(fee, 1)
    }


def get_spread_fee(df, symbol=None):
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

    # ⚠️ 只用「真的有點差資料」的 K 棒算 fee。
    #    DB 裡大量歷史資料的 spread 欄位是 0（代表「沒收到報價」而非「零點差」）：
    #    OILCash D1 有 79% 是 0、XAUUSD D1 有 49%、GER40Cash D1 有 69%。
    #    把 0 一起平均進去 = 系統性低估成本，窗越舊低估越多；
    #    整個窗都是 0 時更等於在無摩擦市場回測（2026-08-07 實測 5 支 OILCash D1 菁英
    #    的錨點窗 100% 免費）。
    nz = df.loc[df['spread'] > 0, 'spread']
    if len(nz) > 0:
        fee = (nz.mean() + 0.25 * nz.std()) / 2
        if fee != fee:                 # NaN（只有一根 K 棒時 std 是 NaN）→ 退回純均值
            fee = float(nz.mean())
    else:
        fee = _FALLBACK_SPREAD.get(symbol, 2.0)

    return {
        "decimal_nub": _resolve_decimal_nub(df['close'], symbol),
        "fee": round(float(fee), 1)
    }
