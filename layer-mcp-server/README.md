# Layer.ai MCP Server

A complete Model Context Protocol (MCP) server for generating 2D game assets using Layer.ai's platform. Perfect for game developers who want to create sprites, characters, and other 2D assets directly from their development environment.

## 🎮 Features

- **🎨 Asset Generation**: Generate 2D game assets using Layer.ai Forge
- **✨ Prompt Optimization**: Optimize prompts with Layer.ai Prompt Genie
- **📊 Usage Tracking**: Monitor usage against free tier limits (600 assets)
- **📁 Workspace Management**: Export and manage workspace data
- **🔧 Asset Refinement**: Refine and modify existing assets
- **💾 Auto-Save**: Automatically save generated assets to your project
- **⚡ Error Handling**: Robust error handling with automatic retries
- **🔒 Quota Protection**: Prevents exceeding your free tier limit

## 🚀 Installation

```bash
# Clone or download the project
cd layer-mcp-server

# Install the package
pip install -e .

# Install test dependencies (optional)
pip install -e ".[test]"
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Required: Your Layer.ai API token
LAYER_API_TOKEN=pat_your_token_here

# Optional: API base URL (defaults to https://api.layer.ai)
LAYER_API_BASE_URL=https://api.layer.ai

# Optional: Usage tracking file (defaults to .layer_usage.json)
LAYER_USAGE_FILE=.layer_usage.json

# Optional: Default save directory (defaults to ./assets)
LAYER_DEFAULT_SAVE_DIR=./assets

# Optional: Default workspace ID
LAYER_WORKSPACE_ID=your_workspace_id
```

### Getting Your API Token

1. Sign up at [Layer.ai](https://layer.ai)
2. Go to your account settings
3. Generate a new API token (starts with `pat_`)
4. Copy the token to your `.env` file

### 🔌 MCP Client Configuration

To use this server with MCP clients like Kiro, Claude Desktop, or other MCP-compatible tools, you need to add it to your MCP configuration.

#### For Kiro IDE

Add to your workspace `.kiro/settings/mcp.json` or user-level `~/.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "layer-ai": {
      "command": "python",
      "args": ["-m", "layer_mcp_server.server"],
      "env": {
        "LAYER_API_TOKEN": "pat_your_token_here"
      },
      "disabled": false,
      "autoApprove": [
        "get_usage_info"
      ]
    }
  }
}
```

**Alternative (if layer-mcp-server command is in PATH):**
```json
{
  "mcpServers": {
    "layer-ai": {
      "command": "layer-mcp-server",
      "env": {
        "LAYER_API_TOKEN": "pat_your_token_here"
      },
      "disabled": false,
      "autoApprove": [
        "get_usage_info"
      ]
    }
  }
}
```

#### For Claude Desktop

Add to your Claude Desktop MCP configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "layer-ai": {
      "command": "layer-mcp-server",
      "env": {
        "LAYER_API_TOKEN": "pat_your_token_here"
      }
    }
  }
}
```

#### For Other MCP Clients

Use the following configuration pattern:

```json
{
  "name": "layer-ai",
  "command": "layer-mcp-server",
  "environment": {
    "LAYER_API_TOKEN": "pat_your_token_here",
    "LAYER_DEFAULT_SAVE_DIR": "./game-assets"
  }
}
```

#### Alternative: Using Python Module

If the `layer-mcp-server` command isn't in your PATH, you can use the Python module directly:

```json
{
  "mcpServers": {
    "layer-ai": {
      "command": "python",
      "args": ["-m", "layer_mcp_server.server"],
      "env": {
        "LAYER_API_TOKEN": "pat_your_token_here"
      }
    }
  }
}
```

#### Configuration Options

You can customize the server behavior with these environment variables in your MCP config:

```json
{
  "mcpServers": {
    "layer-ai": {
      "command": "layer-mcp-server",
      "env": {
        "LAYER_API_TOKEN": "pat_your_token_here",
        "LAYER_API_BASE_URL": "https://api.layer.ai",
        "LAYER_DEFAULT_SAVE_DIR": "./my-game-assets",
        "LAYER_USAGE_FILE": ".my_layer_usage.json",
        "LAYER_WORKSPACE_ID": "your_workspace_id"
      },
      "disabled": false,
      "autoApprove": [
        "get_usage_info",
        "optimize_prompt"
      ]
    }
  }
}
```

**Environment Variables Explained:**
- `LAYER_API_TOKEN`: Your Layer.ai API token (required)
- `LAYER_API_BASE_URL`: API endpoint (optional, defaults to https://api.layer.ai)
- `LAYER_DEFAULT_SAVE_DIR`: Where to save generated assets (optional, defaults to ./assets)
- `LAYER_USAGE_FILE`: Usage tracking file location (optional, defaults to .layer_usage.json)
- `LAYER_WORKSPACE_ID`: Default workspace ID (optional)

**Auto-Approve Options:**
- `get_usage_info`: Automatically approve usage info requests
- `optimize_prompt`: Automatically approve prompt optimization
- `get_workspace_data`: Automatically approve workspace data exports

## 🎯 Usage

### Running the MCP Server

```bash
# Start the MCP server
layer-mcp-server

