#!/usr/bin/env python3
"""Secure Layer.ai MCP Server with encrypted token management."""

import asyncio
import logging
import os
import sys
from typing import Any, Dict, List, Optional
from pathlib import Path

import httpx
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

try:
    from token_manager import LayerTokenManager
except ImportError:
    # Fallback if token_manager not available
    LayerTokenManager = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SecureLayerMCPServer:
    """Secure Layer.ai MCP server with encrypted token management."""
    
    def __init__(self):
        self.api_token = ""
        self.workspace_id = ""
        self._load_credentials()
        self.server = Server("layer-ai")
        self._setup_handlers()
    
    def _load_credentials(self):
        """Load credentials using secure token manager."""
        if LayerTokenManager:
            token_manager = LayerTokenManager()
            credentials = token_manager.get_credentials()
            
            if credentials:
                self.api_token = credentials["api_token"]
                self.workspace_id = credentials["workspace_id"]
                logger.info("🔐 Loaded credentials securely")
                return
        
        # Fallback to environment variables with validation
        self.api_token = os.getenv("LAYER_API_TOKEN", "").strip()
        self.workspace_id = os.getenv("LAYER_WORKSPACE_ID", "").strip()
        
        if self.api_token and self.workspace_id:
            logger.info("🔑 Using environment credentials")
        else:
            logger.error("❌ No valid credentials found")
    
    def _setup_handlers(self):
        """Set up MCP server handlers."""
        
        @self.server.list_tools()
        async def handle_list_tools():
            """List all available tools."""
            tools = [
                Tool(
                    name="create_asset",
                    description="Generate a new asset using Layer.ai - waits for completion and downloads the result",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "prompt": {"type": "string", "description": "Text description of the asset"},
                            "generation_type": {"type": "string", "description": "Type: CREATE, REFILL, EDIT, UPSCALE, IMAGE_TO_VIDEO, TEXT_TO_3D, etc.", "default": "CREATE"},
                            "width": {"type": "integer", "description": "Width in pixels", "default": 512},
                            "height": {"type": "integer", "description": "Height in pixels", "default": 512},
                            "quality": {"type": "string", "description": "Quality: LOW, MEDIUM, HIGH", "default": "HIGH"},
                            "steps": {"type": "integer", "description": "Number of inference steps", "default": 20},
                            "guidance_scale": {"type": "number", "description": "Guidance scale", "default": 7.5},
                            "negative_prompt": {"type": "string", "description": "Negative prompt (optional)"},
                            "seed": {"type": "integer", "description": "Random seed (optional)"},
                            "format": {"type": "string", "description": "Output format (PNG, JPG, etc.)", "default": "PNG"},
                            "save_path": {"type": "string", "description": "Path to save the generated asset", "default": "./assets/generated_asset.png"},
                            "wait_for_completion": {"type": "boolean", "description": "Wait for generation to complete and download", "default": True}
                        },
                        "required": ["prompt"]
                    }
                ),
                Tool(
                    name="get_workspace_info",
                    description="Get information about the current workspace",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="query_schema",
                    description="Query the GraphQL schema to see available generation types and capabilities",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query_type": {"type": "string", "description": "Type of schema info: 'generation_types', 'mutations', 'types'", "default": "generation_types"}
                        },
                        "required": []
                    }
                )
            ]
            
            logger.info(f"Returning {len(tools)} tools")
            return tools
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]):
            """Handle tool calls."""
            try:
                logger.info(f"Calling tool: {name}")
                
                if name == "create_asset":
                    return await self._create_asset(arguments)
                elif name == "get_workspace_info":
                    return await self._get_workspace_info(arguments)
                elif name == "query_schema":
                    return await self._query_schema(arguments)
                else:
                    return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]
                    
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return [TextContent(type="text", text=f"❌ Error: {str(e)}")]
    
    async def _make_graphql_request(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GraphQL request to Layer.ai API."""
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        data = {"query": query}
        if variables:
            data["variables"] = variables
        
        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.app.layer.ai/graphql", headers=headers, json=data, timeout=30.0)
            
            if response.status_code == 200:
                result = response.json()
                if "errors" in result:
                    raise Exception(f"GraphQL error: {result['errors'][0].get('message', 'Unknown error')}")
                return result
            else:
                raise Exception(f"API request failed with status {response.status_code}: {response.text}")
    
    async def _create_asset(self, arguments: Dict[str, Any]):
        """Create a new asset using Layer.ai and wait for completion."""
        prompt = arguments.get("prompt")
        
        # Validate required parameters
        if not prompt:
            return [TextContent(type="text", text="❌ Error: 'prompt' parameter is required")]
        generation_type = arguments.get("generation_type", "CREATE")
        width = arguments.get("width", 512)
        height = arguments.get("height", 512)
        quality = arguments.get("quality", "HIGH")
        steps = arguments.get("steps", 20)
        guidance_scale = arguments.get("guidance_scale", 7.5)
        negative_prompt = arguments.get("negative_prompt")
        seed = arguments.get("seed")
        output_format = arguments.get("format", "PNG")
        save_path = arguments.get("save_path", "./assets/generated_asset.png")
        wait_for_completion = arguments.get("wait_for_completion", True)
        
        if isinstance(wait_for_completion, str):
            wait_for_completion = wait_for_completion.lower() == "true"
        
        # Create the asset directory if it doesn't exist
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Step 1: Create the inference
        mutation = """
        mutation CreateInference($input: CreateInferenceInput!) {
            createInference(input: $input) {
                ... on Inference {
                    id
                    status
                    createdAt
                }
            }
        }
        """
        
        parameters = {
            "generationType": generation_type,
            "prompt": prompt,
            "width": width,
            "height": height,
            "quality": quality,
            "numInferenceSteps": steps,
            "guidanceScale": guidance_scale
        }
        
        if negative_prompt:
            parameters["negativePrompt"] = negative_prompt
        if seed:
            parameters["seed"] = seed
        
        variables = {
            "input": {
                "workspaceId": self.workspace_id,
                "parameters": parameters
            }
        }
        
        result = await self._make_graphql_request(mutation, variables)
        
        # Debug: Log the full response to understand the structure
        logger.info(f"GraphQL Response: {result}")
        
        if "data" not in result or "createInference" not in result["data"]:
            return [TextContent(type="text", text=f"❌ Unexpected API response structure: {result}")]
        
        inference = result["data"]["createInference"]
        
        if not inference or "id" not in inference:
            return [TextContent(type="text", text=f"❌ Invalid inference response: {inference}")]
        
        inference_id = inference["id"]
        
        response_text = f"""🚀 Asset Generation Started!

🎨 Prompt: {prompt}
🔧 Type: {generation_type}
📏 Size: {width}x{height}
⚡ Quality: {quality}
🆔 Inference ID: {inference_id}
📊 Status: {inference['status']}
📅 Created: {inference['createdAt']}

"""
        
        if not wait_for_completion:
            response_text += "⏳ Generation started. Use get_inference_status to check progress."
            return [TextContent(type="text", text=response_text)]
        
        # Step 2: Wait for completion
        response_text += "⏳ Waiting for generation to complete...\n"
        max_wait_time = 300  # 5 minutes max
        check_interval = 5   # Check every 5 seconds
        elapsed_time = 0
        
        status_query = """
        query GetInferenceStatus($input: GetInferencesByIdInput!) {
            getInferencesById(input: $input) {
                ... on InferencesResult {
                    inferences {
                        id
                        status
                        files {
                            id
                            url
                            name
                        }
                    }
                }
            }
        }
        """
        
        while elapsed_time < max_wait_time:
            # Check status first, then sleep if needed
            status_variables = {
                "input": {
                    "inferenceIds": [inference_id]
                }
            }
            
            status_result = await self._make_graphql_request(status_query, status_variables)
            inferences = status_result["data"]["getInferencesById"]["inferences"]
            
            # Check if inference exists
            if not inferences:
                response_text += f"❌ Inference {inference_id} not found."
                break
                
            inference_data = inferences[0]
            current_status = inference_data["status"]
            
            if current_status == "COMPLETE":
                response_text += f"✅ Generation completed in {elapsed_time} seconds!\n\n"
                
                # Step 3: Download the generated image
                files = inference_data.get("files", [])
                if files:
                    file_info = files[0]  # Get the first file
                    file_url = file_info["url"]
                    filename = file_info.get("name", f"generated_asset_{inference_id}.png")
                    
                    # Download the file
                    try:
                        async with httpx.AsyncClient(timeout=60.0) as client:
                            download_response = await client.get(file_url)
                            if download_response.status_code == 200:
                                # Fix file path logic
                                if save_path.endswith('/'):
                                    full_path = Path(save_path) / filename
                                else:
                                    # Use custom filename if provided, otherwise use original
                                    full_path = Path(save_path)
                                    if full_path.suffix == '':  # No extension provided
                                        full_path = full_path.with_suffix('.png')
                                
                                # Ensure parent directory exists
                                full_path.parent.mkdir(parents=True, exist_ok=True)
                                
                                # Write file with error handling
                                with open(full_path, 'wb') as f:
                                    f.write(download_response.content)
                                
                                file_size = len(download_response.content)
                                
                                response_text += f"""🎨 Asset Successfully Generated and Downloaded!

📁 File Path: {full_path}
📊 File Size: {file_size:,} bytes
🔗 Original URL: {file_url}
📝 Filename: {filename}
🎯 Format: {output_format}

🎮 Your asset is ready to use!"""
                            else:
                                response_text += f"❌ Failed to download file: HTTP {download_response.status_code}"
                    except Exception as download_error:
                        response_text += f"❌ Download failed: {str(download_error)}"
                else:
                    response_text += "⚠️ Generation completed but no files found."
                
                break
                
            elif current_status == "FAILED":
                response_text += f"❌ Generation failed after {elapsed_time} seconds."
                break
                
            elif current_status == "CANCELLED":
                response_text += f"⚠️ Generation was cancelled after {elapsed_time} seconds."
                break
                
            else:
                # Still in progress - increment time, then sleep
                elapsed_time += check_interval
                if elapsed_time % 30 == 0:  # Update every 30 seconds
                    response_text += f"⏳ Still generating... ({elapsed_time}s elapsed)\n"
                
                # Only sleep if we're continuing the loop
                if elapsed_time < max_wait_time:
                    await asyncio.sleep(check_interval)
        
        if elapsed_time >= max_wait_time:
            response_text += f"⏰ Timeout after {max_wait_time} seconds. Generation may still be in progress.\n"
            response_text += f"Use get_inference_status with ID: {inference_id} to check later."
        
        return [TextContent(type="text", text=response_text)]
    
    async def _get_workspace_info(self, arguments: Dict[str, Any]):
        """Get workspace information."""
        query = """
        query {
            getMyUser {
                ... on User {
                    id
                }
            }
        }
        """
        
        result = await self._make_graphql_request(query)
        user = result["data"]["getMyUser"]
        
        response_text = f"""📊 Workspace Information

👤 User ID: {user['id']}
🏢 Workspace ID: {self.workspace_id}
🔑 API Token: [CONFIGURED]

✅ Layer.ai MCP Server is connected and ready!"""
        
        return [TextContent(type="text", text=response_text)]
    
    async def _query_schema(self, arguments: Dict[str, Any]):
        """Query the GraphQL schema to see available capabilities."""
        query_type = arguments.get("query_type", "generation_types")
        
        if query_type == "generation_types":
            # Query for available generation types
            query = """
            query {
                __type(name: "GenerationType") {
                    enumValues {
                        name
                        description
                    }
                }
            }
            """
        elif query_type == "mutations":
            # Query for available mutations
            query = """
            query {
                __schema {
                    mutationType {
                        fields {
                            name
                            description
                        }
                    }
                }
            }
            """
        elif query_type == "types":
            # Query for available types
            query = """
            query {
                __schema {
                    types {
                        name
                        kind
                        description
                    }
                }
            }
            """
        else:
            return [TextContent(type="text", text="❌ Invalid query_type. Use: 'generation_types', 'mutations', or 'types'")]
        
        try:
            result = await self._make_graphql_request(query)
            
            if query_type == "generation_types":
                enum_values = result["data"]["__type"]["enumValues"]
                response_text = "🎨 Available Generation Types:\n\n"
                for value in enum_values:
                    name = value["name"]
                    desc = value.get("description", "No description")
                    response_text += f"• **{name}**: {desc}\n"
            
            elif query_type == "mutations":
                mutations = result["data"]["__schema"]["mutationType"]["fields"]
                response_text = "🔧 Available Mutations:\n\n"
                for mutation in mutations[:20]:  # Limit to first 20
                    name = mutation["name"]
                    desc = mutation.get("description", "No description")
                    response_text += f"• **{name}**: {desc}\n"
            
            elif query_type == "types":
                types = result["data"]["__schema"]["types"]
                response_text = "📋 Available Types:\n\n"
                for type_info in types[:30]:  # Limit to first 30
                    if not type_info["name"].startswith("__"):  # Skip introspection types
                        name = type_info["name"]
                        kind = type_info["kind"]
                        desc = type_info.get("description", "No description")
                        response_text += f"• **{name}** ({kind}): {desc}\n"
            
            return [TextContent(type="text", text=response_text)]
            
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Schema query failed: {str(e)}")]
    
    async def run(self):
        """Run the fixed MCP server."""
        logger.info("🚀 Starting Fixed Layer.ai MCP Server...")
        
        if not self.api_token:
            logger.error("❌ LAYER_API_TOKEN environment variable is required")
            sys.exit(1)
        
        if not self.workspace_id:
            logger.error("❌ LAYER_WORKSPACE_ID environment variable is required")
            sys.exit(1)
        
        logger.info("✅ Configuration validated")
        logger.info("🔗 Fixed Layer.ai MCP Server ready for connections")
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="layer-ai",
                    server_version="2.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities=None
                    )
                )
            )


def main():
    """Main entry point."""
    server = SecureLayerMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()