
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from auth.auth_service import authenticate_user, get_current_user
from auth.auth_utils import create_access_token, get_password_hash
from schemas.token import Token
from models.user import UserDB
from schemas.user import UserLogin
from datetime import timedelta

from database.db_setup import get_db
from schemas.user import UserCreate, UserResponse


router = APIRouter(prefix="", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check email
    email = db.query(UserDB).filter(UserDB.email == user.email).first()
    if email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    hashed_password = get_password_hash(user.password)
    db_user = UserDB(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    authenticated_user = await authenticate_user(db, user.username, user.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": authenticated_user.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserDB = Depends(get_current_user)):
    return current_user