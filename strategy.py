import bk_test

def main(account=123, password="", server="",symbol="", capital=10000, volume=1, toggle=True,log=print, backtest_log=None, alert=None):
    # alert(title, message)：跨執行緒彈窗回呼（虧損警戒用）。舊版策略碼沒有這個
    # 具名參數 → 用 TypeError 退回不帶 alert 的呼叫，維持相容。
    try:
        try:
            bk_test.main(account=account,password=password,server=server,symbol=symbol,capital=capital,volume=volume,toggle=toggle,log=log,backtest_log=backtest_log,alert=alert)
        except TypeError:
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


# ── 2026-08-25：讓 UI 能問策略本人「本金 X 會下幾手」 ──
#   背景：資金規模下拉原本用「伺服器建議手數 × 本金倍率」線性推算，但策略真正的
#   手數是 Layer 1A：max(base*0.5, min(base*mult, (capital/10000)*base))，有地板
#   與天花板，且 base/mult 都是**打包當下烘死**的，改伺服器改不到。兩邊各自推算
#   就會不一致（實測 XAUUSD base=0.03：顯示 0.02 實下 0.03；顯示 0.64 實下 0.07）。
#   改由策略自己回答 → 顯示值由定義等於實際下單量。
#   liveTransformer 1.4 起會注入 preview_volume/preview_base_volume；
#   舊版打包的 EXE 沒有這兩支 → 回 None，UI 自動退回舊的線性推算。

def preview_volume(capital):
    """在指定本金下，本策略實際會下的手數；取不到回 None。"""
    fn = getattr(bk_test, "preview_volume", None)
    if not callable(fn):
        return None
    try:
        v = float(fn(capital))
        return v if v > 0 else None
    except Exception:
        return None


def preview_base_volume():
    """本 EXE 打包時烘死的基礎手數；取不到回 None。"""
    fn = getattr(bk_test, "preview_base_volume", None)
    if not callable(fn):
        return None
    try:
        v = float(fn())
        return v if v > 0 else None
    except Exception:
        return None

if __name__ == "__main__":
    main()
