import requests
import os
from dotenv import load_dotenv
from tqdm import tqdm

from db_sync import _dataflow


load_dotenv()
class sync_Dataflow:

    def Dataflow():
        url = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/dataflow/all/all/all/?format=fusion-json"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            DF = data['Dataflow']
            list_df = []
            print("Đang đồng bộ Dataflow")
            for i in tqdm(DF):
                agency_df = i['agencyId']
                df_id = i['id']
                df_name = i['names'][0]['value']
                version_df = str(i['version'])

                dataStructureRef = i['dataStructureRef']

                agency_dsd = dataStructureRef.split(":")[2].replace("org.sdmx.infomodel.datastructure.DataStructure=", "").strip()
                dsd_id = dataStructureRef.split(":")[-1].split("(")[0]
                dsd_version = dataStructureRef.split("(")[1].replace(")", "")

                list_df.append({
                    'agency_df': agency_df,
                    'df_id': df_id,
                    'df_name': df_name,
                    'version_df': version_df,
                    'agency_dsd': agency_dsd,
                    'dsd_id': dsd_id,
                    'version_dsd': dsd_version,
                    'status': 1
                })

        _dataflow.truncate_table()
        _dataflow.ins_record(list_df)

