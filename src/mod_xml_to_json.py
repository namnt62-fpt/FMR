import xml.etree.ElementTree as ET
import json
from pathlib import Path

class XML_TO_JSON:
    def convert_xml_to_json(file_path, name_only):

        def local_name(elem):
            # chuyển '{ns}Tag' -> 'Tag'
            tag = elem.tag
            return tag.split('}', 1)[1] if '}' in tag else tag

        # Parse XML
        tree = ET.parse(file_path)
        root = tree.getroot()

        data_list = []

        # Tìm tất cả element có tên local 'Series'
        for series in root.iter():
            if local_name(series) != "Series":
                continue

            item = {}
            obs_list = []

            # Các con trực tiếp của <generic:Series> thường là <generic:SeriesKey> và nhiều <generic:Obs>
            for child in series:
                ln = local_name(child)

                if ln == "SeriesKey":
                    # trong SeriesKey có nhiều <generic:Value id="..." value="..."/>
                    for val in child:
                        if local_name(val) == "Value":
                            key = val.attrib.get("id")
                            valv = val.attrib.get("value")
                            if key is not None:
                                item[key] = valv

                elif ln == "Obs":
                    obs_item = {}
                    for sub in child:
                        sub_ln = local_name(sub)
                        if sub_ln == "ObsDimension":
                            obs_item["TIME_PERIOD"] = sub.attrib.get("value")
                        elif sub_ln == "ObsValue":
                            obs_item["OBS_VALUE"] = sub.attrib.get("value")
                    if obs_item:
                        obs_list.append(obs_item)

            if obs_list:
                item["OBS"] = obs_list

            # Nếu Series rỗng (hiếm), vẫn thêm để giữ cấu trúc; nếu không muốn, kiểm tra item != {}
            data_list.append(item)

        # Build final object
        final = {
            "header": {
                "org_code": "org_code",
                "report_code": "report_code",
                "submitted_time": "submitted_time",
                "system_code": "HT01",
                "request_id": "request_id"
            },
            "data": data_list
        }

        # Ghi file đẹp
        with open(f"{name_only}.json", "w", encoding="utf-8") as f:
            json.dump(final, f, ensure_ascii=False, indent=4)
