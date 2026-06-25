from sqlalchemy.orm import Session
from app.models.models import StockMovement
from app.schemas.schemas import StockMovementCreate
from fastapi import HTTPException, status

class StockService:

    @staticmethod
    def create_movement(db: Session, movement_data: StockMovementCreate):
        # Validación simple de negocio: el tipo debe ser válido
        if movement_data.movement_type.upper() not in ["INPUT", "OUTPUT"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El tipo de movimiento debe ser 'INPUT' o 'OUTPUT'"
            )
        
        # Validación de cantidad positiva
        if movement_data.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La cantidad debe ser un número mayor a cero"
            )

        db_movement = StockMovement(
            material_id=movement_data.material_id,
            location_id=movement_data.location_id,
            quantity=movement_data.quantity,
            movement_type=movement_data.movement_type.upper(),
            description=movement_data.description
        )
        
        db.add(db_movement)
        db.commit()
        db.refresh(db_movement)
        return db_movement

    @staticmethod
    def get_movements(db: Session):
        return db.query(StockMovement).order_by(StockMovement.created_at.desc()).all()
