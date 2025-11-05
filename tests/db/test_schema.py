from app.db.schema import get_session

def test_get_session():
    session = get_session()
    my_session = next(session)
    assert my_session.is_active
