from app.services.account_service import AccountService
from tests.set_test_db import TestingSessionLocal

from sqlalchemy.exc import IntegrityError


def test_account_create_ko(monkeypatch):
    def mock_commit():
        raise IntegrityError(statement=None, params=None, orig=None)

    session = TestingSessionLocal()
    service = AccountService(session=session)

    # apply the monkeypatch for the commit function
    monkeypatch.setattr(session, "commit", mock_commit)

    account_new = service.create_account(name="Account KO")
    assert account_new is None

def test_account_create_and_update_ko(monkeypatch):
    def mock_commit():
        raise IntegrityError(statement=None, params=None, orig=None)

    session = TestingSessionLocal()
    service = AccountService(session=session)

    account_new = service.create_account(name="Account KO for update")
    id_new = account_new.id

    # apply the monkeypatch for the commit function
    monkeypatch.setattr(session, "commit", mock_commit)

    update_result = service.update_account(account_id=id_new, name="New name")

    assert update_result is None
