# models/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    nombre: str
    email: EmailStr
    rol: str = "user"

class UserCreate(UserBase):
    contraseña: str

class UserResponse(UserBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserInDB(UserResponse):
    contraseña_hash: str