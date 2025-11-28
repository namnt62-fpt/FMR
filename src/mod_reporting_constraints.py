from api import FMR_API
from dotenv import load_dotenv
import os
import requests
import logging
from datetime import datetime,timezone
import json

load_dotenv()
logging.basicConfig(level=logging.INFO)


class RC:
    def get_dim_from_df(agency_df, df_id, version):
        """
        Hàm lấy thông tin các DIM từ DF truyền vào.
        Từ DF truyền vào lấy ra được DSD tương ứng với DF. Từ DSD lấy ra các DIM của DSD
        """
        # Lấy ra thông tin DSD
        url_df = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/dataflow/{agency_df}/{df_id}/{version}/?format=fusion-json"
        res = requests.get(url_df)
        if res.status_code == 200:
            data = res.json()
            dataStructureRef = data["Dataflow"][0]["dataStructureRef"]
            agency_dsd = dataStructureRef.split(":")[2].replace("org.sdmx.infomodel.datastructure.DataStructure=", "").strip()
            dsd_id = dataStructureRef.split(":")[-1].split("(")[0]
            dsd_version = dataStructureRef.split("(")[1].replace(")", "")
        else:
            logging.error(f"Không thể kết nối đến FMR: {res.status_code} - {res.text}")

        # Từ thông tin DSD truy vấn API lấy thông tin DSD để trả ra các DIM
        url_dsd = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/datastructure/{agency_dsd}/{dsd_id}/{dsd_version}/?format=fusion-json"
        res = requests.get(url_dsd)
        if res.status_code == 200:
            data = res.json()
            DataStructure = data["DataStructure"]
            if len(DataStructure) > 1:
                arr_DIM = []
                logging.warning(f"{df_id} được gắn với 2 DSD. Vui lòng kiểm tra lại")
            else:
                arr_DIM = []
                DIM = DataStructure[0]["dimensionList"]["dimensions"]
                for i in DIM:
                    arr_DIM.append(i["id"])
        else:
            logging.error(f"Không thể kết nối đến FMR: {res.status_code} - {res.text}")
        return arr_DIM


    def make_json_rc(agency_df, df_id, df_version, name_df, arr_DIM):
        """
        Hàm tạo ra json rc mẫu từ arr_DIM là các DIM của DSD lấy từ DF.
        RC trong json có rc_name lấy tương ứng với tên của DF, RC_ID thì thay ký tự DF mặc định của DF_ID thành RC.
        """
        def build_include_cube(dimensions, default_values=None):
            include_cube = {}
            for dim in dimensions:
                include_cube[dim] = {
                    "removePrefix": False,
                    "values": default_values.get(dim, []) if default_values else [],
                    "cascade": []
                }
            return include_cube
        
        rc_id = "RC" + df_id[2:]
        urn_rc = f"urn:sdmx:org.sdmx.infomodel.registry.DataConstraint={agency_df}:{rc_id}({df_version})"
        urn_df = f"urn:sdmx:org.sdmx.infomodel.datastructure.Dataflow={agency_df}:{df_id}({df_version})"
        
        json_temp = {
            "meta": {
                "id": "IREF134872",
                "test": False,
                "prepared": datetime.now(timezone.utc).isoformat(),
                "contentLanguages": ["vi"],
                "sender": {"id": "FusionRegistry"},
            },
            "DataConstraint": [
                {
                    "id": rc_id,
                    "urn": urn_rc,
                    "names": [
                        {"locale": "vi", "value": name_df}
                    ],
                    "agencyId": agency_df,
                    "version": df_version,
                    "isFinal": False,
                    "definingDataPresent": False,
                    "type": "CubeRegionConstraint",
                    "attachments": [
                        urn_df
                    ],
                    "includeCube": build_include_cube(arr_DIM, default_values=None),
                }
            ],
        }
        return json_temp
    
    def get_df_non_RC():
        """
        Hàm lấy ra danh sách DF chưa được khai RC.
        Danh sách này sẽ được thả vào dropdown list trên giao diện flet.
        """
        url = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/dataflow/all/all/all/?format=fusion-json&references=parents"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            DataConstraint = data['DataConstraint']
            arr_urn_df = []
            for i in DataConstraint:
                attachments = i['attachments']
                arr_urn_df = arr_urn_df + attachments

            Dataflow = data['Dataflow']
            arr_df = []
            for j in Dataflow:
                if j['urn'] not in arr_urn_df:
                    agency_df = j['agencyId']
                    df_name = j['names'][0]['value']
                    df_id = j['id']
                    df_version = j['version']
                    arr_df.append({
                        'agency_df': agency_df,
                        'df_name': df_name,
                        'df_id': df_id,
                        'df_version': df_version
                    })
        else:
            logging.error(f"Không thể kết nối đến FMR: {res.status_code} - {res.text}")
        return arr_df
        
# X = RC.get_df_non_RC()
# print(X)

# Y = RC.get_dim_from_df("B000.B002", "DF_100_UP_VER", "1.0")   
# X = RC.make_json_rc("B000.B002", "DF_100_UP_VER", "1.0", "RC_100_UP_VER", Y)
# print(X)
