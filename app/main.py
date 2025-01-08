from fastapi import FastAPI
import traceback

from api import n8n
from config import settings
from core.db import init_db
from core.scheduler import scheduler, interval_scheduling
from services.n8n.excuter import task_excuter


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=settings.description,
    debug=settings.debug,
)


@app.on_event("startup")
async def on_startup():
    await init_db()
    scheduler.start()


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()


@interval_scheduling(seconds=5)
async def update():
    try:
        await task_excuter.on_schedule_triggered()
    except Exception as e:
        print(f"Error on schedule triggered: {e}")
        traceback.print_exc()  # 에러 발생 위치 출력


app.include_router(n8n.router)
