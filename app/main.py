from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from app.exceptions import NotFoundException, UserIdMismatchException
from app.security import create_access_token, get_current_user, get_password_hash, verify_password
from . import models, schemas, database

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create tables
models.Base.metadata.create_all(bind=database.engine)

@app.get("/foodlogs/", response_model=List[schemas.FoodLog])
def get_food_logs(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.FoodLog).filter(models.FoodLog.user_id == current_user.id).all()

@app.post("/foodlogs/", response_model=schemas.FoodLog)
def create_food_log(food_log: schemas.FoodLogCreate, 
                   db: Session = Depends(database.get_db), 
                   current_user: models.User = Depends(get_current_user)):
    if not current_user.id == food_log.user_id:
        raise UserIdMismatchException
    db_food_log = models.FoodLog(**food_log.model_dump())
    db.add(db_food_log)
    db.commit()
    db.refresh(db_food_log)
    return db_food_log

@app.delete("/foodlogs/{food_log_id}")
def delete_food_log(food_log_id: int, 
                   db: Session = Depends(database.get_db), 
                   current_user: models.User = Depends(get_current_user)):
    food_log = db.query(models.FoodLog).filter(
        models.FoodLog.id == food_log_id, 
        models.FoodLog.user_id == current_user.id
    ).first()
    if not food_log:
        raise NotFoundException
    db.delete(food_log)
    db.commit()
    return {"ok": True}

@app.post("/safefoods/", response_model=schemas.SafeFood)
def create_safe_food(safe_food: schemas.SafeFoodCreate, db: Session = Depends(database.get_db), 
                     current_user: models.User = Depends(get_current_user)):
   if not current_user.id == safe_food.user_id:
        raise UserIdMismatchException
   db_safe_food = models.SafeFood(**safe_food.model_dump())
   db.add(db_safe_food)
   db.commit()
   db.refresh(db_safe_food)
   return db_safe_food

@app.get("/safefoods/", response_model=List[schemas.SafeFood])
def get_safe_foods(db: Session = Depends(database.get_db)):
   return db.query(models.SafeFood).all()

@app.delete("/safefoods/{safe_food_id}")
def delete_food_log(safe_food_id: int, 
                   db: Session = Depends(database.get_db), 
                   current_user: models.User = Depends(get_current_user)):
    safe_food = db.query(models.SafeFood).filter(
        models.SafeFood.id == safe_food_id, 
        models.SafeFood.user_id == current_user.id
    ).first()
    if not safe_food:
        raise NotFoundException
    db.delete(safe_food)
    db.commit()
    return {"ok": True}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}