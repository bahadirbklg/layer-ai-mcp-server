# Layer.ai MCP Server

A comprehensive Model Context Protocol (MCP) server for Layer.ai's AI asset generation platform. Generate game assets, remove backgrounds, create 3D models, and more directly from your development environment.

## 🎮 Perfect for Game Development

Generate professional game assets using AI:
- **Sprites & Characters** - Any size, with transparency support
- **Backgrounds & Environments** - Detailed landscapes and scenes  
- **Game Items** - Weapons, potions, collectibles
- **UI Elements** - Buttons, icons, decorations
- **Textures** - Tileable materials and patterns
- **Pixel Art** - Retro-style game assets

## ✨ Features

### 🎨 Asset Generation
- **CREATE** - Generate new assets from text prompts
- **TRANSPARENCY** - Perfect sprites with transparent backgrounds
- **TILEABILITY** - Seamless textures for game worlds
- **CUSTOM SIZES** - Any resolution from 64x64 to 2048x2048+
- **QUALITY CONTROL** - Low, Medium, High quality options
- **SEED CONTROL** - Reproducible results

### 🛠️ Advanced Features  
- **REMOVE_BACKGROUND** - AI-powered background removal
- **IMAGE_TO_3D** - Convert 2D images to 3D models*
- **TEXT_TO_3D** - Generate 3D models from text*
- **VECTORIZE_IMAGE** - Convert to vector format*
- **IMAGE_TO_VIDEO** - Create videos from images*
- **TEXT_TO_SPEECH** - Generate speech from text*

*Requires premium Layer.ai workspace plan

### 🔐 Security
- **Encrypted Credentials** - AES-256 encryption for API tokens
- **Secure Storage** - No plain text tokens in config files
- **Easy Setup** - Interactive credential configuration

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Layer.ai account and API token
- MCP-compatible environment (like Kiro IDE)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/layer-ai-mcp-server.git
cd layer-ai-mcp-server
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up credentials**
```bash
python layer-mcp-server/setup_credentials.py
```

4. **Configure MCP**
Add to your `.kiro/settings/mcp.json`:
```json
{
  "mcpServers": {
    "layer-ai-comprehensive": {
      "command": "python",
      "args": ["layer-mcp-server/fully_working_layer_ai_server.py"],
      "env": {
        "LAYER_API_TOKEN": "your_token_here",
        "LAYER_WORKSPACE_ID": "your_workspace_id"
      },
      "disabled": false,
      "autoApprove": [
        "create_asset", "remove_background", "describe_image", 
        "generate_prompt", "get_workspace_info"
      ]
    }
  }
}
```

## 📖 Usage Examples

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

### Remove Background
```python
# Remove background from existing image
remove_background(
    image_path="./assets/character.png",
    save_path="./assets/character_no_bg.png"
)
```

### Generate Optimized Prompts
```python
# Enhance your prompts with AI
generate_prompt(
    base_prompt="dragon character",
    asset_type="game"
)
# Returns: "Majestic dragon character, detailed scales, fantasy RPG style, 
#          dynamic pose, vibrant colors, game asset, high quality"
```

## 🛠️ Available Tools

| Tool | Description | Status |
|------|-------------|--------|
| `create_asset` | Generate any type of asset | ✅ Working |
| `remove_background` | AI background removal | ✅ Working |
| `describe_image` | Get AI image descriptions | ✅ Working |
| `generate_prompt` | Optimize prompts with AI | ✅ Working |
| `get_workspace_info` | Workspace status | ✅ Working |

## 📁 Project Structure

```
layer-ai-mcp-server/
├── layer-mcp-server/
│   ├── fully_working_layer_ai_server.py  # Main MCP server
│   ├── token_manager.py                  # Secure credential management
│   ├── setup_credentials.py              # Interactive setup
│   └── pyproject.toml                    # Dependencies
├── assets/                               # Generated assets
├── backup/                               # Backup files
├── .kiro/                               # Kiro IDE configuration
├── README.md                            # This file
├── .gitignore                           # Git ignore rules
└── requirements.txt                     # Python dependencies
```

## 🔧 Configuration

### Environment Variables
- `LAYER_API_TOKEN` - Your Layer.ai API token
- `LAYER_WORKSPACE_ID` - Your workspace ID

### Generation Parameters
- `prompt` - Text description of the asset
- `generation_type` - Type of generation (CREATE, REMOVE_BACKGROUND, etc.)
- `width/height` - Output dimensions
- `quality` - LOW, MEDIUM, HIGH
- `transparency` - Enable transparent backgrounds
- `tileability` - Make textures seamless
- `steps` - Number of inference steps (quality vs speed)
- `guidance_scale` - How closely to follow prompt
- `negative_prompt` - What to avoid
- `seed` - For reproducible results

## 🎯 Game Development Workflow

1. **Concept** - Describe your asset needs
2. **Generate** - Use AI to create base assets
3. **Refine** - Adjust prompts and parameters
4. **Integrate** - Save directly to your game project
5. **Iterate** - Quickly create variations

## 🔐 Security Features

- **AES-256 Encryption** - API tokens encrypted at rest
- **PBKDF2 Key Derivation** - Secure key generation
- **File Permissions** - Restricted access (600)
- **No Version Control Exposure** - Credentials never committed
- **Easy Token Rotation** - Update credentials without config changes

## 🐛 Troubleshooting

### Common Issues

**"No valid credentials found"**
- Run `python layer-mcp-server/setup_credentials.py`
- Check your API token format (should start with 'pat_')

**"Generation failed: Cannot run three_d inferences"**
- 3D generation requires a premium Layer.ai workspace plan
- Use CREATE generation type for 2D assets

**"MCP connection failed"**
- Check your Python path in MCP configuration
- Ensure all dependencies are installed
- Verify file paths are correct

## 📚 API Documentation

For detailed API documentation, see:
- [Layer.ai API Documentation](https://docs.layer.ai)
- [MCP Protocol Specification](https://modelcontextprotocol.io)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Layer.ai](https://layer.ai) for the amazing AI generation platform
- [Model Context Protocol](https://modelcontextprotocol.io) for the MCP specification
- [Kiro IDE](https://kiro.ai) for MCP integration

## 🔗 Links

- [Layer.ai Platform](https://app.layer.ai)
- [Get API Token](https://app.layer.ai/settings/api-keys)
- [Layer.ai Documentation](https://docs.layer.ai)
- [Report Issues](https://github.com/yourusername/layer-ai-mcp-server/issues)

---

**Made with ❤️ for game developers and AI enthusiasts**