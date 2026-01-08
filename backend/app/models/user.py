from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base

class AuthProvider(str, enum.Enum):
    EMAIL = "email"
    GOOGLE = "google"

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    OWNER = "owner"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=True)  # Nullable for OAuth users
    name = Column(String, nullable=False)
    auth_provider = Column(Enum(AuthProvider), default=AuthProvider.EMAIL)
    role = Column(Enum(UserRole), default=UserRole.USER)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    organization = relationship("Organization", back_populates="members")
    credits = relationship("Credit", back_populates="user", uselist=False)
    credit_transactions = relationship("CreditTransaction", back_populates="user")
    ai_executions = relationship("AIExecution", back_populates="user")