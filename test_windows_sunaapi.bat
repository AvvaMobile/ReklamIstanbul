@echo off
echo ========================================
echo    Windows SUNAPI Kamera Testi
echo ========================================
echo.

REM Virtual environment aktifleştir
if exist venv (
    echo Virtual environment aktiflestiriliyor...
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment bulunamadi!
    echo Once install_windows.bat ile kurulum yapin.
    pause
    exit /b 1
)

echo.
echo SUNAPI kamera testleri basliyor...
echo.

REM Konfigürasyon testi
echo [1/4] Konfigurasyon testi...
python -c "from config import Config; print('SUNAPI Kamera Desteği:', Config.USE_SUNAPI_CAMERAS)" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Konfigurasyon basarili!
) else (
    echo ❌ Konfigurasyon hatasi!
)

REM Import testi
echo.
echo [2/4] Import testi...
python -c "from network_camera import SUNAPICamera, NetworkCamera; print('✅ SUNAPI modulleri basariyla import edildi')" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Import basarili!
) else (
    echo ❌ Import hatasi!
)

REM SUNAPI kamera oluşturma testi
echo.
echo [3/4] SUNAPI kamera olusturma testi...
python -c "
from network_camera import SUNAPICamera
camera = SUNAPICamera('192.168.1.121')
print('✅ SUNAPI kamera olusturuldu')
print(f'   IP: {camera.ip_address}')
print(f'   Port: {camera.port}')
" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Kamera olusturma basarili!
) else (
    echo ❌ Kamera olusturma hatasi!
)

REM URL format testi
echo.
echo [4/4] URL format testi...
python -c "
from network_camera import SUNAPICamera
camera = SUNAPICamera('192.168.1.121')
url = camera.get_rtsp_url('profile')
print('✅ URL format testi basarili')
print(f'   Profile URL: {url}')
" 2>nul
if %errorlevel% equ 0 (
    echo ✅ URL format testi basarili!
) else (
    echo ❌ URL format testi hatasi!
)

echo.
echo ========================================
echo    Test Tamamlandi!
echo ========================================
echo.
echo Sonraki adimlar:
echo 1. Gercek kamera IP adresini config.py'de guncelleyin
echo 2. test_sunaapi_camera.py ile gercek baglantiyi test edin
echo 3. main.py ile ana sistemi calistirin
echo.
echo Detayli test icin: python test_sunaapi_camera.py
echo.

pause
