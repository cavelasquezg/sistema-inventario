from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.schemas import StockMovementCreate, StockMovementResponse
from app.services.stock_service import StockService

router = APIRouter(
    prefix="/stock",
    tags=["Kárdex / Movimientos"]
)

@router.post("/movements", response_model=StockMovementResponse, status_code=status.HTTP_201_CREATED)
def create_movement(movement: StockMovementCreate, db: Session = Depends(get_db)):
    return StockService.create_movement(db=db, movement_data=movement)

@router.get("/movements", response_model=List[StockMovementResponse])
def read_movements(db: Session = Depends(get_db)):
    return StockService.get_movements(db=db)


@router.get("/current-stock", tags=["Kárdex / Movimientos"])
def get_stock(material_id: int, location_id: int, db: Session = Depends(get_db)):
    stock_actual = StockService.get_current_stock(
        db=db, material_id=material_id, location_id=location_id
    )
    return {
        "material_id": material_id,
        "location_id": location_id,
        "current_stock": stock_actual
    }
