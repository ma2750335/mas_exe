import ast

import requests
from cryptography.fernet import Fernet
import enum_setting as es
from env_info import UUID, GENAI_EXE_VERSION
import uuid
import socket
import platform
import socket
import subprocess
import json
# 這是 Fernet.generate_key() 產生的
SHARED_SECRET_KEY = b'qjtolGolAHeJFQIYHtdosSII6vhbGF07DgKY3mnU8bI='

fernet = Fernet(SHARED_SECRET_KEY)


def get_device_info():
    info = {}

    # 1. MAC 位址
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff)
                   for i in range(0, 8*6, 8)][::-1])
    info['mac'] = mac

    # 2. 主機名稱 + 系統平台
    info['hostname'] = socket.gethostname()
    info['platform'] = platform.platform()

    # 3. CPU 資訊
    info['cpu'] = platform.processor()

    # 4. 硬碟序號（需 admin 權限）
    try:
        result = subprocess.check_output(
            "wmic diskdrive get SerialNumber", shell=True)
        info['disk'] = result.decode().split('\n')[1].strip()
    except:
        info['disk'] = "unknown"

    # 5. 網路 IP
    info['ip'] = socket.gethostbyname(info['hostname'])

    return json.dumps(info)


def check_version():
    # CURRENT_VERSION = "1.0.1"
    CURRENT_VERSION = "1.0.0"
    return CURRENT_VERSION


def get_access_by_level(level: str) -> dict:
    all_keys = ["normal_report", "data_report", "kpi_report", "trade_report"]

    # 預設全部 False
    access = {key: False for key in all_keys}

    if level == "PRO":
        access = {key: True for key in all_keys}
    elif level == "GROWTH":
        access["normal_report"] = True
        access["data_report"] = True
        access["kpi_report"] = True
    elif level == "STARTER":
        access["normal_report"] = True
        access["data_report"] = True
    elif level == "FREE":
        access["normal_report"] = True

    return access


def post_request(url, payload):
    error_rsp = {
        "result": False,
        "msg": "An unexpected error occurred, please try again later."
    }
    try:
        response = requests.post(url, data=payload, verify=False)
        response.raise_for_status()  # 若回應非200，將拋出錯誤
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        # print("http_err",http_err)
        return error_rsp
    except Exception as err:
        # print("err:",err)
        return error_rsp
def mock_rsp():
    
    # ── Case 1：正常成功登入（PRO，無附帶訊息）────────────────────────────
    # rsp = {
    #     'result': True,
    #     'msg_toggle': False,
    #     'msg': '',
    #     'userId': '8cbacb88-b3ed-4f1d-876f-23db425b08c9',
    #     'level': 'PRO',
    #     'is_subsription': True,
    #     'healthy': 2,                 # 0=LOW / 1=MEDIUM / 2=HIGH
    #     'expire_date': '2026-12-31',
    #     'symbol': 'EURUSD',
    #     'strategy_id': 'test123',
    #     'capital': 10000,
    #     'lots': 0.1
    # }
    # 行為：不跳訊息 → result=True → 通過 FREE gate → 進主畫面；PRO+訂閱中 → 可多開

    # ── Case 2：成功登入「但附帶通知」（msg_toggle=True + result=True）──────
    rsp = {
        'result': True,
        'msg_toggle': True,
        'msg': '您的訂閱將於 3 天後到期，請及時續訂以免服務中斷。',
        'userId': '8cbacb88-...-23db425b08c9',
        'level': 'STARTER',
        'is_subsription': True,
        'healthy': 1,
        'expire_date': '2026-06-12',
        'symbol': 'EURUSD', 'strategy_id': 'test123', 'capital': 10000, 'lots': 0.03
    }
    # 行為：先跳「提醒」彈窗顯示 msg → 關閉後 result=True → 登入（兩旗標獨立）

    # ── Case 3：登入失敗，顯示後端原因（最常見）──────────────────────────
    # rsp = {
    #     'result': False,
    #     'msg_toggle': True,
    #     'msg': '帳號或密碼錯誤，請重新確認。',
    #     'level': None, 'is_subsription': False, 'healthy': 0
    # }
    # 行為：跳「登入失敗」彈窗顯示 msg → result=False → 不登入

    # ── Case 4：登入失敗，但「靜默不顯示」（風控情境）────────────────────
    # rsp = {
    #     'result': False,
    #     'msg_toggle': False,
    #     'msg': ''
    # }
    # 行為：完全不跳訊息、也不登入（後端決定不透露原因）

    # ── Case 5：成功但 FREE 方案 → 被前端方案 gate 擋在主畫面外 ───────────
    # rsp = {
    #     'result': True,
    #     'msg_toggle': False,
    #     'msg': '',
    #     'userId': '...', 'level': 'FREE', 'is_subsription': False, 'healthy': 2,
    #     'symbol': 'EURUSD', 'strategy_id': 'test123', 'capital': 10000, 'lots': 0.1
    # }
    # 行為：不跳訊息 → result=True，但 check_subscription('FREE') → 跳「需要升級會員」→ 不進主畫面

    # ── Case 6：GROWTH 沒訂閱也能登入（已移除訂閱卡控）────────────────────
    # rsp = {
    #     'result': True,
    #     'msg_toggle': False,
    #     'msg': '',
    #     'userId': '...', 'level': 'GROWTH', 'is_subsription': False, 'healthy': 0,
    #     'symbol': 'XAUUSD', 'strategy_id': 'g-strategy', 'capital': 50000, 'lots': 0.5
    # }
    # 行為：result=True → check_subscription('GROWTH', is_subsription=False) → 非FREE 一律通過 → 進主畫面
    #       但 is_pro=False（非PRO）→ 受單例鎖，不能多開

    # ── Case 7：msg 帶 HTML 連結（_show_html_alert 是 RichText，可放 <a>）──
    # rsp = {
    #     'result': False,
    #     'msg_toggle': True,
    #     'msg': '此帳號已被停用。<br>請至 <a href="https://mas.mindaismart.com/support" style="color:#0078D7;">客服中心</a> 申訴。',
    # }
    # 行為：跳「登入失敗」彈窗，msg 內的連結可點擊（HTML 正常渲染）
    return rsp

