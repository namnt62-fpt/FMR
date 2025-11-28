import flet as ft
from tools import Tools
from mod_xml_to_json import XML_TO_JSON
import os
import json
from datetime import datetime

def Codelist(page: ft.Page):

    codelist_id = ft.TextField(label = "Mã Codelist", width=200)
    codelist_name = ft.TextField(label = "Tên Codelist", width=400)
    codelist_version = ft.TextField(label = "Phiên bản", width=100)
    agency_id = ft.Dropdown(
        label="Chọn loại dữ liệu",
        options=[
            ft.dropdown.Option("B000", "B000 - Cục Thống kê"),
            ft.dropdown.Option("B000.B002", "B000.B002 - Ban Hệ thống Tài khoản quốc gia"),
            ft.dropdown.Option("B000.B003", "B000.B003 - Ban chính sách, Chiến lược và Dữ liệu thống kê"),
            ft.dropdown.Option("B000.B005", "B000.B005 - Ban Thống kê Công nghiệp và Xây dựng"),
            ft.dropdown.Option("B000.B006", "B000.B006 - Ban Thống kê Nông, Lâm nghiệp và Thủy sản"),
            ft.dropdown.Option("B000.B008", "B000.B008 - Ban Thống kê Dân số và Lao động"),
            ft.dropdown.Option("B000.B009", "B000.B009 - Ban Thống kê Xã hội và Môi trường"),
            ft.dropdown.Option("B000.B010", "B000.B010 - Ban Thống kê Tổng hợp và Đối ngoại"),
            ft.dropdown.Option("B000.B016", "B000.B016 - Ban Thống kê Dịch vụ và Giá"),
        ],
        width = 700,
        value="B000"
    )
    result_text = ft.Text(value="")
    result_json= ft.Text(value="")

    txt_code = ft.TextField(
        label="Input Code", multiline=True, min_lines=10, max_lines=20, expand=True
    )

    txt_name = ft.TextField(
        label="Input Name", multiline=True, min_lines=10, max_lines=20, expand=True
    )

    txt_parent = ft.TextField(
        label="Input Parent", multiline=True, min_lines=10, max_lines=20, expand=True
    )

    def make_json(e):

        code_list = [line.strip() for line in txt_code.value.splitlines() if line.strip()]
        name_list = [line.strip() for line in txt_name.value.splitlines() if line.strip()]
        parent_list = [line.strip() for line in txt_parent.value.splitlines()]


        if len(code_list) != len(name_list):
            result_text.value = "❌ Số dòng của Code và Name không khớp!"
            page.update()
            return

        # Dữ liệu meta
        meta = {
            "id": "IREF142691",
            "test": False,
            "prepared": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "contentLanguages": ["vi"],
            "sender": {"id": "FusionRegistry"}
        }

        # Danh sách items
        items = []
        for i, (code, name) in enumerate(zip(code_list, name_list)):
            parent = parent_list[i] if i < len(parent_list) else None
            items.append({
                "id": code,
                "urn": f"urn:sdmx:org.sdmx.infomodel.codelist.Code={agency_id.value}:{codelist_id.value}({codelist_version.value}).{code}",
                "names": [{"locale": "vi", "value": name}],
                "parentCode": parent if parent else None
            })

        # Xóa key "parent" nếu None
        for i in items:
            if i["parentCode"] is None:
                del i["parentCode"]

        # Dữ liệu chính
        codelist_data = {
            "id": codelist_id.value,
            "urn": f"urn:sdmx:org.sdmx.infomodel.codelist.Codelist={agency_id.value}:{codelist_id.value}({codelist_version.value})",
            "names": [{"locale": "vi", "value": codelist_name.value}],
            "agencyId": agency_id.value,
            "version": codelist_version.value,
            "isFinal": False,
            "isPartial": False,
            "validityType": "standard",
            "items": items
        }

        # Gộp thành JSON cuối cùng
        data = {
            "meta": meta,
            "Codelist": [codelist_data]
        }

        # Hiển thị JSON đẹp trong Text widget
        result_json.value = json.dumps(data, ensure_ascii=False, indent=4)

        # (Tuỳ chọn) Lưu ra file nếu muốn
        out_path = os.path.join(os.getcwd(), f"{codelist_id.value}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        result_text.value += f"\n\n✅ Đã lưu file: {out_path}"
        page.update()

    return ft.Column(
        [
            ft.Text(
                "Codelist Information",
                size=20,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            agency_id,
            ft.Row([codelist_id, codelist_name, codelist_version], alignment=ft.MainAxisAlignment.CENTER),
            result_text,
            ft.Row(
                controls=[
                    ft.Container(content=txt_code, height=300, expand=200),
                    ft.Container(content=txt_name, height=300, expand=200),
                    ft.Container(content=txt_parent, height=300, expand=200),
                ],
                expand=True,
            ),
            ft.Row(
                controls=[
                    ft.ElevatedButton("Tạo Json", on_click=make_json),
                    ft.ElevatedButton("Đẩy lên FMR", on_click=None),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            result_json,
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )