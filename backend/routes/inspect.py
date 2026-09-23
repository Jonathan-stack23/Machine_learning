"""
Ruta de Inferencia: POST /api/v1/inspect-vehicle
"""
import base64
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from typing import Optional
from backend.schemas.inspection import InspectionResponse, VehicleInspectionPayload
from backend.models.damage_detector import analyze_vehicle_damage
from backend.models.storage import save_inspection

router = APIRouter(prefix="/api/v1", tags=["Inspección Vehicular con IA"])


@router.post(
    "/inspect-vehicle",
    response_model=InspectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Analizar costado fotografiado con MobileNet",
    description="""
    **Analiza el costado fotografiado de un vehículo y detecta anomalías físicas.**
    
    Retorna el esquema exacto:
    ```json
    {
      "damage_detected": true,
      "type": "Scratch",
      "severity": "Medium",
      "confidence": 0.87,
      "timestamp": "2026-09-23T13:20:59",
      "inspection_id": "uuid..."
    }
    ```
    
    Acepta tanto carga de archivo de imagen (multipart/form-data) vía cámara/galería
    como datos del vehículo (placa, posición del costado).
    """
)
async def inspect_vehicle(
    vehicle_id: str = Form("ABC-123", description="Placa o ID del vehículo"),
    side_position: str = Form("Lateral Derecho", description="Costado del vehículo inspeccionado"),
    notes: Optional[str] = Form(None, description="Notas adicionales del inspector"),
    file: Optional[UploadFile] = File(None, description="Fotografía capturada de la carrocería")
):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar un archivo de imagen válido capturado por la cámara."
        )

    # Validar extensión / mime type
    valid_content_types = ["image/jpeg", "image/png", "image/webp", "image/jpg"]
    if file.content_type not in valid_content_types and not file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato no admitido ({file.content_type}). Utilice JPEG, PNG o WebP."
        )

    image_bytes = await file.read()
    if len(image_bytes) < 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo de imagen está vacío o corrupto."
        )

    # Inferencia del modelo MobileNet
    result = analyze_vehicle_damage(
        image_bytes=image_bytes,
        side_position=side_position,
        vehicle_id=vehicle_id
    )

    # Guardar registro para generación de reportes
    save_inspection(result)

    return result


@router.post(
    "/inspect-vehicle-json",
    response_model=InspectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Analizar costado vía JSON Base64",
    description="Endpoint alternativo para clientes web o móviles que envían la captura en Base64."
)
async def inspect_vehicle_json(payload: VehicleInspectionPayload):
    if not payload.image_base64:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe incluir la imagen en formato Base64."
        )

    # Limpiar prefijo data:image/...;base64, si existe
    raw_b64 = payload.image_base64
    if "," in raw_b64:
        raw_b64 = raw_b64.split(",", 1)[1]

    try:
        image_bytes = base64.b64decode(raw_b64)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al decodificar imagen base64: {str(e)}"
        )

    result = analyze_vehicle_damage(
        image_bytes=image_bytes,
        side_position=payload.side_position,
        vehicle_id=payload.vehicle_id
    )

    save_inspection(result)
    return result
