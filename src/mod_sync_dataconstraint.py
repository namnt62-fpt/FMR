import requests
import os
from dotenv import load_dotenv
from tqdm import tqdm

from db_sync import _dataconstraint, _dataconstraint_detail


load_dotenv()
class sync_dataconstraint:

    def DataConstraint():
        url = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/dataconstraint/all/all/all/?format=fusion-json"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            RC = data['DataConstraint']
            list_rc = []
            _dataconstraint_detail.truncate_table()
            print("Đang đồng bộ Data Constraint")
            for i in tqdm(RC):
                agency_rc = i['agencyId']
                rc_id = i['id']
                rc_name = i['names'][0]['value']
                version_rc = str(i['version'])
                attachments = i['attachments']
                if len(attachments) > 1:
                    print(f"RC {rc_id} được gán cho nhiều hơn 1 DF: {attachments}")
                else:
                    text = attachments[0]
                    agency_df = text.split(":")[2].replace("org.sdmx.infomodel.datastructure.Dataflow=", "").strip()
                    df_id = text.split(":")[-1].split("(")[0]
                    df_version = text.split(":")[-1].split(")")[0].split("(")[1]

                list_rc.append({
                    'agency_rc': agency_rc,
                    'rc_id': rc_id,
                    'rc_name': rc_name,
                    'version_rc': version_rc,
                    'agency_df': agency_df,
                    'df_id': df_id,
                    'version_df': df_version,
                    'status': 1
                })
                list_rc_detail = []
                DIM = i['includeCube']
                for key, value in DIM.items():
                    val = ", ".join(value['values'])
                    list_rc_detail.append({
                        'agency_rc': agency_rc,
                        'rc_id': rc_id,
                        'rc_name': rc_name,
                        'version_rc': version_rc,
                        'agency_df': agency_df,
                        'df_id': df_id,
                        'version_df': df_version,
                        'dimension_id': key,
                        'included_values': val,
                        'status': 1
                    })

                _dataconstraint_detail.ins_record(list_rc_detail)
 
            _dataconstraint.truncate_table()
            _dataconstraint.ins_record(list_rc)
