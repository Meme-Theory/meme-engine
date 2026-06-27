### NASA MCP — NASA Open APIs

Unified access to NASA's open APIs: APOD, Mars rover photos, Near Earth Objects, EPIC Earth imagery, and the NASA Image/Video Library. Bundled source at `tools/mcp-servers/nasa-mcp/nasa_server.py` after install.

**Tool groups:**

- **APOD** — Astronomy Picture of the Day: today, by date, by date range, random selection, HD image URLs.
- **Mars rover photos** — Curiosity, Perseverance, Opportunity, Spirit; query by sol or Earth date, filter by camera (FHAZ, RHAZ, MAST, CHEMCAM, etc.), get rover manifests.
- **Near Earth Objects** — asteroid approach feed, potentially-hazardous-asteroid flags, detailed orbital data, full catalog browse.
- **NASA media library** — search images and videos across all missions, historical mission photography, educational content.

**API key:**

All tools support `DEMO_KEY` at low rate limits (30 requests/hour/IP). For real work, get a key at <https://api.nasa.gov> (free, no credit card) and set `NASA_API_KEY` in your shell or Claude Code env. The `.mcp.json` fragment reads `${NASA_API_KEY:-DEMO_KEY}` so the default works out of the box.

**Guidance:**

- APOD images are public; NEO orbital data is public; neither needs attribution beyond "NASA / JPL / relevant mission."
- Rover photos are high-resolution — cache downloads under `tools/mcp-servers/nasa-mcp/cache/` or a project-chosen directory.
- The demo key rate limit is tight. If you see 429 errors, register for a real key rather than retrying.
