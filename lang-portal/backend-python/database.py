from sqlmodel import SQLModel, Session, create_engine
import os
from models import Word, Group, StudyActivity, WordGroupLink
from sqlalchemy.engine import Engine
from sqlalchemy import event, text

# Create the database URL
sqlite_file_name = "sqlite3.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def add_test_data(session: Session):
    # Create test words
    words = [
        Word(
            kanji="食べる",
            romaji="taberu",
            english="to eat",
            parts={"type": "verb", "group": "ru-verb"},
        ),
        Word(
            kanji="飲む",
            romaji="nomu",
            english="to drink",
            parts={"type": "verb", "group": "u-verb"},
        ),
        Word(kanji="猫", romaji="neko", english="cat", parts={"type": "noun"}),
    ]
    for word in words:
        session.add(word)

    # Create test groups
    groups = [Group(name="Basic Verbs"), Group(name="Animals"), Group(name="All Words")]
    for group in groups:
        session.add(group)

    # Create test activities
    activities = [
        StudyActivity(name="Flashcards", url="/study/flashcards"),
        StudyActivity(name="Quiz", url="/study/quiz"),
    ]
    for activity in activities:
        session.add(activity)

    # Commit to get IDs
    session.commit()

    # Create word-group relationships
    word_groups = [
        WordGroupLink(word_id=words[0].id, group_id=groups[0].id),
        WordGroupLink(word_id=words[1].id, group_id=groups[0].id),
        WordGroupLink(word_id=words[2].id, group_id=groups[1].id),
        # Add all words to "All Words" group
        WordGroupLink(word_id=words[0].id, group_id=groups[2].id),
        WordGroupLink(word_id=words[1].id, group_id=groups[2].id),
        WordGroupLink(word_id=words[2].id, group_id=groups[2].id),
    ]
    for word_group in word_groups:
        session.add(word_group)

    # Update word counts for groups
    groups[0].words_count = 2  # Basic Verbs
    groups[1].words_count = 1  # Animals
    groups[2].words_count = 3  # All Words

    session.commit()


def setup_triggers(engine):
    with engine.connect() as conn:
        try:
            conn.execute(
                text(
                    """
                CREATE TRIGGER IF NOT EXISTS update_group_word_count_insert
                AFTER INSERT ON word_groups
                BEGIN
                    UPDATE groups 
                    SET words_count = (
                        SELECT COUNT(*) 
                        FROM word_groups 
                        WHERE group_id = NEW.group_id
                    )
                    WHERE id = NEW.group_id;
                END;
            """
                )
            )

            conn.execute(
                text(
                    """
                CREATE TRIGGER IF NOT EXISTS update_group_word_count_delete
                AFTER DELETE ON word_groups
                BEGIN
                    UPDATE groups 
                    SET words_count = (
                        SELECT COUNT(*) 
                        FROM word_groups 
                        WHERE group_id = OLD.group_id
                    )
                    WHERE id = OLD.group_id;
                END;
            """
                )
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error setting up triggers: {e}")
            raise


# Update create_db_and_tables function
def create_db_and_tables():
    if not os.path.exists("sqlite3.db"):
        SQLModel.metadata.create_all(engine)
        setup_triggers(engine)  # Add this line
        with Session(engine) as session:
            add_test_data(session)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def get_session():
    with Session(engine) as session:
        yield session
