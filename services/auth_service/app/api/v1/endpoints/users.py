from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from services.auth_service.app.schemas.user import UserCreate, UserRead
from services.auth_service.app.models.user import User
from services.auth_service.app.core.security import hash_password
from services.auth_service.app.services.auth_service import AuthService
from shared.db.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return AuthService.create_user(payload, db)
