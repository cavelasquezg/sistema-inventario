from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.models import Material
from app.schemas.schemas import MaterialCreate

class MaterialService:

    @staticmethod
    def create_material(db: Session, material_data: MaterialCreate) -> Material:
        """
        RF-MAT-01: Crear un nuevo material.
        Valida que el nombre sea único, si ya existe lanza un error 400.
        """
        # Verificamos si ya existe un material con ese mismo nombre
        existing_material = db.execute(
            select(Material).where(Material.name == material_data.name)
        ).scalar_one_or_none()

        if existing_material:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un material registrado con el nombre '{material_data.name}'."
            )

        # Si no existe, lo creamos mapeando los datos del esquema Pydantic al modelo SQLAlchemy
        db_material = Material(
            name=material_data.name,
            description=material_data.description,
            unit_of_measure=material_data.unit_of_measure,
            category=material_data.category
        )
        
        db.add(db_material)
        db.commit() # Guardamos en la base de datos
        db.refresh(db_material) # Refrescamos para obtener el ID generado
        return db_material

    @staticmethod
    def get_materials(db: Session, search: str = None, category: str = None):
        """
        RF-MAT-02: Listar todos los materiales con opción de búsqueda 
        por nombre o filtro por categoría.
        """
        query = select(Material)

        # Si el usuario escribe algo en el buscador, filtramos por nombre (ignorando mayúsculas/minúsculas)
        if search:
            query = query.where(Material.name.ilike(f"%{search}%"))
        
        # Si el usuario selecciona una categoría, filtramos por ella
        if category:
            query = query.where(Material.category == category)

        result = db.execute(query)
        return result.scalars().all()