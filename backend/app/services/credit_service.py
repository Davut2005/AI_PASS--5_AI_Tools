from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.user import User
from ..models.credit import Credit, CreditTransaction, TransactionType

class CreditService:
    @staticmethod
    def get_user_credits(db: Session, user: User) -> int:
        if user.organization_id:
            # Use organization credits
            credits = db.query(Credit).filter(
                Credit.organization_id == user.organization_id
            ).first()
        else:
            # Use personal credits
            credits = db.query(Credit).filter(
                Credit.user_id == user.id
            ).first()
        
        return credits.balance if credits else 0
    
    @staticmethod
    def deduct_credits(
        db: Session, 
        user: User, 
        amount: int, 
        description: str
    ) -> int:
        if user.organization_id:
            # Deduct from organization
            credits = db.query(Credit).filter(
                Credit.organization_id == user.organization_id
            ).first()
            
            if not credits or credits.balance < amount:
                raise HTTPException(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    detail="Insufficient credits"
                )
            
            credits.balance -= amount
            
            # Log transaction
            transaction = CreditTransaction(
                user_id=user.id,
                organization_id=user.organization_id,
                amount=-amount,
                type=TransactionType.USAGE,
                description=description
            )
        else:
            # Deduct from personal
            credits = db.query(Credit).filter(
                Credit.user_id == user.id
            ).first()
            
            if not credits or credits.balance < amount:
                raise HTTPException(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    detail="Insufficient credits"
                )
            
            credits.balance -= amount
            
            # Log transaction
            transaction = CreditTransaction(
                user_id=user.id,
                amount=-amount,
                type=TransactionType.USAGE,
                description=description
            )
        
        db.add(transaction)
        db.commit()
        
        return credits.balance
    
    @staticmethod
    def add_credits(
        db: Session,
        user: User,
        amount: int,
        description: str,
        transaction_type: TransactionType = TransactionType.PURCHASE
    ) -> int:
        if user.organization_id:
            credits = db.query(Credit).filter(
                Credit.organization_id == user.organization_id
            ).first()
            
            credits.balance += amount
            
            transaction = CreditTransaction(
                user_id=user.id,
                organization_id=user.organization_id,
                amount=amount,
                type=transaction_type,
                description=description
            )
        else:
            credits = db.query(Credit).filter(
                Credit.user_id == user.id
            ).first()
            
            credits.balance += amount
            
            transaction = CreditTransaction(
                user_id=user.id,
                amount=amount,
                type=transaction_type,
                description=description
            )
        
        db.add(transaction)
        db.commit()
        
        return credits.balance