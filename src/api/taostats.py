import os
import logging
import asyncio
import aiohttp
from typing import Dict, List
from datetime import datetime
from dotenv import load_dotenv
from substrateinterface.utils.ss58 import ss58_encode
from urllib.parse import quote


class TaostatsAPI:
    def __init__(self):
        load_dotenv("config/.env")
        self.api_key = os.getenv("TAOSTATS_API_KEY")
        self.base_url = "https://api.taostats.io/api"
        self.headers = {"accept": "application/json", "Authorization": self.api_key}

    async def get_current_block(self) -> Dict:
        endpoint = "/block/v1?limit=1"
        return await self._make_request("GET", endpoint)

    async def get_metagraph_history(
        self, block_start: int, block_end: int, page: int = 1, limit: int = 200
    ) -> Dict:
        endpoint = f"/metagraph/root/history/v1?block_start={block_start}&block_end={block_end}&page={page}&limit={limit}"
        return await self._make_request("GET", endpoint)

    @staticmethod
    def parse_timestamp(timestamp: str) -> datetime:
        """Handle both timestamp formats from the chain."""
        try:
            return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

    async def get_block_by_timestamp(
        self, timestamp_start: str, timestamp_end: str
    ) -> Dict:
        encoded_start = quote(timestamp_start)
        encoded_end = quote(timestamp_end)
        endpoint = (
            f"/block?timestamp_start={encoded_start}×tamp_end={encoded_end}&limit=1"
        )
        return await self._make_request("GET", endpoint)

    async def get_subnet_metrics(self, subnet_id: int) -> Dict:
        """Fetch current metrics for a specific subnet."""
        endpoint = f"/subnets/{subnet_id}/metrics"
        return await self._make_request("GET", endpoint)

    async def get_validator_stats(self, validator_address: str) -> Dict:
        """Fetch detailed statistics for a validator."""
        endpoint = f"/validators/{validator_address}/stats"
        return await self._make_request("GET", endpoint)

    async def get_network_overview(self) -> Dict:
        """Fetch network-wide statistics and metrics."""
        endpoint = "/network/overview"
        return await self._make_request("GET", endpoint)

    async def get_subnet_validators(self, subnet_id: int) -> List[Dict]:
        """Fetch list of validators for a specific subnet."""
        endpoint = f"/subnets/{subnet_id}/validators"
        return await self._make_request("GET", endpoint)

    async def _make_request(
        self, method: str, endpoint: str, max_retries: int = 3, **kwargs
    ) -> Dict:
        url = f"{self.base_url}{endpoint}"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            for attempt in range(max_retries):
                try:
                    async with session.request(method, url, **kwargs) as response:
                        response.raise_for_status()
                        return await response.json()
                except aiohttp.ClientError as e:
                    if attempt == max_retries - 1:
                        logging.error(
                            f"API request failed after {max_retries} attempts: {e}"
                        )
                        raise
                    await asyncio.sleep(1 * (attempt + 1))

    async def get_historical_data(
        self, subnet_id: int, start_time: int, end_time: int
    ) -> List[Dict]:
        """Fetch historical metrics for a subnet within a time range."""
        endpoint = f"/subnets/{subnet_id}/historical"
        params = {"start_time": start_time, "end_time": end_time}
        return await self._make_request("GET", endpoint, params=params)

    @staticmethod
    def convert_address(address: str) -> str:
        """Convert hex address to SS58 format."""
        address_bytes = bytes.fromhex(address[2:])
        return ss58_encode(address_bytes)

    async def get_extrinsics(
        self, signer_address: str, page: int = 1, limit: int = 200
    ) -> Dict:
        """Fetch extrinsics for a given address with pagination."""
        endpoint = (
            f"/extrinsic/v1?signer_address={signer_address}&page={page}&limit={limit}"
        )
        return await self._make_request("GET", endpoint)

    async def get_neuron_deregistration(
        self, netuid: int, hotkey: str, block_start: int
    ) -> Dict:
        """Get neuron deregistration information."""
        endpoint = f"/v1/subnet/neuron/deregistration?netuid={netuid}&hotkey={hotkey}&block_start={block_start}&limit=1&order=timestamp_asc"
        return await self._make_request("GET", endpoint)

    async def get_price_history(
        self, asset: str, timestamp_start: str, timestamp_end: str
    ) -> Dict:
        """Get historical price data."""
        endpoint = f"/price/history/v1?asset={asset}×tamp_start={timestamp_start}×tamp_end={timestamp_end}&limit=1&order=timestamp_asc"
        return await self._make_request("GET", endpoint)
