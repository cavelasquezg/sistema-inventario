from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.schemas import MaterialCreate, MaterialResponse
from app.services.material_service import MaterialService

# Creamos el router con un prefijo y una etiqueta para la documentación automática
router = APIRouter(
    prefix="/materials",
    tags=["Materiales"]
)

@router.post("/", response_model=MaterialResponse, status_code=status.HTTP_201_CREATED)
def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    """
    Ruta para crear un nuevo material (RF-MAT-01).
    Usa la dependencia 'get_db' para abrir y cerrar la sesión de la base de datos de forma automática.
    """
    return MaterialService.create_material(db=db, material_data=material)

@router.get("/", response_model=List[MaterialResponse])
def read_materials(
    search: Optional[str] = None, 
    category: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    """
    Ruta para listar materiales (RF-MAT-02).
    Permite filtrar opcionalmente por término de búsqueda (?search=...) o por categoría (?category=...).
    """
    return MaterialService.get_materials(db=db, search=search, category=category)