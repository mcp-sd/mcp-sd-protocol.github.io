# S2SP Protocol Website

Documentation website for the [S2SP (Server-to-Server Protocol)](https://github.com/s2sp-protocol/python-sdk) for MCP.

Live at: **https://s2sp-protocol.github.io/**

## Pages

- [Home](index.html) — overview, quick start, token savings
- [Introduction](docs/introduction.html) — concepts, architecture, flow
- [Protocol](docs/protocol.html) — data model, async/sync modes, security
- [SDK](docs/sdk.html) — API reference, resource/consumer tools
- [Demos](docs/demos.html) — weather agent demo
- [Tutorial](docs/tutorial.html) — Claude Desktop setup, video

## Development

```bash
# Serve locally
python -m http.server 8000

# Regenerate diagram images
pip install matplotlib numpy
python gen_web_images.py
```
