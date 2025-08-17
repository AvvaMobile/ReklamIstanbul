@echo off
echo ========================================
echo    AvvaImageAI - Windows Kurulum
echo ========================================
echo.

REM Python versiyon kontrolü
echo [1/6] Python versiyon kontrolu...
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
echo [2/6] Virtual environment olusturuluyor...
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
echo [3/6] Virtual environment aktiflestiriliyor...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Virtual environment aktiflestirilemedi!
    pause
    exit /b 1
)
echo Virtual environment aktiflestirildi.

REM Pip güncelleme ve cache temizleme
echo.
echo [4/6] Pip guncelleniyor ve cache temizleniyor...
pip install --upgrade pip
pip cache purge
echo Pip guncellendi ve cache temizlendi.

REM Wheel ve temel paketler
echo.
echo [5/6] Temel paketler kuruluyor...
pip install wheel
pip install setuptools --upgrade

REM Alternatif kurulum yöntemi - zip error'ları önlemek için
echo.
echo [6/6] Ana paketler kuruluyor (zip error onleme ile)...

REM OpenCV - alternatif yöntem
echo OpenCV kuruluyor...
pip install opencv-python-headless
if %errorlevel% neq 0 (
    echo OpenCV alternatif yontem deneniyor...
    pip install opencv-python
)

REM Torch - CPU versiyonu (daha az sorun)
echo Torch kuruluyor...
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

REM Diğer paketler
echo Diger paketler kuruluyor...
pip install ultralytics
pip install numpy
pip install requests
pip install schedule
pip install python-dotenv
pip install flask
pip install Pillow
pip install psutil

if %errorlevel% neq 0 (
    echo.
    echo WARNING: Bazı paketler kurulamadi!
    echo Manuel kurulum gerekebilir.
    echo.
    echo Alternatif çözümler:
    echo 1. pip install --upgrade pip
    echo 2. pip cache purge
    echo 3. Her paketi tek tek kur
    echo.
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

