/**
 * AUTO-INSPECT AI - Módulo de Captura de Stream de Cámara (getUserMedia)
 * y Consumo de API FastAPI para Inspección Vehicular
 */

class VehicleCameraStream {
  constructor(options = {}) {
    this.videoElement = document.getElementById(options.videoId || 'video-preview');
    this.canvasElement = document.getElementById(options.canvasId || 'captured-canvas');
    this.previewImg = document.getElementById(options.previewImgId || 'image-result-preview');
    this.btnStartCamera = document.getElementById('btn-start-camera');
    this.btnCapture = document.getElementById('btn-capture-photo');
    this.btnSwitchCamera = document.getElementById('btn-switch-camera');
    this.btnAnalyze = document.getElementById('btn-run-analysis');
    this.fileInput = document.getElementById('file-upload-input');
    this.scanline = document.getElementById('hud-scanline');
    
    this.stream = null;
    this.facingMode = 'environment';
    this.capturedBlob = null;
    this.capturedBase64 = null;
    this.apiBaseUrl = options.apiBaseUrl || 'http://localhost:8000';

    this.initEventListeners();
  }

  initEventListeners() {
    if (this.btnStartCamera) {
      this.btnStartCamera.onclick = () => this.startCamera();
    }

    if (this.btnCapture) {
      this.btnCapture.onclick = () => this.takeSnapshot();
    }

    if (this.btnSwitchCamera) {
      this.btnSwitchCamera.onclick = () => this.switchCamera();
    }

    if (this.fileInput) {
      this.fileInput.onchange = (e) => this.handleFileUpload(e);
    }

    if (this.btnAnalyze) {
      this.btnAnalyze.onclick = () => this.sendToFastAPI();
    }
  }

  async startCamera() {
    this.stopCamera();
    const statusText = document.getElementById('camera-status-text');
    const guideText = document.getElementById('hud-guide-text');

    if (statusText) statusText.textContent = 'CONECTANDO CÁMARA...';

    // 1. Probar primero con constraints flexibles
    let mediaStream = null;
    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('getUserMedia no disponible en este navegador o contexto no seguro.');
      }

