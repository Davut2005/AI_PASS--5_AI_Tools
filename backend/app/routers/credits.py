from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..middleware.auth import get_current_user
from ..models.user import User
from ..models.credit import Credit, CreditTransaction
from ..schemas.credit import CreditResponse, CreditTransactionResponse
from ..services.credit_service import CreditService

router = APIRouter(prefix="/credits", tags=["Credits"])

@router.get("/balance", response_model=CreditResponse)
async def get_credit_balance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current credit balance"""
    balance = CreditService.get_user_credits(db, current_user)
    
    if current_user.organization_id:
        credits = db.query(Credit).filter(
            Credit.organization_id == current_user.organization_id
        ).first()
    else:
        credits = db.query(Credit).filter(
            Credit.user_id == current_user.id
        ).first()
    
    return CreditResponse(
        balance=balance,
        updated_at=credits.updated_at if credits else None
    )

@router.get("/transactions", response_model=List[CreditTransactionResponse])
async def get_credit_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Get credit transaction history"""
    if current_user.organization_id:
        transactions = db.query(CreditTransaction).filter(
            CreditTransaction.organization_id == current_user.organization_id
        ).order_by(CreditTransaction.created_at.desc()).limit(limit).all()
    else:
        transactions = db.query(CreditTransaction).filter(
            CreditTransaction.user_id == current_user.id
        ).order_by(CreditTransaction.created_at.desc()).limit(limit).all()
    
    return [
        CreditTransactionResponse(
            id=t.id,
            amount=t.amount,
            type=t.type.value,
            description=t.description,
            created_at=t.created_at
        )
        for t in transactions
    ]