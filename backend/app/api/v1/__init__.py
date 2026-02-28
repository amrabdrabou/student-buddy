from fastapi import APIRouter

from app.api.v1.admin.router import router as admin_router
from app.api.v1.routers.ai.router import router as ai_router
from app.api.v1.routers.auth.router import router as auth_router
from app.api.v1.routers.documents.router import router as documents_router
from app.api.v1.routers.flashcar_docks.router import router as flashcard_decks_router
from app.api.v1.routers.flashcards.router import router as flashcards_router
from app.api.v1.routers.goals.router import router as goals_router
from app.api.v1.routers.jobs.router import router as jobs_router
from app.api.v1.routers.notes.router import router as notes_router
from app.api.v1.routers.progress.router import router as progress_router
from app.api.v1.routers.study_groups.router import router as study_groups_router
from app.api.v1.routers.study_sessions.router import router as study_sessions_router
from app.api.v1.routers.subjects.router import router as subjects_router
from app.api.v1.routers.users.router import router as users_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(subjects_router)
api_router.include_router(notes_router)
api_router.include_router(documents_router)
api_router.include_router(flashcard_decks_router)
api_router.include_router(flashcards_router)
api_router.include_router(goals_router)
api_router.include_router(study_sessions_router)
api_router.include_router(progress_router)
api_router.include_router(ai_router)
api_router.include_router(study_groups_router)
api_router.include_router(jobs_router)
api_router.include_router(admin_router)
