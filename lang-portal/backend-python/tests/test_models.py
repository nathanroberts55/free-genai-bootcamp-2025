import pytest
from sqlmodel import Session, select, SQLModel, create_engine
from models import Word, Group, WordGroupLink
from sqlalchemy import event, text

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, echo=True)


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def setup_triggers(engine):
    with engine.connect() as conn:
        try:
            # Use text() to create executable SQL statements
            insert_trigger = text(
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

            delete_trigger = text(
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

            conn.execute(insert_trigger)
            conn.execute(delete_trigger)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error setting up triggers: {e}")
            raise


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    setup_triggers(engine)  # Add triggers after creating tables

    with Session(engine) as session:
        yield session

    SQLModel.metadata.drop_all(engine)


def test_word_group_counter_cache(session):
    # Create test data
    word = Word(
        kanji="新しい", romaji="atarashii", english="new", parts={"type": "adjective"}
    )
    group = Group(name="Test Group")
    session.add(word)
    session.add(group)
    session.commit()

    # Link word to group
    word_group = WordGroupLink(word_id=word.id, group_id=group.id)
    session.add(word_group)
    session.commit()

    # Verify counter cache
    updated_group = session.get(Group, group.id)
    assert updated_group.words_count == 1

    # Test deletion
    session.delete(word_group)
    session.commit()

    updated_group = session.get(Group, group.id)
    assert updated_group.words_count == 0
