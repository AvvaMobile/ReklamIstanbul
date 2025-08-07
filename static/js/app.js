// Global değişkenler
let isRunning = false;
let statsInterval = null;
let currentConfig = {
    use_screen_capture: false,
    camera_index: 0,
    screen_region: null,
    detection_threshold: 0.4,
    model_path: 'yolov8s.pt'
};

// DOM elementleri
const videoSource = document.getElementById('videoSource');
const cameraSection = document.getElementById('cameraSection');
const screenSection = document.getElementById('screenSection');
const cameraSelect = document.getElementById('cameraSelect');
const screenRegion = document.getElementById('screenRegion');
const modelSelect = document.getElementById('modelSelect');
const detectionThreshold = document.getElementById('detectionThreshold');
const thresholdValue = document.getElementById('thresholdValue');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const videoFeed = document.getElementById('videoFeed');
const noVideo = document.getElementById('noVideo');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const videoSourceInfo = document.getElementById('videoSourceInfo');
const fpsInfo = document.getElementById('fpsInfo');

// İstatistik elementleri
const hourlyCount = document.getElementById('hourlyCount');
const dailyCount = document.getElementById('dailyCount');
const totalCount = document.getElementById('totalCount');
const activePeople = document.getElementById('activePeople');

// Sayfa yüklendiğinde çalışacak fonksiyonlar
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    loadCameras();
    setupEventListeners();
    updateStatus('ready', 'Hazır');
});

// Uygulamayı başlat
function initializeApp() {
    console.log('İnsan Sayma Sistemi UI başlatıldı');
    
    // Mevcut konfigürasyonu yükle
    loadConfig();
    
    // Video kaynağı değişikliğini dinle
    videoSource.addEventListener('change', handleVideoSourceChange);
    
    // Tespit eşiği değişikliğini dinle
    detectionThreshold.addEventListener('input', function() {
        thresholdValue.textContent = this.value;
        currentConfig.detection_threshold = parseFloat(this.value);
        saveConfig();
    });
    
    // Model seçimi değişikliğini dinle
    modelSelect.addEventListener('change', function() {
        currentConfig.model_path = this.value;
        saveConfig();
    });
}

// Kameraları yükle
async function loadCameras() {
    try {
        const response = await fetch('/api/cameras');
        const cameras = await response.json();
        
        cameraSelect.innerHTML = '';
        
        if (cameras.length === 0) {
            cameraSelect.innerHTML = '<option value="">Kamera bulunamadı</option>';
        } else {
            cameras.forEach(camera => {
                const option = document.createElement('option');
                option.value = camera.index;
                option.textContent = `${camera.name} (${camera.resolution})`;
                cameraSelect.appendChild(option);
            });
            
            // İlk kamerayı seç
            if (cameras.length > 0) {
                cameraSelect.value = cameras[0].index;
                currentConfig.camera_index = cameras[0].index;
            }
        }
    } catch (error) {
        console.error('Kamera yükleme hatası:', error);
        cameraSelect.innerHTML = '<option value="">Kamera yüklenemedi</option>';
    }
}

// Event listener'ları ayarla
function setupEventListeners() {
    // Başlat butonu
    startBtn.addEventListener('click', startSystem);
    
    // Durdur butonu
    stopBtn.addEventListener('click', stopSystem);
    
    // Kamera seçimi
    cameraSelect.addEventListener('change', function() {
        currentConfig.camera_index = parseInt(this.value);
        saveConfig();
    });
    
    // Ekran bölgesi seçimi
    screenRegion.addEventListener('change', function() {
        const regionMap = {
            'full': null,
            'top_left': [0, 0, 800, 600],
            'center': [400, 300, 800, 600],
            'small': [100, 100, 400, 300]
        };
        currentConfig.screen_region = regionMap[this.value];
        saveConfig();
    });
}

// Video kaynağı değişikliğini handle et
function handleVideoSourceChange() {
    const isScreenCapture = videoSource.value === 'screen';
    
    currentConfig.use_screen_capture = isScreenCapture;
    saveConfig();
    
    // UI'ı güncelle
    if (isScreenCapture) {
        cameraSection.style.display = 'none';
        screenSection.style.display = 'block';
        videoSourceInfo.textContent = 'Ekran Yakalama';
    } else {
        cameraSection.style.display = 'block';
        screenSection.style.display = 'none';
        videoSourceInfo.textContent = 'Kamera';
    }
}

// Sistemi başlat
async function startSystem() {
    if (isRunning) {
        showNotification('Sistem zaten çalışıyor', 'warning');
        return;
    }
    
    try {
        updateStatus('loading', 'Başlatılıyor...');
        startBtn.disabled = true;
        startBtn.innerHTML = '<span class="loading"></span> Başlatılıyor...';
        
        // Konfigürasyonu gönder
        const configResponse = await fetch('/api/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(currentConfig)
        });
        
        if (!configResponse.ok) {
            throw new Error('Konfigürasyon güncellenemedi');
        }
        
        // Sistemi başlat
        const startResponse = await fetch('/api/start', {
            method: 'POST'
        });
        
        const result = await startResponse.json();
        
        if (result.status === 'success') {
            isRunning = true;
            updateUI();
            startVideoFeed();
            startStatsUpdate();
            showNotification('Sistem başlatıldı', 'success');
            updateStatus('running', 'Çalışıyor');
        } else {
            throw new Error(result.message);
        }
        
    } catch (error) {
        console.error('Başlatma hatası:', error);
        showNotification(`Başlatma hatası: ${error.message}`, 'error');
        updateStatus('error', 'Hata');
    } finally {
        startBtn.disabled = false;
        startBtn.innerHTML = '<i class="fas fa-play"></i> Başlat';
    }
}

