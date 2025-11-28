import flet as ft
from tools import Tools
from mod_upload_dlm import UPLOAD
import os
import time
import re

def Upload_DLM(page: ft.Page):

    curent_path = Tools.get_current_path()
    control_path = ft.TextField(value=f"{curent_path}", read_only=True, label="Chọn thư mục", width=400)

    # FilePicker để chọn thư mục
    # def on_pick_result(e: ft.FilePickerResultEvent):
    #     control_path.value = e.path if e.path else ""
    #     control_path.update()

    # control_browse = ft.FilePicker(on_result=on_pick_result)
    # page.overlay.append(control_browse)
    # page.update()

    # # Nút chọn thư mục
    # browse_button = ft.ElevatedButton(
    #     "📂 Chọn thư mục",
    #     on_click=lambda _: control_browse.get_directory_path(),
    #     width=150
    # )

    def on_pick_result(e: ft.FilePickerResultEvent):
        if e.path:
            control_path.value = os.path.abspath(e.path)
        else:
            control_path.value = ""
        control_path.update()
        print(f"🧭 Folder đã chọn: {e.path}")

    control_browse = ft.FilePicker(on_result=on_pick_result)
    page.overlay.append(control_browse)
    page.update()  # 🔥 BẮT BUỘC PHẢI CÓ

    browse_button = ft.ElevatedButton(
        "📂 Chọn thư mục",
        on_click=lambda _: control_browse.get_directory_path(),
        width=150
    )

    # Dropdown chọn dataspace (chiều rộng = TextField + Button)
    dataspace_dropdown = ft.Dropdown(
        label="Chọn loại dữ liệu",
        options=[
            ft.dropdown.Option("tctk-disseminate", "KHO - Chính thức"),
            ft.dropdown.Option("tctk-design", "KHO - Sơ bộ"),
            ft.dropdown.Option("tctk-ng-disseminate", "Niên giám - Chính thức"),
            ft.dropdown.Option("tctk-ng-design", "Niên giám - Sơ bộ"),
        ],
        width=control_path.width + browse_button.width,
        value="tctk-disseminate"
    )

    # Switch căn giữa
    upload_df = ft.Switch(
        adaptive=True,
        label="Upload cả Dataflow",
        value=False,
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
        data_space = dataspace_dropdown.value
        is_upload_df = upload_df.value

        file_excel = Tools.get_excel_in_dir(path)

        if not file_excel:
            log("☠️ Không tìm thấy file Excel nào trong thư mục.")
            return

        total_steps = len(file_excel) + (1 if is_upload_df else 0) + len(Tools.get_path_xml_in_dir(path))
        current_step = 0

        progress_bar.value = 0
        progress_bar.visible = True
        page.update()

        file_error = []

        # Convert từng file excel
        for item_file in file_excel:
            log(f"💕 ....................................................... 💕")
            name_only = os.path.splitext(item_file)[0]
            X = name_only.split("-")
            agency_id = X[0]
            version = X[1]
            dataflow_id = X[2]
            log(f"💕 Đang convert file {name_only} ...")
            try:
                status_code, content = UPLOAD.convert_data(
                    path=item_file,
                    agency=f"B000.{agency_id}",
                    version=f"{version}.0",
                    df=dataflow_id
                )
                if status_code != 200:
                    log(f"☠️ Lỗi {status_code} convert file {item_file}\n{content}")
                # log(f"✅ Convert thành công {item_file} (Status {status_code})")
            except Exception as ex:
                file_error.append(item_file)
                log(f"☠️ Lỗi convert file {item_file}: {ex}")

            current_step += 1
            progress_bar.value = current_step / total_steps
            progress_bar.update()

            # Upload Dataflow nếu có chọn
            if is_upload_df:
                try:
                    log(f"💕 Đang tải Dataflow từ FMR ...")
                    status_code,xml = UPLOAD.get_df()
                    if status_code != 200:
                        log(f"☠️ Lỗi {status_code} tải Dataflow từ FMR\n{xml}")
                        return
                except Exception as ex:
                    log(f"☠️ Lỗi kết nối đến FMR ☠️\n{ex}")
                    return

                
                try:
                    log(f"⏳ Đang upload Dataflow từ DLM...")
                    status_code, content = UPLOAD.upload_df(content_xml=xml, data_space=data_space)
                    if status_code not in [200, 207]:
                        log(f"☠️ Lỗi {status_code} upload Dataflow\n{content}")
                except Exception as ex:
                    log(f"☠️ Lỗi kết nối đến DLM ☠️\n{ex}")

                current_step += 1
                progress_bar.value = current_step / total_steps
                progress_bar.update()

            # Upload XML
            path_file_xml = Tools.get_path_xml_in_dir(path)
            for item_file_xml in path_file_xml:
                log(f"💕 Đang upload file {os.path.basename(item_file_xml)} lên DLM...")
                try:
                    status, content = UPLOAD.upload_dlm(path_file_xml=item_file_xml, data_space=data_space)
                    match = re.search(r'\bID\s+(\d+)\b', content)
                    if match:
                        ID_Status = int(match.group(1))
                        time.sleep(10)
                        max_attempts = 8         
                        for attempt in range(1, max_attempts + 1):
                            X = UPLOAD.check_status_dlm(ID_Status, data_space)
                            if X == "Success":
                                log(f"💕 Outcome của ID: {ID_Status}: {X}")
                                break
                            else:
                                if attempt < max_attempts:
                                    log(f"☠️ Thử lần thứ {attempt} -> Outcome của {ID_Status}: {X}")
                                    time.sleep(60)
                                else:
                                    log(f"☠️ Thử 6 lần nhưng Status của ID: {ID_Status} vẫn không phải là Success")
                    if status != 200:
                        log(f"☠️ Lỗi {status} Upload file {os.path.basename(item_file_xml)} lên DLM thất bại:\n{content}")
                except Exception as ex:
                    log(f"☠️ Lỗi kết nối đến DLM ☠️\n{ex}")

                os.remove(item_file_xml)
                # os.remove(item_file)

                log(f"💕 ....................................................... 💕")
                current_step += 1
                progress_bar.value = current_step / total_steps
                progress_bar.update()

        log(f"🎉 Hoàn thành 🎉\n\n")
        log("☠️☠️☠️☠️☠️☠️ Danh sách file lỗi convert ☠️☠️☠️☠️☠️☠️")
        for i in file_error:
            log(f"{i}")
        log("☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️")
        progress_bar.visible = False
        page.update()

    return ft.Column(
        [
            ft.Text(
                "Upload dataflow từ FMR sang DLM",
                size=20,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Row([control_path, browse_button], alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([dataspace_dropdown], alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([upload_df], alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([ft.ElevatedButton("Convert & Upload", on_click=on_submit, width=200)], alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([progress_bar], alignment=ft.MainAxisAlignment.CENTER),

            log_box
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
