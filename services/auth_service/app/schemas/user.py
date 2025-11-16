from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    full_name: str | None = None   # optional, matches DB

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    email: str
    full_name: str | None = None
    is_active: bool
    
    class Config:
        from_attributes = True
