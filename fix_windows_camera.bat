@echo off
echo ========================================
echo    Windows Kamera Sorunu Çözümü
echo ========================================
echo.

echo Bu script Windows'ta kamera görünmeme
echo sorununu çözmek için tasarlanmistir.
echo.

REM Python kontrolü
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python bulunamadi!
    pause
    exit /b 1
)

echo [1/6] Mevcut OpenCV kaldiriliyor...
pip uninstall opencv-python opencv-python-headless -y
echo Eski OpenCV kaldirildi.

echo.
echo [2/6] Windows için OpenCV kuruluyor...
pip install opencv-python
if %errorlevel% neq 0 (
    echo OpenCV alternatif yontem deneniyor...
    pip install opencv-python-headless
)

echo.
echo [3/6] Kamera test paketleri kuruluyor...
pip install opencv-contrib-python
pip install mediapipe

echo.
echo [4/6] Kamera test script'i olusturuluyor...

REM Windows için kamera test script'i oluştur
echo import cv2 > test_camera_windows.py
echo import sys >> test_camera_windows.py
echo. >> test_camera_windows.py
echo def test_cameras(): >> test_camera_windows.py
echo     print("Windows Kamera Testi") >> test_camera_windows.py
echo     print("=" * 30) >> test_camera_windows.py
echo     for i in range(10): >> test_camera_windows.py
echo         cap = cv2.VideoCapture(i) >> test_camera_windows.py
echo         if cap.isOpened(): >> test_camera_windows.py
echo             ret, frame = cap.read() >> test_camera_windows.py
echo             if ret: >> test_camera_windows.py
echo                 print(f"✅ Kamera {i}: Çalışıyor") >> test_camera_windows.py
echo                 print(f"   - Çözünürlük: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}") >> test_camera_windows.py
echo                 print(f"   - FPS: {cap.get(cv2.CAP_PROP_FPS):.1f}") >> test_camera_windows.py
echo             else: >> test_camera_windows.py
echo                 print(f"❌ Kamera {i}: Frame okunamıyor") >> test_camera_windows.py
echo             cap.release() >> test_camera_windows.py
echo         else: >> test_camera_windows.py
echo             print(f"❌ Kamera {i}: Açılamıyor") >> test_camera_windows.py
echo. >> test_camera_windows.py
echo if __name__ == "__main__": >> test_camera_windows.py
echo     test_cameras() >> test_camera_windows.py

echo.
echo [5/6] Kamera test ediliyor...
python test_camera_windows.py

echo.
echo [6/6] Sonuçlar...
echo.
echo Eğer kameralar hala görünmüyorsa:
echo.
echo 1. Windows Ayarlar ^> Gizlilik ve Güvenlik ^> Kamera
echo    - "Kamera erişimine izin ver" açık olsun
echo    - "Uygulamaların kameraya erişmesine izin ver" açık olsun
echo.
echo 2. Aygıt Yöneticisi ^> Kameralar
echo    - Kamera sürücülerini güncelle
echo.
echo 3. Bilgisayarı yeniden başlat
echo.
echo 4. Test script'ini tekrar çalıştır:
echo    python test_camera_windows.py
echo.

pause
