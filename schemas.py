from pydantic import BaseModel, EmailStr, Field

# User create/update pannumpodu checking
class UserBase(BaseModel):
    name: str = Field(..., min_length=1, description="Name is required")
    email: EmailStr # Automatica valid email ah nu check pannum
    age: int = Field(..., ge=18, le=60, description="Age must be between 18 and 60")
    city: str = Field(..., min_length=1, description="City is required")
    is_active: bool = True

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

# Response tharumpodu theriya vendiya details
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
