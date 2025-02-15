import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, select
from main import app
from database import engine, add_test_data
from models import Word, Group, StudySession, WordReviewItem


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        add_test_data(session)
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        return session

    app.dependency_overrides = {}
    app.dependency_overrides[Session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_get_words(client):
    response = client.get("/words")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all(isinstance(word["kanji"], str) for word in data)
    assert all(isinstance(word["parts"], dict) for word in data)


def test_get_words_sorting(client):
    # Test kanji sorting
    response = client.get("/words?sort_by=kanji&order=asc")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert sorted(data, key=lambda x: x["kanji"]) == data


def test_get_words_pagination(client):
    # Test pagination
    response = client.get("/words?page=1&per_page=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 20  # Default per_page value


def test_get_groups(client):
    response = client.get("/groups")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all(isinstance(group["name"], str) for group in data)
    assert all(isinstance(group["words_count"], int) for group in data)


def test_get_group_words(client, session):
    # Get first group from test data
    group = session.exec(select(Group)).first()
    response = client.get(f"/groups/{group.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all(isinstance(word["kanji"], str) for word in data)


def test_get_group_words_not_found(client):
    response = client.get("/groups/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Group not found"


def test_create_study_session(client, session):
    # Get first group from test data
    group = session.exec(select(Group)).first()
    response = client.post("/study_sessions", json={"group_id": group.id})
    assert response.status_code == 200
    data = response.json()
    assert data["group_id"] == group.id


def test_create_word_review(client, session):
    # Create a study session first
    group = session.exec(select(Group)).first()
    session_response = client.post("/study_sessions", json={"group_id": group.id})
    session_id = session_response.json()["id"]

    # Get a word from test data
    word = session.exec(select(Word)).first()

    # Create review
    response = client.post(
        f"/study_sessions/{session_id}/review",
        json={"word_id": word.id, "correct": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["word_id"] == word.id
    assert data["study_session_id"] == session_id
    assert data["correct"] == True


def test_create_word_review_invalid_session(client):
    response = client.post(
        "/study_sessions/999/review", json={"word_id": 1, "correct": True}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Study session not found"
