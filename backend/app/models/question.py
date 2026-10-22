"""
========================================================================================
MODULE:    Question Bank, Curriculum & Content Lifecycle Models
TOPIC:     Curricula, Subjects, Topics, Immutable Versions, Options & Reports
FILE:      backend/app/models/question.py
PURPOSE:   Implements the entities governing academic content quality and versioning.
           Enforces immutable versioning on questions so changes do not corrupt past
           test attempt records, tracks NCTB chapter mappings, cognitive skill tags,
           source citations, plausible distractors, and community issue reports.
AUDIENCE:  Content Engineers, Subject Reviewers, Data Architects & AI Agents
STANDARDS: Clean Architecture, Immutable Versioning, NCTB Curriculum Mapping
========================================================================================
"""

from typing import List, Optional
from backend.app.models.base import BaseModel
from backend.app.schemas.question_schema import QuestionStatus, DifficultyLevel, CognitiveSkill


class Curriculum(BaseModel):
    """
    Academic syllabus authority (e.g. 'NCTB-2024', 'ENGLISH_MEDIUM_CAMBRIDGE').
    """
    def __init__(
        self,
        code: str,
        title: str,
        year_established: int = 2024,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.code = code
        self.title = title
        self.year_established = year_established


class Subject(BaseModel):
    """
    Academic subject scoped to curriculum and educational stage.
    """
    def __init__(
        self,
        curriculum_id: str,
        stage: str,
        code: str,
        name_bn: str,
        name_en: str,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.curriculum_id = curriculum_id
        self.stage = stage
        self.code = code
        self.name_bn = name_bn
        self.name_en = name_en


class Topic(BaseModel):
    """
    Chapter or sub-topic unit within an academic subject.
    """
    def __init__(
        self,
        subject_id: str,
        chapter_number: int,
        title_bn: str,
        title_en: str,
        parent_topic_id: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.subject_id = subject_id
        self.chapter_number = chapter_number
        self.title_bn = title_bn
        self.title_en = title_en
        self.parent_topic_id = parent_topic_id


class Question(BaseModel):
    """
    Top-level question container maintaining lifecycle state across versions.
    """
    def __init__(
        self,
        topic_id: str,
        current_version_id: Optional[str] = None,
        status: QuestionStatus = QuestionStatus.DRAFT,
        created_by: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.topic_id = topic_id
        self.current_version_id = current_version_id
        self.status = status
        self.created_by = created_by


class QuestionVersion(BaseModel):
    """
    Immutable snapshot of a question stem, explanation, and pedagogical tags.
    """
    def __init__(
        self,
        question_id: str,
        version_number: int,
        stem_bn: str,
        explanation_bn: str,
        content_hash: str,
        stem_en: Optional[str] = None,
        explanation_en: Optional[str] = None,
        difficulty: DifficultyLevel = DifficultyLevel.MEDIUM,
        cognitive_skill: CognitiveSkill = CognitiveSkill.REASONING,
        estimated_seconds: int = 60,
        source_attribution: Optional[str] = None,
        reviewed_by: Optional[str] = None,
        reviewed_at: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.question_id = question_id
        self.version_number = version_number
        self.stem_bn = stem_bn
        self.stem_en = stem_en
        self.explanation_bn = explanation_bn
        self.explanation_en = explanation_en
        self.difficulty = difficulty
        self.cognitive_skill = cognitive_skill
        self.estimated_seconds = estimated_seconds
        self.source_attribution = source_attribution
        self.content_hash = content_hash
        self.reviewed_by = reviewed_by
        self.reviewed_at = reviewed_at


class QuestionOption(BaseModel):
    """
    Individual multiple-choice alternative ('A', 'B', 'C', 'D').
    """
    def __init__(
        self,
        question_version_id: str,
        option_key: str,
        option_text_bn: str,
        is_correct: bool = False,
        option_text_en: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.question_version_id = question_version_id
        self.option_key = option_key
        self.option_text_bn = option_text_bn
        self.option_text_en = option_text_en
        self.is_correct = is_correct
