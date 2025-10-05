import httpx
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta, timezone
import hashlib
import gzip
import json

logger = logging.getLogger(__name__)

class SchedulesDirectClient:
    """Client for Schedules Direct JSON API"""
    
    def __init__(self, base_url: str, app_id: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.app_id = app_id or "sd-browser"
        self.session = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "User-Agent": f"{self.app_id}/1.0",
                "Accept": "application/json",
                "Accept-Encoding": "gzip"
            }
        )
    
    async def close(self):
        """Close the HTTP session"""
        await self.session.aclose()
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with retry logic"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        for attempt in range(3):
            try:
                response = await self.session.request(method, url, **kwargs)
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    logger.warning(f"Rate limited, waiting {retry_after}s")
                    await asyncio.sleep(retry_after)
                    continue
                
                # Handle server errors with exponential backoff
                if response.status_code >= 500:
                    wait_time = (2 ** attempt) * 1
                    logger.warning(f"Server error {response.status_code}, retrying in {wait_time}s")
                    await asyncio.sleep(wait_time)
                    continue
                
                response.raise_for_status()
                
                # Handle gzipped responses
                content = response.content
                if response.headers.get("Content-Encoding") == "gzip":
                    content = gzip.decompress(content)
                
                return json.loads(content.decode("utf-8"))
                
            except httpx.TimeoutException:
                if attempt == 2:  # Last attempt
                    raise
                wait_time = (2 ** attempt) * 1
                logger.warning(f"Timeout, retrying in {wait_time}s")
                await asyncio.sleep(wait_time)
            
            except httpx.HTTPStatusError as e:
                if e.response.status_code < 500:
                    raise  # Don't retry client errors
                if attempt == 2:  # Last attempt
                    raise
                wait_time = (2 ** attempt) * 1
                logger.warning(f"HTTP error {e.response.status_code}, retrying in {wait_time}s")
                await asyncio.sleep(wait_time)
        
        raise Exception("Max retries exceeded")
    
    async def authenticate(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate with Schedules Direct"""
        # Hash password as required by SD API
        password_hash = hashlib.sha1(password.encode()).hexdigest()
        
        data = {
            "username": username,
            "password": password_hash
        }
        
        response = await self._request("POST", "/token", json=data)
        
        if response.get("code") != 0:
            raise Exception(f"Authentication failed: {response.get('message', 'Unknown error')}")
        
        token = response.get("token")
        if not token:
            raise Exception("No token received")
        
        # Token typically expires in 24 hours
        expires_at = datetime.now(timezone.utc) + timedelta(hours=23)
        
        return {
            "token": token,
            "expires_at": expires_at
        }
    
    async def get_lineups(self, token: str) -> List[Dict[str, Any]]:
        """Get available lineups for the authenticated user"""
        headers = {"token": token}
        response = await self._request("GET", "/lineups", headers=headers)
        return response.get("lineups", [])
    
    async def get_lineup_details(self, token: str, lineup_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific lineup"""
        headers = {"token": token}
        response = await self._request("GET", f"/lineups/{lineup_id}", headers=headers)
        return response
    
    async def get_stations_for_lineup(self, token: str, lineup_id: str) -> List[Dict[str, Any]]:
        """Get stations for a specific lineup"""
        lineup_details = await self.get_lineup_details(token, lineup_id)
        return lineup_details.get("stations", [])
    
    async def get_programs(self, token: str, program_ids: List[str]) -> List[Dict[str, Any]]:
        """Get program details for multiple program IDs"""
        if not program_ids:
            return []
        
        headers = {"token": token}
        data = program_ids
        
        response = await self._request("POST", "/programs", headers=headers, json=data)
        return response if isinstance(response, list) else []
    
    async def get_schedules(self, token: str, station_ids: List[str], start_date: str, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get schedules for stations within a date range"""
        if not station_ids:
            return []
        
        headers = {"token": token}
        
        # Prepare request data
        data = []
        for station_id in station_ids:
            entry = {"stationID": station_id}
            if end_date:
                entry["date"] = [start_date, end_date]
            else:
                entry["date"] = [start_date]
            data.append(entry)
        
        response = await self._request("POST", "/schedules", headers=headers, json=data)
        return response if isinstance(response, list) else []
    
    async def get_program_images(self, token: str, program_id: str) -> List[Dict[str, Any]]:
        """Get images for a specific program"""
        headers = {"token": token}
        response = await self._request("GET", f"/metadata/programs/{program_id}", headers=headers)
        return response.get("data", {}).get("images", [])
    
    async def batch_get_images(self, token: str, program_ids: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Get images for multiple programs"""
        if not program_ids:
            return {}
        
        headers = {"token": token}
        data = program_ids
        
        try:
            response = await self._request("POST", "/metadata/programs", headers=headers, json=data)
            
            result = {}
            for item in response:
                program_id = item.get("programID")
                if program_id:
                    result[program_id] = item.get("data", {}).get("images", [])
            
            return result
        except Exception as e:
            logger.error(f"Failed to batch get images: {e}")
            return {}
    
    async def get_status(self, token: str) -> Dict[str, Any]:
        """Get account status and quota information"""
        headers = {"token": token}
        response = await self._request("GET", "/status", headers=headers)
        return response