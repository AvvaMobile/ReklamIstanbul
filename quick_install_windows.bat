@echo off
echo ========================================
echo    AvvaImageAI - Hizli Windows Kurulum
echo    SUNAPI Kamera Desteği
echo ========================================
echo.

echo Hizli kurulum basliyor...
echo.

REM Python kontrolü
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python bulunamadi!
    echo Python 3.9+ kurulumu gerekli.
    pause
    exit /b 1
)

REM Virtual environment
if not exist venv (
    echo Virtual environment olusturuluyor...
    python -m venv venv
)

REM Aktifleştir
call venv\Scripts\activate.bat

REM Pip güncelle
echo Pip guncelleniyor...
pip install --upgrade pip

REM Requirements kur
echo Paketler kuruluyor...
pip install -r requirements_windows.txt

REM .env oluştur
if not exist .env (
    copy env_example.txt .env >nul
    echo .env dosyasi olusturuldu.
)

echo.
echo ========================================
echo    Hizli Kurulum Tamamlandi!
echo ========================================
echo.
echo Kullanim:
echo - test_sunaapi_camera.py ile test edin
echo - main.py ile ana sistemi calistirin
echo.
echo Detayli kurulum icin: install_windows.bat
echo.

pause
