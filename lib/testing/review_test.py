import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Game, Review
from conftest import SQLITE_URL

@pytest.fixture(scope='module')
def setup_review_database():
    # Create the database engine and session
    engine = create_engine(SQLITE_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Add test data
    skyrim = Game(
        title="The Elder Scrolls V: Skyrim",
        platform="PC",
        genre="Adventure",
        price=20
    )
    session.add(skyrim)
    session.commit()

    skyrim_review = Review(
        score=10,
        comment="Wow, what a game",
        game_id=skyrim.id
    )
    session.add(skyrim_review)
    session.commit()

    yield {
        'session': session,
        'skyrim': skyrim,
        'skyrim_review': skyrim_review
    }

    # Teardown
    session.close()
    engine.dispose()

def test_review_has_correct_attributes(setup_review_database):
    '''has attributes "id", "score", "comment", "game_id".'''
    skyrim_review = setup_review_database['skyrim_review']
    assert all(
        hasattr(skyrim_review, attr)
        for attr in ["id", "score", "comment", "game_id"]
    )

def test_knows_about_associated_game(setup_review_database):
    '''has attribute "game" that is the "Game" object associated with its game_id.'''
    skyrim_review = setup_review_database['skyrim_review']
    skyrim = setup_review_database['skyrim']
    assert skyrim_review.game == skyrim
