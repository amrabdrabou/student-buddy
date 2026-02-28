import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_setup import get_db
from app.models.ai_conversation import AiConversation
from app.models.ai_conversation_metrics import AiConversationMetrics
from app.models.ai_generated_content import AiGeneratedContent
from app.models.ai_message import AiMessage
from app.models.ai_message_feedback import AiMessageFeedback
from app.models.chatbot_session import ChatbotSession
from app.models.user import User
from app.schemas.ai_conversation import AiConversationCreate, AiConversationUpdate, AiConversationResponse
from app.schemas.ai_conversation_metrics import AiConversationMetricsResponse
from app.schemas.ai_generated_content import AiGeneratedContentCreate, AiGeneratedContentResponse
from app.schemas.ai_message import AiMessageCreate, AiMessageResponse
from app.schemas.ai_message_feedback import AiMessageFeedbackCreate, AiMessageFeedbackResponse
from app.schemas.chatbot_session import ChatbotSessionCreate, ChatbotSessionResponse
from app.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/ai", tags=["AI"])


# ── helpers ────────────────────────────────────────────────────────────────────

async def _get_conversation(
    conversation_id: uuid.UUID, current_user: User, db: AsyncSession
) -> AiConversation:
    result = await db.execute(
        select(AiConversation).where(
            AiConversation.id == conversation_id,
            AiConversation.user_id == current_user.id,
        )
    )
    conv = result.scalar_one_or_none()
    if conv is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return conv


async def _get_message(
    message_id: uuid.UUID, current_user: User, db: AsyncSession
) -> AiMessage:
    result = await db.execute(
        select(AiMessage)
        .join(AiConversation, AiMessage.conversation_id == AiConversation.id)
        .where(AiMessage.id == message_id, AiConversation.user_id == current_user.id)
    )
    msg = result.scalar_one_or_none()
    if msg is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return msg


# ── Conversations ──────────────────────────────────────────────────────────────

