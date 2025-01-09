import requests
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
import asyncio
from config import settings
from core.db import init_db, get_db
from fastapi import Depends
from models.n8n import N8NTaskCreate, N8NTaskRead, N8NTask
from services.n8n.repository import N8NTaskRepository, N8NTaskResultRepository
from services.work.onnx2trt import ONNX2TRTTaskRunner


class N8NTaskExecutionService:

    def __init__(self):
        self.engine = create_async_engine(settings.DATABASE_URL, echo=False)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            class_=AsyncSession,
        )

    async def on_schedule_triggered(self):
        async with self.SessionLocal() as session:
            try:
                # 작업 목록 가져오기
                task_orms: list[N8NTask] = await N8NTaskRepository.get_all_tasks(
                    session
                )
                tasks: list[N8NTaskRead] = [N8NTaskRead.from_orm(t) for t in task_orms]
                print(f"Fetched {len(tasks)} tasks.")
            except Exception as e:
                return
            for task in tasks:
                result = None
                status = False
                try:
                    result = str(await self.execute_task(task))
                    status = True
                except Exception as e:
                    result = str(e)
                    raise
                finally:
                    await N8NTaskResultRepository.create_result(
                        task_id=task.id,
                        task_labels=task.labels,
                        task_type=task.task_type,
                        task_params=task.params,
                        status=status,
                        result=result,
                        db=session,
                    )
                    await N8NTaskRepository.delete_task(task_id=task.id, db=session)

    async def execute_task(self, task: N8NTaskRead):
        print(
            f"Executing task[id:{task.id}, type:{task.task_type}, labels:{task.labels}] with {task.params}"
        )
        runner_map = {
            "onnx2trt": ONNX2TRTTaskRunner,
        }
        if task.task_type not in runner_map.keys():
            if task.task_type == "test":
                return "Test task completed"
            raise Exception(f"No runner found for task type: {task.task_type}")
        runner = runner_map[task.task_type](task)
        return await asyncio.to_thread(runner.execute)


task_excuter = N8NTaskExecutionService()
