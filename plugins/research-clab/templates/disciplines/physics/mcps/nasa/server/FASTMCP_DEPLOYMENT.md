# FastMCP Cloud Deployment Guide

## Your GitHub Repository
✅ **Repository to be Created:** https://github.com/jezweb/nasa-mcp-server

## Step-by-Step Deployment to FastMCP Cloud

### 1. Sign in to FastMCP Cloud
1. Visit https://fastmcp.cloud
2. Click "Sign in with GitHub"
3. Authorize FastMCP to access your repositories

### 2. Create New Project
1. Click "Create Project" or "New Project"
2. You'll see a list of your GitHub repositories
3. Select **nasa-mcp-server** from the list

### 3. Configure Your Project

Fill in the following settings:

#### Basic Configuration:
- **Project Name:** `nasa-server` (or your preferred name)
- **Server Entrypoint:** `nasa_server.py`
- **Python Version:** 3.11 (or latest available)

#### Environment Variables (IMPORTANT):
Click "Add Environment Variable" and add:

| Variable Name | Value | Description |
|--------------|-------|-------------|
| `API_KEY` | `DEMO_KEY` | NASA API key (upgrade to personal key for better limits) |
| `DEFAULT_COUNT` | `10` | Default number of items to return |
| `CACHE_TTL_IMAGES` | `1800` | Cache duration for images (30 minutes) |
| `CACHE_TTL_DYNAMIC` | `600` | Cache duration for dynamic data (10 minutes) |
| `LOG_LEVEL` | `INFO` | Logging level |
| `MAX_HOURLY_CALLS` | `1000` | API rate limit for registered keys |
| `DEMO_HOURLY_LIMIT` | `30` | API rate limit for DEMO_KEY |

### 4. Deploy
1. Review your configuration
2. Click "Deploy"
3. Wait for the deployment to complete (usually 1-2 minutes)
4. You'll receive a URL like: `https://nasa-server.fastmcp.app/mcp`

### 5. Connect to Claude Desktop

#### Option A: Automatic Installation
```bash
fastmcp install claude-desktop https://nasa-server.fastmcp.app/mcp
```

#### Option B: Manual Configuration
1. Open Claude Desktop settings
2. Navigate to MCP Servers configuration
3. Add this configuration:

```json
{
  "mcpServers": {
    "nasa": {
      "url": "https://nasa-server.fastmcp.app/mcp",
      "transport": "http"
    }
  }
}
```

Replace `nasa-server` with your actual project name if different.

### 6. Verify Deployment

In Claude Desktop, test the connection:
```
"What's today's Astronomy Picture of the Day?"
```

The NASA server should respond with APOD content and imagery.

## Features Available After Deployment

Once deployed, you can use these commands in Claude:

### Astronomy & Space Content
- **Today's APOD:** "Show me today's astronomy picture"
- **Historical APOD:** "Get the APOD from July 20, 1969 (Apollo 11 landing)"
- **Random Discovery:** "Show me 5 random astronomy pictures"
- **NASA Media Search:** "Search NASA's library for images of Saturn"

### Mars Exploration
- **Current Rover Status:** "What's the latest from the Curiosity rover?"
- **Mars Photos:** "Show me recent Perseverance rover photos"
- **Mission Comparison:** "Compare photos from Curiosity and Perseverance"
- **Rover Capabilities:** "What cameras does the Curiosity rover have?"

### Asteroid Monitoring
- **Current Threats:** "What asteroids are approaching Earth this week?"
- **Hazardous Objects:** "Show me potentially hazardous asteroids in the next 30 days"
- **Asteroid Details:** "Look up asteroid 2022 AP7"
- **Space Safety:** "Are there any concerning asteroid approaches this month?"


### Comprehensive Analysis
- **Space Briefing:** "Give me today's space exploration update"
- **Mars Mission Report:** "Create a comprehensive report on Perseverance rover's mission"
- **Asteroid Watch:** "Generate an asteroid monitoring report for this month"
- **Educational Content:** "Analyze the current state of Mars exploration"

## Deployment Settings

### Automatic Features:
- ✅ Auto-deploy on push to main branch
- ✅ PR preview deployments  
- ✅ HTTPS/SSL included
- ✅ Global CDN distribution
- ✅ Automatic scaling
- ✅ Smart caching (30min images, 10min dynamic data)

