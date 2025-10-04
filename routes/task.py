from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime

from database.db_setup import get_db
from models.user import UserDB
from models.category import CategoryDB
from models.task import TaskDB
from schemas.task import TaskCreate, TaskResponse, TaskUpdate, TaskStatus
from auth.auth_service import get_current_user


router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("", response_model=list[TaskResponse])
async def read_tasks(
    status: TaskStatus | None = None,
    category_name: str | None = None,
    due_date: datetime | None = None,
    db: Session = Depends(get_db), 
    current_user: UserDB = Depends(get_current_user)):

    query = db.query(TaskDB).filter(TaskDB.user_id == current_user.id)

    if status:
        query = query.filter(TaskDB.status == status)
    if category_name:
        query = query.join(CategoryDB).filter(CategoryDB.name == category_name)
    if due_date:
        query = query.filter(TaskDB.due_date == due_date)

    tasks = query.all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
async def read_task(task_id: int, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id, TaskDB.user_id == current_user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("", response_model=TaskCreate)
async def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):

    if task.category_id:
        category = db.query(CategoryDB).filter(CategoryDB.id == task.category_id, CategoryDB.user_id == current_user.id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Category not found")

    new_task = TaskDB(**task.model_dump(), user_id=current_user.id)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.put("/{task_id}", response_model=TaskUpdate)
async def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id, TaskDB.user_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.category_id:
        category = db.query(CategoryDB).filter(CategoryDB.id == task.category_id, CategoryDB.user_id == current_user.id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Category not found")
        db_task.category_id = task.category_id
      
    if task.status is not None:
        db_task.status = task.status
    if task.due_date is not None:
        db_task.due_date = task.due_date
    
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/{task_id}", response_model=TaskResponse)
async def delete_task(task_id: int, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id, TaskDB.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return task

@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(task_id: int, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id, TaskDB.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = TaskStatus.COMPLETED
    db.commit()
    db.refresh(task)
    return task