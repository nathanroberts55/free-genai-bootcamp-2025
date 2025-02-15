from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query, Depends
from sqlmodel import Session, select, func
from models import (
    StudySessionCreate,
    Word,
    Group,
    StudySession,
    WordReviewCreate,
    WordReviewItem,
    StudyActivity,
)
from database import get_session
from pydantic import BaseModel
from enum import Enum
from database import create_db_and_tables


create_db_and_tables()

app = FastAPI()


# Enums for validation
class SortFieldWords(str, Enum):
    kanji = "kanji"
    romaji = "romaji"
    english = "english"
    correct_count = "correct_count"
    wrong_count = "wrong_count"


class SortFieldGroups(str, Enum):
    name = "name"
    words_count = "words_count"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


# Routes
@app.get("/words")
def get_words(
    page: int = Query(default=1, gt=0),
    sort_by: SortFieldWords = Query(default=SortFieldWords.kanji),
    order: SortOrder = Query(default=SortOrder.asc),
    session: Session = Depends(get_session),
):
    per_page = 20
    offset = (page - 1) * per_page

    # Create base query for words
    query = select(Word)

    # Add sorting
    if sort_by in [SortFieldWords.correct_count, SortFieldWords.wrong_count]:
        # Handle review statistics sorting
        subq = (
            select(
                WordReviewItem.word_id,
                func.count(WordReviewItem.id)
                .filter(WordReviewItem.correct == True)
                .label("correct_count"),
                func.count(WordReviewItem.id)
                .filter(WordReviewItem.correct == False)
                .label("wrong_count"),
            )
            .group_by(WordReviewItem.word_id)
            .subquery()
        )

        query = query.outerjoin(subq, Word.id == subq.c.word_id)
        sort_column = getattr(subq.c, sort_by)
    else:
        sort_column = getattr(Word, sort_by)

    query = query.order_by(
        sort_column.desc() if order == SortOrder.desc else sort_column
    )
    query = query.offset(offset).limit(per_page)

    words = session.exec(query).all()
    return words


@app.get("/groups")
def get_groups(
    page: int = Query(default=1, gt=0),
    sort_by: SortFieldGroups = Query(default=SortFieldGroups.name),
    order: SortOrder = Query(default=SortOrder.asc),
    session: Session = Depends(get_session),
):
    per_page = 20
    offset = (page - 1) * per_page

    query = select(Group)
    sort_column = getattr(Group, sort_by)
    query = query.order_by(
        sort_column.desc() if order == SortOrder.desc else sort_column
    )
    query = query.offset(offset).limit(per_page)

    groups = session.exec(query).all()
    return groups


@app.get("/groups/{group_id}")
def get_group_words(
    group_id: int,
    page: int = Query(default=1, gt=0),
    session: Session = Depends(get_session),
):
    group = session.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    per_page = 20
    offset = (page - 1) * per_page

    # Get words for the group with pagination
    words = session.exec(
        select(Word)
        .join(Word.groups)
        .where(Group.id == group_id)
        .offset(offset)
        .limit(per_page)
    ).all()

    return words


@app.post("/study_sessions")
def create_study_session(
    session_data: StudySessionCreate, session: Session = Depends(get_session)
):
    group = session.get(Group, session_data.group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    study_session = StudySession(group_id=session_data.group_id)
    session.add(study_session)
    session.commit()
    session.refresh(study_session)
    return study_session


@app.post("/study_sessions/{session_id}/review")
def create_word_review(
    session_id: int,
    review_data: WordReviewCreate,
    session: Session = Depends(get_session),
):
    study_session = session.get(StudySession, session_id)
    if not study_session:
        raise HTTPException(status_code=404, detail="Study session not found")

    word = session.get(Word, review_data.word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    review = WordReviewItem(
        word_id=review_data.word_id,
        study_session_id=session_id,
        correct=review_data.correct,
    )

    session.add(review)
    session.commit()
    session.refresh(review)
    return review
