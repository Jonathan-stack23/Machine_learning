"""
Esquemas Pydantic y Modelos de Datos para Inspección Vehicular y Documentación Swagger
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Literal
from datetime import datetime


class DamageBox(BaseModel):
    x: int = Field(..., description="Coordenada X inicial del recuadro")
    y: int = Field(..., description="Coordenada Y inicial del recuadro")
    width: int = Field(..., description="Ancho de la zona de daño")
    height: int = Field(..., description="Alto de la zona de daño")
    label: str = Field(..., description="Etiqueta y nivel de severidad", example="Rayón (Medium)")


class VehicleInspectionPayload(BaseModel):
    vehicle_id: str = Field(..., min_length=3, max_length=20, description="Placa o Identificador único del vehículo", example="ABC-123")
    side_position: Literal[
        "Frontal",
        "Lateral Izquierdo",
        "Lateral Derecho",
        "Trasero",
        "Techo / Panorámico"
    ] = Field(..., description="Costado fotografiado del vehículo", example="Lateral Derecho")
    notes: Optional[str] = Field(None, description="Observaciones preliminares del inspector", example="Revisión previa a entrega de alquiler")
    image_base64: Optional[str] = Field(None, description="Imagen en formato base64 (alternativa a multipart)")


class InspectionResponse(BaseModel):
    """
    Respuesta estandarizada de inspección con modelo de IA.
    Cumple con el esquema exacto solicitado:
    {'damage_detected': true, 'type': 'Scratch', 'severity': 'Medium'}
    """
    model_config = ConfigDict(protected_namespaces=())

    damage_detected: bool = Field(..., description="Indica si se encontró algún daño físico en el vehículo", example=True)
    type: Literal["Scratch", "Dent", "None"] = Field(..., description="Tipo de defecto detectado (Rayón, Abolladura o Ninguno)", example="Scratch")
    severity: Literal["Low", "Medium", "High", "None"] = Field(..., description="Grado de severidad del daño", example="Medium")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Nivel de certeza de la inferencia (0.0 a 1.0)", example=0.87)
    timestamp: str = Field(..., description="Marca de tiempo ISO del análisis", example="2026-09-23T13:20:59")
    inspection_id: str = Field(..., description="Identificador único del registro de inspección", example="3fa85f64-5717-4562-b3fc-2c963f66afa6")
    vehicle_id: str = Field(..., description="Placa del vehículo inspeccionado", example="ABC-123")
    side_position: str = Field(..., description="Costado analizado", example="Lateral Derecho")
    boxes_count: int = Field(0, description="Cantidad de regiones con defectos detectadas", example=1)
    damage_boxes: List[DamageBox] = Field(default=[], description="Coordenadas de localización de daños")
    annotated_image: Optional[str] = Field(None, description="Imagen codificada en Base64 con recuadros delimitadores del modelo")
    model_used: str = Field("MobileNetV2-VehicularInspection", description="Red neuronal utilizada en el análisis")


class DamageDetail(BaseModel):
    side_position: str = Field(..., example="Lateral Derecho")
    type: str = Field(..., example="Scratch")
    severity: str = Field(..., example="Medium")
    confidence: float = Field(..., example=0.87)
    detected_at: str = Field(..., example="2026-09-23T13:20:59")


class InspectionReportResponse(BaseModel):
    """
    Resumen digital oficial de inspección vehicular para prevención de disputas.
    """
    report_id: str = Field(..., description="ID único del reporte digital", example="rep-9938-2026")
    vehicle_id: str = Field(..., description="Placa del vehículo", example="ABC-123")
    inspector_name: str = Field(..., description="Inspector responsable", example="Jonathan SENA")
    generated_at: str = Field(..., description="Fecha y hora de emisión", example="2026-09-23T13:20:59")
    total_inspections_performed: int = Field(..., description="Número de costados analizados", example=4)
    total_damages: int = Field(..., description="Total de anomalías detectadas", example=2)
    has_preexisting_damages: bool = Field(..., description="Bandera de alerta de daños previos", example=True)
    overall_status: Literal["Apto para Entrega", "Observaciones Registradas", "No Apto para Circulación"] = Field(
        ..., example="Observaciones Registradas"
    )
    damages: List[DamageDetail] = Field(default=[], description="Lista detallada de daños detectados")
    digital_certificate_hash: str = Field(..., description="Firma criptográfica SHA256 de validez del acta")
