from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date
from enum import Enum

class Reaction(str, Enum):
   accepted = "accepted"
   rejected = "rejected"
   tried = "tried"

class MealType(str, Enum):
   breakfast = "breakfast"
   lunch = "lunch"
   dinner = "dinner"
   snack = "snack"

class FoodLogBase(BaseModel):
   food: str
   reaction: Reaction
   meal_type: MealType
   notes: Optional[str] = None
   date: date

class FoodLogCreate(FoodLogBase):
   user_id: int

class FoodLog(FoodLogBase):
   id: int
   class Config:
       orm_mode = True

class SafeFoodBase(BaseModel):
   food: str

class SafeFoodCreate(SafeFoodBase):
   user_id: int

class SafeFood(SafeFoodBase):
   id: int
   class Config:
       orm_mode = True

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True