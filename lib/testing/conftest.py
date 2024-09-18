#!/usr/bin/env python3

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Game, Review  # Ensure that Base is imported from models

# Configure SQLite URL
package_dir = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[0:-1])
db_dir = os.path.join(package_dir, 'one_to_many.db')
SQLITE_URL = ''.join(['sqlite:///', db_dir])

@pytest.fixture(scope='module')
def engine():
    """Create an SQLite database engine."""
    engine = create_engine(SQLITE_URL)
    Base.metadata.create_all(engine)  # Create tables
    yield engine
    Base.metadata.drop_all(engine)  # Drop tables after tests

@pytest.fixture(scope='module')
def session(engine):
    """Create a session for testing."""
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))
