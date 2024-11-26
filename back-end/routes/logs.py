from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import TrafficLog, Vehicle
from app.utils import verify_pin

router = APIRouter()

@router.post("/register")
def register_log(
    license_plate: str,
    pin: str,
    origin: str,
    destination: str,
    status: str,
    db: Session = Depends(get_db)
):
    vehicle = db.query(Vehicle).filter(Vehicle.license_plate == license_plate).first()
    if not vehicle or not verify_pin(pin, vehicle.pin_hash):
        raise HTTPException(status_code=401, detail="Placa ou PIN inválidos.")
    new_log = TrafficLog(
        vehicle_id=vehicle.id,
        date_time=datetime.utcnow(),
        origin=origin,
        destination=destination,
        status=status
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return {"message": "Movimentação registrada com sucesso!"}

@router.get("/")
def list_logs(license_plate: str, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.license_plate == license_plate).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")
    return db.query(TrafficLog).filter(TrafficLog.vehicle_id == vehicle.id).all()
