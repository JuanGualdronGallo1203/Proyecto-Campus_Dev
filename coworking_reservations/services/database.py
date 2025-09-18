# services/database.py
import json
import os
from typing import Dict, List, Any, Optional
from fastapi import HTTPException
from datetime import datetime, date, time


class JSONDatabase:
    def __init__(self, file_path: str = "data/database.json"):
        self.file_path = os.path.abspath(file_path)
        self._ensure_file_exists()
        
    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            # Crear estructura inicial basada en tu esquema
            initial_data = {
                "users": [
                    {
                        "id": 1,
                        "nombre": "Administrador",
                        "email": "admin@coworking.com",
                        "contraseña_hash": "",
                        "rol": "admin",
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    },
                    {
                        "id": 2,
                        "nombre": "Juan Pérez",
                        "email": "juan@email.com",
                        "nombre": "Juan Pérez",
                        "email": "juan@email.com",
                        "contraseña_hash": "",
                        "rol": "user",
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    }
                ],
                "sedes": [
                    {
                        "id": 1,
                        "nombre": "Bogotá Norte",
                        "ciudad": "Bogotá",
                        "direccion": "Calle 100 # 15-20",
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    },
                    {
                        "id": 2,
                        "nombre": "Bogotá Centro",
                        "ciudad": "Bogotá",
                        "direccion": "Carrera 7 # 22-45",
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    },
                    {
                        "id": 3,
                        "nombre": "Medellín Poblado",
                        "ciudad": "Medellín",
                        "direccion": "Carrera 43A # 6-50",
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    },
                    {
                        "id": 4,
                        "nombre": "Cali Granada",
                        "ciudad": "Cali",
                        "direccion": "Avenida 4N # 15-30",
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    }
                ],
                "recursos": [
                    {
                        "id": 1,
                        "nombre": "proyector",
                        "descripcion": "Proyector HD con conectores HDMI y VGA",
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 2,
                        "nombre": "pizarra",
                        "descripcion": "Pizarra blanca con marcadores",
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 3,
                        "nombre": "aire_acondicionado",
                        "descripcion": "Sistema de aire acondicionado",
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 4,
                        "nombre": "wifi",
                        "descripcion": "Conexión WiFi de alta velocidad",
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 5,
                        "nombre": "impresora",
                        "descripcion": "Impresora láser multifuncional",
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 6,
                        "nombre": "telefono",
                        "descripcion": "Teléfono para conferencias",
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 7,
                        "nombre": "cafetera",
                        "descripcion": "Máquina de café automática",
                        "created_at": datetime.now().isoformat()
                    }
                ],
                "rooms": [
                    {
                        "id": 1,
                        "nombre": "Sala Ejecutiva A",
                        "sede_id": 1,
                        "capacidad": 10,
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    },
                    {
                        "id": 2,
                        "nombre": "Sala Reuniones B",
                        "sede_id": 1,
                        "capacidad": 6,
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    },
                    {
                        "id": 3,
                        "nombre": "Sala Conferencias C",
                        "sede_id": 2,
                        "capacidad": 20,
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    },
                    {
                        "id": 4,
                        "nombre": "Sala Creativa D",
                        "sede_id": 3,
                        "capacidad": 8,
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    },
                    {
                        "id": 5,
                        "nombre": "Sala Focus E",
                        "sede_id": 4,
                        "capacidad": 4,
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    }
                ],
                "room_recursos": [
                    {
                        "id": 1,
                        "room_id": 1,
                        "recurso_id": 1,
                        "cantidad": 1,
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 2,
                        "room_id": 1,
                        "recurso_id": 2,
                        "cantidad": 1,
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 3,
                        "room_id": 1,
                        "recurso_id": 3,
                        "cantidad": 1,
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 4,
                        "room_id": 1,
                        "recurso_id": 4,
                        "cantidad": 1,
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 5,
                        "room_id": 2,
                        "recurso_id": 2,
                        "cantidad": 1,
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 6,
                        "room_id": 2,
                        "recurso_id": 4,
                        "cantidad": 1,
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 7,
                        "room_id": 3,
                        "recurso_id": 1,
                        "cantidad": 2,
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 8,
                        "room_id": 3,
                        "recurso_id": 2,
                        "cantidad": 1,
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 9,
                        "room_id": 3,
                        "recurso_id": 3,
                        "cantidad": 1,
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 10,
                        "room_id": 3,
                        "recurso_id": 4,
                        "cantidad": 1,
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 11,
                        "room_id": 3,
                        "recurso_id": 5,
                        "cantidad": 1,
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 12,
                        "room_id": 4,
                        "recurso_id": 2,
                        "cantidad": 2,
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 13,
                        "room_id": 4,
                        "recurso_id": 4,
                        "cantidad": 1,
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 14,
                        "room_id": 4,
                        "recurso_id": 6,
                        "cantidad": 1,
                        "created_at": datetime.now().isoformat()
                    },
                    {
                        "id": 15,
                        "room_id": 5,
                        "recurso_id": 4,
                        "cantidad": 1,
                        "created_at": datetime.now().isoformat()
                    }
                ],
                "reservations": [],
                "penalizaciones": []
            }
            self._write_data(initial_data)
    
    def _read_data(self) -> Dict[str, List[Any]]:
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _convert_dates(self, obj):
        if isinstance(obj, (datetime, date, time)):
            return obj.isoformat()
        if isinstance(obj, dict):
            return {k: self._convert_dates(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._convert_dates(i) for i in obj]
        return obj

    def _write_data(self, data: Dict[str, List[Any]]):
        data = self._convert_dates(data)
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_all(self, collection: str) -> List[Any]:
        data = self._read_data()
        return data.get(collection, [])
    
    def get_by_id(self, collection: str, item_id: int) -> Optional[Any]:
        data = self._read_data()
        items = data.get(collection, [])
        for item in items:
            # Convertir item["id"] a int para comparación segura
            try:
                item_id_value = int(item.get("id"))
            except (ValueError, TypeError):
                continue
            if item_id_value == item_id:
                return item
        return None
    
    def get_by_field(self, collection: str, field: str, value: Any) -> Optional[Any]:
        data = self._read_data()
        items = data.get(collection, [])
        for item in items:
            if item.get(field) == value:
                return item
        return None
    
    def get_all_by_field(self, collection: str, field: str, value: Any) -> List[Any]:
        data = self._read_data()
        items = data.get(collection, [])
        return [item for item in items if item.get(field) == value]
    
    def create(self, collection: str, item: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read_data()
        items = data.get(collection, [])

        # Generar ID
        new_id = max([item.get("id", 0) for item in items] or [0]) + 1
        item["id"] = new_id

        # Agregar timestamps si no existen
        if "created_at" not in item:
            item["created_at"] = datetime.now().isoformat()
        if "updated_at" not in item and any(key in item for key in ["updated_at", "update_at"]):
            item["updated_at"] = datetime.now().isoformat()

        # Convertir objetos de fecha a strings antes de guardar
        item = self._convert_dates(item)

        items.append(item)
        data[collection] = items
        self._write_data(data)

        return item
    
    def update(self, collection: str, item_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read_data()
        items = data.get(collection, [])

        # Convertir objetos de fecha en updates a strings
        updates = self._convert_dates(updates)

        for i, item in enumerate(items):
            if item.get("id") == item_id:
                # Actualizar campos
                items[i].update(updates)
                # Actualizar timestamp de modificación
                if "updated_at" in items[i] or any(key in items[i] for key in ["updated_at", "update_at"]):
                    items[i]["updated_at"] = datetime.now().isoformat()

                data[collection] = items
                self._write_data(data)
                return items[i]

        raise HTTPException(status_code=404, detail=f"{collection[:-1]} not found")
    
    def delete(self, collection: str, item_id: int) -> bool:
        data = self._read_data()
        items = data.get(collection, [])
        
        for i, item in enumerate(items):
            if item.get("id") == item_id:
                del items[i]
                data[collection] = items
                self._write_data(data)
                return True
        
        return False
    
    # services/database.py (agregar esta función)
def init_default_admin():
    """Inicializa el usuario admin por defecto si no existe"""
    admin_user = database.get_by_field("users", "email", "admin@coworking.com")
    if not admin_user:
        from utils.security import get_password_hash
        admin_data = {
            "nombre": "Administrador",
            "email": "admin@coworking.com",
            "contraseña_hash": get_password_hash("admin123"),
            "rol": "admin"
        }
        database.create("users", admin_data)
        print("👤 Usuario admin creado por defecto")

# Instancia global de la base de datos
database = JSONDatabase()
