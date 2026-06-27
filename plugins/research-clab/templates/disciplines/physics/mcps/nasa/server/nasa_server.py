"""
NASA MCP Server
==============
A comprehensive MCP server for NASA's open APIs.
Provides access to APOD, Mars rovers, asteroids, and NASA media library.
"""

import os
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from dotenv import load_dotenv
import httpx
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

# ============================================================================
# Configuration
# ============================================================================

class Config:
    """Configuration from environment variables."""
    
    # API Settings
    API_KEY = os.getenv("API_KEY", "DEMO_KEY")  # NASA API key
    BASE_URL = os.getenv("BASE_URL", "https://api.nasa.gov")
    
    # Default Settings
    DEFAULT_COUNT = int(os.getenv("DEFAULT_COUNT", "10"))  # Default image count
    
    # Cache Settings
    CACHE_TTL_IMAGES = int(os.getenv("CACHE_TTL_IMAGES", "1800"))  # 30 minutes for images
    CACHE_TTL_DYNAMIC = int(os.getenv("CACHE_TTL_DYNAMIC", "600"))   # 10 minutes for dynamic data
    
    # Server Settings
    SERVER_NAME = os.getenv("SERVER_NAME", "NASA MCP Server")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Rate Limiting
    MAX_HOURLY_CALLS = int(os.getenv("MAX_HOURLY_CALLS", "1000"))  # Registered API key limit
    DEMO_HOURLY_LIMIT = int(os.getenv("DEMO_HOURLY_LIMIT", "30"))   # DEMO_KEY limit

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ============================================================================
# Cache Implementation
# ============================================================================

