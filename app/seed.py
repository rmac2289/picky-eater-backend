from sqlalchemy.orm import Session
from app import models, database
from app.security import get_password_hash
from datetime import date

def seed_data(db: Session):
    # Create test user
    test_user = models.User(
        email="test@example.com",
        hashed_password=get_password_hash("password123")
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    # Create food logs
    food_logs = [
        {
            "food": "Carrots",
            "reaction": "tried",
            "meal_type": "lunch",
            "notes": "Ate two baby carrots",
            "date": date(2025, 1, 2),
            "user_id": test_user.id
        },
        {
            "food": "Mac and Cheese",
            "reaction": "accepted",
            "meal_type": "dinner",
            "notes": "Loved it!",
            "date": date(2024, 6, 4),
            "user_id": test_user.id
        },
        {
            "food": "Broccoli",
            "reaction": "rejected",
            "meal_type": "dinner",
            "notes": "Wouldn't try it",
            "date": date(2025, 1, 3),
            "user_id": test_user.id
        }
    ]

    for log in food_logs:
        db_log = models.FoodLog(**log)
        db.add(db_log)

    # Create safe foods
    safe_foods = ["Mac and Cheese", "Banana", "PB&J Sandwich", "Yogurt"]
    for food in safe_foods:
        db_safe_food = models.SafeFood(food=food, user_id=test_user.id)
        db.add(db_safe_food)

    db.commit()

if __name__ == "__main__":
    db = database.SessionLocal()
    try:
        seed_data(db)
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()