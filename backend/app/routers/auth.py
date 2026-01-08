from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.user import UserCreate, UserLogin, UserResponse, Token, GoogleAuthRequest
from ..services.auth_service import AuthService
from ..services.credit_service import CreditService
from ..models.user import AuthProvider, User, UserRole

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with email/password"""
    user = AuthService.create_user(
        db=db,
        email=user_data.email,
        password=user_data.password,
        name=user_data.name,
        auth_provider=AuthProvider.EMAIL,
        organization_name=user_data.organization_name
    )
    
    # Get user credits
    credits = CreditService.get_user_credits(db, user)
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        role=user.role.value,
        organization_id=user.organization_id,
        credits=credits,
        created_at=user.created_at
    )

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login with email/password"""
    user = AuthService.authenticate_user(db, user_data.email, user_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = AuthService.create_access_token(data={"sub": user.id})
    
    return Token(access_token=access_token)

@router.post("/google", response_model=Token)
async def google_auth(auth_data: GoogleAuthRequest, db: Session = Depends(get_db)):
    """Authenticate with Google OAuth"""
    try:
        google_user = await AuthService.verify_google_token(auth_data.token)
        
        # Check if user exists
        user = db.query(User).filter(User.email == google_user["email"]).first()
        
        if not user:
            # Create new user
            user = AuthService.create_user(
                db=db,
                email=google_user["email"],
                password=None,
                name=google_user["name"],
                auth_provider=AuthProvider.GOOGLE
            )
        
        access_token = AuthService.create_access_token(data={"sub": user.id})
        
        return Token(access_token=access_token)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )