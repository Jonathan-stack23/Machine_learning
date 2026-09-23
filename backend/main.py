"""
FastAPI Backend - Asistente de Inspección de Daños Físicos en Vehículos
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "Autenticación",
        "description": "Endpoints de control de acceso e inicio de sesión con tokens JWT.",
    },
    {
        "name": "Inspección Vehicular con IA",
        "description": "Inferencia con MobileNet para detección de abolladuras y rayones en carrocería.",
    },
    {
        "name": "Reportes Digitales de Inspección",
        "description": "Generación de actas y resúmenes digitales de inspección para prevención de disputas.",
    },
    {
        "name": "Health",
        "description": "Monitoreo del estado y disponibilidad del servicio.",
    },
]

app = FastAPI(
    title="Asistente de Inspección de Daños en Vehículos API",
    description="""
    ## Sistema de Inteligencia Artificial para Empresas de Alquiler de Vehículos
    
    Este backend procesa fotografías de vehículos mediante modelos de visión por computadora
    (MobileNet / YOLOv8 Seg) para detectar rayones y abolladuras preexistentes, resolviendo disputas
    al momento de la entrega y recepción.
    
    ### Características:
    - **Inferencia en tiempo real**: Detección de `Scratch`, `Dent` o superficie limpia.
    - **Clasificación de Severidad**: `Low`, `Medium`, `High`.
    - **Cálculo de Confianza**: Probabilidad estadística del modelo.
    - **Generación de Actas Digitales**: Resumen de inspección con hash de integridad.
    """,
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración de CORS para permitir peticiones desde el frontend Django
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from backend.auth.routes import router as auth_router
from backend.routes.inspect import router as inspect_router
from backend.routes.report import router as report_router

app.include_router(auth_router)
app.include_router(inspect_router)
app.include_router(report_router)

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "service": "Vehicle Damage Inspection API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "inspect_vehicle": "POST /api/v1/inspect-vehicle",
            "inspection_report": "GET /api/v1/inspection-report",
            "auth_login": "POST /api/v1/auth/login"
        }
    }

