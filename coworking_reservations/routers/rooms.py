
# routers/rooms.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from coworking_reservations.models.room import RoomResponse, RoomWithResources
from coworking_reservations.services.database import database
from coworking_reservations.models.room import RoomCreate
from coworking_reservations.utils.security import get_current_admin_user

router = APIRouter()

@router.get("/", response_model=List[RoomResponse])
async def get_rooms():
    return database.get_all("rooms")

@router.post("/", response_model=RoomResponse)
async def create_room(room: RoomCreate, current_user: dict = Depends(get_current_admin_user)):
    """Crear sala (solo admin)"""
    room_data = room.dict()
    return database.create("rooms", room_data)

@router.put("/{room_id}", response_model=RoomResponse)
async def update_room(room_id: int, room: RoomCreate, current_user: dict = Depends(get_current_admin_user)):
    """Actualizar sala (solo admin)"""
    room_data = room.dict()
    return database.update("rooms", room_id, room_data)

@router.delete("/{room_id}")
async def delete_room(room_id: int, current_user: dict = Depends(get_current_admin_user)):
    """Eliminar sala (solo admin)"""
    if not database.delete("rooms", room_id):
        raise HTTPException(status_code=404, detail="Room not found")
    return {"message": "Room deleted successfully"}