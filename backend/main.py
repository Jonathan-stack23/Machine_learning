"""
FastAPI Backend - Asistente de Inspección de Daños Físicos en Vehículos
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Asistente de Inspección de Daños en Vehículos API",
    description="Backend de IA para detección de abolladuras y rayones en vehículos de alquiler.",
    version="1.0.0",
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

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "service": "Vehicle Damage Inspection API",
        "version": "1.0.0",
        "docs": "/docs"
    }
