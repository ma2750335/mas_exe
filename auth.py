import ast

import requests
from cryptography.fernet import Fernet
import enum_setting as es
from env_info import UUID
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
    elif level == "STARTER":
        access = {key: True for key in all_keys}
        access["trade_report"] = False
    elif level == "FREETRAIL":
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


def login_request(email, password):
    url = es.url.login.value
    strategy_uuid = UUID
    payload = {
        "email": email,
        "password": password,
        "device_info": get_device_info(),
        "uuid": strategy_uuid
    }
    rsp = post_request(url, payload)
    # testing
    # TODO: implement testing
    print('rsp',  rsp)
    # data_str = "{'result': False, 'code': 'Error_exe_login_001', 'msg': 'Incorrect_password', 'userId': '8cbacb88-b3ed-4f1d-876f-23db425b08c9', 'level': 'STARTER', 'is_subsription': True, 'remainingDays': None, 'versionCode': '0.0.5', 'healthy': 0, 'symbol':'EURUSD','strategy_id':'test123','capital':10000,'lots':0.1}"
    # rsp = ast.literal_eval(data_str)
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
