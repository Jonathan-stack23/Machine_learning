"""
Servicio de Integración HTTP entre Django y el Backend FastAPI
"""
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

class FastAPIService:
    """Cliente HTTP para comunicación entre Django y los microservicios de FastAPI"""
    
    @staticmethod
    def get_base_url():
        return getattr(settings, 'FASTAPI_BACKEND_URL', 'http://localhost:8000')

    @classmethod
    def inspect_vehicle(cls, image_bytes: bytes, filename: str, vehicle_id: str, side_position: str, notes: str = "") -> dict:
        """Envía imagen y metadatos a POST /api/v1/inspect-vehicle en FastAPI"""
        url = f"{cls.get_base_url()}/api/v1/inspect-vehicle"
        files = {
            'file': (filename or 'capture.jpg', image_bytes, 'image/jpeg')
        }
        data = {
            'vehicle_id': vehicle_id,
            'side_position': side_position,
            'notes': notes
        }

        try:
            response = requests.post(url, data=data, files=files, timeout=20)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error comunicando con FastAPI inspect-vehicle: {e}")
            raise Exception(f"Fallo de conexión con el motor de IA de FastAPI: {str(e)}")

    @classmethod
    def get_report(cls, vehicle_id: str = "ABC-123", inspector_name: str = "Jonathan SENA") -> dict:
        """Consulta GET /api/v1/inspection-report en FastAPI"""
        url = f"{cls.get_base_url()}/api/v1/inspection-report"
        params = {
            'vehicle_id': vehicle_id,
            'inspector_name': inspector_name
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error consultando reporte en FastAPI: {e}")
            raise Exception(f"Fallo al obtener reporte digital de FastAPI: {str(e)}")

    @classmethod
    def authenticate_jwt(cls, username: str, password: str) -> dict:
        """Autenticación remota contra FastAPI POST /api/v1/auth/login"""
        url = f"{cls.get_base_url()}/api/v1/auth/login"
        payload = {
            'username': username,
            'password': password
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de autenticación en FastAPI: {e}")
            return None
