import requests
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from config import settings
from core.db import init_db, get_db
from fastapi import Depends
from models.n8n import N8NTaskCreate, N8NTaskRead, N8NTask, N8NTaskResult
from sqlalchemy.orm.exc import NoResultFound


class N8NTaskRepository:
    @staticmethod
    async def create_task(task: N8NTaskCreate, db: AsyncSession):
        new_task = N8NTask(**task.dict())
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        return new_task

    @staticmethod
    async def get_all_tasks(db: AsyncSession):
        result = await db.execute(select(N8NTask))
        tasks = result.scalars().all()
        if not tasks:
            raise NoResultFound("No tasks found.")
        return tasks

    @staticmethod
    async def get_task(task_id: int, db: AsyncSession):
        result = await db.execute(select(N8NTask).where(N8NTask.id == task_id))
        task = result.scalar_one()
        if not task:
            raise NoResultFound(f"Task with id {task_id} not found.")
        return task

    @staticmethod
    async def update_task(task_id: int, updated_task: N8NTaskCreate, db: AsyncSession):
        result = await db.execute(select(N8NTask).where(N8NTask.id == task_id))
        task = result.scalar_one()
        if not task:
            raise NoResultFound(f"Task with id {task_id} not found.")
        for key, value in updated_task.dict().items():
            setattr(task, key, value)
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def delete_task(task_id: int, db: AsyncSession):
        result = await db.execute(select(N8NTask).where(N8NTask.id == task_id))
        task = result.scalar_one()
        if not task:
            raise NoResultFound(f"Task with id {task_id} not found.")
        await db.delete(task)
        await db.commit()
        return {"message": "Task deleted successfully"}


class N8NTaskResultRepository:
    @staticmethod
    async def create_result(
        task_id: int,
        task_labels: list[str],
        task_type: str,
        task_params: dict,
        status: str,
        result: dict,
        db: AsyncSession,
    ):
        """
        작업 결과를 생성하여 저장합니다.
        """
        new_result = N8NTaskResult(
            task_id=task_id,
            task_labels=task_labels,
            task_type=task_type,
            task_params=task_params,
            status=status,
            result=result,
        )
        db.add(new_result)
        await db.commit()
        await db.refresh(new_result)
        return new_result

    @staticmethod
    async def get_result_by_id(result_id: int, db: AsyncSession):
        """
        특정 결과 ID로 작업 결과를 조회합니다.
        """
        result = await db.execute(
            select(N8NTaskResult).where(N8NTaskResult.id == result_id)
        )
        result_instance = result.scalar_one_or_none()
        if result_instance is None:
            raise NoResultFound(f"Result with id {result_id} not found.")
        return result_instance

    @staticmethod
    async def get_results_by_task_id(task_id: int, db: AsyncSession):
        """
        특정 작업 ID와 관련된 모든 결과를 조회합니다.
        """
        result = await db.execute(
            select(N8NTaskResult).where(N8NTaskResult.task_id == task_id)
        )
        return result.scalars().all()

    @staticmethod
    async def delete_result_by_id(result_id: int, db: AsyncSession):
        """
        특정 결과 ID로 작업 결과를 삭제합니다.
        """
        result = await db.execute(
            select(N8NTaskResult).where(N8NTaskResult.id == result_id)
        )
        result_instance = result.scalar_one_or_none()
        if result_instance is None:
            raise NoResultFound(f"Result with id {result_id} not found.")
        await db.delete(result_instance)
        await db.commit()
        return {"message": "Result deleted successfully"}

    @staticmethod
    async def get_all_results(db: AsyncSession):
        """
        모든 작업 결과를 조회합니다.
        """
        result = await db.execute(select(N8NTaskResult))
        return result.scalars().all()
