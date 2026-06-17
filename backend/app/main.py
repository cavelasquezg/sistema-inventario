from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import materials
from app.core.database import engine, Base  # <-- NUEVA IMPORTACIÓN
from app.models import models               # <-- NUEVA IMPORTACIÓN

# Ordenamos a SQLAlchemy que cree todas las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)       # <-- LÍNEA MÁGICA

app = FastAPI(
    title="Sistema de Gestión de Inventario",
    description="API Backend para el control de materiales, ubicaciones y órdenes de movimiento.",
    version="1.0.0"
)

# Configuración de CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(materials.router, prefix="/api/v1")

@app.get("/", tags=["General"])
def read_root():
    return {
        "status": "online",
        "message": "Bienvenido al Sistema de Gestión de Inventario API"
    }
