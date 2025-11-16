from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.auth_service.app.schemas.auth import LoginRequest, Token
from services.auth_service.app.models.user import User
from services.auth_service.app.core.security import (
    verify_password,
    create_access_token,
)
from services.auth_service.app.services.auth_service import AuthService
from shared.db.database import get_db
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
async def login(payload: LoginRequest, db=Depends(get_db)):
    user = await AuthService.authenticate(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id)})

    return Token(access_token=token)
