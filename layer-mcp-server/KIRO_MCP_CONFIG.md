# Kiro IDE MCP Configuration Guide

## 🚀 Quick Setup for Kiro IDE

This guide helps you configure the Layer.ai MCP Server in Kiro IDE for seamless AI asset generation.

## 📋 Prerequisites

1. **Kiro IDE** installed and running
2. **Python 3.8+** available in your system PATH
3. **Layer.ai account** with API access
4. **Layer.ai API token** from [settings page](https://app.layer.ai/settings/api-keys)

## ⚙️ Configuration Steps

### 1. Install Dependencies
```bash
pip install mcp httpx cryptography
```

### 2. Set Up Credentials
```bash
python layer-mcp-server/setup_credentials.py
```

### 3. Configure MCP in Kiro IDE

#### Option A: Workspace Configuration (Recommended)
Create or edit `.kiro/settings/mcp.json` in your project:

```json
{
  "mcpServers": {
    "layer-ai-comprehensive": {
      "command": "python",
      "args": ["layer-mcp-server/fully_working_layer_ai_server.py"],
      "env": {
        "LAYER_API_TOKEN": "pat_your_token_here",
        "LAYER_WORKSPACE_ID": "your_workspace_id_here"
      },
      "disabled": false,
      "autoApprove": [
        "create_asset",
        "remove_background", 
        "describe_image",
        "generate_prompt",
        "get_workspace_info"
      ]
    }
  }
}
```

#### Option B: Global Configuration
Edit `~/.kiro/settings/mcp.json` for system-wide access:

```json
{
  "mcpServers": {
    "layer-ai-comprehensive": {
      "command": "python",
      "args": ["/absolute/path/to/layer-mcp-server/fully_working_layer_ai_server.py"],
      "env": {
        "LAYER_API_TOKEN": "pat_your_token_here",
        "LAYER_WORKSPACE_ID": "your_workspace_id_here"
      },
      "disabled": false,
      "autoApprove": [
        "create_asset",
        "remove_background",
        "describe_image", 
        "generate_prompt",
        "get_workspace_info"
      ]
    }
  }
}
```

## 🔧 Configuration Options

### Server Settings
- **`command`**: Python executable path
- **`args`**: Path to the MCP server script
- **`env`**: Environment variables (API credentials)
- **`disabled`**: Enable/disable the server
- **`autoApprove`**: Tools that don't require manual approval

### Environment Variables
- **`LAYER_API_TOKEN`**: Your Layer.ai Personal Access Token
- **`LAYER_WORKSPACE_ID`**: Your Layer.ai workspace ID

### Auto-Approve Tools
Add tools to `autoApprove` for seamless operation:
```json
"autoApprove": [
  "create_asset",           // Generate assets
  "remove_background",      // Remove backgrounds
  "describe_image",         // Describe images
  "generate_prompt",        // Optimize prompts
  "get_workspace_info"      // Get workspace status
]
```

## 🎮 Usage in Kiro IDE

### 1. Access MCP Tools
- Open Kiro IDE command palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
- Search for "MCP" to see available Layer.ai tools
- Or use the MCP panel in the sidebar

### 2. Generate Game Assets
```
Tool: create_asset
Prompt: "fantasy sword sprite, pixel art, 64x64, RPG game"
Generation Type: CREATE
Width: 64
Height: 64
Transparency: true
Save Path: ./assets/sword_sprite.png
```

### 3. Remove Backgrounds
```
Tool: remove_background
Image Path: ./assets/character.png
Save Path: ./assets/character_no_bg.png
```

### 4. Optimize Prompts
```
Tool: generate_prompt
Base Prompt: "dragon character"
Asset Type: "game"
```

## 🔍 Troubleshooting

### Common Issues

#### "MCP Server Failed to Start"
**Causes:**
- Python not found in PATH
- Missing dependencies
- Incorrect file paths

**Solutions:**
```bash
# Check Python installation
python --version

# Install dependencies
pip install mcp httpx cryptography

# Verify file paths
ls -la layer-mcp-server/fully_working_layer_ai_server.py
```

#### "Authentication Failed"
**Causes:**
- Invalid API token
- Incorrect workspace ID
- Token permissions

**Solutions:**
1. Verify token at [Layer.ai Settings](https://app.layer.ai/settings/api-keys)
2. Check workspace ID in Layer.ai dashboard
3. Run credential setup: `python layer-mcp-server/setup_credentials.py`

#### "Tool Not Found"
**Causes:**
- Server not connected
- Configuration errors
- Tool name mismatch

**Solutions:**
1. Check MCP server status in Kiro IDE
2. Restart Kiro IDE
3. Verify configuration syntax

### Debug Mode
Enable detailed logging by adding to your MCP configuration:
```json
{
  "mcpServers": {
    "layer-ai-comprehensive": {
      "command": "python",
      "args": ["layer-mcp-server/fully_working_layer_ai_server.py"],
      "env": {
        "LAYER_API_TOKEN": "pat_your_token_here",
        "LAYER_WORKSPACE_ID": "your_workspace_id_here",
        "DEBUG": "true"
      },
      "disabled": false
    }
  }
}
```

## 🚀 Advanced Configuration

### Custom Python Environment
```json
{
  "mcpServers": {
    "layer-ai-comprehensive": {
      "command": "/path/to/venv/bin/python",
      "args": ["layer-mcp-server/fully_working_layer_ai_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/your/project",
        "LAYER_API_TOKEN": "pat_your_token_here",
        "LAYER_WORKSPACE_ID": "your_workspace_id_here"
      }
    }
  }
}
```

### Multiple Workspaces
```json
{
  "mcpServers": {
    "layer-ai-dev": {
      "command": "python",
      "args": ["layer-mcp-server/fully_working_layer_ai_server.py"],
      "env": {
        "LAYER_API_TOKEN": "pat_dev_token_here",
        "LAYER_WORKSPACE_ID": "dev_workspace_id"
      }
    },
    "layer-ai-prod": {
      "command": "python", 
      "args": ["layer-mcp-server/fully_working_layer_ai_server.py"],
      "env": {
        "LAYER_API_TOKEN": "pat_prod_token_here",
        "LAYER_WORKSPACE_ID": "prod_workspace_id"
      }
    }
  }
}
```

### Performance Tuning
```json
{
  "mcpServers": {
    "layer-ai-comprehensive": {
      "command": "python",
      "args": ["layer-mcp-server/fully_working_layer_ai_server.py"],
      "env": {
        "LAYER_API_TOKEN": "pat_your_token_here",
        "LAYER_WORKSPACE_ID": "your_workspace_id_here",
        "HTTPX_TIMEOUT": "120",
        "MAX_CONCURRENT_REQUESTS": "5"
      },
      "disabled": false,
      "autoApprove": ["create_asset", "get_workspace_info"]
    }
  }
}
```

## 📊 Monitoring and Logs

### View MCP Logs in Kiro IDE
1. Open the MCP panel
2. Select "Layer.ai Comprehensive" server
3. View connection status and logs
4. Monitor tool execution

### Log Locations
- **Kiro IDE Logs**: Available in MCP panel
- **Server Logs**: Console output from Python process
- **API Logs**: HTTP request/response logs (if debug enabled)

## 🔄 Updates and Maintenance

### Update the Server
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### Restart MCP Server
1. In Kiro IDE, go to MCP panel
2. Find "Layer.ai Comprehensive" server
3. Click "Restart" or "Reconnect"
4. Or restart Kiro IDE completely

### Configuration Validation
```bash
# Validate JSON syntax
python -m json.tool .kiro/settings/mcp.json

# Test server connection
python layer-mcp-server/fully_working_layer_ai_server.py --test
```

## 🎯 Best Practices

### 1. Security
- Use workspace-specific configurations
- Rotate API tokens regularly
- Don't commit tokens to version control
- Use the secure credential manager

### 2. Performance
- Enable auto-approve for frequently used tools
- Use appropriate image dimensions
- Monitor API usage and quotas
- Cache generated assets locally

### 3. Organization
- Use descriptive save paths
- Organize assets by project/type
- Use consistent naming conventions
- Document your generation prompts

## 🔗 Additional Resources

- [Kiro IDE Documentation](https://docs.kiro.ai)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [Layer.ai API Documentation](https://docs.layer.ai)
- [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk)

---

**Happy generating! 🎨✨**