from pydantic import BaseModel, Field

class CategoryCreate(BaseModel):
    name: str = Field(description="Task category name", min_length=1, max_length=100)

class CategoryResponse(BaseModel):
    id: int
    name: str
    