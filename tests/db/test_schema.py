import pytest

from app.db.schema import get_session

@pytest.mark.asyncio
async def test_get_session():
    async for session in get_session():
        assert session.is_active
