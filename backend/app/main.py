from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import materials  # Importamos el router que creaste hace un momento

# Inicializamos la aplicación FastAPI con un título y versión profesionales
app = FastAPI(
    title="Sistema de Gestión de Inventario",
    description="API Backend para el control de materiales, ubicaciones y órdenes de movimiento.",
    version="1.0.0"
)

# Configuración de CORS (Seguridad)
# RNF-06: Permitir que tu frontend (que estará en otra URL) pueda hacer consultas al backend
origins = [
    "http://localhost:3000",      # URL típica de desarrollo para React/Next.js
    "http://127.0.0.1:3000",
    # Más adelante agregaremos aquí la URL real de producción de tu frontend en Vercel
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos: GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Permite todos los encabezados
)

# Registrar las rutas del sistema
# Todo lo relacionado con materiales ahora empezará con /api/v1/materials
app.include_router(materials.router, prefix="/api/v1")

# Ruta de prueba de salud del sistema (Health Check)
@app.get("/", tags=["General"])
def read_root():
    return {
        "status": "online",
        "message": "Bienvenido al Sistema de Gestión de Inventario API"
    }