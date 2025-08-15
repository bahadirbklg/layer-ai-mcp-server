#!/bin/bash
# Layer.ai MCP Server Installation Script

set -e  # Exit on any error

echo "🚀 Installing Layer.ai MCP Server..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.10+ required. Found: Python $python_version"
    echo "Please install Python 3.10 or higher and try again."
    exit 1
fi

echo "✅ Python version check passed: $python_version"

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

# Create assets directory
echo "📁 Creating assets directory..."
mkdir -p assets

# Set up credentials
echo "🔐 Setting up credentials..."
echo "Please run the following command to configure your Layer.ai API token:"
echo "python layer-mcp-server/setup.py"

# Test installation
echo "🧪 Testing installation..."
python3 verify-install.py

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Next steps:"
echo "1. Get your API token from https://app.layer.ai/settings/api-keys"
echo "2. Run: python layer-mcp-server/setup.py"
echo "3. Configure your MCP client (see README.md for details)"
echo ""
echo "To activate the virtual environment in the future:"
echo "source venv/bin/activate"
echo ""
echo "To test your installation anytime:"
echo "python3 verify-install.py"