# Or run directly with Python
python -m layer_mcp_server.server
```

### MCP Tools Available

#### 1. `forge_2d_asset` - Generate 2D Game Assets

Generate sprites, characters, backgrounds, and other 2D assets.

**Parameters:**
- `prompt` (required): Description of the asset to generate
- `style` (optional): Art style preference
- `reference_type` (optional): Type of reference (image, style, etc.)
- `reference_data` (optional): Reference image or data
- `advanced_settings` (optional): Advanced generation settings
- `save_path` (optional): Local path to save the asset

**Example:**
```json
{
  "prompt": "A cute pixel art character for a platformer game",
  "style": "pixel_art",
  "save_path": "./sprites/player_character.png"
}
```

#### 2. `optimize_prompt` - Optimize Asset Prompts

Use Layer.ai's Prompt Genie to improve your asset generation prompts.

**Parameters:**
- `original_prompt` (required): Your original prompt
- `asset_type` (optional): Type of asset being generated

**Example:**
```json
{
  "original_prompt": "sword",
  "asset_type": "weapon"
}
```

#### 3. `get_usage_info` - Check API Usage

Monitor your API usage against the 600 asset free tier limit.

**Parameters:** None

**Returns:** Current usage, remaining quota, daily/monthly breakdowns

#### 4. `get_workspace_data` - Export Workspace Data

Export and retrieve data from your Layer.ai workspace.

**Parameters:**
- `workspace_id` (optional): Specific workspace ID
- `export_format` (optional): Export format preference

#### 5. `refine_asset` - Refine Existing Assets

Modify and improve existing assets using Layer.ai's refine tools.

**Parameters:**
- `asset_id` (required): ID of the asset to refine
- `refinement_type` (required): Type of refinement to apply
- `parameters` (optional): Refinement-specific parameters

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install -e ".[test]"

# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=layer_mcp_server
```

Test the server components:

```bash
python test_server.py
```

## 📊 Usage Tracking

The server automatically tracks your API usage to help you stay within the free tier limit:

- **Free Tier Limit**: 600 2D assets
- **Automatic Tracking**: Every successful generation increments the counter
- **Quota Protection**: Prevents API calls when limit is reached
- **Usage Warnings**: Alerts when approaching the limit (90%)
- **Persistent Storage**: Usage data saved to `.layer_usage.json`

## 🔧 Development

### Project Structure

```
layer-mcp-server/
├── src/layer_mcp_server/
│   ├── __init__.py
│   ├── server.py          # Main MCP server
│   ├── config.py          # Configuration management
│   ├── api_client.py      # Layer.ai API client
│   ├── tools.py           # MCP tools implementation
│   ├── forge_manager.py   # Asset generation manager
│   └── usage_tracker.py   # Usage tracking system
├── tests/                 # Test suite
├── assets/               # Generated assets (auto-created)
├── .env                  # Environment configuration
├── pyproject.toml        # Project configuration
└── README.md
```

### Adding New Features

1. Extend the `LayerAPIClient` for new API endpoints
2. Add new tools to `LayerTools` class
3. Update tool definitions in `get_tool_definitions()`
4. Add tests for new functionality

## 🐛 Issues & Bug Tracking

### 🔴 Open Issues

#### High Priority
- **[BUG-001]** Timeout issues with complex asset generation (>60s)
  - **Status**: RESOLVED ✅ (Fixed with 180s timeout in MCP config)
  - **Solution**: Added `"timeout": 180` to MCP server configuration
  - **Date**: 2025-08-15

