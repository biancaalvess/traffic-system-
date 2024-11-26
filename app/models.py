from sqlalchemy import Colum, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Company(Base):
    __tablename__ = "companies"
    id = Colum(Integer, primary_key = True, index = True)
    name = Colum(String, unique = True, index = True)
    email = Colum(String, unique = True, index = True)
    password = Colum(String)
    vehicles = relationship("Vehicles", back_populates = "company")
    
class vehicle(Base):
    __tablename__ = "vehicles"
    id = Colum(Integer, primary_key = True, index = True)
    license_plate = Colum(String, unique = True, index = True)
    pin_hash = Colum(String)
    company_id = Colum(Integer, ForeignKey("companies.id"))
    logs = relationship("TrafficLog", back_populates= "vehicles")
    company = relationship("Company", back_populates= "vehicle")
    
class TrafficLog(Base):
    __tablename__: "traffic_logs"
    id = Colum(Integer, primary_key = True, index = True)
    vehicle_id = Colum(Integer, ForeignKey("vehicle.id"))
    date_time = Colum(DateTime)
    origin = Colum(String)
    destination = Colum(String)
    status = Colum(String)
    vehicle = relationship("Vehicle", back_populates= "logs")
    