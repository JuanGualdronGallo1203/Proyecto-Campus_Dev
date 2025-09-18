# services/validation.py
from datetime import datetime, time, date
from coworking_reservations.services.database import database

def validate_reservation(reservation, user_id):
    # Verificar que la sala existe
    room = database.get_by_id("rooms", reservation.room_id)
    if not room:
        return {"valid": False, "message": "Room not found"}
    
    # Verificar que la fecha no es en el pasado
    if reservation.fecha < date.today():
        return {"valid": False, "message": "Cannot make reservations for past dates"}
    
    # Verificar que la hora de inicio es antes de la hora de fin
    if reservation.hora_inicio >= reservation.hora_fin:
        return {"valid": False, "message": "Start time must be before end time"}
    
    # Verificar que la reserva es en bloques de 1 hora
    start_minutes = reservation.hora_inicio.hour * 60 + reservation.hora_inicio.minute
    end_minutes = reservation.hora_fin.hour * 60 + reservation.hora_fin.minute
    duration_minutes = end_minutes - start_minutes
    
    if duration_minutes != 60:
        return {"valid": False, "message": "Reservations must be exactly 1 hour long"}
    
    # Verificar que no hay cruce de horarios
    existing_reservations = database.get_all_by_field("reservations", "room_id", reservation.room_id)
    existing_reservations = [r for r in existing_reservations if r["fecha"] == reservation.fecha.isoformat() and r["estado"] != "cancelada"]
    
    for existing in existing_reservations:
        existing_start = time.fromisoformat(existing["hora_inicio"])
        existing_end = time.fromisoformat(existing["hora_fin"])
        
        if (reservation.hora_inicio < existing_end and reservation.hora_fin > existing_start):
            return {"valid": False, "message": "Time slot already booked"}
    
    return {"valid": True, "message": "Reservation is valid"}