import flet as ft
import requests
import os
import glob
import sys
import json
import datetime
from dotenv import load_dotenv
from scr_reporting_constraints import Report_Constraints
from scr_convert_upload import Upload_DLM
from scr_convert_xml_to_json import CONVERT_JSON
from scr_codelist import Codelist
from scr_make_excel_from_json import Make_Excel
import pip_system_certs

def main(page: ft.Page):
    page.title = "FMR Tools"
    content = ft.Container(expand=True)

    # Khởi tạo view
    home = Report_Constraints(page)
    upload  = Upload_DLM(page)
    convert_json = CONVERT_JSON(page)
    codelist_src = Codelist(page)
    make_excel_src = Make_Excel(page)

    # Hàm cập nhật view khi đổi tab
    def update_view(index: int):
        if index == 0:
            content.content = upload
        elif index == 1:
            content.content = home
        elif index == 2:
            content.content = convert_json
        elif index == 3:
            content.content = codelist_src
        elif index == 4:
            content.content = make_excel_src
        page.update()

    # NavigationBar ở dưới cùng
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.UPLOAD_FILE, label="Upload to DLM"),
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Config RC"),
            ft.NavigationBarDestination(icon=ft.Icons.SYNC, label="Convert XML to JSON"),
            ft.NavigationBarDestination(icon=ft.Icons.LIST, label="Codelist"),
            ft.NavigationBarDestination(icon=ft.Icons.EXPAND_CIRCLE_DOWN_OUTLINED, label="Report Temp CĐBC"),
        ],
        on_change=lambda e: update_view(e.control.selected_index),
    )

    # add container chứa nội dung
    page.add(content)

    # Load Home mặc định
    update_view(0)

if __name__ == "__main__":
    ft.app(target=main)