@echo off
echo ========================================
echo    Windows Zip Error Çözümü
echo ========================================
echo.

echo Bu script Windows'ta pip kurulum sırasında oluşan
echo zip error'larını çözmek için tasarlanmistir.
echo.

REM Python kontrolü
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python bulunamadi!
    pause
    exit /b 1
)

echo [1/5] Pip cache temizleniyor...
pip cache purge
echo Cache temizlendi.

echo.
echo [2/5] Pip guncelleniyor...
python -m pip install --upgrade pip
echo Pip guncellendi.

echo.
echo [3/5] Wheel ve setuptools guncelleniyor...
pip install --upgrade wheel setuptools
echo Temel paketler guncellendi.

echo.
echo [4/5] Alternatif paket kurulumu deneniyor...

REM OpenCV alternatifleri
echo OpenCV kuruluyor...
pip install opencv-python-headless
if %errorlevel% neq 0 (
    echo OpenCV alternatif yontem deneniyor...
    pip install opencv-python
    if %errorlevel% neq 0 (
        echo OpenCV kurulamadi! Manuel kurulum gerekebilir.
    )
)

REM Torch alternatifleri
echo Torch kuruluyor...
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
if %errorlevel% neq 0 (
    echo Torch alternatif yontem deneniyor...
    pip install torch
    pip install torchvision
)

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

echo.
echo [5/5] Kurulum test ediliyor...
python -c "import cv2, ultralytics, torch; print('Temel moduller yuklendi!')"
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Bazı modüller yüklenemedi!
    echo.
    echo Manuel çözümler:
    echo 1. pip install --upgrade pip
    echo 2. pip cache purge
    echo 3. Her paketi tek tek kur
    echo 4. Visual C++ Redistributable kur
    echo 5. Python'u yeniden kur
    echo.
) else (
    echo.
    echo ========================================
    echo    Zip Error Çözüldü!
    echo ========================================
    echo.
    echo Artık requirements.txt'yi kurabilirsiniz:
    echo pip install -r requirements.txt
    echo.
)

echo.
echo Script tamamlandi!
pause
