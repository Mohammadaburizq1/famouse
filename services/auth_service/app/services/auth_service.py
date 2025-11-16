from sqlalchemy.orm import Session
from services.auth_service.app.schemas.user import UserCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from ..models.user import User
from ..core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status

class AuthService:

    @staticmethod
    def create_user(payload, db):
        try:
            # check if exists
            existing = db.query(User).filter(User.email == payload.email).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )

            user = User(
                email=payload.email,
                full_name=payload.full_name,
                hashed_password=hash_password(payload.password),
                is_active=True
            )

            db.add(user)
            db.commit()
            db.refresh(user)
            return user

        except IntegrityError:
            db.rollback()  # important
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )
   
        
    @staticmethod
    async def authenticate(db: Session, email: str, password: str) -> User:
        user = db.query(User).filter(User.email == email).first()

        # Email not found
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # User inactive
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        # Wrong password
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        return user


auth_service = AuthService()
