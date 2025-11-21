from app.db.schema import get_session

def test_get_session():
    session_gen = get_session()
    session = next(session_gen)

    try:
        assert session.is_active
    finally:
        # Close the generator to trigger the finally block inside get_session
        # which ensures the session is closed
        session_gen.close()