def login_request(email, password):
    # 延遲 import 避免模組載入順序問題；default_lang 取使用者「當下」選擇的語言
    from i18n_strings import get_current_lang
    url = es.url.login.value
    strategy_uuid = UUID
    payload = {
        "email": email,
        "password": password,
        "device_info": get_device_info(),
        "uuid": strategy_uuid,
        "genai_exe_version": GENAI_EXE_VERSION,
        "default_lang": get_current_lang()
    }
    # rsp = post_request(url, payload)
    # testing
    # TODO: implement testing
    # print('rsp',  rsp)
    rsp = mock_rsp()
    print(rsp)
    # rsp['healthy']=0
    # testing
    if rsp["result"]:
        rsp["access"] = get_access_by_level(rsp["level"])
    return rsp


def get_strategy_health(strategy_id=None, health_token=None):
    """Fetch strategy health from GET /api/mas-genie/strategy-health/{strategy_id}.

    Auth is passed via X-Health-Token header (64-char hex embedded at build time).

    Args:
        strategy_id: userGenieStrategyId UUID. Defaults to env_info.UUID.
        health_token: 64-char hex token. Defaults to env_info.HEALTH_TOKEN.

    Returns:
        dict with keys: healthLevel, shouldStop, action, message, messageKey,
        severity, subscriptionStatus, eliteStatus — or None if request fails.
    """
    from env_info import UUID as _UUID, HEALTH_TOKEN as _DEFAULT_TOKEN
    if strategy_id is None:
        strategy_id = _UUID
    if health_token is None:
        health_token = _DEFAULT_TOKEN

    url = f"{es.url.strategy_health.value}/{strategy_id}"
    try:
        response = requests.get(
            url,
            headers={"X-Health-Token": health_token},
            verify=False,
            timeout=10,
        )
        return response.json()
    except Exception:
        return None


def healthy_from_login(n) -> dict:
    """Convert login-response healthy int (0/1/2) → health-response dict.

    Normalises the initial value at login so every downstream consumer
    (display badge, alert, auto-stop) only ever deals with dicts.
    """
    _level_map = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}
    level = _level_map.get(n, "UNKNOWN")
    action = "CONTINUE" if level == "HIGH" else "WARN"
    return {"healthLevel": level, "shouldStop": False, "action": action, "message": None}


def encrypt_payload(data_dict: dict) -> str:
    import json
    json_data = json.dumps(data_dict).encode()
    return fernet.encrypt(json_data).decode()


if __name__ == "__main__":
    # 測試用：
    result = login_request("sam@mindaismart.com", "12345")
    print(result)
    if result:
        result_value = result.get("result")  # 或 response_data["result"]
        print(f"登入結果：{result_value}")
    else:
        print("登入失敗或無回應")
