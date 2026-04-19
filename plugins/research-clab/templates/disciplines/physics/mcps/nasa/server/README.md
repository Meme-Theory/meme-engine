# NASA MCP Server

A comprehensive Model Context Protocol (MCP) server providing access to NASA's open APIs, including astronomy imagery, Mars rover photos, asteroid tracking, Earth observations, and NASA's media library.

## ✨ Features

### 🌌 **Astronomy Picture of the Day (APOD)**
- Daily astronomy images with scientific explanations
- Historical APOD lookup by date or date range
- Random APOD discovery
- High-resolution image support

### 🚀 **Mars Rover Photos**
- Photos from all active and historical rovers (Curiosity, Perseverance, Opportunity, Spirit)
- Search by Martian sol (day) or Earth date
- Multiple camera support (FHAZ, RHAZ, MAST, CHEMCAM, etc.)
- Latest mission updates and rover manifests

### ☄️ **Near Earth Objects (Asteroids)**
- Real-time asteroid approach tracking
- Potentially hazardous asteroid identification
- Detailed orbital and physical characteristics
- Comprehensive asteroid database browsing

### 📸 **NASA Media Library**
- Search NASA's vast image and video collection
- High-resolution space imagery
- Historical mission photography
- Educational content discovery

### 🚄 **Performance & Reliability**
- Smart caching (30min for images, 10min for dynamic data)
- Rate limit awareness and management
- Comprehensive error handling
- Multi-tier caching strategy

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- NASA API key (get free at [api.nasa.gov](https://api.nasa.gov/))
- pip or uv package manager

### Installation

1. **Clone the project:**
```bash
git clone https://github.com/jezweb/nasa-mcp-server.git
cd nasa-mcp-server
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your NASA API key
```

4. **Run the server:**
```bash
# STDIO transport (default)
python nasa_server.py

# HTTP transport
TRANSPORT=http PORT=8000 python nasa_server.py

# Development with FastMCP
fastmcp dev nasa_server.py

# Test the server
python nasa_server.py --test
```

## 🛠 Available Tools

### APOD Tools

#### `get_apod`
Get today's Astronomy Picture of the Day or specific date.

**Parameters:**
- `date_str` (optional): Date in YYYY-MM-DD format
- `hd` (bool): Request high-definition image URL (default: true)
- `include_concepts` (bool): Include concept tags (default: false)

**Example:**
```json
{
  "date_str": "2024-01-15",
  "hd": true,
  "include_concepts": false
}
```

#### `get_random_apod`
Get random APOD images for discovery.

**Parameters:**
- `count` (int): Number of random images (1-100, default: 5)

#### `get_apod_date_range`
Get APOD images for a date range.

**Parameters:**
- `start_date` (str): Start date in YYYY-MM-DD format
- `end_date` (str): End date in YYYY-MM-DD format (max 7 days)
- `hd` (bool): Request high-definition images (default: true)

### Mars Rover Tools

#### `get_mars_photos_by_sol`
Get Mars rover photos by Martian sol (day).

**Parameters:**
- `rover` (str): Rover name (curiosity, perseverance, opportunity, spirit)
- `sol` (int): Martian sol number (default: 1000)
- `camera` (optional): Camera abbreviation (fhaz, rhaz, mast, chemcam, etc.)
- `page` (int): Page number for pagination (default: 1)

**Example:**
```json
{
  "rover": "curiosity",
  "sol": 3000,
  "camera": "mast"
}
```

#### `get_mars_photos_by_date`
Get Mars rover photos by Earth date.

**Parameters:**
- `rover` (str): Rover name (default: "curiosity")
- `earth_date` (optional): Date in YYYY-MM-DD format (defaults to today)
- `camera` (optional): Camera abbreviation

#### `get_latest_mars_photos`
Get the latest photos from a Mars rover.

**Parameters:**
- `rover` (str): Rover name (default: "curiosity")
- `camera` (optional): Camera abbreviation

#### `get_rover_manifest`
Get Mars rover mission information and photo availability.

**Parameters:**
- `rover` (str): Rover name (default: "curiosity")

### Asteroid Tools

#### `get_asteroids_feed`
Get asteroids approaching Earth within a date range.

**Parameters:**
- `start_date` (optional): Start date in YYYY-MM-DD format (defaults to today)
- `end_date` (optional): End date in YYYY-MM-DD format (max 7 days from start)
- `detailed` (bool): Include detailed orbital data (default: false)

**Example:**
```json
{
  "start_date": "2024-08-18",
  "end_date": "2024-08-25",
  "detailed": true
}
```

#### `lookup_asteroid`
Look up specific asteroid by NASA JPL ID.

**Parameters:**
- `asteroid_id` (str): NASA JPL small body database ID

#### `browse_asteroids`
Browse the Near Earth Objects database.

**Parameters:**
- `page` (int): Page number (0-based, default: 0)
- `size` (int): Results per page (max 20, default: 20)

### NASA Media Tools

#### `search_nasa_media`
Search NASA's image and video library.

**Parameters:**
- `query` (str): Search terms
- `media_type` (str): Type of media (image, video, audio) (default: "image")
- `page` (int): Page number (default: 1)
- `page_size` (int): Results per page (max 100, default: 100)

**Example:**
```json
{
  "query": "apollo moon landing",
  "media_type": "image",
  "page": 1,
  "page_size": 20
}
```

## 📋 Resources

### `nasa://api/status`
Get API status, usage statistics, and rate limiting information.

### `nasa://cache/stats`
Get cache performance statistics for both image and dynamic caches.

### `nasa://rovers/info`
Get detailed information about all Mars rovers, their cameras, and capabilities.

## 🎯 Prompts

### `space_exploration`
Generate comprehensive space exploration analysis for any topic.

**Parameters:**
- `topic` (str): Space exploration topic to analyze

### `mars_mission_report`
Create detailed Mars rover mission reports.

**Parameters:**
- `rover` (str): Rover name (default: "curiosity")

### `asteroid_watch`
Generate asteroid monitoring and threat assessment reports.

**Parameters:**
- `days_ahead` (int): Days to monitor (default: 30)

### `daily_space_brief`
Generate comprehensive daily space exploration briefings.

## ⚙️ Configuration

Edit the `.env` file to customize server behavior:

```env
# API Configuration
API_KEY=your_nasa_api_key_here
DEFAULT_COUNT=10

# Cache Settings
CACHE_TTL_IMAGES=1800      # 30 minutes
CACHE_TTL_DYNAMIC=600      # 10 minutes

# Rate Limiting
MAX_HOURLY_CALLS=1000      # For registered API keys
DEMO_HOURLY_LIMIT=30       # For DEMO_KEY

# Server Settings
LOG_LEVEL=INFO
TRANSPORT=stdio
PORT=8000
```

### NASA API Key

1. **Free Tier (DEMO_KEY):** 30 requests/hour, 50/day per IP
2. **Registered Key:** 1,000 requests/hour (free signup at [api.nasa.gov](https://api.nasa.gov/))

## 🚀 Deployment

### Local Installation (Claude Desktop)

```bash
fastmcp install claude-desktop nasa_server.py
```

### FastMCP Cloud Deployment

1. **Create GitHub repository:**
```bash
git init
git add .
git commit -m "NASA MCP Server"
gh repo create nasa-mcp-server --public
git push -u origin main
```

2. **Deploy on [fastmcp.cloud](https://fastmcp.cloud):**
   - Sign in with GitHub
   - Create new project from repository
   - Set entrypoint: `nasa_server.py`
   - Add environment variables from `.env`
   - Deploy

3. **Connect to Claude Desktop:**
```json
{
  "mcpServers": {
    "nasa": {
      "url": "https://your-project.fastmcp.app/mcp",
      "transport": "http"
    }
  }
}
```

## 📚 Usage Examples

### Space Exploration Analysis
```
"Analyze the current status of Mars exploration missions and show me recent rover discoveries."
```

### Asteroid Monitoring
```
"What potentially hazardous asteroids are approaching Earth in the next 30 days?"
```

### Daily Space Brief
```
"Give me today's space exploration update including APOD, Mars photos, and Earth imagery."
```

### Historical Space Events
```
"Show me APOD images from the Apollo 11 anniversary week in July 2019."
```

### Mars Mission Comparison
```
"Compare the latest photos from Curiosity and Perseverance rovers, what are they currently investigating?"
```

### Educational Content
```
"Search NASA's media library for educational content about black holes and show me the most relevant images."
```

## 🔧 Development

### Testing
```bash
# Run test mode
python nasa_server.py --test

# Test with FastMCP client
fastmcp dev nasa_server.py
```

### Logging
Enable debug logging in `.env`:
```env
LOG_LEVEL=DEBUG
```

### Adding New Features

The server is modular and extensible:

1. Add new tools by creating `@mcp.tool` decorated functions
2. Add new resources using `@mcp.resource(uri)` decorators
3. Add new prompts using `@mcp.prompt(name)` decorators
4. Update configuration in `Config` class
5. Add caching strategy for new endpoints

## 🚨 Rate Limits & Best Practices

- **DEMO_KEY:** 30 requests/hour, 50/day per IP address
- **Registered Key:** 1,000 requests/hour
- **Caching:** 30 minutes for images, 10 minutes for dynamic data
- **Batch Requests:** Use date ranges and pagination wisely
- **Error Handling:** Server gracefully handles API limits and errors

## 📖 API Documentation

- [NASA Open APIs](https://api.nasa.gov/)
- [APOD API Documentation](https://github.com/nasa/apod-api)
- [Mars Rover Photos API](https://api.nasa.gov/)
- [NeoWs API Documentation](https://api.nasa.gov/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- [NASA API Documentation](https://api.nasa.gov/)
- [FastMCP Documentation](https://docs.fastmcp.com)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [GitHub Issues](https://github.com/jezweb/nasa-mcp-server/issues)

---

**Explore the universe with NASA's data!** 🌌🚀✨