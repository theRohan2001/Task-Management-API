from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from database.db_setup import get_db
from models.user import UserDB
from models.category import CategoryDB
from schemas.category import CategoryResponse, CategoryCreate
from auth.auth_service import get_current_user


router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    existing = db.query(CategoryDB).filter(CategoryDB.name == category.name, CategoryDB.user_id == current_user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    

    new_category = CategoryDB(**category.model_dump(), user_id=current_user.id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("", response_model=list[CategoryResponse])
async def read_categories(db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    categories = db.query(CategoryDB).filter(CategoryDB.user_id == current_user.id).all()
    return categories   