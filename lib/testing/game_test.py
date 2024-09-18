import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Game, Review
from conftest import SQLITE_URL

@pytest.fixture(scope='module')
def setup_database():
    # Create the database engine and session
    engine = create_engine(SQLITE_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Add test data
    mario_kart = Game(
        title="Mario Kart",
        platform="Switch",
        genre="Racing",
        price=60
    )
    session.add(mario_kart)
    session.commit()

    mk_review_1 = Review(
        score=10,
        comment="Wow, what a game",
        game_id=mario_kart.id
    )

    mk_review_2 = Review(
        score=8,
        comment="A classic",
        game_id=mario_kart.id
    )
    session.bulk_save_objects([mk_review_1, mk_review_2])
    session.commit()

    yield {
        'session': session,
        'mario_kart': mario_kart
    }

    # Teardown
    session.close()
    engine.dispose()

def test_game_has_correct_attributes(setup_database):
    '''has attributes "id", "title", "platform", "genre", "price".'''
    mario_kart = setup_database['mario_kart']
    assert all(
        hasattr(mario_kart, attr)
        for attr in ["id", "title", "platform", "genre", "price"]
    )

def test_has_associated_reviews(setup_database):
    '''has two reviews with scores 10 and 8.'''
    mario_kart = setup_database['mario_kart']
    reviews = mario_kart.reviews
    assert (
        len(reviews) == 2 and
        reviews[0].score == 10 and
        reviews[1].score == 8
    )
