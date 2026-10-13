@echo off
setlocal

py -3.11 -m pip install -r requirements.txt
if errorlevel 1 exit /b 1

py -3.11 -m PyInstaller --noconfirm --clean --onefile --windowed ^
  --name "Muthyara Smart Calculator" ^
  --collect-all customtkinter ^
  main.py
if errorlevel 1 exit /b 1

echo Built dist\Muthyara Smart Calculator.exe