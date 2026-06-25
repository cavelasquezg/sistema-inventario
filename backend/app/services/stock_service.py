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

        # --- VALIDACIÓN DE STOCK DISPONIBLE ANTES DE SACAR ---
        if movement_data.movement_type.upper() == "OUTPUT":
            current_stock = StockService.get_current_stock(
                db, movement_data.material_id, movement_data.location_id
            )
            if current_stock < movement_data.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuficiente. Stock actual: {current_stock}, intentas sacar: {movement_data.quantity}"
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

# --- NUEVO MÉTODO PARA CALCULAR EL STOCK ACTUAL ---
    @staticmethod
    def get_current_stock(db: Session, material_id: int, location_id: int) -> int:
        # 1. Sumar todas las entradas (INPUT)
        inputs = db.query(StockMovement).filter(
            StockMovement.material_id == material_id,
            StockMovement.location_id == location_id,
            StockMovement.movement_type == "INPUT"
        ).all()
        total_inputs = sum(m.quantity for m in inputs)

        # 2. Sumar todas las salidas (OUTPUT)
        outputs = db.query(StockMovement).filter(
            StockMovement.material_id == material_id,
            StockMovement.location_id == location_id,
            StockMovement.movement_type == "OUTPUT"
        ).all()
        total_outputs = sum(m.quantity for m in outputs)

        # 3. El saldo neto es la resta
        return total_inputs - total_outputs
