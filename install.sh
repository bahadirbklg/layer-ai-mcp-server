#!/bin/bash
# Layer.ai MCP Server - Quick Installation Script

set -e

echo "🚀 Layer.ai MCP Server - Quick Installation"
echo "=========================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8+ is required. Found: Python $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run credential setup
echo "🔐 Setting up credentials..."
python layer-mcp-server/setup_credentials.py

# Test installation
echo "🧪 Testing installation..."
python -c "
import sys
sys.path.insert(0, 'layer-mcp-server')
from production_ready_layer_ai_server import ProductionReadyLayerMCPServer
print('✅ Installation successful!')
"

echo ""
echo "🎉 Installation Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Add the MCP server to your Kiro IDE configuration:"
echo "   - Edit .kiro/settings/mcp.json"
echo "   - Add the server configuration (see README.md)"
echo ""
echo "2. Start using the Layer.ai MCP Server:"
echo "   - Generate game assets with AI"
echo "   - Remove backgrounds from images"
echo "   - Create transparent sprites"
echo "   - And much more!"
echo ""
echo "📚 Documentation: README.md"
echo "🐛 Issues: https://github.com/yourusername/layer-ai-mcp-server/issues"
echo ""
echo "Happy generating! 🎨✨"