#### Medium Priority
- **[FEATURE-001]** Background removal feature not implemented
  - **Status**: IN PROGRESS 🚧
  - **Description**: `remove_background` tool returns "implementation in progress"
  - **Priority**: Medium
  - **Date**: 2025-08-15

- **[FEATURE-002]** Image description feature not implemented
  - **Status**: IN PROGRESS 🚧
  - **Description**: `describe_image` tool returns "implementation in progress"
  - **Priority**: Medium
  - **Date**: 2025-08-15

- **[FEATURE-003]** Prompt generation feature not implemented
  - **Status**: IN PROGRESS 🚧
  - **Description**: `generate_prompt` tool returns "implementation in progress"
  - **Priority**: Medium
  - **Date**: 2025-08-15

#### Low Priority
- **[ENHANCEMENT-001]** Add support for batch asset generation
  - **Status**: PLANNED 📋
  - **Description**: Generate multiple assets in a single request
  - **Priority**: Low
  - **Date**: 2025-08-15

- **[ENHANCEMENT-002]** Add asset preview before saving
  - **Status**: PLANNED 📋
  - **Description**: Show preview of generated assets before saving to disk
  - **Priority**: Low
  - **Date**: 2025-08-15

### ✅ Resolved Issues

- **[BUG-001]** Timeout issues with complex asset generation
  - **Resolution**: Added 180-second timeout configuration
  - **Fixed**: 2025-08-15
  - **Details**: Updated both workspace and user MCP configs with `"timeout": 180`

### 🚧 Known Limitations

1. **Free Tier Limits**: 600 assets per month on free tier
2. **File Size Limits**: Large assets (>10MB) may have slower processing
3. **Network Dependency**: Requires stable internet connection for Layer.ai API
4. **Python Version**: Requires Python 3.8+ for full compatibility

### 📝 Feature Requests

#### Requested Features
- **3D Asset Generation**: Support for generating 3D models and textures
- **Animation Support**: Generate sprite animations and sequences
- **Style Transfer**: Apply artistic styles to existing assets
- **Bulk Operations**: Process multiple assets simultaneously
- **Asset Versioning**: Track and manage different versions of assets
- **Custom Templates**: Save and reuse asset generation templates

#### Under Consideration
- **Real-time Preview**: Live preview of assets during generation
- **Asset Marketplace**: Browse and use community-generated assets
- **Collaborative Workspaces**: Share assets across team members
- **Advanced Filtering**: Filter assets by style, type, complexity

### 🔧 Troubleshooting

#### Common Issues

**"Invalid API token"**
- Check your `.env` file has the correct `LAYER_API_TOKEN`
- Ensure the token starts with `pat_`
- Verify the token is valid in your Layer.ai account

**"Quota exceeded"**
- Check usage with `get_usage_info` tool
- You've reached the 600 asset limit for free tier
- Consider upgrading your Layer.ai plan

**"Network errors"**
- Check your internet connection
- Verify Layer.ai API is accessible
- The server automatically retries failed requests

**"MCP connection issues"**
- Ensure you're running the server correctly
- Check MCP client configuration
- Review server logs for detailed error messages

**"Timeout errors"**
- Increase timeout in MCP configuration: `"timeout": 180`
- Complex assets may take 30-60 seconds to generate
- Check network stability for long-running operations

### 📊 Issue Reporting Template

When reporting new issues, please use this format:

```
**[TYPE-###]** Brief description
- **Status**: NEW/IN PROGRESS/RESOLVED
- **Priority**: High/Medium/Low
- **Description**: Detailed description of the issue
- **Steps to Reproduce**: 
  1. Step one
  2. Step two
  3. Expected vs actual result
- **Environment**: 
  - OS: [Windows/macOS/Linux]
  - Python version: [3.x.x]
  - MCP Client: [Kiro/Claude Desktop/Other]
- **Date**: YYYY-MM-DD
```

**Issue Types:**
- `BUG` - Something is broken
- `FEATURE` - New functionality needed
- `ENHANCEMENT` - Improvement to existing feature
- `DOCS` - Documentation issue
- `PERFORMANCE` - Performance problem

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 🎮 Happy Game Development!

Start generating amazing 2D assets for your games with Layer.ai! 🚀