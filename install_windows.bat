@echo off
echo ========================================
echo    AvvaImageAI - Windows Kurulum
echo    SUNAPI Kamera Desteği Dahil
echo ========================================
echo.

REM Python versiyon kontrolü
echo [1/7] Python versiyon kontrolu...
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
echo [2/7] Virtual environment olusturuluyor...
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
echo [3/7] Virtual environment aktiflestiriliyor...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Virtual environment aktiflestirilemedi!
    pause
    exit /b 1
)
echo Virtual environment aktiflestirildi.

REM Pip güncelleme ve cache temizleme
echo.
echo [4/7] Pip guncelleniyor ve cache temizleniyor...
pip install --upgrade pip
pip cache purge
echo Pip guncellendi ve cache temizlendi.

REM Wheel ve temel paketler
echo.
echo [5/7] Temel paketler kuruluyor...
pip install wheel
pip install setuptools --upgrade

REM Ana paketler kurulumu
echo.
echo [6/7] Ana paketler kuruluyor (zip error onleme ile)...

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

REM Temel paketler
echo Temel paketler kuruluyor...
pip install ultralytics
pip install numpy
pip install requests
pip install schedule
pip install python-dotenv
pip install flask
pip install Pillow
pip install psutil

REM SUNAPI Kamera Desteği için ek paketler
echo.
echo SUNAPI kamera desteği paketleri kuruluyor...
pip install urllib3
pip install certifi
pip install chardet
pip install idna

REM Network kamera ve streaming paketleri
echo Network kamera paketleri kuruluyor...
pip install av
pip install pysrt
pip install websockets

REM Test ve geliştirme paketleri
echo Test ve geliştirme paketleri kuruluyor...
pip install pytest
pip install pytest-cov
pip install black
pip install flake8

REM Kurulum kontrolü
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
    echo SUNAPI Kamera Desteği Kuruldu!
    echo.
    echo Kullanim:
    echo - Ana sistem: python main.py
    echo - Web arayuzu: python app.py
    echo - Hizli test: python quick_start.py
    echo - SUNAPI test: python test_sunaapi_camera.py
    echo - Entegrasyon test: python test_sunaapi_integration.py
    echo - Demo: python demo_sunaapi_camera.py
    echo.
    echo SUNAPI Kamera Konfigurasyonu:
    echo 1. config.py dosyasinda kamera IP adresini guncelleyin
    echo 2. .env dosyasinda kamera bilgilerini ayarlayin
    echo 3. test_sunaapi_camera.py ile baglantiyi test edin
    echo.
)

REM Kurulum sonrası konfigürasyon
echo.
echo [7/7] Konfigurasyon dosyalari olusturuluyor...

REM .env dosyası oluştur (eğer yoksa)
if not exist .env (
    echo .env dosyasi olusturuluyor...
    copy env_example.txt .env >nul
    echo .env dosyasi olusturuldu.
) else (
    echo .env dosyasi zaten mevcut.
)

REM Konfigürasyon testi
echo.
echo Konfigurasyon testi yapiliyor...
python -c "from config import Config; print('SUNAPI Kamera Desteği:', Config.USE_SUNAPI_CAMERAS)" 2>nul
if %errorlevel% equ 0 (
    echo SUNAPI konfigurasyonu basarili!
) else (
    echo SUNAPI konfigurasyonu test edilemedi.
)

echo.
echo ========================================
echo    Kurulum ve Konfigurasyon Tamamlandi!
echo ========================================
echo.
echo Sonraki adimlar:
echo 1. .env dosyasinda kamera bilgilerini guncelleyin
echo 2. test_sunaapi_camera.py ile baglantiyi test edin
echo 3. main.py ile ana sistemi calistirin
echo.
echo Detayli bilgi icin: SUNAPI_CAMERA_README.md
echo.
echo SUNAPI Kamera Desteği Kurulumu Tamamlandi!
echo Artik SUNAPI dokümantasyonuna göre kamera erisimi saglayabilirsiniz.
echo.

pause
