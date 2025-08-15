# Layer.ai Comprehensive MCP Server Documentation

## Overview

This comprehensive MCP server provides full access to Layer.ai's powerful AI generation platform through a Model Context Protocol interface. Based on extensive API exploration, it supports all major Layer.ai functionality including asset generation, file management, style creation, and workspace collaboration.

## 🚀 Quick Start

### Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "layer-ai-comprehensive": {
      "command": "python",
      "args": ["layer-mcp-server/fully_working_layer_ai_server.py"],
      "env": {
        "LAYER_API_TOKEN": "your_layer_ai_token_here",
        "LAYER_WORKSPACE_ID": "your_workspace_id_here"
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

## 🎨 Asset Generation Tools

### 1. `create_asset`
Generate any type of asset using Layer.ai's AI models.

**Parameters:**
- `prompt` (required): Text description of the asset
- `generation_type`: CREATE, REFILL, EDIT, UPSCALE, IMAGE_TO_VIDEO, TEXT_TO_3D, etc.
- `width`, `height`: Dimensions in pixels (default: 512x512)
- `quality`: LOW, MEDIUM, HIGH (default: HIGH)
- `steps`: Number of inference steps (default: 20)
- `guidance_scale`: How closely to follow the prompt (default: 7.5)
- `negative_prompt`: What to avoid in the generation
- `seed`: Random seed for reproducible results
- `transparency`: Generate with transparent background
- `tileability`: Make texture seamless/tileable
- `creativity`: How creative the AI should be (0.0-1.0)
- `resemblance`: How similar to input (0.0-1.0)
- `include_textures`: Include textures for 3D models
- `face_limit`: Maximum faces for 3D models
- `duration_seconds`: Length for video/audio generation

**Example:**
```
Create a pixel art ninja warrior with katana sword, dark hood, detailed armor
```

### 2. `remove_background`
Remove background from any image using AI.

**Parameters:**
- `image_path` or `image_url` (required): Input image
- `return_mask`: Whether to return the mask as well
- `save_path`: Where to save the result

### 3. `describe_image`
Get AI-generated descriptions of images.

**Parameters:**
- `image_path` or `image_url` (required): Input image
- `detail_level`: basic, detailed, comprehensive

### 4. `generate_prompt`
Optimize prompts using Layer.ai's Prompt Genie.

**Parameters:**
- `base_prompt` (required): Your initial prompt
- `asset_type`: Type of asset (game, art, photo, etc.)

### 5. `get_workspace_info`
Get information about your current workspace and available features.

## 🔧 Generation Types

Layer.ai supports multiple generation types:

- **CREATE**: Generate new assets from text
- **REFILL**: Fill in missing parts of images
- **EDIT**: Modify existing images
- **UPSCALE**: Increase image resolution
- **IMAGE_TO_VIDEO**: Convert images to video
- **TEXT_TO_3D**: Generate 3D models from text
- **IMAGE_TO_3D**: Convert 2D images to 3D models
- **VECTORIZE_IMAGE**: Convert to vector format
- **REMOVE_BACKGROUND**: Remove image backgrounds
- **TEXT_TO_SPEECH**: Generate speech from text
- **SOUND_EFFECT**: Create audio effects
- **LIP_SYNC**: Sync audio to video
- **ANIMATE_MESH**: Animate 3D models

## 📊 Quality Levels

- **LOW**: Fast generation, lower quality
- **MEDIUM**: Balanced speed and quality
- **HIGH**: Best quality, slower generation

## 🎨 Use Cases

### Game Development
- Generate sprites, textures, and UI elements
- Create character designs and environments
- Generate sound effects and music
- Create 3D models and animations

### Art & Design
- Create concept art and illustrations
- Generate marketing materials
- Design logos and branding assets
- Create social media content

### Content Creation
- Generate video thumbnails
- Create presentation graphics
- Design website assets
- Generate placeholder content

### Prototyping
- Quickly generate placeholder assets
- Test different visual styles
- Create mockups and wireframes
- Iterate on design concepts

## 🔐 Authentication

The server uses Layer.ai Personal Access Tokens for authentication. Get your token from the Layer.ai dashboard and set it using the secure credential manager.

## 🌐 Workspace Management

Each Layer.ai account can have multiple workspaces for organizing projects. Different workspace plans have different feature availability:

- **Free Plan**: Basic 2D generation
- **Pro Plan**: Advanced features, higher limits
- **Enterprise Plan**: 3D generation, video, custom models

## 🛠️ Error Handling

The server provides detailed error messages and status information for all operations. Common issues:

- **Authentication errors**: Check your API token
- **Feature not available**: Upgrade workspace plan
- **Invalid parameters**: Review parameter requirements
- **Network issues**: Check internet connection
- **Generation failed**: Try different prompts or parameters

## 📚 Examples

### Generate a Game Character
```python
create_asset(
    prompt="fantasy warrior character, pixel art style, 32x32 sprite, RPG game",
    generation_type="CREATE",
    width=32,
    height=32,
    quality="HIGH",
    transparency=True
)
```

### Remove Background from Image
```python
remove_background(
    image_path="./character.png",
    save_path="./character_no_bg.png"
)
```

### Create Tileable Texture
```python
create_asset(
    prompt="stone brick wall texture, medieval, seamless",
    generation_type="CREATE",
    width=256,
    height=256,
    tileability=True
)
```

### Generate 3D Model (Premium Feature)
```python
create_asset(
    prompt="low poly sword, game asset, simple geometry",
    generation_type="TEXT_TO_3D",
    include_textures=True,
    face_limit=1000
)
```

### Optimize a Prompt
```python
generate_prompt(
    base_prompt="dragon character",
    asset_type="game"
)
# Returns enhanced prompt with better descriptors
```

## 🔧 Advanced Configuration

### Custom Parameters
```python
create_asset(
    prompt="your prompt here",
    generation_type="CREATE",
    width=1024,
    height=1024,
    quality="HIGH",
    steps=30,
    guidance_scale=8.0,
    negative_prompt="blurry, low quality, distorted",
    seed=12345,
    transparency=True,
    creativity=0.7,
    resemblance=0.8
)
```

### Batch Processing
For multiple assets, call the tools multiple times or use different seeds for variations.

### File Management
The server automatically:
- Creates output directories
- Determines file extensions from content type
- Handles file naming conflicts
- Provides download progress

## 🚀 Performance Tips

1. **Use appropriate dimensions** - Larger images take longer
2. **Adjust steps vs quality** - More steps = better quality but slower
3. **Use seeds for consistency** - Same seed = same result
4. **Optimize prompts** - Use the prompt generator for better results
5. **Choose right quality level** - HIGH for final assets, MEDIUM for iteration

## 🔍 Troubleshooting

### Common Error Messages

**"Cannot run three_d inferences on this workspace"**
- Solution: Upgrade to a workspace plan that supports 3D generation

**"GraphQL error: Invalid parameters"**
- Solution: Check parameter types and required fields

**"Generation failed after X seconds"**
- Solution: Try simpler prompts or different parameters

**"File not found"**
- Solution: Check file paths and permissions

### Debug Mode
Enable detailed logging by setting the log level to DEBUG in the server configuration.

This comprehensive MCP server brings the full power of Layer.ai's AI generation platform to your development workflow!