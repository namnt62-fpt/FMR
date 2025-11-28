import requests
import os
from dotenv import load_dotenv
from tqdm import tqdm

from db_sync import _codelist, _codelist_detail


load_dotenv()
class sync_codelist:

    def Codelist():
        url = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/codelist/all/all/all/?format=fusion-json"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            CL = data['Codelist']
            list_codelist = []
            _codelist_detail.truncate_table()
            print("Đang đồng bộ Codelist")
            for i in tqdm(CL):
                codelist_id = i['id']
                names = i['names']
                agency_codelist = i['agencyId']
                codelist_version = str(i['version'])
                codelist_name_en = ''
                codelist_name_vi = ''
                for n in names:
                    if n['locale'] == 'en':
                        codelist_name_en = n['value']
                    elif n['locale'] == 'vi':
                        codelist_name_vi = n['value']

                list_codelist.append({
                    'agency_codelist': agency_codelist,
                    'codelist_id': codelist_id,
                    'codelist_name_vi': codelist_name_vi,
                    'codelist_name_en': codelist_name_en,
                    'codelist_version': codelist_version,
                    'status': 1
                })

                items = i['items']

                list_codelist_detail = []
                for k in items:
                    codelist_code = k['id']
                    names = k['names']
                    code_name_en = ''
                    code_name_vi = ''
                    for j in names:
                        if j['locale'] == 'en':
                            code_name_en = j['value']
                        elif j['locale'] == 'vi':
                            code_name_vi = j['value']
                    list_codelist_detail.append({
                        'agency_codelist': agency_codelist,
                        'codelist_id': codelist_id,
                        'codelist_version': codelist_version,
                        'codelist_code': codelist_code,
                        'code_name_vi': code_name_vi,
                        'code_name_en': code_name_en,
                        'status': 1
                    })
                _codelist_detail.ins_record(list_codelist_detail)
            _codelist.truncate_table()
            _codelist.ins_record(list_codelist)