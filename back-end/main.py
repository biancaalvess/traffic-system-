from fastapi import FastAPI
from app.database import engine, Base
from app.routes import auth, vehicles, logs

Base.metadata.creat_all(bind=engine)

app = FastAPI

app.incluide_router(auth.router, prefix="/auth", tags=['Auth'])
app.include_router(vehicles.router, prefix="/vehicles", tag=["Vehicles"])
app.include_router(logs.router, prefix="/logs", tags=["Logs"])


def read_root():
    return{"message": "Sisteema de Tráfego de Transporte Ativo!"}

