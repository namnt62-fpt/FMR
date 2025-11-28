import requests
import os
from dotenv import load_dotenv
from tqdm import tqdm

from db_sync import _datastructure, _datastructure_detail


load_dotenv()
class sync_datastructure:

    def DataStructure():
        url = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/datastructure/all/all/all/?format=fusion-json"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            DSD = data['DataStructure']
            list_dsd = []
            _datastructure_detail.truncate_table()
            print("Đang đồng bộ Data Structure")
            for i in tqdm(DSD):
                agency_dsd = i['agencyId']
                dsd_id = i['id']
                dsd_name = i['names'][0]['value']
                version_dsd = str(i['version'])
                list_dsd.append({
                    'agency_dsd': agency_dsd,
                    'dsd_id': dsd_id,
                    'dsd_name': dsd_name,
                    'version_dsd': version_dsd,
                    'status': 1
                })

                DIM = i['dimensionList']['dimensions']
                MEA = i['measures']
                list_dsd_detail = []
                for d in DIM:
                    detail_type = "DIM"
                    detail_id = d['id']
                    try:
                        text_cl = d['representation']['representation']
                        agency_codelist = text_cl.split(":")[2].replace("org.sdmx.infomodel.codelist.Codelist=", "").strip()
                        codelist_id = text_cl.split(":")[-1].split("(")[0]
                        codelist_version = text_cl.split("(")[1].replace(")", "")
                    except:
                        agency_codelist = ""
                        codelist_id = ""
                        codelist_version = ""
                    text_cs = d['concept']
                    concept_representation_id = text_cs.split(".")[-1]
                    agency_concept = text_cs.split(":")[2].replace("org.sdmx.infomodel.conceptscheme.Concept=", "").strip()
                    concept_id = text_cs.split(":")[-1].split("(")[0]
                    concept_version = text_cs.split(":")[-1].split(")")[0].split("(")[1]
                    list_dsd_detail.append({
                        'agency_dsd': agency_dsd,
                        'dsd_id': dsd_id,
                        'detail_type': detail_type,
                        'detail_id': detail_id,
                        'agency_codelist': agency_codelist,
                        'codelist_id': codelist_id,
                        'codelist_version': codelist_version,
                        'agency_concept': agency_concept,
                        'concept_id': concept_id,
                        'concept_version': concept_version,
                        'concept_representation_id': concept_representation_id,
                        'status': 1
                    })
                for m in MEA:
                    detail_type = "MEA"
                    detail_id = m['id']
                    text_cs_mea = m['concept']
                    concept_representation_id = text_cs_mea.split(".")[-1]
                    agency_concept = text_cs_mea.split(":")[2].replace("org.sdmx.infomodel.conceptscheme.Concept=", "").strip()
                    concept_id = text_cs_mea.split(":")[-1].split("(")[0]
                    concept_version = text_cs_mea.split(":")[-1].split(")")[0].split("(")[1]
                    list_dsd_detail.append({
                    'agency_dsd': agency_dsd,
                    'dsd_id': dsd_id,
                    'detail_type': detail_type,
                    'detail_id': detail_id,
                    'agency_codelist': "",
                    'codelist_id': "",
                    'codelist_version': "",
                    'agency_concept': agency_concept,
                    'concept_id': concept_id,
                    'concept_version': concept_version,
                    'concept_representation_id': concept_representation_id,
                    'status': 1
                    })
                _datastructure_detail.ins_record(list_dsd_detail)

            _datastructure.truncate_table()
            _datastructure.ins_record(list_dsd)
