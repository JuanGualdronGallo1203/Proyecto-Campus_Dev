from fastapi import APIRouter, HTTPException, status, FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from coworking_reservations.models.user import UserCreate, UserResponse, Token
from coworking_reservations.utils.security import (authenticate_user, create_access_token, get_password_hash)
from coworking_reservations.services.database import database


router = APIRouter()

@router.post("/register", response_model=UserResponse)
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

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
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
