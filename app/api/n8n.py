from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from models.n8n import *
from services.n8n.repository import N8NTaskRepository

# 라우터 생성
router = APIRouter(prefix="/n8n")


@router.post("/", response_model=N8NTaskRead)
async def create_task_api(task: N8NTaskCreate, db: AsyncSession = Depends(get_db)):
    return await N8NTaskRepository.create_task(task, db)


# Read - 모든 작업 조회
@router.get("/", response_model=list[N8NTaskRead])
async def get_all_tasks_api(db: AsyncSession = Depends(get_db)):
    return await N8NTaskRepository.get_all_tasks(db)


# Read - 특정 작업 조회
@router.get("/{task_id}", response_model=N8NTaskRead)
async def get_task_api(task_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await N8NTaskRepository.get_task(task_id, db)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Task not found.")


# Update - 특정 작업 업데이트
@router.put("/{task_id}", response_model=N8NTaskRead)
async def update_task_api(
    task_id: int, updated_task: N8NTaskCreate, db: AsyncSession = Depends(get_db)
):
    try:
        return await N8NTaskRepository.update_task(task_id, updated_task, db)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Task not found")


# Delete - 특정 작업 삭제
@router.delete("/{task_id}", response_model=dict)
async def delete_task_api(task_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await N8NTaskRepository.delete_task(task_id, db)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Task not found")
