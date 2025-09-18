# routers/reservations.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from coworking_reservations.models.reservation import ReservationCreate, ReservationResponse
from coworking_reservations.utils.security import get_current_active_user
from coworking_reservations.services.database import database
from coworking_reservations.services.validation import validate_reservation
from datetime import date

router = APIRouter()

@router.post("/", response_model=ReservationResponse)
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

@router.get("/me", response_model=List[ReservationResponse])
async def get_my_reservations(current_user: dict = Depends(get_current_active_user)):
    return database.get_all_by_field("reservations", "usuario_id", current_user["id"])

@router.get("/room/{room_id}", response_model=List[ReservationResponse])
async def get_reservations_by_room(room_id: int, current_user: dict = Depends(get_current_active_user)):
    """Obtener reservas por sala"""
    room = database.get_by_id("rooms", room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return database.get_all_by_field("reservations", "room_id", room_id)

@router.get("/date/{reservation_date}", response_model=List[ReservationResponse])
async def get_reservations_by_date(reservation_date: date, current_user: dict = Depends(get_current_active_user)):
    """Obtener reservas por fecha"""
    # Convertir date a string para comparar con la base de datos
    date_str = reservation_date.isoformat()
    all_reservations = database.get_all("reservations")
    
    # Filtrar reservas por fecha
    reservations_on_date = [
        reservation for reservation in all_reservations 
        if reservation.get("fecha") == date_str
    ]
    
    return reservations_on_date

@router.delete("/{reservation_id}")
async def cancel_reservation(reservation_id: int, current_user: dict = Depends(get_current_active_user)):
    """Cancelar reserva (solo el usuario dueño o admin)"""
    reservation = database.get_by_id("reservations", reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    # Verificar que el usuario es el dueño de la reserva o es admin
    if reservation["usuario_id"] != current_user["id"] and current_user["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to cancel this reservation")
    
    # Actualizar estado a cancelada
    database.update("reservations", reservation_id, {"estado": "cancelada"})
    
    return {"message": "Reservation cancelled successfully"}