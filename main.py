from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

import models, schemas, crud
from database import engine, get_db

# Tables create pannum code
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Management API")

# 1. CREATE User
@app.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# 2. GET All Users (With Bonus Filters)
@app.get("/users", response_model=List[schemas.UserResponse])
def read_users(city: Optional[str] = None, is_active: Optional[bool] = None, db: Session = Depends(get_db)):
    return crud.get_users(db, city=city, is_active=is_active)

# 3. GET User by ID
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 4. UPDATE User
@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    # Email duplicate check for other users
    db_user_by_email = crud.get_user_by_email(db, email=user.email)
    if db_user_by_email and db_user_by_email.id != user_id:
        raise HTTPException(status_code=400, detail="Email already registered by another user")
        
    updated_user = crud.update_user(db=db, user_id=user_id, user_data=user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# 5. DELETE User
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None
