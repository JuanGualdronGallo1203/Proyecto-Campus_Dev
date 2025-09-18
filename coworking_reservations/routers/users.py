from fastapi import APIRouter, Depends, FastAPI, HTTPException
from coworking_reservations.models.user import UserResponse
from coworking_reservations.utils.security import get_current_active_user, get_current_admin_user
from coworking_reservations.services.database import database
from typing import List

router = APIRouter()

# Información del usuario actual
@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_active_user)):
    return current_user

@router.get("/", response_model=List[UserResponse])
async def get_all_users(current_user: dict = Depends(get_current_admin_user)):
    """Obtener todos los usuarios (solo admin)"""
    return database.get_all("users")

@router.delete("/{user_id}")
async def delete_user(user_id: int, current_user: dict = Depends(get_current_admin_user)):
    """Eliminar usuario (solo admin)"""
    if not database.delete("users", user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}