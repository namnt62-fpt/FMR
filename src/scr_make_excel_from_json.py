import flet as ft
from mod_cdbc import cdbc

def Make_Excel(page: ft.Page):

    txt_report_id = ft.TextField(
        label="Nhập vào mã báo cáo của chế độ báo cáo: Ví dụ 10265", 
        width=500
    )
    result_text = ft.Text(value="")

    def make_excel(e):
        report_id = txt_report_id.value.strip()
        # Lấy token của hệ thống chế độ báo cao
        token = cdbc.get_token()
        # Lấy cấu trúc của báo cáo qua API
        report = cdbc.get_layout(token, report_id)
        # Đóng báo cáo thành excel
        result = cdbc.make_excel(report, report_id)
        result_text.value = f"{report_id} - {result}"
        page.update()

    # Nội dung chính
    content = ft.Column(
        [
            ft.Text(
                "Gọi API lấy cấu hình mẫu biểu từ hệ thống chế độ báo cáo và chuyển đổi thành file excel",
                size=20,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            txt_report_id,
            ft.ElevatedButton("Kết xuất Excel", on_click=make_excel),
            result_text,
        ],
        alignment=ft.MainAxisAlignment.START,          # nằm trên
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # giữa ngang
        expand=False,
    )

    # Căn giữa ngang toàn bộ, nhưng ở trên cùng
    return ft.Container(
        content,
        alignment=ft.alignment.top_center,   # 🔹 nằm trên cùng, giữa ngang
        expand=True,
        padding=20,
    )
