from pydantic import BaseModel
from typing import Optional

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
