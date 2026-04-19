# MCP-SD / S2SP Website

Documentation website for **MCP-SD** (Selective Disclosure for MCP) and its reference implementation **S2SP** (Server-to-Server Protocol). Source: [python-sdk](https://github.com/mcp-sd/python-sdk).

Live at: **https://mcp-sd.github.io/**

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
