from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from aiogram import BaseMiddleware
from src.models.user_base import User_base
from src.config import POSTGRES_URL
import logging

# Инициализация асинхронного движка для PostgreSQL
engine = create_async_engine(
    POSTGRES_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

# Создание фабрики сессий
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_user(self, user: User_base):
        """Сохраняет или обновляет пользователя в PostgreSQL"""
        try:
            logging.info("Saving user in PostgreSQL...")
            stmt = """
            INSERT INTO users (id, name, email, last_updated)
            VALUES (:id, :name, :email, :last_updated)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                email = EXCLUDED.email,
                last_updated = EXCLUDED.last_updated
            """
            await self.session.execute(stmt, user.dict())
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            logging.error(f"Error saving user: {e}")
            raise
