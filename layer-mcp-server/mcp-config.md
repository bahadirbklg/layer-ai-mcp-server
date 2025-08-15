# MCP Configuration Guide

## Quick Setup for MCP Clients

This guide helps you configure the Layer.ai MCP Server with various MCP-compatible clients for seamless AI asset generation.

## Prerequisites

1. **MCP-compatible client** (Claude Desktop, etc.)
2. **Python 3.10+** available in your system PATH
3. **Layer.ai account** with API access

## Installation

### 1. Install the Server
```bash
git clone https://github.com/bahadirbklg/layer-ai-mcp-server.git
cd layer-ai-mcp-server
./install.sh
```

### 2. Set Up Credentials
```bash
python layer-mcp-server/setup.py
```

### 3. Configure Your MCP Client

#### For Claude Desktop

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "layer-ai": {
      "command": "python",
      "args": ["path/to/layer-mcp-server/server.py"],
      "env": {
        "LAYER_API_TOKEN": "pat_your_token_here",
        "LAYER_WORKSPACE_ID": "your_workspace_id"
      }
    }
  }
}
```

#### For Other MCP Clients

Use this general configuration pattern:

```json
{
  "name": "layer-ai",
  "command": "python",
  "args": ["path/to/layer-mcp-server/server.py"],
  "environment": {
    "LAYER_API_TOKEN": "pat_your_token_here",
    "LAYER_WORKSPACE_ID": "your_workspace_id"
  }
}
```

## Usage

### Available Tools

1. **create_asset** - Generate 2D game assets
2. **get_workspace_info** - Check workspace status
3. **remove_background** - AI background removal (in development)
4. **describe_image** - AI image analysis (in development)
5. **generate_prompt** - Prompt optimization (in development)

### Example Usage

```
Generate a pixel art character for my platformer game
```

The MCP server will:
1. Process your request
2. Generate the asset using Layer.ai
3. Save it to your assets directory
4. Provide the file path and details

## Troubleshooting

### Common Issues

**"Server not found"**
- Check the file path in your MCP configuration
- Ensure Python is in your system PATH
- Verify the server.py file exists

**"Authentication failed"**
- Run the credential setup: `python layer-mcp-server/setup.py`
- Check your API token at https://app.layer.ai/settings/api-keys
- Verify workspace ID in Layer.ai dashboard

**"Tool not found"**
- Restart your MCP client
- Check server logs for errors
- Verify the server started successfully

**"Generation failed"**
- Check your Layer.ai quota (600 assets on free tier)
- Verify internet connection
- Check Layer.ai service status

### Restart MCP Server

1. Close your MCP client
2. Restart the client application
3. The server will reconnect automatically

### Configuration Validation

```bash
# Test server connection
python layer-mcp-server/server.py --test

# Verify credentials
python layer-mcp-server/setup.py --verify
```

## Advanced Configuration

### Environment Variables

You can set these in your MCP client configuration:

- `LAYER_API_TOKEN` - Your Layer.ai API token (required)
- `LAYER_WORKSPACE_ID` - Your workspace ID (required)
- `LAYER_API_BASE_URL` - API endpoint (optional)
- `LAYER_DEFAULT_SAVE_DIR` - Asset save directory (optional)

### Timeout Settings

For complex asset generation, increase timeout in your MCP client:

```json
{
  "mcpServers": {
    "layer-ai": {
      "command": "python",
      "args": ["path/to/layer-mcp-server/server.py"],
      "timeout": 180,
      "env": {
        "LAYER_API_TOKEN": "pat_your_token_here"
      }
    }
  }
}
```

## Security

- API tokens are encrypted and stored locally
- No credentials are sent to version control
- Secure file permissions (600) on credential files
- Local-only credential storage

## Additional Resources

- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [Layer.ai API Documentation](https://docs.layer.ai)
- [Layer.ai Platform](https://app.layer.ai)