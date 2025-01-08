from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import settings


# 데이터베이스 엔진 생성
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# 세션 생성
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# 데이터베이스 초기화
async def init_db():
    from models.base import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# 종속성: 세션 제공
async def get_db():
    async with async_session() as session:
        yield session
