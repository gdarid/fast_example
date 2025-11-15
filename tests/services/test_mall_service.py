from app.services.account_service import AccountService
from app.services.mall_service import MallService
from tests.set_test_db import TestingSessionLocal

from sqlalchemy.exc import IntegrityError


def test_mall_create_ko(monkeypatch):
    def mock_commit():
        raise IntegrityError(statement=None, params=None, orig=None)

    session = TestingSessionLocal()
    account_service = AccountService(session=session)
    service = MallService(session=session)

    account = account_service.create_account(name="Account for mall 1")
    account_id = account.id

    # apply the monkeypatch for the commit function
    monkeypatch.setattr(session, "commit", mock_commit)

    mall_new = service.create_mall(name="Mall KO", owner_id=account_id)
    assert mall_new is None

def test_mall_create_and_update_ko(monkeypatch):
    def mock_commit():
        raise IntegrityError(statement=None, params=None, orig=None)

    session = TestingSessionLocal()
    account_service = AccountService(session=session)
    service = MallService(session=session)

    account = account_service.create_account(name="Account for mall 2")
    account_id = account.id

    mall_new = service.create_mall(name="Mall KO for update", owner_id=account_id)
    id_new = mall_new.id

    # apply the monkeypatch for the commit function
    monkeypatch.setattr(session, "commit", mock_commit)

    update_result = service.update_mall(mall_id=id_new, name="New name", owner_id=None)

    assert update_result is None
