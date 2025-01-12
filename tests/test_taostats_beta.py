import pytest
from datetime import datetime, timedelta
from src.api.taostats import TaostatsAPI

pytest_plugins = ("pytest_asyncio",)
pytestmark = pytest.mark.asyncio(scope="function")


@pytest.fixture
def api_client():
    return TaostatsAPI()


@pytest.mark.asyncio
async def test_get_current_block(api_client):
    result = await api_client.get_current_block()
    assert result is not None
    assert "blocks" in result
    print(f"Current Block Info: {result}")


@pytest.mark.asyncio
async def test_get_block_range(api_client):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=1)
    result = await api_client.get_block_by_timestamp(
        start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    assert result is not None
    assert "blocks" in result
    print(f"Block Range Info: {result}")
