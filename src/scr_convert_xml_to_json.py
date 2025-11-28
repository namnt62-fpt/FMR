import flet as ft
from tools import Tools
from mod_xml_to_json import XML_TO_JSON
import os

def CONVERT_JSON(page: ft.Page):

    curent_path = Tools.get_current_path()
    control_path = ft.TextField(value=f"{curent_path}", read_only=True, label="Chọn thư mục", width=400)

    # FilePicker để chọn thư mục
    def on_pick_result(e: ft.FilePickerResultEvent):
        control_path.value = e.path if e.path else ""
        control_path.update()

    control_browse = ft.FilePicker(on_result=on_pick_result)
    page.overlay.append(control_browse)

    # Nút chọn thư mục
    browse_button = ft.ElevatedButton(
        "📂 Chọn thư mục",
        on_click=lambda _: control_browse.get_directory_path(),
        width=150
    )

    # Progress bar
    progress_bar = ft.ProgressBar(width=control_path.width + browse_button.width, visible=False)

    # Khung log
    log_box = ft.TextField(
        multiline=True,
        min_lines=10,
        expand=True,
        read_only=True,
        label="Logs",
    )

    # Hàm log thay cho print
    def log(message: str):
        log_box.value += message + "\n"
        log_box.update()

    def on_submit(e):
        path = control_path.value.strip()
        print(path)

        file_xml = Tools.get_path_xml_in_dir(path)
        print(file_xml)

        if not file_xml:
            log("☠️ Không tìm thấy file XML nào trong thư mục.")
            return

        total_steps = len(file_xml) + len(Tools.get_path_xml_in_dir(path))
        current_step = 0

        progress_bar.value = 0
        progress_bar.visible = True
        page.update()

        # Convert từng file xml
        for item_file in file_xml:
            name_only = os.path.splitext(item_file)[0]
            try:
                XML_TO_JSON.convert_xml_to_json(item_file, name_only)
            except Exception as ex:
                log(f"☠️ Lỗi convert file {item_file}: {ex}")

            current_step += 1
            progress_bar.value = current_step / total_steps
            progress_bar.update()

        log("🎉 Hoàn thành 🎉")
        progress_bar.visible = False
        page.update()

    return ft.Column(
        [
            ft.Text(
                "Chuyển đổi từ XML sang JSON.\nSử dụng tool Convert để chuyển đổi Excel sang XML. Từ file XML sẽ hỗ trợ chuyển sang json.\nĐây chính là json body cho nội dung nhận dữ liệu vào kho",
                size=20,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Row([control_path, browse_button], alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([ft.ElevatedButton("Convert XML to JSON", on_click=on_submit, width=200)], alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([progress_bar], alignment=ft.MainAxisAlignment.CENTER),

            log_box
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )