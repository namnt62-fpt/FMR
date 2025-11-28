import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

class FMR_API():
    def  load_structures(body):
        """
        Hàm load_structures dùng để upload file json lên FMR với tham số body là dữ liệu json cần upload.
        Dùng để upload các cấu trúc như Dataflow, DataStructureDefinition, ConceptScheme, Agency, Organization, CategoryScheme, Category, Codelist, Code.
        """
        endpoint = f"{os.getenv('FMR')}/fmr/ws/secure/sdmxapi/rest"
        body_api = body
        auth = HTTPBasicAuth(os.getenv('USER_FMR'), os.getenv('PASSWORD_FMR'))
        headers = {"Content-Type": "application/json"}

        try:
            res = requests.post(url = endpoint, json = body_api, headers = headers, auth = auth)
            if res.status_code == 200:
                return f"OK - {str(res.status_code)}"
            else:
                return f"OK - {str(res.status_code)}"
        except:
            return "ERROR"
        
    def get_dataflow():
        url = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/dataflow/all/all/all/?format=fusion-json"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            dataflow = data['Dataflow']
        return dataflow
        

    def token_kho():
        """
        Hàm token_kho dùng để lấy token đăng nhập từ hệ thống với tham số user và password.
        Token được sử dụng để sử dụng cho api convert data từ excel sang xml
        """
        url = f"{os.getenv('ENDPOINT_KHO')}/api/qtdc/qtht/auth/login?userName={os.getenv('USER_KHO')}&password={os.getenv('PASSWORD_KHO')}"

        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        res = requests.post(url, headers=header)
        if res.status_code == 200:
            token = res.json()["data"]["accessToken"]
            logging.info(f"token_kho: {token}")
            return token
        else:
            logging.error(f"Không lấy được token kho {res.status_code} - {res.text}")
            return "Error"
        
    def token_dlm():
        """
        Hàm dùng để lấy token trên DLM
        Token lấy được sử dụng để upload dữ liệu lên DLM và kiểm tra trạng thái upload dữ liệu
        """
        url = f"{os.getenv('ENDPOINT_DLM')}/realms/TCTK-DLM/protocol/openid-connect/token"
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "username": os.getenv('USER_DLM'),
            "password": os.getenv('PASSWORD_DLM'),
            "grant_type": os.getenv('GRANT_TYPE_DLM'),
            "client_id": os.getenv('CLIENT_ID_DLM')
        }

        res = requests.post(url, headers=header, data=data)
        if res.status_code == 200:
            token = res.json()["access_token"]
            logging.info(f"token_dlm: {token}")
            return token
        else:
            logging.error("Không lấy được token dlm")
            return "Error"