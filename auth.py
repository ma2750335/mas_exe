import requests
from cryptography.fernet import Fernet
import enum_setting as es
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

    if level in ["free_trail", "gold"]:
        access = {key: True for key in all_keys}
    elif level == "silver":
        access = {key: True for key in all_keys}
        access["trade_report"] = False
    elif level == "bronze":
        access["normal_report"] = True
        access["data_report"] = True
    elif level == "free":
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
    payload = {
        "email": email,
        "password": password,
        "device_info": get_device_info()
    }
    rsp = post_request(url, payload)

    if rsp["result"]:
        rsp["access"] = get_access_by_level(rsp["level"])
    return rsp


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