### Management:
- View logs at: https://fastmcp.cloud/projects/nasa-server/logs
- Monitor usage at: https://fastmcp.cloud/projects/nasa-server/analytics
- Update environment variables without redeploying
- Monitor API rate limit usage

## Performance Optimization

### Caching Strategy:
- **Images (APOD, Mars photos):** 30 minutes cache
- **Dynamic data (asteroids, manifests):** 10 minutes cache
- **Static info (rover specs):** Long-term cache

### Rate Limit Management:
- **DEMO_KEY:** 30 calls/hour (sufficient for testing)
- **Personal Key:** 1,000 calls/hour (recommended for production)
- Server automatically tracks and warns at 90% usage

## Troubleshooting

### If deployment fails:
1. Check that `nasa_server.py` is in the root directory
2. Verify all dependencies are in `requirements.txt`
3. Check deployment logs for specific error messages
4. Ensure Python version compatibility (3.8+)

### If connection fails in Claude:
1. Ensure the URL ends with `/mcp`
2. Verify transport is set to `"http"`
3. Restart Claude Desktop after configuration changes
4. Check FastMCP Cloud deployment status

### API Key Issues:
- **DEMO_KEY Limits:** 30 requests/hour, 50/day per IP
- **Rate Limiting:** Server handles gracefully with caching
- **Upgrade Path:** Get free personal key at https://api.nasa.gov/
- **Environment Update:** Change API_KEY in FastMCP Cloud settings

### Common Issues:

#### "Tool not responding"
- Check API rate limits in server logs
- Verify NASA API service status
- Ensure proper environment variable configuration

#### "Cache issues"
- Cache automatically expires and refreshes
- Manual cache clear not needed - server handles automatically
- Monitor cache statistics via `nasa://cache/stats` resource

#### "Missing images/data"
- Some historical dates may not have APOD entries
- Mars rovers have different active periods

## NASA API Key Management

### Getting Your Own API Key:
1. Visit https://api.nasa.gov/
2. Click "Get Started" or "Generate API Key"
3. Fill out the simple form (name, email, intended use)
4. Receive key via email (usually within minutes)
5. Update `API_KEY` environment variable in FastMCP Cloud

### Benefits of Personal API Key:
- **1,000 requests/hour** vs 30 for DEMO_KEY
- **No daily IP-based limits**
- **Priority access** during high-traffic periods
- **Better performance** and reliability

### API Usage Monitoring:
- Check usage via `nasa://api/status` resource
- Server tracks daily/hourly usage automatically
- Warnings at 90% of rate limits
- Graceful degradation with caching

## Advanced Configuration

### Custom Caching:
```env
CACHE_TTL_IMAGES=3600      # 1 hour for images
CACHE_TTL_DYNAMIC=300      # 5 minutes for dynamic data
```

### Logging Levels:
- `DEBUG`: Detailed API call logging
- `INFO`: Standard operational logging (default)
- `WARNING`: Only warnings and errors
- `ERROR`: Error-only logging

### Performance Tuning:
```env
DEFAULT_COUNT=20           # Return more items by default
MAX_HOURLY_CALLS=2000     # If you have premium NASA API access
```

## Next Steps

1. **Customize:** Modify tools and add new NASA API endpoints
2. **Monitor:** Check usage statistics and performance metrics
3. **Optimize:** Adjust cache settings based on usage patterns
4. **Extend:** Add more space APIs or data sources
5. **Scale:** Upgrade to personal NASA API key for higher limits

## Support Resources

- **FastMCP Cloud:** https://docs.fastmcp.com
- **NASA API Docs:** https://api.nasa.gov/
- **Server Issues:** Check deployment logs in FastMCP Cloud dashboard
- **API Status:** https://api.nasa.gov/ (service status updates)

## Security & Best Practices

- ✅ No sensitive data stored in repository
- ✅ Environment variables properly configured
- ✅ Rate limiting and error handling
- ✅ Automatic HTTPS/SSL certificates
- ✅ Input validation and sanitization
- ✅ Comprehensive logging for debugging

---

**Your NASA MCP server is ready to explore the universe!** 🌌🚀

Connect to Claude Desktop and start asking about space exploration, Mars missions, asteroid tracking, and astronomy imagery. The server provides real-time access to NASA's vast collection of space data and imagery.

**Example first query:** "Show me today's astronomy picture and tell me about any asteroids approaching Earth this week."