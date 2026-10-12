from sqlalchemy.orm import Session
import models, schemas

# Get User by ID
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Get User by Email (Unique check panna udhavum)
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Get All Users (Bonus filtering logic udan)
def get_users(db: Session, city: str = None, is_active: bool = None):
    query = db.query(models.User)
    if city:
        query = query.filter(models.User.city.ilike(city))
    if is_active is not None:
        query = query.filter(models.User.is_active == is_active)
    return query.all()

# Create User
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
        age=user.age,
        city=user.city,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Update User
def update_user(db: Session, user_id: int, user_data: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.name = user_data.name
        db_user.email = user_data.email
        db_user.age = user_data.age
        db_user.city = user_data.city
        db_user.is_active = user_data.is_active
        db.commit()
        db.refresh(db_user)
    return db_user

# Delete User
def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
