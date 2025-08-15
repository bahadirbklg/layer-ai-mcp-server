#!/usr/bin/env python3
"""Test script to verify Layer.ai MCP Server installation."""

import importlib
import sys
from pathlib import Path


def test_python_version():
    """Test Python version compatibility."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(
            f"❌ Python {version.major}.{version.minor} detected. Python 3.10+ required."
        )
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True


def test_dependencies():
    """Test if all required dependencies are installed."""
    required_packages = [
        "mcp",
        "httpx",
        "cryptography",
        "pydantic",
        "dotenv",
        "aiofiles",
    ]

    failed = []
    for package in required_packages:
        try:
            if package == "dotenv":
                importlib.import_module("dotenv")
            else:
                importlib.import_module(package)
            print(f"✅ {package} - Installed")
        except ImportError:
            print(f"❌ {package} - Missing")
            failed.append(package)

    return len(failed) == 0


def test_project_structure():
    """Test if project files are in place."""
    required_files = [
        "layer-mcp-server/server.py",
        "layer-mcp-server/auth.py",
        "layer-mcp-server/setup.py",
        "requirements.txt",
        "README.md",
    ]

    failed = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} - Found")
        else:
            print(f"❌ {file_path} - Missing")
            failed.append(file_path)

    return len(failed) == 0


def test_server_import():
    """Test if the main server can be imported."""
    try:
        sys.path.append("layer-mcp-server")
        from server import ProductionReadyLayerMCPServer

        print("✅ Main server class - Can be imported")
        return True
    except ImportError as e:
        print(f"❌ Main server class - Import failed: {e}")
        return False


def main():
    """Run all installation tests."""
    print("🧪 Testing Layer.ai MCP Server Installation\n")

    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Project Structure", test_project_structure),
        ("Server Import", test_server_import),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"   Fix the issues above and try again.")

    print(f"\n📊 Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 Installation test successful!")
        print("Your Layer.ai MCP Server is ready to use.")
        print("\nNext steps:")
        print("1. Get your API token from https://app.layer.ai/settings/api-keys")
        print("2. Run: python layer-mcp-server/setup.py")
        print("3. Configure your MCP client (see README.md)")
    else:
        print(f"\n❌ Installation test failed ({total-passed} issues)")
        print("Please fix the issues above and run the test again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
