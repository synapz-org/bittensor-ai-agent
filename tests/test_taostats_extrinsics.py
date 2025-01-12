import pytest
from src.api.taostats import TaostatsAPI


@pytest.mark.asyncio
async def test_get_extrinsics():
    api = TaostatsAPI()
    # Test with a known coldkey address
    coldkey = "5F5CcZnp9VfqL5kpZskkHtQjueraN8LqHHHeBGkPHhDPBHiz"

    result = await api.get_extrinsics(signer_address=coldkey, limit=5)
    assert result is not None
    assert "data" in result
    print(f"Extrinsics Test Result: {result}")
