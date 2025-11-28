import flet as ft
import json
import os
import datetime
from api import FMR_API
from mod_reporting_constraints import RC

def Report_Constraints(page: ft.Page):
    file_name = ""
    include_cube_data = {}
    item_controls = []
    selected_df = {}

    status_text = ft.Text(value="", color=ft.Colors.GREEN, size=12)

    def load_dropdown_df():
        """
        Hàm load giá trị vào dropdown list chọn danh sách DF chưa có RC
        """
        data_json = RC.get_df_non_RC()
        arr = data_json
        dropdown.options = [
            ft.dropdown.Option(f"{item['df_id']} - {item['df_name']}") for item in arr
        ]
        dropdown.data = arr
        page.update()

    def on_dropdown_change(e):
        """
        Hàm bắt sự kiện khi NSD chọn dropdown list
        """
        selected = dropdown.value
        if not selected:
            return
        df_id = selected.split(" - ")[0]

        for item in dropdown.data:
            if item["df_id"] == df_id:
                selected_df.update(item)
                agency_df = item['agency_df']
                df_name = item['df_name']
                df_id = item['df_id']
                df_version = item['df_version']

                arr_DIM = RC.get_dim_from_df(agency_df, df_id, df_version)
                json_rc = RC.make_json_rc(agency_df, df_id, df_version, df_name, arr_DIM)
                json_preview.value = json.dumps(json_rc, indent=4, ensure_ascii=False)

                include_cube_data = {}
                if "DataConstraint" in json_rc and len(json_rc["DataConstraint"]) > 0:
                    include_cube_data = json_rc["DataConstraint"][0].get("includeCube", {})

                item_controls.clear()
                editor_column.controls.clear()
                for item, data in include_cube_data.items():
                    add_item_row(item, data.get("values", []))
                page.update()
                break

    def parse_values(text):
        items = list(dict.fromkeys(filter(None, text.replace("\t", " ").split())))
        return ", ".join(items)

    def remove_duplicates(e, item_textfield, values_textfield):
        """
        Loại bỏ trung lặp các mã trong giá trị phân tổ
        """
        cleaned = parse_values(values_textfield.value)
        values_textfield.value = cleaned
        page.update()

    def add_item_row(item=None, values=None):
        """
        Thêm một dòng phân tổ mới
        """
        item_tf = ft.TextField(
            value=item or "",
            label="Phân Tổ",
            expand=1,
            multiline=True,
            min_lines=1,
            max_lines=3
        )

        values_tf = ft.TextField(
            value=",".join(values) if values else "",
            label="Giá trị phân tổ",
            expand=3,
            multiline=True,
            min_lines=1,
            max_lines=4
        )

        remove_dups_icon = ft.IconButton(
            icon=ft.Icons.AUTO_FIX_HIGH,
            tooltip="Loại bỏ trùng lặp",
            on_click=lambda e: remove_duplicates(e, item_tf, values_tf)
        )

        delete_btn = ft.IconButton(
            icon=ft.Icons.DELETE,
            tooltip="Xóa",
            on_click=lambda e: remove_row(row)
        )

        row = ft.Row([
            item_tf,
            values_tf,
            remove_dups_icon,
            delete_btn
        ], alignment=ft.MainAxisAlignment.START)

        item_controls.append(row)
        editor_column.controls.append(row)
        page.update()

    def remove_row(row):
        if row in item_controls:
            item_controls.remove(row)
        if row in editor_column.controls:
            editor_column.controls.remove(row)
        page.update()
    
    def make_json():
        """
        Hàm này xử lý để tạo ra json rc cuối cùng để chuẩn bị lưu trữ hoặc upload lên FMR.
        Json được tạo ra bằng cách đọc json từ json preview và thay thế nội dung includeCube bằng nội dung mới được NSD định nghĩa trên giao diện
        """
        new_include_cube = {}
        for row in item_controls:
            item = row.controls[0].value.strip()
            values = [v.strip() for v in row.controls[1].value.split(",") if v.strip()]
            if item:
                new_include_cube[item] = {
                    "removePrefix": False,
                    "values": values,
                    "cascade": []
                }
        json_data = json.loads(json_preview.value)
        json_data["DataConstraint"][0]["includeCube"] = new_include_cube
        return json.dumps(json_data, ensure_ascii=False, indent=4)

    def preview_button_click(e):
        json_rc_final = make_json()
        json_preview.value = json_rc_final
        page.update()

    def upload_to_fmr(json_rc_final):
        result = FMR_API.load_structures(json_rc_final)
        status_text.value = f"🖕 {result} 🖕"
        page.update()

    def save_json(e):
        json_rc_final = make_json()
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"RC_SAVE_{now}.json"

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(json_rc_final)

        json_preview.value = json_rc_final
        page.update()

    def pick_file_result(e: ft.FilePickerResultEvent):
        """
        Xử lý sự kiện chọn file json RC.
        Cập nhật vào Preview Json và Include Cube
        """
        nonlocal file_name, include_cube_data
        if e.files:
            status_text.value = ""
            file_name = e.files[0].path
            with open(file_name, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

            json_preview.value = json.dumps(json_data, indent=4, ensure_ascii=False)

            include_cube_data = {}
            if "DataConstraint" in json_data and len(json_data["DataConstraint"]) > 0:
                include_cube_data = json_data["DataConstraint"][0].get("includeCube", {})

            item_controls.clear()
            editor_column.controls.clear()
            for item, data in include_cube_data.items():
                add_item_row(item, data.get("values", []))
            page.update()

    pick_file_dialog = ft.FilePicker(on_result=pick_file_result)
    page.overlay.append(pick_file_dialog)

    json_preview = ft.TextField(
        label="Json Preview",
        multiline=True,
        min_lines=30,
        expand=True,
        read_only=True,
        text_style=ft.TextStyle(font_family="Courier New")
    )

    editor_column = ft.Column(controls=[], scroll=ft.ScrollMode.AUTO, expand=True)
    dropdown =  ft.Dropdown(
        label="Danh sách DF",
        hint_text="Chọn giá trị",
        options=[],
        on_change=on_dropdown_change,
        width=400
        )
    # Gọi hàm load sau khi đã tạo dropdown nhưng trước return
    load_dropdown_df()

    left = ft.Container(
        content=ft.Column([
            ft.ElevatedButton("📂 Chọn file JSON", on_click=lambda _: pick_file_dialog.pick_files()),
            dropdown,
            json_preview
        ], expand=True),
        expand=2,
        alignment=ft.alignment.top_left
    )

    right = ft.Container(
        content=ft.Column([
            ft.Text("Danh sách các phân tổ cần khai báo RC.", size=20, weight=ft.FontWeight.BOLD),
            editor_column,
            ft.Row([
                ft.IconButton(ft.Icons.ADD, tooltip="Thêm", on_click=lambda _: add_item_row()),
                ft.IconButton(ft.Icons.SAVE, tooltip="Lưu", on_click=save_json),
                ft.IconButton(ft.Icons.REMOVE_RED_EYE, tooltip="Xem trước JSON", on_click=preview_button_click),
                ft.IconButton(ft.Icons.UPLOAD, tooltip="Đẩy dữ liệu lên FMR", on_click=lambda _: upload_to_fmr(make_json())),
            ], alignment=ft.MainAxisAlignment.CENTER),
            status_text
        ], expand=True),
        expand=3,
        alignment=ft.alignment.top_left,
        border=ft.border.all(1, ft.Colors.GREY),
        padding=10
    )

    return ft.Row([left, right], expand=True, vertical_alignment=ft.CrossAxisAlignment.START)
