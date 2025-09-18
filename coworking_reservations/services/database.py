# services/database.py
import json
import os
from typing import Dict, List, Any
from fastapi import HTTPException

class JSONDatabase:
    def __init__(self, file_path: str = "data/database.json"):
        self.file_path = file_path
        self._ensure_file_exists()
        
    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({"users": [], "rooms": [], "reservations": []}, f)
    
    def _read_data(self) -> Dict[str, List[Any]]:
        with open(self.file_path, 'r') as f:
            return json.load(f)
    
    def _write_data(self, data: Dict[str, List[Any]]):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_all(self, collection: str) -> List[Any]:
        data = self._read_data()
        return data.get(collection, [])
    
    def get_by_id(self, collection: str, item_id: int) -> Any:
        data = self._read_data()
        items = data.get(collection, [])
        for item in items:
            if item.get("id") == item_id:
                return item
        return None
    
    def create(self, collection: str, item: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read_data()
        items = data.get(collection, [])
        
        # Generate ID
        new_id = max([item.get("id", 0) for item in items] or [0]) + 1
        item["id"] = new_id
        
        items.append(item)
        data[collection] = items
        self._write_data(data)
        
        return item
    
    def update(self, collection: str, item_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read_data()
        items = data.get(collection, [])
        
        for i, item in enumerate(items):
            if item.get("id") == item_id:
                items[i].update(updates)
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

# Global database instance
database = JSONDatabase()