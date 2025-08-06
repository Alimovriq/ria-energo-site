# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.endpoints import main


app = FastAPI(title="РИА-Энерго")

# Роутеры
app.include_router(main.router)

# Статика
app.mount("/static", StaticFiles(directory="app/static"), name="static")