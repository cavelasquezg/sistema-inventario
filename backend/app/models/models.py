from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    unit_of_measure = Column(String(20), nullable=False)
    category = Column(String(50), nullable=False)

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    type = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

# --- NUEVO MODELO DE MOVIMIENTOS DE STOCK (KÁRDEX) ---
class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    quantity = Column(Integer, nullable=False) # Cantidad movida (siempre positiva)
    movement_type = Column(String(20), nullable=False) # 'INPUT' (Entrada) o 'OUTPUT' (Salida)
    description = Column(Text, nullable=True) # Ej: "Compra según factura 123" o "Instalación cliente X"
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # Fecha/Hora automática
