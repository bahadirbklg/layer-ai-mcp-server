# Production Deployment Guide

## 🚀 Production Deployment Checklist

### Pre-Deployment Requirements

- [ ] **Python 3.8+** installed
- [ ] **Layer.ai API Token** obtained from [Layer.ai Settings](https://app.layer.ai/settings/api-keys)
- [ ] **Workspace ID** from Layer.ai dashboard
- [ ] **Kiro IDE** or compatible MCP client
- [ ] **Network access** to api.app.layer.ai

### Quick Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/layer-ai-mcp-server.git
cd layer-ai-mcp-server

# Run the installation script
chmod +x install.sh
./install.sh
```

### Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up credentials
python layer-mcp-server/setup_credentials.py
```

### Production Configuration

#### 1. Environment Variables (Recommended for Production)

```bash
export LAYER_API_TOKEN="pat_your_token_here"
export LAYER_WORKSPACE_ID="your_workspace_id_here"
```

#### 2. Kiro IDE Configuration

Add to `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "layer-ai-production": {
      "command": "python",
      "args": ["layer-mcp-server/production_ready_layer_ai_server.py"],
      "env": {
        "LAYER_API_TOKEN": "pat_your_token_here",
        "LAYER_WORKSPACE_ID": "your_workspace_id_here"
      },
      "disabled": false,
      "autoApprove": [
        "create_asset",
        "get_workspace_info"
      ]
    }
  }
}
```

### Security Hardening

#### 1. File Permissions
```bash
# Secure credential files
chmod 600 .kiro/secure/*
chmod 700 .kiro/secure/

# Secure configuration
chmod 600 .kiro/settings/mcp.json
```

#### 2. Network Security
- Use HTTPS only (enforced by default)
- Implement rate limiting if needed
- Monitor API usage and quotas

#### 3. Credential Management
- Use encrypted credential storage (default)
- Rotate API tokens every 90 days
- Never commit credentials to version control

### Monitoring and Logging

#### 1. Enable Debug Logging
```json
{
  "mcpServers": {
    "layer-ai-production": {
      "env": {
        "DEBUG": "true",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

#### 2. Log Locations
- **MCP Logs**: Available in Kiro IDE MCP panel
- **Server Logs**: Console output from Python process
- **API Logs**: HTTP request/response logs (if debug enabled)

### Performance Optimization

#### 1. Resource Limits
```python
# Default limits in production server:
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
MAX_WAIT_TIME = 300  # 5 minutes
MAX_RETRIES = 3
```

#### 2. Concurrent Requests
```bash
# Limit concurrent requests if needed
export MAX_CONCURRENT_REQUESTS=5
export HTTPX_TIMEOUT=120
```

### Health Checks

#### 1. Server Health Check
```bash
# Test server connectivity
python -c "
import sys
sys.path.insert(0, 'layer-mcp-server')
from production_ready_layer_ai_server import ProductionReadyLayerMCPServer
try:
    server = ProductionReadyLayerMCPServer()
    print('✅ Server healthy')
except Exception as e:
    print(f'❌ Server unhealthy: {e}')
    sys.exit(1)
"
```

#### 2. API Connectivity Test
```bash
# Test Layer.ai API connectivity
curl -H "Authorization: Bearer $LAYER_API_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"query": "query { __typename }"}' \
     https://api.app.layer.ai/graphql
```

### Troubleshooting

#### Common Issues

**"No valid credentials found"**
```bash
# Solution 1: Run credential setup
python layer-mcp-server/setup_credentials.py

# Solution 2: Set environment variables
export LAYER_API_TOKEN="pat_your_token_here"
export LAYER_WORKSPACE_ID="your_workspace_id_here"
```

**"MCP Server Failed to Start"**
```bash
# Check Python version
python3 --version

# Check dependencies
pip list | grep -E "(mcp|httpx|cryptography)"

# Check file permissions
ls -la layer-mcp-server/production_ready_layer_ai_server.py
```

**"Generation failed: Cannot run three_d inferences"**
- 3D generation requires premium Layer.ai workspace plan
- Use CREATE generation type for 2D assets

**"Network timeout errors"**
```bash
# Increase timeout values
export HTTPX_TIMEOUT=180
export MAX_WAIT_TIME=600
```

### Backup and Recovery

#### 1. Backup Credentials
```bash
# Backup encrypted credentials
cp -r .kiro/secure/ backup/credentials-$(date +%Y%m%d)/
```

#### 2. Configuration Backup
```bash
# Backup MCP configuration
cp .kiro/settings/mcp.json backup/mcp-config-$(date +%Y%m%d).json
```

### Updates and Maintenance

#### 1. Update Server
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

#### 2. Restart MCP Server
1. In Kiro IDE, go to MCP panel
2. Find "layer-ai-production" server
3. Click "Restart" or "Reconnect"

#### 3. Security Updates
```bash
# Check for security vulnerabilities
safety check

# Update dependencies
pip install -r requirements.txt --upgrade
```

### Production Metrics

#### Key Performance Indicators
- **Generation Success Rate**: >95%
- **Average Generation Time**: <60 seconds
- **API Error Rate**: <1%
- **Server Uptime**: >99.9%

#### Monitoring Commands
```bash
# Check server status
systemctl status layer-ai-mcp-server  # If using systemd

# Monitor resource usage
htop | grep python

# Check network connectivity
ping api.app.layer.ai
```

### Scaling Considerations

#### 1. Multiple Workspaces
```json
{
  "mcpServers": {
    "layer-ai-dev": {
      "env": {
        "LAYER_WORKSPACE_ID": "dev_workspace_id"
      }
    },
    "layer-ai-prod": {
      "env": {
        "LAYER_WORKSPACE_ID": "prod_workspace_id"
      }
    }
  }
}
```

#### 2. Load Balancing
- Use multiple API tokens for different projects
- Implement request queuing if needed
- Monitor API rate limits

### Support and Maintenance

#### 1. Regular Tasks
- [ ] **Weekly**: Check server logs for errors
- [ ] **Monthly**: Review API usage and quotas
- [ ] **Quarterly**: Rotate API tokens
- [ ] **Annually**: Review security configuration

#### 2. Emergency Contacts
- **Layer.ai Support**: support@layer.ai
- **Security Issues**: security@layer.ai
- **GitHub Issues**: https://github.com/yourusername/layer-ai-mcp-server/issues

---

**🎯 Production deployment complete! Your Layer.ai MCP Server is ready for enterprise use.**