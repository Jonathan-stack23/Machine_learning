# 🚗 Asistente de Inspección de Daños Físicos en Vehículos (Alquileres)

> **Monorepo de Inteligencia Artificial para Detección de Daños Preexistentes**  
> Proyecto Machine Learning — 3er Trimestre — SENA

---

## 👥 Integrantes del Proyecto

- **Jonathan** — [GitHub: @Jonathan-stack23](https://github.com/Jonathan-stack23) — *Desarrollo Backend / Frontend & Machine Learning*
- **Angela Martínez** — [Email: angela_smartinez@soy.sena.edu.co](mailto:angela_smartinez@soy.sena.edu.co) — *Desarrollo Backend / Frontend & Control de Calidad*

---

## 🔗 Enlaces y Accesos del Sistema

| Componente | Entorno Local | Documentación / Producción |
|------------|---------------|----------------------------|
| **Frontend (Django)** | `http://localhost:8000` o `http://127.0.0.1:8001` | Interfaz interactiva de captura de cámara (`getUserMedia`) |
| **Backend (FastAPI)** | `http://localhost:8000` | **Swagger Interactivo**: [`http://localhost:8000/docs`](http://localhost:8000/docs) |
| **ReDoc API** | `http://localhost:8000/redoc` | Especificación técnica OpenAPI 3.0 |
| **Repositorio GitHub** | [https://github.com/Jonathan-stack23/Machine_learning.git](https://github.com/Jonathan-stack23/Machine_learning.git) | Monorepo completo con los 8 commits requeridos |
| **Despliegue Vercel** | Configurado en `vercel.json` | Serverless Functions Python (`@vercel/python`) |

---

## 🎯 1. Problema Real Solucionado

En las empresas de alquiler de automóviles (*Rent-a-Car*), uno de los puntos más críticos de fricción con los clientes son las **disputas por rayones, hendiduras o abolladuras preexistentes** al momento de devolver el vehículo. Los procesos manuales con papel y hojas de checklist con frecuencia omiten detalles que luego se cobran injustamente al usuario o representan pérdidas patrimoniales para la compañía.

### ✅ Solución Propuesta
Un sistema web con **visión por computadora (MobileNet)** que:
1. Permite al inspector capturar fotografías del vehículo en tiempo real mediante el stream de cámara en el navegador web (`navigator.mediaDevices.getUserMedia`).
2. Analiza instantáneamente el costado fotografiado con inferencia de redes neuronales convolucionales.
3. Detecta y clasifica la anomalía (`Scratch` / `Dent` / `Clean`), calcula el grado de severidad (`Low`, `Medium`, `High`) y su nivel de confianza estadística.
4. Genera un **Acta Digital de Inspección** firmada criptográficamente con hash SHA-256 para exonerar al arrendatario y proteger a la empresa.

---

## 🛠️ 2. Stack Tecnológico

- **Frontend**: **Django 4.2+** (vistas, sistema de sesiones, plantillas HTML5 semánticas, CSS moderno con estética Glassmorphism en modo oscuro, JavaScript ES6+ para captura de stream de cámara vía `getUserMedia` y consumo de API REST).
- **Backend**: **FastAPI 0.115+** (procesamiento de imágenes con Python, validación de datos con **Pydantic v2**, documentación interactiva Swagger en `/docs`).
- **Visión por Computadora / ML**: Arquitectura **MobileNetV2** preentrenada, OpenCV y Pillow para preprocesamiento tensorial, extracción morfológica de discontinuidades y generación de bounding boxes visuales.
- **Autenticación**: Sistema de Login/Password con sesiones en Django y generación/validación de tokens **JWT** (JSON Web Tokens) en FastAPI.
- **Despliegue**: Configuración para **Vercel** mediante Serverless Functions (`vercel.json`).

---

## 📁 3. Estructura del Monorepo

```
Machine_learning/
├── README.md                        # Documentación técnica completa
├── vercel.json                      # Configuración para despliegue serverless en Vercel
├── requirements.txt                 # Dependencias consolidadas del proyecto
├── .gitignore                       # Filtros de exclusión de Git
│
├── backend/                         # Microservicio API FastAPI
│   ├── main.py                      # App principal FastAPI, CORS, middlewares y rutas
│   ├── requirements.txt             # Dependencias específicas de FastAPI
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── jwt_handler.py           # Creación, firma y verificación de tokens JWT
│   │   └── routes.py                # Endpoints de login, registro y perfil (/auth/login)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── mobilenet_loader.py      # Cargador de arquitectura MobileNet y tensores
│   │   ├── damage_detector.py       # Pipeline de inferencia, bounding boxes y anotación
│   │   └── storage.py               # Almacén de inspecciones registradas
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py                  # Esquemas Pydantic para login y tokens
│   │   └── inspection.py            # Esquemas Pydantic de inspección y actas
│   └── routes/
│       ├── __init__.py
│       ├── inspect.py               # POST /api/v1/inspect-vehicle
│       └── report.py                # GET /api/v1/inspection-report
│
└── frontend/                        # Aplicación Web Django
    ├── manage.py                    # Gestor CLI de Django
    ├── requirements.txt             # Dependencias específicas de Django
    ├── vehicle_inspector/           # Proyecto base Django
    │   ├── __init__.py
    │   ├── settings.py              # Configuración, static, templates y settings de FastAPI
    │   ├── urls.py                  # Enrutador principal de URLs
    │   ├── wsgi.py                  # Entrada WSGI para producción y Vercel
    │   └── asgi.py                  # Entrada ASGI
    └── inspection/                  # App de inspección vehicular
        ├── __init__.py
        ├── models.py                # Modelos de datos
        ├── views.py                 # Vistas: login, dashboard, inspect, report, proxy
        ├── urls.py                  # Rutas internas de la app
        ├── services.py              # Cliente HTTP (FastAPIService) para integración
        ├── static/
        │   ├── css/
        │   │   └── style.css        # Sistema de diseño, Glassmorphism y Dark Theme
        │   └── js/
        │       └── camera.js        # getUserMedia, canvas snapshot y comunicación API
        └── templates/
            ├── base.html            # Layout maestro con navbar y pie de página
            ├── login.html           # Inicio de sesión con credenciales demo
            ├── dashboard.html       # Panel de métricas y resumen de flota
            ├── inspect.html         # Visor de cámara en vivo con HUD reticular
            └── report.html          # Acta digital de entrega con sello criptográfico
```

---

## 🚀 4. Endpoints de la API en Swagger (`/docs`)

### 1. `POST /api/v1/inspect-vehicle`
Analiza la fotografía del costado del vehículo y retorna la detección del modelo:

- **Formato:** `multipart/form-data`
  - `file`: Archivo de imagen (JPEG/PNG/WebP) capturado por la cámara.
  - `vehicle_id`: Placa o VIN (Ej: `SNA-2026`).
  - `side_position`: Costado (`Lateral Derecho`, `Lateral Izquierdo`, `Frontal`, etc.).
  - `notes`: Observaciones del inspector.

**Ejemplo de Respuesta:**
```json
{
  "damage_detected": true,
  "type": "Scratch",
  "severity": "Medium",
  "confidence": 0.87,
  "timestamp": "2026-09-23T13:20:59",
  "inspection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "vehicle_id": "SNA-2026",
  "side_position": "Lateral Derecho",
  "boxes_count": 1,
  "damage_boxes": [
    {
      "x": 120,
      "y": 85,
      "width": 160,
      "height": 45,
      "label": "Rayón (Medium)"
    }
  ],
  "annotated_image": "data:image/jpeg;base64,...",
  "model_used": "MobileNetV2-VehicularInspection"
}
```

---

### 2. `GET /api/v1/inspection-report`
Genera el resumen digital consolidado de inspección para prevención de disputas:

- **Parámetros Query:**
  - `vehicle_id`: Placa del automóvil (Ej: `SNA-2026`).
  - `inspector_name`: Nombre del inspector responsable.

**Ejemplo de Respuesta:**
```json
{
  "report_id": "REP-8A2F91C",
  "vehicle_id": "SNA-2026",
  "inspector_name": "Jonathan SENA - Inspector",
  "generated_at": "2026-09-23T13:20:59",
  "total_inspections_performed": 4,
  "total_damages": 1,
  "has_preexisting_damages": true,
  "overall_status": "Observaciones Registradas",
  "damages": [
    {
      "side_position": "Lateral Derecho",
      "type": "Scratch",
      "severity": "Medium",
      "confidence": 0.87,
      "detected_at": "2026-09-23T13:20:59"
    }
  ],
  "digital_certificate_hash": "c8f2b7a9e14d3c90e21a88b56f1498b3c45781a980562e..."
}
```

---

### 3. `POST /api/v1/auth/login`
Autenticación de inspectores mediante JWT:
- **Body:** `{"username": "inspector", "password": "sena2026"}`
- **Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "username": "inspector",
  "full_name": "Jonathan SENA - Inspector",
  "role": "Inspector Vehicular"
}
```

---

## 📌 5. Estructura de los 8 Commits en GitHub

El repositorio sigue estrictamente la progresión cronológica de 8 commits solicitada:

1. `init: estructura base django frontend y fastapi backend`
2. `feat: modulo de autenticacion de usuario y control de acceso`
3. `feat: carga e inferencia del modelo preentrenado en fastapi`
4. `docs: esquemas pydantic y documentacion de endpoints en swagger`
5. `feat: interfaz ui en django y captura de stream de camara en js`
6. `feat: integracion http entre cliente django y servidor fastapi`
7. `fix: optimizacion de respuesta, manejo de errores y ui polish`
8. `deploy: configuracion vercel.json y pruebas finales de produccion`

---

## 💻 6. Guía de Ejecución Local Paso a Paso

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Jonathan-stack23/Machine_learning.git
cd Machine_learning
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Iniciar el Backend (FastAPI con Swagger)
En una terminal:
```bash
uvicorn backend.main:app --reload --port 8000
```
- Swagger interactivo disponible en: `http://localhost:8000/docs`

### 4. Iniciar el Frontend (Django con Captura de Cámara)
En una segunda terminal:
```bash
cd frontend
python manage.py migrate
python manage.py runserver 8001
```
- Acceso web: `http://localhost:8001`
- Credenciales por defecto:
  - **Usuario:** `inspector` | **Contraseña:** `sena2026`
  - **Usuario:** `admin` | **Contraseña:** `admin123`

---

## 🎤 7. Guía para la Exposición Presencial (15 Minutos)

| Minutos | Sección | Puntos Clave a Explicar |
|---------|---------|-------------------------|
| **0 - 3** | **Introducción y Problema Real** | Explicar el problema de disputas entre clientes y empresas de alquiler por rayones y abolladuras no identificadas previamente. Presentar el objetivo del proyecto. |
| **3 - 6** | **Arquitectura y Stack Tecnológico** | Detallar la arquitectura Monorepo: Frontend en Django + Backend en FastAPI + Modelo MobileNet. Explicar la ventaja de separar la UI del motor de IA. |
| **6 - 9** | **Demostración en Vivo (Live Demo)** | Iniciar sesión como inspector, activar la cámara web vía `getUserMedia`, capturar el fotograma con el HUD de carrocería, ejecutar la inferencia y mostrar los recuadros de daños detectados. |
| **9 - 12** | **Documentación Swagger y API REST** | Mostrar la documentación Swagger en `/docs`, probar el endpoint `POST /api/v1/inspect-vehicle` y `GET /api/v1/inspection-report` demostrando los esquemas Pydantic y el hash criptográfico del acta digital. |
| **12 - 15** | **Conclusiones y Preguntas** | Repasar los 8 commits en GitHub, la configuración para despliegue en Vercel y responder preguntas de los evaluadores. |

---

*Desarrollado con dedicación para el programa de formación en Inteligencia Artificial y Machine Learning — SENA.*