// Sistemi durdur
async function stopSystem() {
    if (!isRunning) {
        showNotification('Sistem zaten durmuş', 'warning');
        return;
    }
    
    try {
        updateStatus('loading', 'Durduruluyor...');
        stopBtn.disabled = true;
        stopBtn.innerHTML = '<span class="loading"></span> Durduruluyor...';
        
        const response = await fetch('/api/stop', {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            isRunning = false;
            updateUI();
            stopVideoFeed();
            stopStatsUpdate();
            showNotification('Sistem durduruldu', 'success');
            updateStatus('stopped', 'Durduruldu');
        } else {
            throw new Error(result.message);
        }
        
    } catch (error) {
        console.error('Durdurma hatası:', error);
        showNotification(`Durdurma hatası: ${error.message}`, 'error');
        updateStatus('error', 'Hata');
    } finally {
        stopBtn.disabled = false;
        stopBtn.innerHTML = '<i class="fas fa-stop"></i> Durdur';
    }
}

// UI'ı güncelle
function updateUI() {
    if (isRunning) {
        startBtn.disabled = true;
        stopBtn.disabled = false;
        videoSource.disabled = true;
        cameraSelect.disabled = true;
        screenRegion.disabled = true;
        modelSelect.disabled = true;
        detectionThreshold.disabled = true;
    } else {
        startBtn.disabled = false;
        stopBtn.disabled = true;
        videoSource.disabled = false;
        cameraSelect.disabled = false;
        screenRegion.disabled = false;
        modelSelect.disabled = false;
        detectionThreshold.disabled = false;
    }
}

// Video akışını başlat
function startVideoFeed() {
    videoFeed.style.display = 'block';
    noVideo.style.display = 'none';
    videoFeed.src = '/video_feed?' + new Date().getTime();
}

// Video akışını durdur
function stopVideoFeed() {
    videoFeed.style.display = 'none';
    noVideo.style.display = 'block';
    videoFeed.src = '';
}

// İstatistikleri güncellemeye başla
function startStatsUpdate() {
    statsInterval = setInterval(updateStats, 1000);
}

// İstatistikleri güncellemeyi durdur
function stopStatsUpdate() {
    if (statsInterval) {
        clearInterval(statsInterval);
        statsInterval = null;
    }
}

// İstatistikleri güncelle
async function updateStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        if (stats.is_running) {
            hourlyCount.textContent = stats.hourly_count || 0;
            dailyCount.textContent = stats.daily_count || 0;
            totalCount.textContent = stats.total_count || 0;
            activePeople.textContent = stats.active_people || 0;
        }
    } catch (error) {
        console.error('İstatistik güncelleme hatası:', error);
    }
}

// Durumu güncelle
function updateStatus(status, text) {
    statusDot.className = `status-dot ${status}`;
    statusText.textContent = text;
}

// Konfigürasyonu yükle
function loadConfig() {
    const savedConfig = localStorage.getItem('humanCounterConfig');
    if (savedConfig) {
        const config = JSON.parse(savedConfig);
        currentConfig = { ...currentConfig, ...config };
        
        // UI'ı güncelle
        videoSource.value = currentConfig.use_screen_capture ? 'screen' : 'camera';
        modelSelect.value = currentConfig.model_path;
        detectionThreshold.value = currentConfig.detection_threshold;
        thresholdValue.textContent = currentConfig.detection_threshold;
        
        handleVideoSourceChange();
    }
}

// Konfigürasyonu kaydet
function saveConfig() {
    localStorage.setItem('humanCounterConfig', JSON.stringify(currentConfig));
}

// Bildirim göster
function showNotification(message, type = 'info') {
    // Basit bir bildirim sistemi
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // 5 saniye sonra otomatik kaldır
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// FPS hesaplama (basit implementasyon)
let frameCount = 0;
let lastTime = Date.now();

function updateFPS() {
    frameCount++;
    const currentTime = Date.now();
    
    if (currentTime - lastTime >= 1000) {
        const fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
        fpsInfo.textContent = `${fps} FPS`;
        frameCount = 0;
        lastTime = currentTime;
    }
}

// Video yüklendiğinde FPS hesaplamayı başlat
videoFeed.addEventListener('load', function() {
    if (isRunning) {
        setInterval(updateFPS, 100);
    }
});

// Hata yönetimi
window.addEventListener('error', function(e) {
    console.error('JavaScript hatası:', e.error);
    showNotification('Bir hata oluştu', 'error');
});

// Sayfa kapatılırken temizlik
window.addEventListener('beforeunload', function() {
    if (isRunning) {
        stopSystem();
    }
}); 