import requests
from db_csdl import _codelist_item_used
import os
from dotenv import load_dotenv

load_dotenv()

class FMR_Check:
    def codelist():
        url = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/codelist/all/all/all/?format=fusion-json&detail=allstubs&references=children"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            CL = data['Codelist']
            for i in CL:
                url = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/codelist/{i['agencyId']}/{i['id']}/{str(i['version'])}?format=fusion-json&detail=allstubs&references=parents&includeMetadata=true&includeAllAnnotations=true"
                res = requests.get(url)
                if res.status_code == 200:
                    data = res.json()
                    if ("ConceptScheme" not in data) and ("DataStructure" not in data):
                        result = f"{i['agencyId']} - {i['id']} - {i['version']}"
                        print (result)
                else:
                    result = res.text
                    return result
    def ConceptScheme():
        url = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/conceptscheme/all/all/all/?format=fusion-json&detail=allstubs&references=children"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            CS = data['ConceptScheme']
            for i in CS:
                url = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/conceptscheme/{i['agencyId']}/{i['id']}/{str(i['version'])}?format=fusion-json&detail=allstubs&references=parents&includeMetadata=true&includeAllAnnotations=true"
                res = requests.get(url)
                if res.status_code == 200:
                    data = res.json()
                    if "DataStructure" not in data:
                        result = f"{i['agencyId']} - {i['id']} - {i['version']}"
                        print (f"{result}")

    def DataStructure():
        url = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/datastructure/all/all/all/?format=fusion-json&detail=allstubs&references=children"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            DSD = data['DataStructure']
            for i in DSD:
                url = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/datastructure/{i['agencyId']}/{i['id']}/{str(i['version'])}?format=fusion-json&detail=allstubs&references=parents&includeMetadata=true&includeAllAnnotations=true"
                res = requests.get(url)
                if res.status_code == 200:
                    data = res.json()
                    if "Dataflow" not in data:
                        result = f"{i['agencyId']} - {i['id']} - {i['version']}"
                        print (f"{result}")
    
    def DataFlow():
        url = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/dataflow/all/all/all/?format=fusion-json&detail=allstubs&references=children"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            DF = data['Dataflow']
            for i in DF:
                url = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/dataflow/{i['agencyId']}/{i['id']}/{str(i['version'])}?format=fusion-json&detail=allstubs&references=parents&includeMetadata=true&includeAllAnnotations=true"
                res = requests.get(url)
                if res.status_code == 200:
                    data = res.json()
                    if "DataConstraint" not in data:
                        result = f"{i['agencyId']} - {i['id']} - {i['version']}"

                        print (f"{result}")
                        with open(f"DataFlow.txt", "a", encoding="utf-8") as f:
                            f.write(f"{i['agencyId']} - {i['id']} - {i['version']}\n")

    def Item_Codelist():
        url = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/dataconstraint/all/all/all/?format=fusion-json"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            RC = data['DataConstraint']
            for i in RC:
                if len(i['attachments']) > 1:
                    print(f"RC: {i['id']} được dán cho 2 DF trở lên")
                else:
                    print(f"----------------------\n{i['id']}\n")
                    text = i['attachments'][0].split(":")[-1]
                    DF = text.split("(")[0]
                    VER = text.split("(")[1].replace(")", "")
                    arr_cs = i['includeCube']
                    names = list(arr_cs.keys())

                    url = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/dataflow/all/{DF}/{VER}/?format=fusion-json&references=children"
                    res = requests.get(url)
                    if res.status_code == 200:
                        data = res.json()
                        DIM = data['DataStructure'][0]['dimensionList']['dimensions']
                        for d in DIM:
                            if d['id'] in names:
                                CS = d['id']
                                try:
                                    AGENCY = d['representation']['representation'].split(":")[2].replace("org.sdmx.infomodel.codelist.Codelist=", "").strip()
                                except:
                                    continue
                                text = d['representation']['representation'].split(":")[-1]
                                CL = text.split("(")[0]
                                VER_CL = text.split("(")[1].replace(")", "")
                                arr_item = arr_cs[CS]['values']
                                records = []
                                for i in arr_item:
                                    records.append({
                                        "cs_id": CS,
                                        "agency_id": AGENCY,
                                        "codelist_id": CL,
                                        "ver_codelist": VER_CL,
                                        "item_codelist_used": i,
                                        "status": 1
                                    })
                                    _codelist_item_used.ins_record(records)
                                    # print(f"{AGENCY} - {CS} - {CL} - {VER_CL} - {i}")
                # break    

class get_FMR:
    def DataFlow(agency):
        url = f"{os.getenv('FMR')}/fmr/sdmx/v2/structure/dataflow/{agency}/all/all/?format=fusion-json&detail=allstubs&references=children"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            DF = data['Dataflow']
            for i in DF:
                print(f"{i['id']} | {i['version']} # {i['names'][0]['value']}")
                

# X = get_FMR.DataFlow("B000.B006")
# print(X)

# Y = FMR_Check.DataFlow()
# print(Y)

X = FMR_Check.Item_Codelist()