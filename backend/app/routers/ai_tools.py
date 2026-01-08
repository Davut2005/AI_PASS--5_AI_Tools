from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..middleware.auth import get_current_user
from ..models.user import User
from ..models.ai_execution import AIExecution, ExecutionStatus
from ..schemas.ai_tool import AIToolRequest, AIToolResponse
from ..services.ai_service import ai_service
from ..services.credit_service import CreditService

router = APIRouter(prefix="/ai", tags=["AI Tools"])

@router.post("/chat", response_model=AIToolResponse)
async def chat_completion(
    request: AIToolRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """AI Chat Completion - 1 credit"""
    try:
        # Execute AI
        result = await ai_service.chat_completion(request.input_text)
        
        # Deduct credits
        remaining = CreditService.deduct_credits(
            db, current_user, result["credits"], "Chat completion"
        )
        
        # Log execution
        execution = AIExecution(
            user_id=current_user.id,
            tool_name="chat",
            input_text=request.input_text,
            output_text=result["output"],
            credits_used=result["credits"],
            status=ExecutionStatus.SUCCESS
        )
        db.add(execution)
        db.commit()
        
        return AIToolResponse(
            output_text=result["output"],
            credits_used=result["credits"],
            remaining_credits=remaining
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize", response_model=AIToolResponse)
async def text_summarizer(
    request: AIToolRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Text Summarizer - 2 credits"""
    try:
        result = await ai_service.text_summarizer(request.input_text)
        
        remaining = CreditService.deduct_credits(
            db, current_user, result["credits"], "Text summarization"
        )
        
        execution = AIExecution(
            user_id=current_user.id,
            tool_name="summarizer",
            input_text=request.input_text,
            output_text=result["output"],
            credits_used=result["credits"],
            status=ExecutionStatus.SUCCESS
        )
        db.add(execution)
        db.commit()
        
        return AIToolResponse(
            output_text=result["output"],
            credits_used=result["credits"],
            remaining_credits=remaining
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate", response_model=AIToolResponse)
async def content_generator(
    request: AIToolRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Content Generator - 3 credits"""
    try:
        result = await ai_service.content_generator(request.input_text)
        
        remaining = CreditService.deduct_credits(
            db, current_user, result["credits"], "Content generation"
        )
        
        execution = AIExecution(
            user_id=current_user.id,
            tool_name="generator",
            input_text=request.input_text,
            output_text=result["output"],
            credits_used=result["credits"],
            status=ExecutionStatus.SUCCESS
        )
        db.add(execution)
        db.commit()
        
        return AIToolResponse(
            output_text=result["output"],
            credits_used=result["credits"],
            remaining_credits=remaining
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/code-help", response_model=AIToolResponse)
async def code_helper(
    request: AIToolRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Code Helper - 2 credits"""
    try:
        result = await ai_service.code_helper(request.input_text)
        
        remaining = CreditService.deduct_credits(
            db, current_user, result["credits"], "Code assistance"
        )
        
        execution = AIExecution(
            user_id=current_user.id,
            tool_name="code_helper",
            input_text=request.input_text,
            output_text=result["output"],
            credits_used=result["credits"],
            status=ExecutionStatus.SUCCESS
        )
        db.add(execution)
        db.commit()
        
        return AIToolResponse(
            output_text=result["output"],
            credits_used=result["credits"],
            remaining_credits=remaining
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze", response_model=AIToolResponse)
async def text_analyzer(
    request: AIToolRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Text Analyzer - 2 credits"""
    try:
        result = await ai_service.text_analyzer(request.input_text)
        
        remaining = CreditService.deduct_credits(
            db, current_user, result["credits"], "Text analysis"
        )
        
        execution = AIExecution(
            user_id=current_user.id,
            tool_name="analyzer",
            input_text=request.input_text,
            output_text=result["output"],
            credits_used=result["credits"],
            status=ExecutionStatus.SUCCESS
        )
        db.add(execution)
        db.commit()
        
        return AIToolResponse(
            output_text=result["output"],
            credits_used=result["credits"],
            remaining_credits=remaining
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))