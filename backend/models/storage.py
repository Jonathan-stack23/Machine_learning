"""
Almacenamiento en memoria para registro de inspecciones vehiculares
"""
from typing import List, Dict

INSPECTIONS_STORE: List[Dict] = []

def save_inspection(record: dict):
    INSPECTIONS_STORE.append(record)

def get_all_inspections() -> List[Dict]:
    return list(reversed(INSPECTIONS_STORE))

def get_inspections_by_vehicle(vehicle_id: str) -> List[Dict]:
    return [r for r in INSPECTIONS_STORE if r.get("vehicle_id", "").upper() == vehicle_id.upper()]
