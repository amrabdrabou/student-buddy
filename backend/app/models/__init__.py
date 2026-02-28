# Import all models so SQLAlchemy registers them with the metadata.
# The order matters: tables with no FK dependencies come first.

from app.models.user import User
from app.models.associations import flashcard_tags, note_tags, document_tags
from app.models.user_preferences import UserPreferences
from app.models.study_subject import StudySubject
from app.models.tag import Tag
from app.models.flashcard_deck import FlashcardDeck
from app.models.flashcard import Flashcard
from app.models.study_session import StudySession
from app.models.flashcard_review import FlashcardReview
from app.models.note import Note
from app.models.document import Document
from app.models.study_goal import StudyGoal
from app.models.daily_progress import DailyProgress
from app.models.system_prompt import SystemPrompt
from app.models.system_prompt_version import SystemPromptVersion
from app.models.ai_conversation import AiConversation
from app.models.ai_message import AiMessage
from app.models.ai_message_intent import AiMessageIntent
from app.models.ai_message_entity import AiMessageEntity
from app.models.ai_message_content_store import AiMessageContentStore
from app.models.ai_message_context import AiMessageContext
from app.models.ai_conversation_metrics import AiConversationMetrics
from app.models.ai_usage_stats import AiUsageStats
from app.models.ai_message_feedback import AiMessageFeedback
from app.models.ai_generated_content import AiGeneratedContent
from app.models.ai_gen_note_source import AiGenNoteSource
from app.models.ai_gen_document_source import AiGenDocumentSource
from app.models.chatbot_session import ChatbotSession
from app.models.embedding_vector import EmbeddingVector
from app.models.audit_log import AuditLog
from app.models.study_group import StudyGroup
from app.models.study_group_member import StudyGroupMember
from app.models.shared_resource import SharedResource
from app.models.refresh_token import RefreshToken

__all__ = [
    "User",
    "flashcard_tags",
    "note_tags",
    "document_tags",
    "UserPreferences",
    "StudySubject",
    "Tag",
    "FlashcardDeck",
    "Flashcard",
    "FlashcardReview",
    "Note",
    "Document",
    "StudySession",
    "StudyGoal",
    "DailyProgress",
    "AiConversation",
    "AiMessage",
    "AiMessageIntent",
    "AiMessageEntity",
    "AiMessageContentStore",
    "AiMessageContext",
    "AiConversationMetrics",
    "AiUsageStats",
    "AiMessageFeedback",
    "AiGeneratedContent",
    "AiGenNoteSource",
    "AiGenDocumentSource",
    "ChatbotSession",
    "SystemPrompt",
    "SystemPromptVersion",
    "EmbeddingVector",
    "AuditLog",
    "StudyGroup",
    "StudyGroupMember",
    "SharedResource",
    "RefreshToken",
]
