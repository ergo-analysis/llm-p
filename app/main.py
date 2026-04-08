from fastapi import FastAPI
from app.api.routes_auth import router as auth_router
from app.api.routes_chat import router as chat_router
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Создает таблицы при запуске"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

def create_app() -> FastAPI:
    """Фабрика приложения FastAPI"""
    app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
    app.include_router(auth_router)
    app.include_router(chat_router)
    
    @app.get("/health")
    async def health():
        """Пингует сервер, проверяет работоспособность"""
        return {"status": "ok", "env": settings.ENV}
    
    return app

app = create_app()
