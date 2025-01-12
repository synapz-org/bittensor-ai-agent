import pytest
from src.api.taostats import TaostatsAPI


@pytest.mark.asyncio
async def test_api_connection():
    api = TaostatsAPI()
    # Test current block endpoint as it's a good baseline check
    result = await api.get_current_block()
    assert result is not None
    assert "data" in result
    print(f"API Connection Test Result: {result}")