class SimpleCache:
    """Simple in-memory cache with TTL."""
    
    def __init__(self, ttl_seconds: int = 600):
        self.cache = {}
        self.ttl = timedelta(seconds=ttl_seconds)
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired."""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                return data
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any):
        """Set cache value with timestamp."""
        self.cache[key] = (value, datetime.now())
    
    def clear(self):
        """Clear all cache entries."""
        self.cache.clear()
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        now = datetime.now()
        active = sum(1 for _, (_, ts) in self.cache.items() if now - ts < self.ttl)
        return {
            "total_entries": len(self.cache),
            "active_entries": active,
            "expired_entries": len(self.cache) - active,
            "ttl_seconds": self.ttl.total_seconds()
        }

# ============================================================================
# Server Creation
# ============================================================================

def create_nasa_server() -> FastMCP:
    """Create the NASA MCP server."""
    
    logger.info(f"Creating {Config.SERVER_NAME}")
    
    mcp = FastMCP(
        name=Config.SERVER_NAME,
        instructions="""
        NASA MCP Server providing comprehensive access to NASA's open APIs.
        
        Available tools:
        - get_apod: Today's Astronomy Picture of the Day
        - get_random_apod: Random APOD entries
        - get_apod_date_range: APOD entries for a date range
        - get_mars_photos_by_sol: Mars rover photos by Martian sol
        - get_mars_photos_by_date: Mars rover photos by Earth date
        - get_latest_mars_photos: Most recent Mars rover photos
        - get_rover_manifest: Mars rover mission details
        - get_asteroids_feed: Near Earth Objects feed (includes hazardous flag)
        - lookup_asteroid: Detailed asteroid information
        - browse_asteroids: Browse NEO database
        - search_nasa_media: Search NASA's media library
        
        Features:
        - Smart caching (30min for images, 10min for dynamic data)
        - Rate limit awareness
        - Support for all NASA rovers
        - Comprehensive asteroid tracking
        """
    )
    
    # Initialize caches with different TTLs
    image_cache = SimpleCache(ttl_seconds=Config.CACHE_TTL_IMAGES)
    dynamic_cache = SimpleCache(ttl_seconds=Config.CACHE_TTL_DYNAMIC)
    
    # HTTP client with timeout
    client = httpx.AsyncClient(
        timeout=30.0,
        headers={"User-Agent": "NASA-MCP-Server/1.0"}
    )
    
    # API call counter
    api_calls = {"count": 0, "hour": datetime.now().hour, "date": datetime.now().date()}
    
    def track_api_call():
        """Track API calls for rate limiting awareness."""
        now = datetime.now()
        
        # Reset hourly counter
        if now.hour != api_calls["hour"] or now.date() != api_calls["date"]:
            api_calls["count"] = 0
            api_calls["hour"] = now.hour
            api_calls["date"] = now.date()
        
        api_calls["count"] += 1
        
        # Warn when approaching limits
        limit = Config.DEMO_HOURLY_LIMIT if Config.API_KEY == "DEMO_KEY" else Config.MAX_HOURLY_CALLS
        if api_calls["count"] > limit * 0.9:
            logger.warning(f"Approaching API limit: {api_calls['count']}/{limit} calls this hour")
    
    # ========== APOD Tools ==========
    
    @mcp.tool
    async def get_apod(date: str = None) -> Dict[str, Any]:
        """
        Get NASA's Astronomy Picture of the Day.
        
        Args:
            date: Date in YYYY-MM-DD format (defaults to today)
        
        Returns:
            APOD data including image URL, explanation, and metadata
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        cache_key = f"apod:{date}"
        cached = image_cache.get(cache_key)
        if cached:
            logger.info(f"Returning cached APOD for {date}")
            return {"source": "cache", **cached}
        
        try:
            params = {"api_key": Config.API_KEY, "date": date}
            
            track_api_call()
            response = await client.get(f"{Config.BASE_URL}/planetary/apod", params=params)
            response.raise_for_status()
            data = response.json()
            
            result = {
                "date": data.get("date"),
                "title": data.get("title"),
                "explanation": data.get("explanation"),
                "url": data.get("url"),
                "hdurl": data.get("hdurl"),
                "media_type": data.get("media_type"),
                "service_version": data.get("service_version"),
                "copyright": data.get("copyright", "Public Domain"),
                "thumbnail_url": data.get("thumbnail_url") if data.get("media_type") == "video" else None
            }
            
            image_cache.set(cache_key, result)
            return {"source": "api", **result}
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                return {"error": f"No APOD available for date {date}. APOD started on 1995-06-16."}
            return {"error": f"API error: {e.response.status_code}"}
        except Exception as e:
            logger.error(f"Error fetching APOD: {e}")
            return {"error": str(e)}
    
    @mcp.tool
    async def get_random_apod(count: int = 1) -> Dict[str, Any]:
        """
        Get random APOD entries.
        
        Args:
            count: Number of random entries (1-100)
        
        Returns:
            List of random APOD entries
        """
        count = min(max(count, 1), 100)
        cache_key = f"apod_random:{count}"
        cached = dynamic_cache.get(cache_key)
        if cached:
            return {"source": "cache", **cached}
        
        try:
            params = {"api_key": Config.API_KEY, "count": count}
            
            track_api_call()
            response = await client.get(f"{Config.BASE_URL}/planetary/apod", params=params)
            response.raise_for_status()
            data = response.json()
            
            # Handle single vs multiple results
            if isinstance(data, dict):
                data = [data]
            
            result = {
                "count": len(data),
                "entries": data
            }
            
            dynamic_cache.set(cache_key, result)
            return {"source": "api", **result}
            
        except Exception as e:
            logger.error(f"Error fetching random APOD: {e}")
            return {"error": str(e)}
    
    @mcp.tool
    async def get_apod_date_range(
        start_date: str,
        end_date: str = None
    ) -> Dict[str, Any]:
        """
        Get APOD entries for a date range.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format (defaults to today)
        
        Returns:
            List of APOD entries for the date range
        """
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        # Limit range to prevent excessive API calls
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        if (end - start).days > 100:
            return {"error": "Date range too large. Maximum 100 days allowed."}
        
        cache_key = f"apod_range:{start_date}:{end_date}"
        cached = dynamic_cache.get(cache_key)
        if cached:
            return {"source": "cache", **cached}
        
        try:
            params = {
                "api_key": Config.API_KEY,
                "start_date": start_date,
                "end_date": end_date
            }
            
            track_api_call()
            response = await client.get(f"{Config.BASE_URL}/planetary/apod", params=params)
            response.raise_for_status()
            data = response.json()
            
            result = {
                "start_date": start_date,
                "end_date": end_date,
                "count": len(data),
                "entries": data
            }
            
            dynamic_cache.set(cache_key, result)
            return {"source": "api", **result}
            
        except Exception as e:
            logger.error(f"Error fetching APOD range: {e}")
            return {"error": str(e)}
    
    # ========== Mars Rover Photos Tools ==========
    
    @mcp.tool
    async def get_mars_photos_by_sol(
        rover: str = "perseverance",
        sol: int = 100,
        camera: str = None,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Get Mars rover photos by Martian sol (day).
        
        Args:
            rover: Rover name (curiosity, opportunity, spirit, perseverance)
            sol: Martian sol (0 to current)
            camera: Specific camera (FHAZ, RHAZ, MAST, CHEMCAM, NAVCAM, etc.)
            page: Page number for pagination
        
        Returns:
            Mars rover photos for the specified sol
        """
        rover = rover.lower()
        cache_key = f"mars_photos:{rover}:{sol}:{camera}:{page}"
        cached = image_cache.get(cache_key)
        if cached:
            return {"source": "cache", **cached}
        
        try:
            params = {
                "api_key": Config.API_KEY,
                "sol": sol,
                "page": page
            }
            
            if camera:
                params["camera"] = camera.upper()
            
            track_api_call()
            response = await client.get(
                f"{Config.BASE_URL}/mars-photos/api/v1/rovers/{rover}/photos",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            photos = []
            for photo in data.get("photos", [])[:25]:  # Limit to 25 photos
                photos.append({
                    "id": photo.get("id"),
                    "sol": photo.get("sol"),
                    "camera": {
                        "name": photo.get("camera", {}).get("name"),
                        "full_name": photo.get("camera", {}).get("full_name")
                    },
                    "img_src": photo.get("img_src"),
                    "earth_date": photo.get("earth_date"),
                    "rover": photo.get("rover", {}).get("name")
                })
            
            result = {
                "rover": rover,
                "sol": sol,
                "camera": camera,
                "page": page,
                "total_photos": len(photos),
                "photos": photos
            }
            
            image_cache.set(cache_key, result)
            return {"source": "api", **result}
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {"error": f"No photos found for rover '{rover}' on sol {sol}"}
            return {"error": f"API error: {e.response.status_code}"}
        except Exception as e:
            logger.error(f"Error fetching Mars photos: {e}")
            return {"error": str(e)}
    
    @mcp.tool
    async def get_mars_photos_by_date(
        rover: str = "curiosity",
        earth_date: str = None,
        camera: str = None,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Get Mars rover photos by Earth date.
        
        Args:
            rover: Rover name
            earth_date: Earth date in YYYY-MM-DD format
            camera: Specific camera
            page: Page number
        
        Returns:
            Mars rover photos for the specified date
        """
        if not earth_date:
            earth_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        rover = rover.lower()
        cache_key = f"mars_photos_date:{rover}:{earth_date}:{camera}:{page}"
        cached = image_cache.get(cache_key)
        if cached:
            return {"source": "cache", **cached}
        
        try:
            params = {
                "api_key": Config.API_KEY,
                "earth_date": earth_date,
                "page": page
            }
            
            if camera:
                params["camera"] = camera.upper()
            
            track_api_call()
            response = await client.get(
                f"{Config.BASE_URL}/mars-photos/api/v1/rovers/{rover}/photos",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            photos = []
            for photo in data.get("photos", [])[:25]:
                photos.append({
                    "id": photo.get("id"),
                    "sol": photo.get("sol"),
                    "camera": {
                        "name": photo.get("camera", {}).get("name"),
                        "full_name": photo.get("camera", {}).get("full_name")
                    },
                    "img_src": photo.get("img_src"),
                    "earth_date": photo.get("earth_date"),
                    "rover": photo.get("rover", {}).get("name")
                })
            
            result = {
                "rover": rover,
                "earth_date": earth_date,
                "camera": camera,
                "page": page,
                "total_photos": len(photos),
                "photos": photos
            }
            
            image_cache.set(cache_key, result)
            return {"source": "api", **result}
            
        except Exception as e:
            logger.error(f"Error fetching Mars photos by date: {e}")
            return {"error": str(e)}
    
    @mcp.tool
    async def get_latest_mars_photos(
        rover: str = "perseverance",
        camera: str = None
    ) -> Dict[str, Any]:
        """
        Get the most recent Mars rover photos.
        
        Args:
            rover: Rover name
            camera: Specific camera (optional)
        
        Returns:
            Latest available Mars rover photos
        """
        rover = rover.lower()
        cache_key = f"mars_photos_latest:{rover}:{camera}"
        cached = dynamic_cache.get(cache_key)
        if cached:
            return {"source": "cache", **cached}
        
        try:
            params = {"api_key": Config.API_KEY}
            if camera:
                params["camera"] = camera.upper()
            
            track_api_call()
            response = await client.get(
                f"{Config.BASE_URL}/mars-photos/api/v1/rovers/{rover}/latest_photos",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            photos = []
            for photo in data.get("latest_photos", [])[:25]:
                photos.append({
                    "id": photo.get("id"),
                    "sol": photo.get("sol"),
                    "camera": {
                        "name": photo.get("camera", {}).get("name"),
                        "full_name": photo.get("camera", {}).get("full_name")
                    },
                    "img_src": photo.get("img_src"),
                    "earth_date": photo.get("earth_date"),
                    "rover": photo.get("rover", {}).get("name")
                })
            
            result = {
                "rover": rover,
                "camera": camera,
                "latest_sol": photos[0]["sol"] if photos else None,
                "latest_date": photos[0]["earth_date"] if photos else None,
                "total_photos": len(photos),
                "photos": photos
            }
            
            dynamic_cache.set(cache_key, result)
            return {"source": "api", **result}
            
        except Exception as e:
            logger.error(f"Error fetching latest Mars photos: {e}")
            return {"error": str(e)}
    
    @mcp.tool
    async def get_rover_manifest(rover: str = "perseverance") -> Dict[str, Any]:
        """
        Get Mars rover mission manifest and details.
        
        Args:
            rover: Rover name
        
        Returns:
            Rover mission details including status, landing date, and photo counts
        """
        rover = rover.lower()
        cache_key = f"rover_manifest:{rover}"
        cached = dynamic_cache.get(cache_key)
        if cached:
            return {"source": "cache", **cached}
        
        try:
            params = {"api_key": Config.API_KEY}
            
            track_api_call()
            response = await client.get(
                f"{Config.BASE_URL}/mars-photos/api/v1/manifests/{rover}",
                params=params
            )
            response.raise_for_status()
            data = response.json().get("photo_manifest", {})
            
            result = {
                "name": data.get("name"),
                "landing_date": data.get("landing_date"),
                "launch_date": data.get("launch_date"),
                "status": data.get("status"),
                "max_sol": data.get("max_sol"),
                "max_date": data.get("max_date"),
                "total_photos": data.get("total_photos"),
                "recent_photos": data.get("photos", [])[-10:] if data.get("photos") else []
            }
            
            dynamic_cache.set(cache_key, result)
            return {"source": "api", **result}
            
        except Exception as e:
            logger.error(f"Error fetching rover manifest: {e}")
            return {"error": str(e)}
    
    # ========== Near Earth Objects (Asteroids) Tools ==========
    
    @mcp.tool
    async def get_asteroids_feed(
        start_date: str = None,
        end_date: str = None,
        detailed: bool = False
    ) -> Dict[str, Any]:
        """
        Get Near Earth Objects feed.
        
        Args:
            start_date: Start date in YYYY-MM-DD format (defaults to today)
            end_date: End date in YYYY-MM-DD format (defaults to 7 days from start)
            detailed: Include detailed orbital data
        
        Returns:
            Feed of asteroids approaching Earth
        """
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")
        
        if not end_date:
            end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=7)).strftime("%Y-%m-%d")
        
        # API limits to 7 days
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        if (end - start).days > 7:
            end_date = (start + timedelta(days=7)).strftime("%Y-%m-%d")
        
        cache_key = f"asteroids_feed:{start_date}:{end_date}:{detailed}"
        cached = dynamic_cache.get(cache_key)
        if cached:
            return {"source": "cache", **cached}
        
        try:
            params = {
                "api_key": Config.API_KEY,
                "start_date": start_date,
                "end_date": end_date,
                "detailed": str(detailed).lower()
            }
            
            track_api_call()
            response = await client.get(f"{Config.BASE_URL}/neo/rest/v1/feed", params=params)
            response.raise_for_status()
            data = response.json()
            
            # Process asteroid data
            asteroids_by_date = {}
            for date, asteroids in data.get("near_earth_objects", {}).items():
                asteroids_by_date[date] = []
                for neo in asteroids:
                    asteroid_info = {
                        "id": neo.get("id"),
                        "neo_reference_id": neo.get("neo_reference_id"),
                        "name": neo.get("name"),
                        "absolute_magnitude": neo.get("absolute_magnitude_h"),
                        "is_potentially_hazardous": neo.get("is_potentially_hazardous_asteroid"),
                        "estimated_diameter": {
                            "kilometers": neo.get("estimated_diameter", {}).get("kilometers", {}),
                            "meters": neo.get("estimated_diameter", {}).get("meters", {})
                        },
                        "close_approach": neo.get("close_approach_data", [{}])[0] if neo.get("close_approach_data") else {},
                        "nasa_jpl_url": neo.get("nasa_jpl_url")
                    }
                    
                    if detailed:
                        asteroid_info["orbital_data"] = neo.get("orbital_data", {})
                    
                    asteroids_by_date[date].append(asteroid_info)
            
            result = {
                "element_count": data.get("element_count"),
                "start_date": start_date,
                "end_date": end_date,
                "asteroids_by_date": asteroids_by_date,
                "links": data.get("links", {})
            }
            
            dynamic_cache.set(cache_key, result)
            return {"source": "api", **result}
            
        except Exception as e:
            logger.error(f"Error fetching asteroids feed: {e}")
            return {"error": str(e)}
    
    @mcp.tool
    async def lookup_asteroid(asteroid_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific asteroid.
        
        Args:
            asteroid_id: Asteroid SPK-ID or designation
        
        Returns:
            Detailed asteroid data including orbital parameters
        """
        cache_key = f"asteroid:{asteroid_id}"
        cached = image_cache.get(cache_key)
        if cached:
            return {"source": "cache", **cached}
        
        try:
            params = {"api_key": Config.API_KEY}
            
            track_api_call()
            response = await client.get(
                f"{Config.BASE_URL}/neo/rest/v1/neo/{asteroid_id}",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            result = {
                "id": data.get("id"),
                "neo_reference_id": data.get("neo_reference_id"),
                "name": data.get("name"),
                "designation": data.get("designation"),
                "absolute_magnitude": data.get("absolute_magnitude_h"),
                "estimated_diameter": {
                    "kilometers": data.get("estimated_diameter", {}).get("kilometers", {}),
                    "meters": data.get("estimated_diameter", {}).get("meters", {}),
                    "miles": data.get("estimated_diameter", {}).get("miles", {}),
                    "feet": data.get("estimated_diameter", {}).get("feet", {})
                },
                "is_potentially_hazardous": data.get("is_potentially_hazardous_asteroid"),
                "orbital_data": data.get("orbital_data", {}),
                "close_approach_data": [
                    {
                        "close_approach_date": approach.get("close_approach_date"),
                        "close_approach_date_full": approach.get("close_approach_date_full"),
                        "epoch_date_close_approach": approach.get("epoch_date_close_approach"),
                        "relative_velocity": approach.get("relative_velocity"),
                        "miss_distance": approach.get("miss_distance"),
                        "orbiting_body": approach.get("orbiting_body")
                    }
                    for approach in data.get("close_approach_data", [])[:10]  # Limit to 10 approaches
                ]
            }
            
            image_cache.set(cache_key, result)
            return {"source": "api", **result}
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {"error": f"Asteroid with ID '{asteroid_id}' not found"}
            return {"error": f"API error: {e.response.status_code}"}
        except Exception as e:
            logger.error(f"Error looking up asteroid: {e}")
            return {"error": str(e)}
    
    @mcp.tool
    async def browse_asteroids(page: int = 0, size: int = 20) -> Dict[str, Any]:
        """
        Browse the overall Near Earth Objects database.
        
        Args:
            page: Page number (0-based)
            size: Number of asteroids per page (max 20)
        
        Returns:
            Paginated list of Near Earth Objects
        """
        size = min(size, 20)  # API limitation
        cache_key = f"browse_asteroids:{page}:{size}"
        cached = dynamic_cache.get(cache_key)
        if cached:
            return {"source": "cache", **cached}
        
        try:
            params = {
                "api_key": Config.API_KEY,
                "page": page,
                "size": size
            }
            
            track_api_call()
            response = await client.get(f"{Config.BASE_URL}/neo/rest/v1/neo/browse", params=params)
            response.raise_for_status()
            data = response.json()
            
            asteroids = []
            for neo in data.get("near_earth_objects", []):
                asteroids.append({
                    "id": neo.get("id"),
                    "neo_reference_id": neo.get("neo_reference_id"),
                    "name": neo.get("name"),
                    "absolute_magnitude": neo.get("absolute_magnitude_h"),
                    "is_potentially_hazardous": neo.get("is_potentially_hazardous_asteroid"),
                    "nasa_jpl_url": neo.get("nasa_jpl_url"),
                    "estimated_diameter_km": {
                        "min": neo.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_min"),
                        "max": neo.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_max")
                    }
                })
            
            result = {
                "page": page,
                "size": size,
                "total_elements": data.get("page", {}).get("total_elements"),
                "total_pages": data.get("page", {}).get("total_pages"),
                "asteroids": asteroids,
                "links": data.get("links", {})
            }
            
            dynamic_cache.set(cache_key, result)
            return {"source": "api", **result}
            
        except Exception as e:
            logger.error(f"Error browsing asteroids: {e}")
            return {"error": str(e)}
    
    # ========== NASA Media Library Tools ==========
    
    @mcp.tool
    async def search_nasa_media(
        query: str,
        media_type: str = "image",
        page: int = 1,
        page_size: int = 100
    ) -> Dict[str, Any]:
        """
        Search NASA's image and video library.
        
        Args:
            query: Search terms
            media_type: Type of media (image, video, audio)
            page: Page number
            page_size: Results per page (max 100)
        
        Returns:
            NASA media search results with URLs and metadata
        """
        page_size = min(page_size, 100)
        cache_key = f"nasa_media:{query}:{media_type}:{page}:{page_size}"
        cached = dynamic_cache.get(cache_key)
        if cached:
            return {"source": "cache", **cached}
        
        try:
            params = {
                "q": query,
                "media_type": media_type,
                "page": page,
                "page_size": page_size
            }
            
            track_api_call()
            response = await client.get("https://images-api.nasa.gov/search", params=params)
            response.raise_for_status()
            data = response.json()
            
            collection = data.get("collection", {})
            items = []
            
            for item in collection.get("items", []):
                item_data = item.get("data", [{}])[0]
                links = item.get("links", [])
                
                # Get preview image URL
                preview_url = None
                original_url = None
                for link in links:
                    if link.get("rel") == "preview":
                        preview_url = link.get("href")
                    elif link.get("render") == "image":
                        original_url = link.get("href")
                
                # Get JSON manifest for additional media links
                href = item.get("href")
                
                items.append({
                    "nasa_id": item_data.get("nasa_id"),
                    "title": item_data.get("title"),
                    "description": item_data.get("description", "")[:500],  # Limit description length
                    "date_created": item_data.get("date_created"),
                    "center": item_data.get("center"),
                    "media_type": item_data.get("media_type"),
                    "keywords": item_data.get("keywords", [])[:10],  # Limit keywords
                    "preview_url": preview_url,
                    "original_url": original_url,
                    "manifest_url": href
                })
            
            result = {
                "query": query,
                "media_type": media_type,
                "page": page,
                "page_size": page_size,
                "total_hits": collection.get("metadata", {}).get("total_hits"),
                "items": items[:Config.DEFAULT_COUNT * 2]  # Reasonable limit
            }
            
            dynamic_cache.set(cache_key, result)
            return {"source": "api", **result}
            
        except Exception as e:
            logger.error(f"Error searching NASA media: {e}")
            return {"error": str(e)}
    
    # ========== Resources ==========
    
    @mcp.resource("nasa://api/status")
    def api_status() -> Dict[str, Any]:
        """Get API status and usage statistics."""
        limit = Config.DEMO_HOURLY_LIMIT if Config.API_KEY == "DEMO_KEY" else Config.MAX_HOURLY_CALLS
        
        return {
            "status": "operational",
            "api_key_type": "DEMO_KEY" if Config.API_KEY == "DEMO_KEY" else "REGISTERED",
            "hourly_limit": limit,
            "calls_this_hour": api_calls["count"],
            "calls_remaining": max(0, limit - api_calls["count"]),
            "cache_stats": {
                "image_cache": image_cache.stats(),
                "dynamic_cache": dynamic_cache.stats()
            },
            "timestamp": datetime.now().isoformat()
        }
    
    @mcp.resource("nasa://cache/stats")
    def cache_statistics() -> Dict[str, Any]:
        """Get detailed cache statistics."""
        return {
            "image_cache": image_cache.stats(),
            "dynamic_cache": dynamic_cache.stats(),
            "total_cached_items": len(image_cache.cache) + len(dynamic_cache.cache)
        }
    
    @mcp.resource("nasa://rovers/info")
    def rovers_info() -> Dict[str, Any]:
        """Information about Mars rovers."""
        return {
            "active_rovers": ["perseverance", "curiosity"],
            "completed_missions": ["opportunity", "spirit"],
            "rover_details": {
                "perseverance": {
                    "landing_date": "2021-02-18",
                    "landing_site": "Jezero Crater",
                    "status": "active",
                    "cameras": ["NAVCAM", "MASTCAM", "HAZCAM", "SHERLOC", "WATSON", "SUPERCAM", "PIXL"]
                },
                "curiosity": {
                    "landing_date": "2012-08-06",
                    "landing_site": "Gale Crater",
                    "status": "active",
                    "cameras": ["FHAZ", "RHAZ", "MAST", "CHEMCAM", "MAHLI", "MARDI", "NAVCAM"]
                },
                "opportunity": {
                    "landing_date": "2004-01-25",
                    "landing_site": "Meridiani Planum",
                    "status": "completed",
                    "mission_end": "2018-06-10",
                    "cameras": ["FHAZ", "RHAZ", "NAVCAM", "PANCAM", "MINITES"]
                },
                "spirit": {
                    "landing_date": "2004-01-04",
                    "landing_site": "Gusev Crater",
                    "status": "completed",
                    "mission_end": "2010-03-22",
                    "cameras": ["FHAZ", "RHAZ", "NAVCAM", "PANCAM", "MINITES"]
                }
            }
        }
    
    # ========== Prompts ==========
    
    @mcp.prompt("space_exploration_update")
    def space_exploration_prompt() -> str:
        """Generate a space exploration update prompt."""
        return """
        Please provide a comprehensive space exploration update:
        
        1. Get today's Astronomy Picture of the Day
        2. Check for any asteroids approaching Earth in the next 7 days
        3. Get the latest photos from the Perseverance rover
        4. Search for recent NASA mission updates
        
        Compile this into a brief but informative space exploration briefing.
        """
    
    @mcp.prompt("mars_mission_analysis")
    def mars_mission_prompt(rover: str = "perseverance") -> str:
        """Generate a Mars mission analysis prompt."""
        return f"""
        Analyze the {rover} Mars rover mission:
        
        1. Get the rover's mission manifest
        2. Retrieve the latest photos from the rover
        3. Get photos from different cameras to show variety
        4. Provide insights on the mission's progress and discoveries
        
        Focus on recent activities and scientific significance.
        """
    
    @mcp.prompt("asteroid_monitoring")
    def asteroid_monitoring_prompt(days: int = 30) -> str:
        """Generate an asteroid monitoring prompt."""
        return f"""
        Monitor potentially hazardous asteroids for the next {days} days:
        
        1. Get the asteroid feed for the coming period
        2. Identify any potentially hazardous asteroids
        3. For the closest approaches, look up detailed information
        4. Assess the risk level and provide context
        
        Present findings in order of closest approach distance.
        """
    
    logger.info(f"{Config.SERVER_NAME} created successfully")
    return mcp

# ============================================================================
# Main Execution
# ============================================================================

# Create server instance
mcp = create_nasa_server()

def main():
    """Main entry point."""
    import sys
    
    if "--test" in sys.argv:
        # Test mode
        import asyncio
        from fastmcp import Client
        
        async def test():
            async with Client(mcp) as client:
                print("Testing NASA MCP Server...")
                
                # List tools
                tools = await client.list_tools()
                print(f"\nAvailable tools: {[t.name for t in tools]}")
                
                # Test APOD
                result = await client.call_tool("get_apod", {})
                print(f"\nToday's APOD: {result.data.get('title', 'N/A')}")
                
                # List resources
                resources = await client.list_resources()
                print(f"\nAvailable resources: {[r.uri for r in resources]}")
        
        asyncio.run(test())
    else:
        # Run server
        transport = os.getenv("TRANSPORT", "stdio")
        if transport == "http":
            port = int(os.getenv("PORT", "8000"))
            mcp.run(transport="http", port=port)
        else:
            mcp.run(transport="stdio")

if __name__ == "__main__":
    main()