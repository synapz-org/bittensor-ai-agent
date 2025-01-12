import pytest
import asyncio
from src.api.taostats import TaostatsAPI


@pytest.fixture
def api_client():
    return TaostatsAPI()


@pytest.mark.asyncio
async def test_get_subnet_metrics(api_client):
    # Test with subnet 1
    result = await api_client.get_subnet_metrics(1)
    assert result is not None
    print(f"Subnet Metrics: {result}")


@pytest.mark.asyncio
async def test_get_network_overview(api_client):
    result = await api_client.get_network_overview()
    assert result is not None
    print(f"Network Overview: {result}")


@pytest.mark.asyncio
async def test_get_subnet_validators(api_client):
    result = await api_client.get_subnet_validators(1)
    assert result is not None
    print(f"Subnet Validators: {result}")


if __name__ == "__main__":
    # Run tests directly
    api = TaostatsAPI()
    asyncio.run(test_get_subnet_metrics(api))
    asyncio.run(test_get_network_overview(api))
    asyncio.run(test_get_subnet_validators(api))


@pytest.mark.asyncio
async def test_get_current_block(api_client):
    result = await api_client.get_current_block()
    assert result is not None
    assert "blocks" in result
    print(f"Current Block: {result}")


@pytest.mark.asyncio
async def test_get_block_by_timestamp(api_client):
    # Get a timestamp range for the last minute
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=1)

    result = await api_client.get_block_by_timestamp(
        start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    assert result is not None
    assert "blocks" in result
    print(f"Block by Timestamp: {result}")
