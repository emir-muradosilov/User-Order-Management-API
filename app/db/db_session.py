from models.models import Base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from db.base import AsyncConfigDB, ConfigDB
from sqlalchemy import create_engine


# Асинхронное подключение и создание сессии

async_dbconfig = AsyncConfigDB()

async_engine = create_async_engine(
    async_dbconfig.async_get_url(),
    echo = False,
    )

AsyncSessionLocal = async_sessionmaker[AsyncSession](async_engine, expire_on_commit=False)

async def async_get_db():
    async with AsyncSessionLocal() as session:
        yield session
        await session.close()

async def init_db():
    async with async_engine.begin() as conn:
    # Создаем все таблицы
        await conn.run_sync(Base.metadata.create_all)



# Стандартное подключение и создание сессии

db_config = ConfigDB()

engine = create_engine(
     db_config.get_url(),
     echo = False,
)


async def init_db():
    async with async_engine.begin() as conn:
    # Создаем все таблицы
        await conn.run_sync(Base.metadata.create_all)

        
# Создание фабрики сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


