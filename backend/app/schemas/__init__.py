from app.schemas.user import UserBase, UserCreate, UserUpdate, UserResponse
from app.schemas.user_preferences import (
    UserPreferencesBase, UserPreferencesCreate, UserPreferencesUpdate, UserPreferencesResponse,
)
from app.schemas.study_subject import (
    StudySubjectBase, StudySubjectCreate, StudySubjectUpdate, StudySubjectResponse,
)
from app.schemas.tag import TagBase, TagCreate, TagUpdate, TagResponse
from app.schemas.flashcard_deck import (
    FlashcardDeckBase, FlashcardDeckCreate, FlashcardDeckUpdate, FlashcardDeckResponse,
)
from app.schemas.flashcard import (
    FlashcardBase, FlashcardCreate, FlashcardUpdate, FlashcardResponse,
)
from app.schemas.flashcard_review import (
    FlashcardReviewBase, FlashcardReviewCreate, FlashcardReviewUpdate, FlashcardReviewResponse,
)
from app.schemas.note import NoteBase, NoteCreate, NoteUpdate, NoteResponse
from app.schemas.document import DocumentBase, DocumentCreate, DocumentUpdate, DocumentResponse
from app.schemas.study_session import (
    StudySessionBase, StudySessionCreate, StudySessionUpdate, StudySessionResponse,
)
from app.schemas.study_goal import (
    StudyGoalBase, StudyGoalCreate, StudyGoalUpdate, StudyGoalResponse,
)
from app.schemas.daily_progress import (
    DailyProgressBase, DailyProgressCreate, DailyProgressUpdate, DailyProgressResponse,
)
from app.schemas.ai_conversation import (
    AiConversationBase, AiConversationCreate, AiConversationUpdate, AiConversationResponse,
)
from app.schemas.ai_message import (
    AiMessageBase, AiMessageCreate, AiMessageUpdate, AiMessageResponse,
)
from app.schemas.ai_message_intent import (
    AiMessageIntentBase, AiMessageIntentCreate, AiMessageIntentUpdate, AiMessageIntentResponse,
)
from app.schemas.ai_message_entity import (
    AiMessageEntityBase, AiMessageEntityCreate, AiMessageEntityUpdate, AiMessageEntityResponse,
)
from app.schemas.ai_message_content_store import (
    AiMessageContentStoreBase, AiMessageContentStoreCreate,
    AiMessageContentStoreUpdate, AiMessageContentStoreResponse,
)
from app.schemas.ai_message_context import (
    AiMessageContextBase, AiMessageContextCreate, AiMessageContextUpdate, AiMessageContextResponse,
)
from app.schemas.ai_conversation_metrics import (
    AiConversationMetricsBase, AiConversationMetricsCreate,
    AiConversationMetricsUpdate, AiConversationMetricsResponse,
)
from app.schemas.ai_usage_stats import (
    AiUsageStatsBase, AiUsageStatsCreate, AiUsageStatsUpdate, AiUsageStatsResponse,
)
from app.schemas.ai_message_feedback import (
    AiMessageFeedbackBase, AiMessageFeedbackCreate, AiMessageFeedbackUpdate, AiMessageFeedbackResponse,
)
from app.schemas.ai_generated_content import (
    AiGeneratedContentBase, AiGeneratedContentCreate, AiGeneratedContentUpdate, AiGeneratedContentResponse,
)
from app.schemas.ai_gen_note_source import (
    AiGenNoteSourceBase, AiGenNoteSourceCreate, AiGenNoteSourceUpdate, AiGenNoteSourceResponse,
)
from app.schemas.ai_gen_document_source import (
    AiGenDocumentSourceBase, AiGenDocumentSourceCreate,
    AiGenDocumentSourceUpdate, AiGenDocumentSourceResponse,
)
from app.schemas.chatbot_session import (
    ChatbotSessionBase, ChatbotSessionCreate, ChatbotSessionUpdate, ChatbotSessionResponse,
)
from app.schemas.system_prompt import (
    SystemPromptBase, SystemPromptCreate, SystemPromptUpdate, SystemPromptResponse,
)
from app.schemas.system_prompt_version import (
    SystemPromptVersionBase, SystemPromptVersionCreate,
    SystemPromptVersionUpdate, SystemPromptVersionResponse,
)
from app.schemas.embedding_vector import (
    EmbeddingVectorBase, EmbeddingVectorCreate, EmbeddingVectorUpdate, EmbeddingVectorResponse,
)
from app.schemas.audit_log import (
    AuditLogBase, AuditLogCreate, AuditLogUpdate, AuditLogResponse,
)
from app.schemas.study_group import (
    StudyGroupBase, StudyGroupCreate, StudyGroupUpdate, StudyGroupResponse,
)
from app.schemas.study_group_member import (
    StudyGroupMemberBase, StudyGroupMemberCreate, StudyGroupMemberUpdate, StudyGroupMemberResponse,
)
from app.schemas.shared_resource import (
    SharedResourceBase, SharedResourceCreate, SharedResourceUpdate, SharedResourceResponse,
)
from app.schemas.refresh_token import (
    RefreshTokenBase, RefreshTokenCreate, RefreshTokenUpdate, RefreshTokenResponse,
)

