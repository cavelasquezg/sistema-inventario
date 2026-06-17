from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.schemas import LocationCreate, LocationResponse
from app.services.location_service import LocationService

router = APIRouter(
    prefix="/locations",
    tags=["Ubicaciones"]
)

@router.post("/", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    return LocationService.create_location(db=db, location_data=location)

@router.get("/", response_model=List[LocationResponse])
def read_locations(db: Session = Depends(get_db)):
    return LocationService.get_locations(db=db)
