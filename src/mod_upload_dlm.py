import requests
import os
from tools import Tools
import base64

import glob
import sys
from dotenv import load_dotenv

from api import FMR_API

def resource_path(relative_path):
    """Lấy đường dẫn thực khi chạy exe hoặc script"""
    try:
        # Khi chạy file exe
        base_path = sys._MEIPASS
    except Exception:
        # Khi chạy bằng python trực tiếp
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ✅ Trỏ đúng tới src/.env
dotenv_path = resource_path(os.path.join("src", ".env"))
print("Đang load:", dotenv_path)
load_dotenv(dotenv_path)

class UPLOAD:
    def get_df():
        urn = []
        excel_file = Tools.get_excel_in_dir(Tools.get_current_path())
        for item_file in excel_file:
            name_only = os.path.splitext(item_file)[0]
            X = name_only.split("-")
            agency = X[0]
            df = X[2]
            version = X[1]
            urn.append(f"urn:sdmx:org.sdmx.infomodel.datastructure.Dataflow=B000.{agency}:{df}({version}.0)")

        url = f"{os.getenv('FMR')}/fmr/ws/registry/downloadStructures"
        boby = {
            "compression": False,
            "incCrossRef": True,
            "includeParents": True,
            "returnFormat": "V2_1",
            "detail": "raw",
            "urns": urn
        }
        res = requests.post(url, json=boby)
        if res.status_code != 200:
            return res.status_code, res.text
        else:
            # with open(f"dataflow.xml", "w", encoding="utf-8") as f:
            #     f.write(res.text)
            return res.status_code, res.text

    def convert_data(agency, path, version, df):
        url = f"{os.getenv('ENDPOINT_CONVERT_DATA')}/api/kho/convert/compact-sdmx-blob-v3"

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
        }

        token = FMR_API.token_kho()
        if not token:
            return "Error"

        headers["Authorization"] = f"Bearer {token}"

        files = {
            "excelFile": (
                path.split("\\")[-1],  # tên file
                open(path, "rb"),      # file object
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        }

        data = {
            "dataflowId": df,
            "agency": agency,
            "version": version
        }

        res = requests.post(url = url, headers=headers, files=files, data=data)
        if res.status_code != 200:
            return res.status_code , res.text
        else:
            blobData = res.json()['data']['blobData']
            xml = base64.b64decode(blobData).decode("utf-8")

            with open(f"{df}.xml", "w", encoding="utf-8") as f:
                f.write(xml)
            
            return res.status_code, res.text

    def upload_df(content_xml, data_space):
        if data_space == "tctk-disseminate":
            url = f"{os.getenv('ENDPOINT_UPLOAD_DF')}:80/rest/structure/"
        elif data_space == "tctk-design":
            url = f"{os.getenv('ENDPOINT_UPLOAD_DF')}:81/rest/structure/"

        header = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {FMR_API.token_dlm()}",
            "Origin": f"{os.getenv('ENDPOINT_UPLOAD_DF')}",
        }

        res = requests.post(url = url , data=content_xml, headers=header)
        return res.status_code, res.text

    def upload_dlm(path_file_xml, data_space):
        url = f"{os.getenv('ENDPOINT_UPLOAD_DLM')}/2/import/sdmxFile"
        
        headers = {
            "Authorization": f"Bearer {FMR_API.token_dlm()}"  # token của bạn
        }

        data = {
            "dataspace": data_space,
            "targetVersion": "0",
            "restorationOptionRequired": False,
            "validationType": "1"
        }

        filename = os.path.basename(path_file_xml)
        files = {
            "file": (
                filename,
                open(path_file_xml, "rb"),
                "application/xml"
            )
        }
        res = requests.post(url = url, headers=headers, data=data, files=files)
        return res.status_code, res.text

    def check_status_dlm(id, data_space):
        url = f"{os.getenv('ENDPOINT_UPLOAD_DLM')}/2/status/request"
        headers = {
            "Authorization": f"Bearer {FMR_API.token_dlm()}"
        }

        data = {
            "dataspace": data_space,
            "id": id
        }

        res = requests.post(url, headers=headers, data=data)
        if res.status_code != 200:
            return "Error"
        else:
            status = res.json()["outcome"]
            return status