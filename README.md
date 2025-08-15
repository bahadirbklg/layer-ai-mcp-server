# Layer.ai MCP Server

A Model Context Protocol (MCP) server for generating game assets using Layer.ai's AI platform. Generate sprites, characters, backgrounds, and other 2D assets directly from your development environment.

**Made with AI - Use with caution**

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/bahadirbklg)

## Features

- **Asset Generation**: Generate 2D game assets using Layer.ai Forge
- **Prompt Optimization**: Optimize prompts with Layer.ai Prompt Genie  
- **Usage Tracking**: Monitor usage against free tier limits (600 assets)
- **Workspace Management**: Export and manage workspace data
- **Asset Refinement**: Refine and modify existing assets
- **Auto-Save**: Automatically save generated assets to your project
- **Error Handling**: Robust error handling with automatic retries
- **Quota Protection**: Prevents exceeding your free tier limit

## Installation

### Prerequisites
- **Python 3.10+** (required for MCP compatibility)
- **Git** for cloning the repository
- **Layer.ai account** and API token

### Quick Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/bahadirbklg/layer-ai-mcp-server.git
cd layer-ai-mcp-server

# Run the installation script
chmod +x install.sh
./install.sh
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/bahadirbklg/layer-ai-mcp-server.git
cd layer-ai-mcp-server

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create assets directory
mkdir -p assets

