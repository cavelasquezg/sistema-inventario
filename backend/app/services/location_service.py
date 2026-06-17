from sqlalchemy.orm import Session
from app.models.models import Location
from app.schemas.schemas import LocationCreate

class LocationService:

    @staticmethod
    def create_location(db: Session, location_data: LocationCreate):
        db_location = Location(
            name=location_data.name,
            type=location_data.type,
            description=location_data.description
        )
        db.add(db_location)
        db.commit()
        db.refresh(db_location)
        return db_location

    @staticmethod
    def get_locations(db: Session):
        return db.query(Location).all()
