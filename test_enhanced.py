#!/usr/bin/env python3
"""Test the enhanced Layer.ai MCP server."""

import sys
import os
import asyncio
sys.path.append('layer-mcp-server')

# Set environment variables
os.environ["LAYER_API_TOKEN"] = "pat_d0IrUtTcJ6SKgorrBZd2R32Qa8aFRZcHRjhk9NkjrkUKMHup4HOvniCxiUM9aLgEZZH5NMTAg4esYnYS6NOgfg"
os.environ["LAYER_WORKSPACE_ID"] = "64395f47-25fc-42b2-bcf6-c195e3e944f4"

from enhanced_server import EnhancedLayerMCPServer

async def test_enhanced_server():
    """Test the enhanced server functionality."""
    try:
        print("🧪 Testing Enhanced Layer.ai MCP Server...")
        
        server = EnhancedLayerMCPServer()
        print("✅ Server initialized successfully")
        
        # Test workspace info
        print("\n📊 Testing workspace info...")
        result = await server._get_workspace_info({})
        print(result[0].text)
        
        # Test inference creation
        print("\n🎨 Testing inference creation...")
        result = await server._create_inference({
            "prompt": "a simple test icon, 32x32 pixels",
            "width": 32,
            "height": 32,
            "quality": "HIGH"
        })
        print(result[0].text)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_enhanced_server())