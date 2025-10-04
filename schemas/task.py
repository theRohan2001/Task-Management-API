from enum import Enum
from pydantic import BaseModel, Field
from datetime import timedelta, datetime


class TaskStatus(str, Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'


class TaskCreate(BaseModel):
    title: str = Field(description="Task title", min_length=1, max_length=100)
    due_date: datetime | None = None
    category_id: int | None = None



class TaskResponse(TaskCreate):
    id: int
    title: str
    status: TaskStatus 
    due_date : datetime | None = None
    created_at: datetime
    category_id: int | None = None


class TaskUpdate(BaseModel):
    status: TaskStatus | None = None
    due_date: datetime | None = None
    category_id: int | None = None