@router.get("/conversations", response_model=List[AiConversationResponse])
async def list_conversations(
    skip: int = 0,
    limit: int = 20,
    subject_id: Optional[uuid.UUID] = None,
    is_archived: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[AiConversationResponse]:
    query = select(AiConversation).where(AiConversation.user_id == current_user.id)
    if subject_id is not None:
        query = query.where(AiConversation.subject_id == subject_id)
    if is_archived is not None:
        query = query.where(AiConversation.is_archived == is_archived)
    query = query.order_by(AiConversation.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    convs = result.scalars().all()
    return [AiConversationResponse.model_validate(c) for c in convs]


@router.post("/conversations", response_model=AiConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    payload: AiConversationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AiConversationResponse:
    conv = AiConversation(
        user_id=current_user.id,
        subject_id=payload.subject_id,
        title=payload.title,
        conversation_type=payload.conversation_type,
        related_note_id=payload.related_note_id,
        related_document_id=payload.related_document_id,
        related_deck_id=payload.related_deck_id,
        is_archived=payload.is_archived,
    )
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return AiConversationResponse.model_validate(conv)


@router.get("/conversations/{conversation_id}", response_model=AiConversationResponse)
async def get_conversation(
    conversation_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AiConversationResponse:
    conv = await _get_conversation(conversation_id, current_user, db)
    return AiConversationResponse.model_validate(conv)


@router.patch("/conversations/{conversation_id}", response_model=AiConversationResponse)
async def update_conversation(
    conversation_id: uuid.UUID,
    payload: AiConversationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AiConversationResponse:
    conv = await _get_conversation(conversation_id, current_user, db)
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(conv, field, value)
    await db.commit()
    await db.refresh(conv)
    return AiConversationResponse.model_validate(conv)


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    conv = await _get_conversation(conversation_id, current_user, db)
    await db.delete(conv)
    await db.commit()


# ── Messages ───────────────────────────────────────────────────────────────────

@router.get("/conversations/{conversation_id}/messages", response_model=List[AiMessageResponse])
async def list_messages(
    conversation_id: uuid.UUID,
    skip: int = 0,
    limit: int = 20,
    role: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[AiMessageResponse]:
    await _get_conversation(conversation_id, current_user, db)
    query = select(AiMessage).where(AiMessage.conversation_id == conversation_id)
    if role is not None:
        query = query.where(AiMessage.role == role)
    query = query.order_by(AiMessage.message_order.asc()).offset(skip).limit(limit)
    result = await db.execute(query)
    messages = result.scalars().all()
    return [AiMessageResponse.model_validate(m) for m in messages]


@router.post("/conversations/{conversation_id}/messages", response_model=AiMessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    conversation_id: uuid.UUID,
    payload: AiMessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AiMessageResponse:
    conv = await _get_conversation(conversation_id, current_user, db)

    msg = AiMessage(
        conversation_id=conversation_id,
        parent_message_id=payload.parent_message_id,
        role=payload.role,
        content=payload.content,
        content_preview=payload.content_preview,
        message_order=payload.message_order,
        thread_depth=payload.thread_depth,
        is_thread_root=payload.is_thread_root,
        context_window_position=payload.context_window_position,
        has_large_content=payload.has_large_content,
        tokens_used=payload.tokens_used,
        model_used=payload.model_used,
        processing_time_ms=payload.processing_time_ms,
    )
    db.add(msg)
    conv.total_messages = (conv.total_messages or 0) + 1
    from datetime import datetime, timezone
    conv.last_message_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(msg)
    return AiMessageResponse.model_validate(msg)


@router.get("/messages/{message_id}", response_model=AiMessageResponse)
async def get_message(
    message_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AiMessageResponse:
    msg = await _get_message(message_id, current_user, db)
    return AiMessageResponse.model_validate(msg)


@router.get("/messages/{message_id}/thread", response_model=List[AiMessageResponse])
async def get_message_thread(
    message_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[AiMessageResponse]:
    root_msg = await _get_message(message_id, current_user, db)

    result = await db.execute(
        select(AiMessage)
        .where(
            AiMessage.conversation_id == root_msg.conversation_id,
            AiMessage.parent_message_id == root_msg.id,
        )
        .order_by(AiMessage.message_order.asc())
    )
    replies = result.scalars().all()
    return [AiMessageResponse.model_validate(root_msg)] + [
        AiMessageResponse.model_validate(r) for r in replies
    ]


# ── Feedback ───────────────────────────────────────────────────────────────────

@router.post("/messages/{message_id}/feedback", response_model=AiMessageFeedbackResponse, status_code=status.HTTP_201_CREATED)
async def create_feedback(
    message_id: uuid.UUID,
    payload: AiMessageFeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AiMessageFeedbackResponse:
    msg = await _get_message(message_id, current_user, db)

    feedback = AiMessageFeedback(
        message_id=msg.id,
        user_id=current_user.id,
        conversation_id=msg.conversation_id,
        feedback_type=payload.feedback_type,
        rating=payload.rating,
        is_helpful=payload.is_helpful,
        is_accurate=payload.is_accurate,
        feedback_categories=payload.feedback_categories,
        comment=payload.comment,
        reported_issue=payload.reported_issue,
    )
    db.add(feedback)
    await db.commit()
    await db.refresh(feedback)
    return AiMessageFeedbackResponse.model_validate(feedback)


# ── Generated content ──────────────────────────────────────────────────────────

class GenerateRequest(BaseModel):
    source_type: str
    source_id: uuid.UUID
    count: Optional[int] = None


@router.post("/generate/flashcards", response_model=AiGeneratedContentResponse, status_code=status.HTTP_201_CREATED)
async def generate_flashcards(
    payload: GenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AiGeneratedContentResponse:
    content = AiGeneratedContent(
        user_id=current_user.id,
        content_type="flashcards",
        source_type=payload.source_type,
        source_id=payload.source_id,
        generated_content={"count": payload.count, "status": "queued"},
    )
    db.add(content)
    await db.commit()
    await db.refresh(content)
    return AiGeneratedContentResponse.model_validate(content)


@router.post("/generate/summary", response_model=AiGeneratedContentResponse, status_code=status.HTTP_201_CREATED)
async def generate_summary(
    payload: GenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AiGeneratedContentResponse:
    content = AiGeneratedContent(
        user_id=current_user.id,
        content_type="summary",
        source_type=payload.source_type,
        source_id=payload.source_id,
        generated_content={"status": "queued"},
    )
    db.add(content)
    await db.commit()
    await db.refresh(content)
    return AiGeneratedContentResponse.model_validate(content)


@router.get("/generated", response_model=List[AiGeneratedContentResponse])
async def list_generated_content(
    skip: int = 0,
    limit: int = 20,
    content_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[AiGeneratedContentResponse]:
    query = select(AiGeneratedContent).where(AiGeneratedContent.user_id == current_user.id)
    if content_type is not None:
        query = query.where(AiGeneratedContent.content_type == content_type)
    query = query.order_by(AiGeneratedContent.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()
    return [AiGeneratedContentResponse.model_validate(i) for i in items]


# ── Chatbot sessions ───────────────────────────────────────────────────────────

@router.get("/sessions", response_model=List[ChatbotSessionResponse])
async def list_chatbot_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[ChatbotSessionResponse]:
    result = await db.execute(
        select(ChatbotSession)
        .where(ChatbotSession.user_id == current_user.id)
        .order_by(ChatbotSession.started_at.desc())
    )
    sessions = result.scalars().all()
    return [ChatbotSessionResponse.model_validate(s) for s in sessions]


@router.post("/sessions", response_model=ChatbotSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_chatbot_session(
    payload: ChatbotSessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ChatbotSessionResponse:
    session = ChatbotSession(
        user_id=current_user.id,
        conversation_id=payload.conversation_id,
        session_token=payload.session_token,
        device_type=payload.device_type,
        is_active=payload.is_active,
        session_type=payload.session_type,
        context_window_size=payload.context_window_size,
        active_model=payload.active_model,
        system_prompt_id=payload.system_prompt_id,
        temperature=payload.temperature,
        session_params=payload.session_params,
        active_subject_id=payload.active_subject_id,
        active_note_id=payload.active_note_id,
        active_document_id=payload.active_document_id,
        expires_at=payload.expires_at,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return ChatbotSessionResponse.model_validate(session)


@router.delete("/sessions/{session_token}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chatbot_session(
    session_token: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    result = await db.execute(
        select(ChatbotSession).where(
            ChatbotSession.session_token == session_token,
            ChatbotSession.user_id == current_user.id,
        )
    )
    session = result.scalar_one_or_none()
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chatbot session not found")
    await db.delete(session)
    await db.commit()


# ── Metrics ────────────────────────────────────────────────────────────────────

@router.get("/conversations/{conversation_id}/metrics", response_model=AiConversationMetricsResponse)
async def get_conversation_metrics(
    conversation_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AiConversationMetricsResponse:
    await _get_conversation(conversation_id, current_user, db)

    result = await db.execute(
        select(AiConversationMetrics).where(
            AiConversationMetrics.conversation_id == conversation_id
        )
    )
    metrics = result.scalar_one_or_none()
    if metrics is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Metrics not found for this conversation")
    return AiConversationMetricsResponse.model_validate(metrics)
