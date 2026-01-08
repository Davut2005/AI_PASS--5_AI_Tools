from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException, status

from ..models.user import User, AuthProvider, UserRole
from ..models.credit import Credit
from ..models.organization import Organization
from ..config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not AuthService.verify_password(password, user.password_hash):
            return None
        return user
    
    @staticmethod
    async def verify_google_token(token: str) -> dict:
        try:
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                settings.GOOGLE_CLIENT_ID
            )
            
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            
            return {
                "email": idinfo['email'],
                "name": idinfo.get('name', ''),
                "google_id": idinfo['sub']
            }
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google token"
            )
    
    @staticmethod
    def create_user(
        db: Session, 
        email: str, 
        password: Optional[str],
        name: str,
        auth_provider: AuthProvider = AuthProvider.EMAIL,
        organization_name: Optional[str] = None
    ) -> User:
        # Check if user exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Determine role
        role = UserRole.USER
        organization = None
        
        # Create organization if provided
        if organization_name:
            role = UserRole.OWNER
            organization = Organization(name=organization_name)
            db.add(organization)
            db.flush()
            
            # Create organization credits
            org_credits = Credit(
                organization_id=organization.id,
                balance=500  # Starting credits for organizations
            )
            db.add(org_credits)
        
        # Hash password if provided
        password_hash = None
        if password:
            password_hash = AuthService.get_password_hash(password)
        
        # Create user
        user = User(
            email=email,
            password_hash=password_hash,
            name=name,
            auth_provider=auth_provider,
            role=role,
            organization_id=organization.id if organization else None
        )
        db.add(user)
        db.flush()
        
        # Create user credits
        user_credits = Credit(
            user_id=user.id,
            balance=100  # Starting credits for individual users
        )
        db.add(user_credits)
        
        db.commit()
        db.refresh(user)
        
        return user