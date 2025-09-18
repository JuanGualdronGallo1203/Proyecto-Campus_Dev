#main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from coworking_reservations.routers import auth, users, rooms, reservations
from coworking_reservations.services.database import init_default_admin


# Configuración del lifespan para inicialización
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializar datos al iniciar la aplicación
    init_default_admin()
    print("✅ Base de datos inicializada")
    yield
    # Código de limpieza al cerrar la aplicación
    print("🔄 Cerrando aplicación...")


# Configuración de la aplicación FastAPI
app = FastAPI(
    title="Gestor de Reservas de Salas de Coworking",
    description="API para gestionar reservas de salas de coworking",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Importacion de routers
app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
app.include_router(users.router, prefix="/users", tags=["Usuarios"])
app.include_router(rooms.router, prefix="/rooms", tags=["Salas"])
app.include_router(reservations.router, prefix="/reservations", tags=["Reservas"])



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)