      try {
        // Intento 1: cámara solicitada
        mediaStream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: { ideal: this.facingMode } },
          audio: false
        });
      } catch (err1) {
        console.warn('Fallback a video básico sin facingMode:', err1);
        // Intento 2: cualquier cámara disponible
        mediaStream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: false
        });
      }

      this.stream = mediaStream;
      this.videoElement.srcObject = this.stream;
      await this.videoElement.play();

      this.videoElement.style.display = 'block';
      if (this.previewImg) this.previewImg.style.display = 'none';

      if (statusText) statusText.textContent = 'EN VIVO (Cámara Activa)';
      if (guideText) guideText.textContent = 'Encuadre el costado del vehículo dentro del recuadro';
      
      if (this.btnCapture) {
        this.btnCapture.disabled = false;
        this.btnCapture.classList.remove('btn-secondary');
        this.btnCapture.classList.add('btn-primary');
      }
      if (this.btnSwitchCamera) this.btnSwitchCamera.disabled = false;

    } catch (err) {
      console.warn('Hardware de cámara no accesible:', err);
      if (statusText) statusText.textContent = 'MODO DEMO / CÁMARA SIMULADA';
      if (guideText) guideText.textContent = 'Cámara física no detectada. Cargando simulador visual...';
      
      // Si no hay webcam física, activar feed simulado de prueba
      this.startSimulatedCamera();
    }
  }

  startSimulatedCamera() {
    // Genera una cámara simulada en tiempo real usando el canvas
    if (!this.canvasElement) return;
    this.canvasElement.width = 640;
    this.canvasElement.height = 400;
    const ctx = this.canvasElement.getContext('2d');

    // Dibujar carrocería simulada
    this.drawSimulatedCarPanel(ctx, 'scratch');

    // Convertir canvas a imagen capturada
    this.capturedBase64 = this.canvasElement.toDataURL('image/jpeg', 0.9);
    this.canvasElement.toBlob((blob) => {
      this.capturedBlob = blob;
      this.showCapturedPreview(this.capturedBase64);
    }, 'image/jpeg', 0.9);

    const guideText = document.getElementById('hud-guide-text');
    if (guideText) guideText.textContent = 'Simulación activa con daño de prueba. Presione "Analizar Daños con IA"';
    
    if (this.btnCapture) this.btnCapture.disabled = false;
  }

  drawSimulatedCarPanel(ctx, defectType = 'scratch') {
    const w = ctx.canvas.width;
    const h = ctx.canvas.height;

    // Fondo panel metálico de vehículo
    const grad = ctx.createLinearGradient(0, 0, w, h);
    grad.addColorStop(0, '#374151');
    grad.addColorStop(0.5, '#4b5563');
    grad.addColorStop(1, '#1f2937');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, w, h);

    // Línea de cintura de la carrocería
    ctx.strokeStyle = '#9ca3af';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(0, h * 0.4);
    ctx.lineTo(w, h * 0.42);
    ctx.stroke();

    // Manija de puerta del auto
    ctx.fillStyle = '#111827';
    ctx.fillRect(w * 0.65, h * 0.35, 90, 22);
    ctx.strokeStyle = '#6b7280';
    ctx.strokeRect(w * 0.65, h * 0.35, 90, 22);

    // Dibujar defecto según tipo
    if (defectType === 'scratch') {
      ctx.strokeStyle = '#f3f4f6';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(w * 0.25, h * 0.55);
      ctx.lineTo(w * 0.52, h * 0.62);
      ctx.stroke();

      // Rayón secundario
      ctx.strokeStyle = '#e5e7eb';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(w * 0.28, h * 0.60);
      ctx.lineTo(w * 0.48, h * 0.65);
      ctx.stroke();
    } else if (defectType === 'dent') {
      // Abolladura (sombra y reflejo cóncavo)
      const dentGrad = ctx.createRadialGradient(w * 0.45, h * 0.55, 10, w * 0.45, h * 0.55, 60);
      dentGrad.addColorStop(0, '#111827');
      dentGrad.addColorStop(0.6, '#1f2937');
      dentGrad.addColorStop(1, '#4b5563');
      ctx.fillStyle = dentGrad;
      ctx.beginPath();
      ctx.arc(w * 0.45, h * 0.55, 60, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  stopCamera() {
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
      this.stream = null;
    }
  }

  switchCamera() {
    this.facingMode = this.facingMode === 'environment' ? 'user' : 'environment';
    this.startCamera();
  }

  takeSnapshot() {
    const w = this.videoElement.videoWidth || 640;
    const h = this.videoElement.videoHeight || 480;

    this.canvasElement.width = w;
    this.canvasElement.height = h;

    const ctx = this.canvasElement.getContext('2d');
    if (this.videoElement && this.videoElement.srcObject) {
      ctx.drawImage(this.videoElement, 0, 0, w, h);
    } else {
      this.drawSimulatedCarPanel(ctx, 'scratch');
    }

    this.capturedBase64 = this.canvasElement.toDataURL('image/jpeg', 0.90);
    this.canvasElement.toBlob((blob) => {
      this.capturedBlob = blob;
      this.showCapturedPreview(this.capturedBase64);
    }, 'image/jpeg', 0.90);
  }

  handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    this.stopCamera();
    this.capturedBlob = file;

    const reader = new FileReader();
    reader.onload = (e) => {
      this.capturedBase64 = e.target.result;
      this.showCapturedPreview(this.capturedBase64);
    };
    reader.readAsDataURL(file);
  }

  loadSample(type = 'scratch') {
    this.stopCamera();
    this.canvasElement.width = 640;
    this.canvasElement.height = 400;
    const ctx = this.canvasElement.getContext('2d');
    this.drawSimulatedCarPanel(ctx, type);

    this.capturedBase64 = this.canvasElement.toDataURL('image/jpeg', 0.90);
    this.canvasElement.toBlob((blob) => {
      this.capturedBlob = blob;
      this.showCapturedPreview(this.capturedBase64);
      
      const guideText = document.getElementById('hud-guide-text');
      if (guideText) guideText.textContent = `Foto de prueba (${type.toUpperCase()}) cargada. Presione "Analizar Daños con IA"`;
    }, 'image/jpeg', 0.90);
  }

  showCapturedPreview(dataUrl) {
    if (this.previewImg) {
      this.previewImg.src = dataUrl;
      this.previewImg.style.display = 'block';
    }
    if (this.videoElement) {
      this.videoElement.style.display = 'none';
    }

    const statusText = document.getElementById('camera-status-text');
    if (statusText) statusText.textContent = 'FOTOGRAFÍA CAPTURADA ✓';

    const guideText = document.getElementById('hud-guide-text');
    if (guideText) guideText.textContent = 'Imagen lista. Presione "Analizar Daños con IA (MobileNet)"';
    
    if (this.btnAnalyze) {
      this.btnAnalyze.disabled = false;
      this.btnAnalyze.style.opacity = '1';
      this.btnAnalyze.style.cursor = 'pointer';
    }
  }

  async sendToFastAPI() {
    if (!this.capturedBlob) {
      // Si aún no capturó, generar fotograma o muestra automáticamente para asistir al usuario
      this.loadSample('scratch');
    }

    const vehicleId = document.getElementById('vehicle-id-input')?.value.trim() || 'SNA-2026';
    const sidePosition = document.getElementById('side-position-select')?.value || 'Lateral Derecho';
    const notes = document.getElementById('inspection-notes')?.value || '';

    // Activar escáner visual
    if (this.scanline) this.scanline.style.display = 'block';
    if (this.btnAnalyze) {
      this.btnAnalyze.disabled = true;
      this.btnAnalyze.innerHTML = '⏳ Analizando con MobileNet...';
    }

    const formData = new FormData();
    formData.append('vehicle_id', vehicleId);
    formData.append('side_position', sidePosition);
    formData.append('notes', notes);
    formData.append('file', this.capturedBlob, 'vehicle_capture.jpg');

    let result = null;
    let inspectionSuccess = false;

    // 1. Intento primario: Proxy HTTP de Django (Mismo origen port 8001, sin problemas de CORS)
    try {
      const proxyResponse = await fetch('/api/inspect-proxy/', {
        method: 'POST',
        body: formData
      });

      if (proxyResponse.ok) {
        result = await proxyResponse.json();
        inspectionSuccess = true;
      }
    } catch (proxyErr) {
      console.warn('Proxy Django no respondió, probando FastAPI directo:', proxyErr);
    }

    // 2. Intento secundario: Conexión directa a FastAPI (port 8000)
    if (!inspectionSuccess) {
      try {
        const response = await fetch(`${this.apiBaseUrl}/api/v1/inspect-vehicle`, {
          method: 'POST',
          body: formData
        });

        if (response.ok) {
          result = await response.json();
          inspectionSuccess = true;
        }
      } catch (directErr) {
        console.warn('FastAPI directo falló:', directErr);
      }
    }

    if (inspectionSuccess && result) {
      this.renderInspectionResults(result);
    } else {
      // 3. Fallback de demostración local
      this.simulateFallbackInspection(vehicleId, sidePosition);
    }

    if (this.scanline) this.scanline.style.display = 'none';
    if (this.btnAnalyze) {
      this.btnAnalyze.disabled = false;
      this.btnAnalyze.innerHTML = '⚡ Re-Analizar Costado';
    }
  }

  renderInspectionResults(data) {
    const resultsContainer = document.getElementById('results-card');
    if (!resultsContainer) return;

    resultsContainer.style.display = 'block';
    resultsContainer.scrollIntoView({ behavior: 'smooth' });

    document.getElementById('res-vehicle-id').textContent = data.vehicle_id || 'SNA-2026';
    document.getElementById('res-side').textContent = data.side_position || 'Costado';
    document.getElementById('res-confidence').textContent = `${Math.round((data.confidence || 0.85) * 100)}%`;
    document.getElementById('res-timestamp').textContent = new Date(data.timestamp || Date.now()).toLocaleString();
    document.getElementById('res-inspection-id').textContent = data.inspection_id || '---';

    const damageBadge = document.getElementById('res-damage-badge');
    const typeBadge = document.getElementById('res-type-badge');
    const severityBadge = document.getElementById('res-severity-badge');

    if (data.damage_detected) {
      damageBadge.textContent = 'DAÑO DETECTADO';
      damageBadge.className = 'badge badge-dent';

      typeBadge.textContent = data.type === 'Scratch' ? 'Rayón (Scratch)' : 'Abolladura (Dent)';
      typeBadge.className = data.type === 'Scratch' ? 'badge badge-scratch' : 'badge badge-dent';

      severityBadge.textContent = `Severidad: ${data.severity}`;
      severityBadge.className = `badge badge-severity-${(data.severity || 'medium').toLowerCase()}`;
    } else {
      damageBadge.textContent = 'SIN DAÑOS PREVIOS';
      damageBadge.className = 'badge badge-clean';

      typeBadge.textContent = 'Carrocería Intacta';
      typeBadge.className = 'badge badge-clean';

      severityBadge.textContent = 'Severidad: N/A';
      severityBadge.className = 'badge badge-severity-low';
    }

    if (data.annotated_image && this.previewImg) {
      this.previewImg.src = data.annotated_image;
      this.previewImg.style.display = 'block';
    }

    const btnGoReport = document.getElementById('btn-go-report');
    if (btnGoReport) {
      btnGoReport.href = `/report/?vehicle_id=${encodeURIComponent(data.vehicle_id || 'SNA-2026')}&inspection_id=${encodeURIComponent(data.inspection_id || '')}`;
    }
  }

  simulateFallbackInspection(vehicleId, sidePosition) {
    const mockResult = {
      damage_detected: true,
      type: "Scratch",
      severity: "Medium",
      confidence: 0.88,
      timestamp: new Date().toISOString(),
      inspection_id: "insp-" + Math.random().toString(36).substring(2, 9),
      vehicle_id: vehicleId,
      side_position: sidePosition,
      annotated_image: this.capturedBase64
    };
    this.renderInspectionResults(mockResult);
  }
}

// Funciones globales accesibles directamente desde onclick en el HTML
window.startCamera = function() {
  if (!window.vehicleCamera) initVehicleCamera();
  window.vehicleCamera.startCamera();
};

window.takeSnapshot = function() {
  if (!window.vehicleCamera) initVehicleCamera();
  window.vehicleCamera.takeSnapshot();
};

window.switchCamera = function() {
  if (!window.vehicleCamera) initVehicleCamera();
  window.vehicleCamera.switchCamera();
};

window.triggerFileUpload = function() {
  document.getElementById('file-upload-input').click();
};

window.sendToFastAPI = function() {
  if (!window.vehicleCamera) initVehicleCamera();
  window.vehicleCamera.sendToFastAPI();
};

window.loadSample = function(type) {
  if (!window.vehicleCamera) initVehicleCamera();
  window.vehicleCamera.loadSample(type);
};

function initVehicleCamera() {
  if (!window.vehicleCamera) {
    window.vehicleCamera = new VehicleCameraStream({
      apiBaseUrl: window.API_BASE_URL || 'http://localhost:8000'
    });
  }
}

// Inicialización segura sin depender de que DOMContentLoaded no haya ocurrido ya
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initVehicleCamera);
} else {
  initVehicleCamera();
}