__all__ = [
    # user
    "UserBase", "UserCreate", "UserUpdate", "UserResponse",
    # user_preferences
    "UserPreferencesBase", "UserPreferencesCreate", "UserPreferencesUpdate", "UserPreferencesResponse",
    # study_subject
    "StudySubjectBase", "StudySubjectCreate", "StudySubjectUpdate", "StudySubjectResponse",
    # tag
    "TagBase", "TagCreate", "TagUpdate", "TagResponse",
    # flashcard_deck
    "FlashcardDeckBase", "FlashcardDeckCreate", "FlashcardDeckUpdate", "FlashcardDeckResponse",
    # flashcard
    "FlashcardBase", "FlashcardCreate", "FlashcardUpdate", "FlashcardResponse",
    # flashcard_review
    "FlashcardReviewBase", "FlashcardReviewCreate", "FlashcardReviewUpdate", "FlashcardReviewResponse",
    # note
    "NoteBase", "NoteCreate", "NoteUpdate", "NoteResponse",
    # document
    "DocumentBase", "DocumentCreate", "DocumentUpdate", "DocumentResponse",
    # study_session
    "StudySessionBase", "StudySessionCreate", "StudySessionUpdate", "StudySessionResponse",
    # study_goal
    "StudyGoalBase", "StudyGoalCreate", "StudyGoalUpdate", "StudyGoalResponse",
    # daily_progress
    "DailyProgressBase", "DailyProgressCreate", "DailyProgressUpdate", "DailyProgressResponse",
    # ai_conversation
    "AiConversationBase", "AiConversationCreate", "AiConversationUpdate", "AiConversationResponse",
    # ai_message
    "AiMessageBase", "AiMessageCreate", "AiMessageUpdate", "AiMessageResponse",
    # ai_message_intent
    "AiMessageIntentBase", "AiMessageIntentCreate", "AiMessageIntentUpdate", "AiMessageIntentResponse",
    # ai_message_entity
    "AiMessageEntityBase", "AiMessageEntityCreate", "AiMessageEntityUpdate", "AiMessageEntityResponse",
    # ai_message_content_store
    "AiMessageContentStoreBase", "AiMessageContentStoreCreate",
    "AiMessageContentStoreUpdate", "AiMessageContentStoreResponse",
    # ai_message_context
    "AiMessageContextBase", "AiMessageContextCreate", "AiMessageContextUpdate", "AiMessageContextResponse",
    # ai_conversation_metrics
    "AiConversationMetricsBase", "AiConversationMetricsCreate",
    "AiConversationMetricsUpdate", "AiConversationMetricsResponse",
    # ai_usage_stats
    "AiUsageStatsBase", "AiUsageStatsCreate", "AiUsageStatsUpdate", "AiUsageStatsResponse",
    # ai_message_feedback
    "AiMessageFeedbackBase", "AiMessageFeedbackCreate", "AiMessageFeedbackUpdate", "AiMessageFeedbackResponse",
    # ai_generated_content
    "AiGeneratedContentBase", "AiGeneratedContentCreate", "AiGeneratedContentUpdate", "AiGeneratedContentResponse",
    # ai_gen_note_source
    "AiGenNoteSourceBase", "AiGenNoteSourceCreate", "AiGenNoteSourceUpdate", "AiGenNoteSourceResponse",
    # ai_gen_document_source
    "AiGenDocumentSourceBase", "AiGenDocumentSourceCreate",
    "AiGenDocumentSourceUpdate", "AiGenDocumentSourceResponse",
    # chatbot_session
    "ChatbotSessionBase", "ChatbotSessionCreate", "ChatbotSessionUpdate", "ChatbotSessionResponse",
    # system_prompt
    "SystemPromptBase", "SystemPromptCreate", "SystemPromptUpdate", "SystemPromptResponse",
    # system_prompt_version
    "SystemPromptVersionBase", "SystemPromptVersionCreate",
    "SystemPromptVersionUpdate", "SystemPromptVersionResponse",
    # embedding_vector
    "EmbeddingVectorBase", "EmbeddingVectorCreate", "EmbeddingVectorUpdate", "EmbeddingVectorResponse",
    # audit_log
    "AuditLogBase", "AuditLogCreate", "AuditLogUpdate", "AuditLogResponse",
    # study_group
    "StudyGroupBase", "StudyGroupCreate", "StudyGroupUpdate", "StudyGroupResponse",
    # study_group_member
    "StudyGroupMemberBase", "StudyGroupMemberCreate", "StudyGroupMemberUpdate", "StudyGroupMemberResponse",
    # shared_resource
    "SharedResourceBase", "SharedResourceCreate", "SharedResourceUpdate", "SharedResourceResponse",
    # refresh_token
    "RefreshTokenBase", "RefreshTokenCreate", "RefreshTokenUpdate", "RefreshTokenResponse",
]