# Set up credentials
python layer-mcp-server/setup.py
```

### Installation Options

- **Production**: `pip install -r requirements.min.txt` (core dependencies only)
- **Development**: `pip install -r requirements.dev.txt` (includes testing and linting tools)
- **Full**: `pip install -r requirements.txt` (recommended for most users)

### Verify Installation

Test your installation to make sure everything is working:

```bash
# Run the installation test
python3 verify-install.py
```

This will check:
- Python version compatibility (3.10+)
- All required dependencies are installed
- Project files are in place
- Main server can be imported successfully

## Configuration

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

### MCP Client Configuration

#### For Kiro IDE

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "layer-ai-comprehensive": {
      "command": "python",
      "args": ["layer-mcp-server/server.py"],
      "env": {
        "LAYER_API_TOKEN": "pat_your_token_here",
        "LAYER_WORKSPACE_ID": "your_workspace_id"
      },
      "disabled": false,
      "timeout": 180,
      "autoApprove": [
        "create_asset", "remove_background", "describe_image", 
        "generate_prompt", "get_workspace_info"
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

## Usage

### Available Tools

#### 1. `create_asset` - Generate Assets

Generate sprites, characters, backgrounds, and other assets.

**Parameters:**
- `prompt` (required): Description of the asset to generate
- `generation_type` (optional): CREATE, UPSCALE, etc.
- `width/height` (optional): Output dimensions (default: 512x512)
- `quality` (optional): LOW, MEDIUM, HIGH (default: HIGH)
- `transparency` (optional): Enable transparent backgrounds
- `save_path` (optional): Local path to save the asset

**Example:**
```json
{
  "prompt": "A cute pixel art character for a platformer game",
  "generation_type": "CREATE",
  "width": 512,
  "height": 512,
  "transparency": true,
  "save_path": "./sprites/player_character.png"
}
```

#### 2. `get_workspace_info` - Check Status

Get information about your Layer.ai workspace and available features.

#### 3. `remove_background` - Background Removal (In Development)

Remove backgrounds from existing images using AI.

#### 4. `describe_image` - Image Analysis (In Development)

Get AI-generated descriptions of images.

#### 5. `generate_prompt` - Prompt Optimization (In Development)

Optimize your prompts using Layer.ai's Prompt Genie.

## Usage Examples

### Generate a Game Sprite
```python
# Create a transparent character sprite
create_asset(
    prompt="fantasy warrior character, pixel art, 64x64, RPG game",
    generation_type="CREATE",
    width=64,
    height=64,
    transparency=True,
    save_path="./assets/warrior_sprite.png"
)
```

### Create a Tileable Texture
```python
# Generate seamless stone texture
create_asset(
    prompt="medieval stone brick wall, seamless texture",
    generation_type="CREATE", 
    width=256,
    height=256,
    tileability=True,
    save_path="./assets/stone_texture.png"
)
```

## Project Structure

```
layer-ai-mcp-server/
├── layer-mcp-server/
│   ├── server.py                            # Main MCP server
│   ├── auth.py                              # Authentication & token management
│   ├── setup.py                             # Interactive credential setup
│   ├── api-docs.md                          # API documentation
│   ├── mcp-config.md                        # MCP configuration guide
│   ├── security.md                          # Security documentation
│   └── pyproject.toml                       # Package configuration
├── assets/                                  # Generated assets (auto-created)
├── README.md                                # Main documentation
├── .gitignore                               # Git ignore patterns
├── requirements.txt                         # Core dependencies
├── requirements.min.txt                     # Minimal dependencies
├── requirements.dev.txt                     # Development dependencies
├── install.sh                               # Installation script
├── verify-install.py                        # Installation verification
├── setup.py                                 # Package setup
└── LICENSE                                  # MIT License
```

## Issues & Bug Tracking

### Open Issues

#### High Priority
- **[BUG-001]** Timeout issues with complex asset generation (>60s)
  - **Status**: RESOLVED (Fixed with 180s timeout in MCP config)
  - **Solution**: Added `"timeout": 180` to MCP server configuration
  - **Date**: 2025-08-15

#### Medium Priority
- **[FEATURE-001]** Background removal feature not implemented
  - **Status**: IN PROGRESS
  - **Description**: `remove_background` tool returns "implementation in progress"
  - **Date**: 2025-08-15

- **[FEATURE-002]** Image description feature not implemented
  - **Status**: IN PROGRESS
  - **Description**: `describe_image` tool returns "implementation in progress"
  - **Date**: 2025-08-15

- **[FEATURE-003]** Prompt generation feature not implemented
  - **Status**: IN PROGRESS
  - **Description**: `generate_prompt` tool returns "implementation in progress"
  - **Date**: 2025-08-15

### Known Limitations

1. **Free Tier Limits**: 600 assets per month on free tier
2. **File Size Limits**: Large assets (>10MB) may have slower processing
3. **Network Dependency**: Requires stable internet connection for Layer.ai API
4. **Python Version**: Requires Python 3.10+ for full compatibility

### Feature Requests

- **3D Asset Generation**: Support for generating 3D models and textures
- **Animation Support**: Generate sprite animations and sequences
- **Style Transfer**: Apply artistic styles to existing assets
- **Bulk Operations**: Process multiple assets simultaneously
- **Asset Versioning**: Track and manage different versions of assets

## Troubleshooting

### Common Issues

**"Invalid API token"**
- Check your `.env` file has the correct `LAYER_API_TOKEN`
- Ensure the token starts with `pat_`
- Verify the token is valid in your Layer.ai account

**"Quota exceeded"**
- Check usage with `get_workspace_info` tool
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

**"Installation errors"**
- **Python version**: Ensure you have Python 3.10+ (`python3 --version`)
- **Virtual environment**: Use a virtual environment to avoid conflicts
- **Permissions**: On Linux/macOS, you may need `chmod +x install.sh`
- **Dependencies**: Try `pip install --upgrade pip` before installing requirements
- **MCP compatibility**: Some older Python versions may have MCP compatibility issues

**"Import errors"**
- **Missing dependencies**: Run `pip install -r requirements.txt` again
- **Virtual environment**: Make sure your virtual environment is activated
- **Path issues**: Ensure you're running from the correct directory
- **Token manager**: If token_manager import fails, run the setup script

### Issue Reporting Template

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
  - MCP Client: [Claude Desktop/Other]
- **Date**: YYYY-MM-DD
```

**Issue Types:**
- `BUG` - Something is broken
- `FEATURE` - New functionality needed
- `ENHANCEMENT` - Improvement to existing feature
- `DOCS` - Documentation issue
- `PERFORMANCE` - Performance problem

## Security

This project uses secure credential management:
- **AES-256 Encryption**: API tokens encrypted at rest
- **PBKDF2 Key Derivation**: Secure key generation
- **File Permissions**: Restricted access (600)
- **No Version Control Exposure**: Credentials never committed

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## Links

- [Layer.ai Platform](https://app.layer.ai)
- [Get API Token](https://app.layer.ai/settings/api-keys)
- [Layer.ai Documentation](https://docs.layer.ai)

---

**Made with AI - Use with caution**

Start generating amazing assets for your projects with Layer.ai!