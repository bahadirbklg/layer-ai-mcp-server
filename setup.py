#!/usr/bin/env python3
"""Setup script for Layer.ai MCP Server."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements
requirements = []
with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="layer-ai-mcp-server",
    version="1.0.0",
    author="Layer.ai MCP Server Contributors",
    author_email="your-email@example.com",
    description="A comprehensive Model Context Protocol server for Layer.ai's AI asset generation platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/layer-ai-mcp-server",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Games/Entertainment",
        "Topic :: Multimedia :: Graphics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",

        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "flake8>=5.0.0",
            "bandit>=1.7.0",
            "safety>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "layer-ai-mcp-server=layer_mcp_server.server:main",
            "layer-ai-setup=layer_mcp_server.setup:main",
        ],
    },
    include_package_data=True,
    package_data={
        "layer_mcp_server": [
            "*.md",
            "*.toml",
        ],
    },
    keywords="layer.ai mcp model-context-protocol ai game-development asset-generation",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/layer-ai-mcp-server/issues",
        "Source": "https://github.com/yourusername/layer-ai-mcp-server",
        "Documentation": "https://github.com/yourusername/layer-ai-mcp-server#readme",
    },
)