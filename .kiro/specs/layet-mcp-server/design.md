# Design Document

## Overview

The Layer MCP Server is a Model Context Protocol server that integrates with Layer.ai's platform for 2D game asset generation. Based on Layer.ai's third-party integration capabilities and User Management API, the server provides MCP tools for forging 2D assets, managing workspace data, and exporting generated content. The design leverages Layer.ai's Forge functionality, advanced settings, reference types, and export capabilities while respecting the free tier limit of 600 2D assets.

## Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MCP Client    │◄──►│  Layer MCP      │◄──►│   Layer.ai      │
│   (Kiro/IDE)    │    │    Server       │    │  Platform API   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Local Storage  │
                       │ (Usage/Assets)  │
                       └─────────────────┘
```

### Component Structure

- **MCP Protocol Handler**: Manages MCP protocol communication
- **Layer API Client**: Handles HTTP requests to Layer.ai User Management API
- **Forge Manager**: Manages 2D asset generation using Layer.ai Forge with advanced settings
- **Export Manager**: Handles workspace data export and asset retrieval
- **Usage Tracker**: Monitors API usage against free tier limits (600 assets)
- **Reference Manager**: Handles different reference types for asset generation
- **Prompt Optimizer**: Integrates with Layer.ai's Prompt Genie for optimized prompts
- **File Manager**: Handles asset saving and file operations

## Components and Interfaces

### MCP Tools Interface

The server exposes the following MCP tools based on Layer.ai capabilities:

1. **forge_2d_asset**
   - Description: Generate a 2D game asset using Layer.ai Forge
   - Parameters:
     - `prompt` (required): Text description of the asset to generate
     - `style` (optional): Art style preference
     - `reference_type` (optional): Type of reference (image, style, etc.)
     - `reference_data` (optional): Reference image or data
     - `advanced_settings` (optional): Advanced generation settings
     - `save_path` (optional): Local path to save the generated asset

2. **optimize_prompt**
   - Description: Use Layer.ai's Prompt Genie to optimize asset generation prompts
   - Parameters:
     - `original_prompt` (required): Original prompt text
     - `asset_type` (optional): Type of asset being generated

3. **get_workspace_data**
   - Description: Export and retrieve workspace data from Layer.ai
   - Parameters:
     - `workspace_id` (optional): Specific workspace ID
     - `export_format` (optional): Export format preference

4. **get_usage_info**
   - Description: Get current API usage statistics
   - Parameters: None
   - Returns: Current usage count, remaining quota (600 limit), percentage used

5. **refine_asset**
   - Description: Use Layer.ai's refine tools to modify existing assets
   - Parameters:
     - `asset_id` (required): ID of the asset to refine
     - `refinement_type` (required): Type of refinement to apply
     - `parameters` (optional): Refinement-specific parameters

### Layer API Client

```python
class LayerAPIClient:
    def __init__(self, api_token: str, base_url: str = "https://api.layer.ai"):
        self.api_token = api_token
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    async def forge_asset(self, prompt: str, **kwargs) -> dict:
        """Generate 2D asset via Layer.ai Forge API"""
        pass
    
    async def get_user_info(self) -> dict:
        """Get user information and usage stats via User Management API"""
        pass
    
    async def export_workspace_data(self, workspace_id: str = None) -> dict:
        """Export workspace data"""
        pass
    
    async def optimize_prompt(self, prompt: str) -> dict:
        """Use Prompt Genie to optimize prompts"""
        pass
    
    async def refine_asset(self, asset_id: str, refinement_type: str, **kwargs) -> dict:
        """Apply refinements to existing assets"""
        pass
```

### Usage Tracker

```python
class UsageTracker:
    def __init__(self, storage_path: str = ".layer_usage.json"):
        self.storage_path = storage_path
        self.usage_data = self._load_usage()
        self.free_tier_limit = 600  # Layer.ai free tier limit
    
    def increment_usage(self) -> None:
        """Increment usage counter for 2D asset generation"""
        pass
    
    def get_usage_info(self) -> dict:
        """Get current usage statistics"""
        pass
    
    def check_quota_limit(self) -> bool:
        """Check if usage is within Layer.ai free tier limit"""
        pass
    
    def get_remaining_quota(self) -> int:
        """Get remaining quota from 600 asset limit"""
        pass
