# models/room.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RoomBase(BaseModel):
    nombre: str
    sede_id: int
    capacidad: int

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class RoomWithResources(RoomResponse):
    recursos: List[dict] = []