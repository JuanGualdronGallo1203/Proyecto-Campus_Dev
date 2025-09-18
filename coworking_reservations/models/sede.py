# models/sede.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SedeBase(BaseModel):
    nombre: str
    ciudad: str
    direccion: Optional[str] = None

class SedeCreate(SedeBase):
    pass

class SedeResponse(SedeBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True