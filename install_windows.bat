@echo off
echo ========================================
echo    AvvaImageAI - Windows Kurulum
echo ========================================
echo.

REM Python versiyon kontrolü
echo [1/5] Python versiyon kontrolu...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python bulunamadi!
    echo Python 3.9+ kurulumu gerekli: https://www.python.org/downloads/
    echo Kurulum sirasinda "Add Python to PATH" secenegini isaretleyin.
    pause
    exit /b 1
)
echo Python bulundu: 
python --version

REM Virtual environment oluştur
echo.
echo [2/5] Virtual environment olusturuluyor...
if exist venv (
    echo Virtual environment zaten mevcut.
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Virtual environment olusturulamadi!
        pause
        exit /b 1
    )
    echo Virtual environment olusturuldu.
)

REM Virtual environment aktifleştir
echo.
echo [3/5] Virtual environment aktiflestiriliyor...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Virtual environment aktiflestirilemedi!
    pause
    exit /b 1
)
echo Virtual environment aktiflestirildi.

REM Dependencies kur
echo.
echo [4/5] Dependencies kuruluyor...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Dependencies kurulamadi!
    echo Internet baglantinizi kontrol edin.
    pause
    exit /b 1
)
echo Dependencies kuruldu.

REM Sistem testi
echo.
echo [5/5] Sistem testi yapiliyor...
python quick_start.py
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Sistem testinde sorunlar var!
    echo Log dosyalarini kontrol edin.
) else (
    echo.
    echo ========================================
    echo    Kurulum basarili!
    echo ========================================
    echo.
    echo Kullanim:
    echo - Kamera modu: python main.py
    echo - Web arayuzu: python app.py
    echo - Test: python quick_start.py
    echo.
)

pause
