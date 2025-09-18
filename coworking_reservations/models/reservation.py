# models/reservation.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date, time

class ReservationBase(BaseModel):
    room_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(ReservationBase):
    id: int
    usuario_id: int
    estado: str = "pendiente"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True