# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
import json
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from typing import Optional

# Configuración de seguridad
SECRET_KEY = "tu_clave_secreta_super_segura_aqui_cambiar_en_produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Modelos Pydantic
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str = "user"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class UserInDB(UserResponse):
    password_hash: str

class RoomBase(BaseModel):
    name: str
    location: str
    capacity: int
    resources: List[str] = []

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int
    
    class Config:
        from_attributes = True

class ReservationBase(BaseModel):
    room_id: int
    date: str  # formato YYYY-MM-DD
    start_time: str  # formato HH:MM
    end_time: str  # formato HH:MM

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(ReservationBase):
    id: int
    user_id: int
    status: str = "confirmed"
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

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

# Servicio de base de datos JSON
class JSONDatabase:
    def __init__(self, file_path: str = "data/database.json"):
        self.file_path = file_path
        self._ensure_file_exists()
        
    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            # Datos iniciales con un usuario admin por defecto
            initial_data = {
                "users": [
                    {
                        "id": 1,
                        "name": "Administrador",
                        "email": "admin@example.com",
                        "password_hash": pwd_context.hash("admin123"),
                        "role": "admin"
                    }
                ],
                "rooms": [],
                "reservations": []
            }
            with open(self.file_path, 'w') as f:
                json.dump(initial_data, f, indent=2)
    
    def _read_data(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)
    
    def _write_data(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_all(self, collection: str):
        data = self._read_data()
        return data.get(collection, [])
    
    def get_by_id(self, collection: str, item_id: int):
        data = self._read_data()
        items = data.get(collection, [])
        for item in items:
            if item.get("id") == item_id:
                return item
        return None
    
    def get_by_field(self, collection: str, field: str, value):
        data = self._read_data()
        items = data.get(collection, [])
        for item in items:
            if item.get(field) == value:
                return item
        return None
    
    def create(self, collection: str, item: dict):
        data = self._read_data()
        items = data.get(collection, [])
        
        # Generar ID
        new_id = max([item.get("id", 0) for item in items] or [0]) + 1
        item["id"] = new_id
        
        items.append(item)
        data[collection] = items
        self._write_data(data)
        
        return item
    
    def update(self, collection: str, item_id: int, updates: dict):
        data = self._read_data()
        items = data.get(collection, [])
        
        for i, item in enumerate(items):
            if item.get("id") == item_id:
                items[i].update(updates)
                data[collection] = items
                self._write_data(data)
                return items[i]
        
        raise HTTPException(status_code=404, detail=f"{collection[:-1]} not found")
    
    def delete(self, collection: str, item_id: int):
        data = self._read_data()
        items = data.get(collection, [])
        
        for i, item in enumerate(items):
            if item.get("id") == item_id:
                del items[i]
                data[collection] = items
                self._write_data(data)
                return True
        
        return False

# Instancia global de la base de datos
database = JSONDatabase()

# Funciones de utilidad para autenticación
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_by_email(email: str):
    users = database.get_all("users")
    for user in users:
        if user["email"] == email:
            return user
    return None

def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user["password_hash"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    return current_user

async def get_current_admin_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

# Rutas de autenticación
@app.post("/auth/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    # Verificar si el usuario ya existe
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Crear usuario
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["password_hash"] = hashed_password
    del user_dict["password"]
    
    new_user = database.create("users", user_dict)
    return new_user

@app.post("/auth/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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
async def read_users_me(current_user: UserResponse = Depends(get_current_active_user)):
    return current_user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)