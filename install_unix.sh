#!/bin/bash

echo "========================================"
echo "    AvvaImageAI - Unix Kurulum"
echo "========================================"
echo

# Python versiyon kontrolü
echo "[1/5] Python versiyon kontrolu..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 bulunamadi!"
    echo "Python 3.9+ kurulumu gerekli."
    echo
    echo "Ubuntu/Debian: sudo apt install python3.9 python3.9-pip"
    echo "macOS: brew install python@3.9"
    echo "Veya: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python bulundu: $(python3 --version)"

# Virtual environment oluştur
echo
echo "[2/5] Virtual environment olusturuluyor..."
if [ -d "venv" ]; then
    echo "Virtual environment zaten mevcut."
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Virtual environment olusturulamadi!"
        exit 1
    fi
    echo "Virtual environment olusturuldu."
fi

# Virtual environment aktifleştir
echo
echo "[3/5] Virtual environment aktiflestiriliyor..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Virtual environment aktiflestirilemedi!"
    exit 1
fi
echo "Virtual environment aktiflestirildi."

# Dependencies kur
echo
echo "[4/5] Dependencies kuruluyor..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Dependencies kurulamadi!"
    echo "Internet baglantinizi kontrol edin."
    exit 1
fi
echo "Dependencies kuruldu."

# Sistem testi
echo
echo "[5/5] Sistem testi yapiliyor..."
python3 quick_start.py
if [ $? -ne 0 ]; then
    echo
    echo "WARNING: Sistem testinde sorunlar var!"
    echo "Log dosyalarini kontrol edin."
else
    echo
    echo "========================================"
    echo "    Kurulum basarili!"
    echo "========================================"
    echo
    echo "Kullanim:"
    echo "- Kamera modu: python3 main.py"
    echo "- Web arayuzu: python3 app.py"
    echo "- Test: python3 quick_start.py"
    echo
fi

# macOS için ek izinler
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo
    echo "macOS tespit edildi!"
    echo "Ekran yakalama icin izin gerekebilir:"
    echo "Sistem Tercihleri > Guvenlik ve Gizlilik > Ekran Kaydi"
    echo "Terminal/Python uygulamasina izin verin."
fi

echo
echo "Kurulum tamamlandi!"
