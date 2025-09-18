# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime, timedelta

# Importar modelos
from models.user import UserCreate, UserResponse
from models.sede import SedeResponse
from models.room import RoomResponse, RoomWithResources
from models.reservation import ReservationCreate, ReservationResponse

# Importar utilidades y servicios
from utils.security import (
    get_password_hash, authenticate_user, create_access_token,
    get_current_user, get_current_active_user, get_current_admin_user
)
from services.database import database
from services.validation import validate_reservation

# Configuración de la aplicación FastAPI
app = FastAPI(
    title="Gestor de Reservas de Salas de Coworking",
    description="API para gestionar reservas de salas de coworking",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas de autenticación
@app.post("/auth/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    # Verificar si el usuario ya existe
    existing_user = database.get_by_field("users", "email", user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Crear usuario
    hashed_password = get_password_hash(user.contraseña)
    user_dict = user.dict()
    user_dict["contraseña_hash"] = hashed_password
    del user_dict["contraseña"]
    
    new_user = database.create("users", user_dict)
    return new_user

@app.post("/auth/login")
async def login_for_access_token(form_data: dict):
    user = authenticate_user(form_data["username"], form_data["password"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Ruta de prueba
@app.get("/")
async def root():
    return {"message": "Bienvenido al Gestor de Reservas de Salas de Coworking"}

# Información del usuario actual
@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_active_user)):
    return current_user

# Rutas para salas
@app.get("/rooms", response_model=List[RoomResponse])
async def get_rooms():
    return database.get_all("rooms")

@app.get("/rooms/{room_id}", response_model=RoomWithResources)
async def get_room(room_id: int):
    room = database.get_by_id("rooms", room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Obtener recursos de la sala
    room_resources = database.get_all_by_field("room_recursos", "room_id", room_id)
    resources = []
    for room_resource in room_resources:
        resource = database.get_by_id("recursos", room_resource["recurso_id"])
        if resource:
            resources.append({
                **resource,
                "cantidad": room_resource["cantidad"]
            })
    
    room["recursos"] = resources
    return room

# Rutas para reservas
@app.post("/reservations", response_model=ReservationResponse)
async def create_reservation(
    reservation: ReservationCreate,
    current_user: dict = Depends(get_current_active_user)
):
    # Validar la reserva
    validation_result = validate_reservation(reservation, current_user["id"])
    if not validation_result["valid"]:
        raise HTTPException(status_code=400, detail=validation_result["message"])
    
    # Crear la reserva
    reservation_dict = reservation.dict()
    reservation_dict["usuario_id"] = current_user["id"]
    reservation_dict["estado"] = "confirmada"
    
    new_reservation = database.create("reservations", reservation_dict)
    return new_reservation

@app.get("/reservations/me", response_model=List[ReservationResponse])
async def get_my_reservations(current_user: dict = Depends(get_current_active_user)):
    return database.get_all_by_field("reservations", "usuario_id", current_user["id"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)