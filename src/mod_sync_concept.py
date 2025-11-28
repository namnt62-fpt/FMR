import requests
import os
from dotenv import load_dotenv
from tqdm import tqdm

from db_sync import _concept, _concept_representation


load_dotenv()
class sync_concept:

    def conceptscheme():
        url = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/conceptscheme/all/all/all/?format=fusion-json"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            CS = data['ConceptScheme']
            list_records = []
            _concept_representation.truncate_table()
            print("Đang đồng bộ Concept Scheme")
            for i in tqdm(CS):
                concept_id = i['id']
                concept_name = i['names'][0]['value']
                description = i['descriptions'][0]['value'] if 'descriptions' in i and len(i['descriptions']) > 0 else ''
                agency_id = i['agencyId']
                version = str(i['version'])
                list_records.append({
                    'agency_id': agency_id,
                    'concept_id': concept_id,
                    'concept_version': version,
                    'concept_name': concept_name,
                    'description': description,
                    'status': 1
                })
                items = i['items']

                list_concept_representation = []
                for i in items:
                    representation_id = i['id']
                    representation_name = i['names'][0]['value']
                    try:
                        text = i['representation']['representation']
                        representation_type = 'Representation Codelist'
                        agency_codelist = text.split(":")[2].replace("org.sdmx.infomodel.codelist.Codelist=", "").strip()
                        codelist = text.split(":")[-1].split("(")[0]
                        codelist_version = text.split("(")[1].replace(")", "")
                    except:
                        representation_type = 'Representation String'
                        agency_codelist = ""
                        codelist = ""
                        codelist_version = ""
                    list_concept_representation.append({
                        'agency_concept': agency_id,
                        'concept_id': concept_id,
                        'concept_version': version,
                        'representation_id': representation_id,
                        'representation_name': representation_name,
                        'representation_type': representation_type,
                        'agency_codelist': agency_codelist,
                        'codelist_id': codelist,
                        'codelist_version': codelist_version,
                        'status': 1
                    })
                _concept_representation.ins_record(list_concept_representation)
            _concept.truncate_table()
            _concept.ins_record(list_records)