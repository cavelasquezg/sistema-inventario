from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Lo que el cliente envía cuando quiere CREAR un material
class MaterialCreate(BaseModel):
    name: str
    description: Optional[str] = None
    unit_of_measure: str
    category: str

# Lo que la API responde al cliente (incluye el ID generado)
class MaterialResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    unit_of_measure: str
    category: str

    class Config:
        from_attributes = True

# --- NUEVOS ESQUEMAS PARA UBICACIONES ---
class LocationCreate(BaseModel):
    name: str
    type: str
    description: Optional[str] = None

class LocationResponse(BaseModel):
    id: int
    name: str
    type: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

# --- NUEVOS ESQUEMAS PARA MOVIMIENTOS ---
class StockMovementCreate(BaseModel):
    material_id: int
    location_id: int
    quantity: int
    movement_type: str # Debe ser 'INPUT' o 'OUTPUT'
    description: Optional[str] = None

class StockMovementResponse(BaseModel):
    id: int
    material_id: int
    location_id: int
    quantity: int
    movement_type: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
