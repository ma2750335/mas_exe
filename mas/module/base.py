def clean_symbol(symbol: str) -> str:
    """
    將 MT5 商品代碼中的 '.sml' 後綴去除，其餘後綴（如 '.UK'）保留不變。

    Args:
        symbol (str): MT5 原始商品代碼，例如 'EURUSD.sml' 或 'BATS_CFD.UK'。

    Returns:
        str: 清理後的商品代碼。若原始代碼以 '.sml'（不區分大小寫）結尾，
             則去除該後綴；否則原樣回傳。

    Remove the '.sml' suffix from an MT5 symbol code. Other suffixes (e.g., '.UK') are kept unchanged.

    Args:
        symbol (str): Raw MT5 symbol code, e.g., 'EURUSD.sml' or 'BATS_CFD.UK'.

    Returns:
        str: Cleaned symbol code. If the original code ends with '.sml' (case-insensitive),
             the suffix is stripped; otherwise the original string is returned unchanged.
    """
    if symbol.lower().endswith('.sml'):
        return symbol.rsplit('.', 1)[0]
    return symbol
