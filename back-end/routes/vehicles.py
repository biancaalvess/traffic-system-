from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Vehicle, Company
from app.utlils import hash_pin
from fastapi.security import OAuth2AuthorizationCodeBearer
import sys
import os

sys.path.append(os.path.abspath(os.join(os.path.dirname(__file__), "../../")))

router = APIRouter()
oauth2_sheme = OAuth2AuthorizationCodeBearer(tokenUrl="auth/login")


def get_current_company(token: str = Depends(oauth2_sheme), db: Session = Depends(get_db)):
    from jwt import decode
    from app.utlils import SECRET_KEY, ALGORITHM
    payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Token Inválido")
    company = db.query(Company).filter(Company.email == email). first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    return company

@router.post("/register")
def register_vehicle(license_plate: str, pin: str, db: Session = Depends(get_db), company: Company = Depends(get_current_company)):
    if db.query(Vehicle).filter(Vehicle.license_plate == license_plate).first():
        raise HTTPException(status_code=400, detail="Veículo já cadastrado.")
    hashed_pin = hash_pin(pin)
    new_vehicle = Vehicle(license_plate=license_plate, pin_hash=hashed_pin, company_id=company.id)
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return {"message": "Veículo registrado com sucesso!"}

@router.get("/")
def list_vehicles(db: Session = Depends(get_db), company: Company = Depends(get_current_company)):
    return db.query(Vehicle).filter(Vehicle.company_id == company.id).all()