from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON


class WordGroupLink(SQLModel, table=True):
    __tablename__ = "word_groups"

    word_id: Optional[int] = Field(
        default=None, foreign_key="words.id", primary_key=True
    )
    group_id: Optional[int] = Field(
        default=None, foreign_key="groups.id", primary_key=True
    )


class WordReviewCreate(SQLModel):
    word_id: int
    correct: bool


class Word(SQLModel, table=True):
    __tablename__ = "words"

    id: Optional[int] = Field(default=None, primary_key=True)
    kanji: str
    romaji: str
    english: str
    parts: Dict[str, Any] = Field(sa_type=JSON)

    groups: List["Group"] = Relationship(
        back_populates="words", link_model=WordGroupLink
    )
    word_review_items: List["WordReviewItem"] = Relationship(back_populates="word")


class Group(SQLModel, table=True):
    __tablename__ = "groups"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    words_count: int = Field(default=0)

    words: List[Word] = Relationship(back_populates="groups", link_model=WordGroupLink)
    study_sessions: List["StudySession"] = Relationship(back_populates="group")


class StudyActivity(SQLModel, table=True):
    __tablename__ = "study_activities"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: str

    study_sessions: List["StudySession"] = Relationship(back_populates="study_activity")


class StudySession(SQLModel, table=True):
    __tablename__ = "study_sessions"

    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: Optional[int] = Field(foreign_key="groups.id")
    study_activity_id: Optional[int] = Field(foreign_key="study_activities.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    group: Group = Relationship(back_populates="study_sessions")
    study_activity: StudyActivity = Relationship(back_populates="study_sessions")
    word_review_items: List["WordReviewItem"] = Relationship(
        back_populates="study_session"
    )


class StudySessionCreate(SQLModel):
    group_id: int


class WordReviewItem(SQLModel, table=True):
    __tablename__ = "word_review_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    word_id: Optional[int] = Field(foreign_key="words.id")
    study_session_id: Optional[int] = Field(foreign_key="study_sessions.id")
    correct: bool
    created_at: datetime = Field(default_factory=datetime.utcnow)

    word: Word = Relationship(back_populates="word_review_items")
    study_session: StudySession = Relationship(back_populates="word_review_items")
