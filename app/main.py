from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .db.database import engine, Base
from .frontend.routes import home, about, login, registration
from .api.v1.endpoints import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Контекстный менеджер для управления жизненным циклом приложения"""
    # Стартовые действия (аналог startup)

    print("Создание таблиц в БД...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield  # Здесь приложение работает

    # Действия при завершении (аналог shutdown)
    print("Закрытие соединений с БД...")
    await engine.dispose()


app = FastAPI(
    title="РИА-Энерго",
    lifespan=lifespan
)

# Подключение роутеров
app.include_router(home.router)
app.include_router(about.router)
app.include_router(registration.router)
app.include_router(login.router)

app.include_router(auth.router)

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="app/static"), name="static")