import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_setup import get_db
from app.models.document import Document
from app.models.user import User
from app.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/documents/{document_id}/status")
async def get_document_processing_status(
    document_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    result = await db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.user_id == current_user.id,
        )
    )
    doc = result.scalar_one_or_none()
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    return {
        "document_id": str(doc.id),
        "processing_status": doc.processing_status,
        "processed_at": doc.processed_at,
    }


@router.post("/documents/{document_id}/reprocess", status_code=status.HTTP_202_ACCEPTED)
async def reprocess_document(
    document_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    result = await db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.user_id == current_user.id,
        )
    )
    doc = result.scalar_one_or_none()
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    doc.processing_status = "pending"
    doc.processed_at = None
    doc.extracted_text = None
    doc.summary = None
    doc.topics = None
    await db.commit()

    return {
        "detail": "Document reprocessing queued",
        "document_id": str(doc.id),
        "processing_status": doc.processing_status,
    }
