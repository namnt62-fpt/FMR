pyinstaller --onefile --noconsole --icon=src/assets/icon.ico --name=FMR_Tools --add-data "src/.env;src" src/main.py


pyinstaller --onefile --noconsole --icon=src/assets/icon.ico --name=FMR_Tools --add-data "cert.pem;." --add-data "src/.env;src" src/main.py