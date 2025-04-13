import logging

from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine


#Лучше использовать миграции через алембик, но в тз не упоминяется


async def safe_create_tables(engine: AsyncEngine):
    """Безопасное создание таблиц с обработкой ошибок"""
    try:
        async with engine.begin() as conn:
            inspector = await conn.run_sync(lambda sync_conn: inspect(sync_conn))
            existing_tables = await conn.run_sync(lambda sync_conn: inspector.get_table_names())

            if 'users' not in existing_tables:
                await conn.run_sync(metadata.create_all)
                logging.info("Таблицы созданы успешно")
                return True
            logging.debug("Таблицы уже существуют")
            return False
    except SQLAlchemyError as e:
        logging.error(f"Ошибка при создании таблиц: {e}")
        raise

metadata = MetaData()
users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String),
    Column('last_updated', DateTime)
)