```

## Data Models

### Asset Generation Request

```python
@dataclass
class AssetForgeRequest:
    prompt: str
    style: Optional[str] = None
    reference_type: Optional[str] = None
    reference_data: Optional[str] = None
    advanced_settings: Optional[dict] = None
    save_path: Optional[str] = None
```

### Asset Generation Response

```python
@dataclass
class AssetForgeResponse:
    success: bool
    asset_id: Optional[str] = None
    asset_data: Optional[str] = None  # Base64 encoded or URL
    file_path: Optional[str] = None
    usage_count: int = 0
    error_message: Optional[str] = None
```

### Workspace Export Request

```python
@dataclass
class WorkspaceExportRequest:
    workspace_id: Optional[str] = None
    export_format: Optional[str] = "json"
    include_assets: bool = True
```

### Usage Information

```python
@dataclass
class UsageInfo:
    current_usage: int
    quota_limit: int = 600  # Layer.ai free tier limit
    remaining: int
    percentage_used: float
    last_reset: Optional[datetime] = None
```

## Error Handling

### API Error Categories

1. **Authentication Errors**
   - Invalid API token
   - Expired token
   - Insufficient permissions

2. **Request Errors**
   - Invalid parameters
   - Malformed requests
   - Missing required fields

3. **Quota Errors**
   - Usage limit exceeded
   - Rate limiting

4. **Network Errors**
   - Connection timeouts
   - Service unavailable
   - DNS resolution failures

### Error Response Format

```python
{
    "error": {
        "type": "quota_exceeded",
        "message": "Monthly usage limit of 600 sprites exceeded",
        "code": "QUOTA_LIMIT_REACHED",
        "details": {
            "current_usage": 600,
            "limit": 600
        }
    }
}
```

### Retry Strategy

- Exponential backoff for network errors
- Maximum 3 retry attempts
- Rate limit respect with appropriate delays
- Circuit breaker pattern for persistent failures

## Testing Strategy

### Unit Tests

1. **API Client Tests**
   - Mock HTTP responses
   - Test parameter validation
   - Test error handling scenarios

2. **Usage Tracker Tests**
   - Test counter increment/decrement
   - Test quota limit checking
   - Test persistence mechanisms

3. **File Manager Tests**
   - Test file saving operations
   - Test directory creation
   - Test file format handling

### Integration Tests

1. **MCP Protocol Tests**
   - Test tool registration
   - Test request/response flow
   - Test error propagation

2. **End-to-End Tests**
   - Test complete sprite generation workflow
   - Test usage tracking across sessions
   - Test file saving and retrieval

### Mock Testing

- Mock Layer.ai API responses
- Test various API response scenarios
- Test network failure conditions
- Test quota limit scenarios
- Test workspace export functionality
- Test prompt optimization features

## Configuration

### Environment Variables

```bash
LAYER_API_TOKEN=pat_9uAtXgmdyDP400kkr1o4hxjIQZ9tS3qVfH2dh0sAVS8sIE9N27ElXCmdhZUynQEgvFEY34Mw8snETjUaRFt3Za
LAYER_API_BASE_URL=https://api.layer.ai  # Optional, defaults to official API
LAYER_USAGE_FILE=.layer_usage.json       # Optional, defaults to local file
LAYER_DEFAULT_SAVE_DIR=./assets          # Optional, default asset save location
LAYER_WORKSPACE_ID=                      # Optional, default workspace ID
```

### MCP Server Configuration

```json
{
  "name": "layer-asset-generator",
  "version": "1.0.0",
  "description": "Generate 2D game assets using Layer.ai",
  "tools": [
    {
      "name": "forge_2d_asset",
      "description": "Generate a 2D game asset using Layer.ai Forge"
    },
    {
      "name": "optimize_prompt",
      "description": "Optimize prompts using Layer.ai Prompt Genie"
    },
    {
      "name": "get_workspace_data",
      "description": "Export and retrieve workspace data"
    },
    {
      "name": "get_usage_info", 
      "description": "Get API usage statistics"
    },
    {
      "name": "refine_asset",
      "description": "Refine existing assets using Layer.ai tools"
    }
  ]
}
```

## Security Considerations

1. **API Token Management**
   - Store tokens securely in environment variables
   - Never log or expose tokens in error messages
   - Validate token format before API calls

2. **File System Security**
   - Validate file paths to prevent directory traversal
   - Restrict file operations to designated directories
   - Sanitize filenames to prevent injection attacks

3. **Data Validation**
   - Validate all input parameters
   - Sanitize user-provided descriptions
   - Limit file sizes and formats