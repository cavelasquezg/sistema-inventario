from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    unit_of_measure = Column(String(20), nullable=False) # Ej: Unidades, Metros, Global
    category = Column(String(50), nullable=False)        # Ej: Cableado, Herramientas

    # --- NUEVO MODELO DE UBICACIONES ---
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True) # Ej: Bodega Norte, Estante A
    type = Column(String(50), nullable=False)        # Ej: Principal, Vehículo, Estante
    description = Column(Text, nullable=True)         # Ej: Pasillo 2, Casillero 5
