from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio

scheduler = AsyncIOScheduler()


# 데코레이터 정의
def interval_scheduling(*args, **kwargs):
    trigger = IntervalTrigger(*args, **kwargs)

    def decorator(func):
        scheduler.add_job(func, trigger)
        return func

    return decorator
