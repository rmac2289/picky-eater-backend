from sqlalchemy.orm import registry
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship

mapper_registry = registry()

Base = mapper_registry.generate_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    food_logs = relationship("FoodLog", back_populates="user", foreign_keys="FoodLog.user_id")
    safe_foods = relationship("SafeFood", back_populates="user", foreign_keys="SafeFood.user_id")

class FoodLog(Base):
    __tablename__ = "food_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    food = Column(String(100), nullable=False)
    reaction = Column(String(20), nullable=False)
    meal_type = Column(String(20), nullable=False)
    notes = Column(Text)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="food_logs")

class SafeFood(Base):
    __tablename__ = "safe_foods"
    
    id = Column(Integer, primary_key=True, index=True)
    food = Column(String(100), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="safe_foods")

mapper_registry.configure()