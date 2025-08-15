#!/usr/bin/env python3
"""Critical bug fixes for Layer.ai MCP Server - Apply these fixes immediately."""

import os
import base64
from pathlib import Path
from typing import Dict, Any, Optional


class BugFixedLayerMCPServer:
    """Layer.ai MCP Server with critical bugs fixed."""
    
    def _load_credentials(self):
        """Load credentials with proper error handling (BUG #1 FIX)."""
        if LayerTokenManager:
            token_manager = LayerTokenManager()
            credentials = token_manager.get_credentials()
            
            if credentials:
                self.api_token = credentials["api_token"]
                self.workspace_id = credentials["workspace_id"]
                logger.info("🔐 Loaded credentials securely")
                return
        
        # Fallback to environment variables
        self.api_token = os.getenv("LAYER_API_TOKEN", "")
        self.workspace_id = os.getenv("LAYER_WORKSPACE_ID", "")
        
        if not self.api_token or not self.workspace_id:
            logger.error("❌ No valid credentials found")
            # FIX: Don't crash with sys.exit(1), raise exception instead
            raise ValueError(
                "Missing Layer.ai credentials. Please run 'python setup_credentials.py' "
                "or set LAYER_API_TOKEN and LAYER_WORKSPACE_ID environment variables."
            )
    
    def _encode_image_to_base64(self, image_path: str) -> str:
        """Encode image file to base64 with proper error handling (BUG #2 FIX)."""
        try:
            # Validate file exists
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            # Check if it's actually a file
            if not os.path.isfile(image_path):
                raise ValueError(f"Path is not a file: {image_path}")
            
            # Read and validate file content
            with open(image_path, 'rb') as f:
                content = f.read()
                
            if len(content) == 0:
                raise ValueError(f"Image file is empty: {image_path}")
            
            # Check file size (prevent memory issues with huge files)
            if len(content) > 50 * 1024 * 1024:  # 50MB limit
                raise ValueError(f"Image file too large (>50MB): {image_path}")
            
            return base64.b64encode(content).decode('utf-8')
            
        except (OSError, IOError) as e:
            raise Exception(f"Failed to read image file {image_path}: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to encode image {image_path}: {str(e)}")
    
    async def _upload_file_to_layer(self, file_path: str) -> str:
        """Upload file with proper validation (BUG #3 FIX)."""
        # Validate input
        if not file_path or not os.path.exists(file_path):
            raise ValueError(f"Invalid file path: {file_path}")
        
        mutation = """
        mutation CreateUploadUrls($input: CreateUploadUrlsInput!) {
            createUploadUrls(input: $input) {
                ... on UploadUrls {
                    uploadUrls {
                        url
                        fileId
                    }
                }
                ... on Error {
                    message
                }
            }
        }
        """
        
        filename = os.path.basename(file_path)
        variables = {
            "input": {
                "workspaceId": self.workspace_id,
                "filenames": [filename]
            }
        }
        
        try:
            result = await self._make_graphql_request(mutation, variables)
            
            # FIX: Validate response structure before accessing
            create_upload_response = result.get("data", {}).get("createUploadUrls")
            if not create_upload_response:
                raise Exception("Invalid response from createUploadUrls")
            
            # Check for error response
            if "message" in create_upload_response:
                raise Exception(f"Upload URL creation failed: {create_upload_response['message']}")
            
            # Validate upload URLs exist
            upload_urls = create_upload_response.get("uploadUrls", [])
            if not upload_urls:
                raise Exception("No upload URLs received from Layer.ai API")
            
            upload_info = upload_urls[0]
            upload_url = upload_info.get("url")
            file_id = upload_info.get("fileId")
            
            if not upload_url or not file_id:
                raise Exception("Invalid upload URL or file ID received")
            
        except Exception as e:
            raise Exception(f"Failed to get upload URL: {str(e)}")
        
        # Upload the file with error handling
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                upload_response = await client.put(upload_url, content=file_content)
                if upload_response.status_code not in [200, 201]:
                    raise Exception(f"Upload failed with status {upload_response.status_code}: {upload_response.text}")
        
        except Exception as e:
            raise Exception(f"Failed to upload file: {str(e)}")
        
        # Return the file URL for Layer.ai
        return f"https://media.app.layer.ai/workspaces/{self.workspace_id}/files/{file_id}/{filename}"
    
    async def _handle_input_files(self, input_files: list) -> Dict[str, Any]:
        """Handle input files with proper error reporting (BUG #4 FIX)."""
        if not input_files:
            return {}
        
        file_urls = []
        failed_uploads = []
        
        for file_path in input_files:
            if not os.path.exists(file_path):
                failed_uploads.append(f"{file_path} (file not found)")
                continue
            
            try:
                file_url = await self._upload_file_to_layer(file_path)
                file_urls.append({"url": file_url})
                logger.info(f"✅ Uploaded: {file_path}")
            except Exception as e:
                logger.error(f"❌ Failed to upload {file_path}: {e}")
                failed_uploads.append(f"{file_path} ({str(e)})")
        
        # If any uploads failed, report to user
        if failed_uploads:
            error_msg = f"❌ Failed to upload {len(failed_uploads)} file(s):\n" + "\n".join(f"  • {f}" for f in failed_uploads)
            if not file_urls:
                # All uploads failed
                raise Exception(error_msg)
            else:
                # Some uploads succeeded, warn user
                logger.warning(error_msg)
        
        return {"files": file_urls} if file_urls else {}
    
    async def _wait_for_completion_with_retry(self, inference_id: str, save_path: str) -> str:
        """Wait for completion with proper error handling (BUG #5 FIX)."""
        response_text = "⏳ Waiting for completion...\n"
        max_wait_time = 300
        check_interval = 5
        elapsed_time = 0
        consecutive_failures = 0
        max_consecutive_failures = 3
        
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
                ... on Error {
                    message
                }
            }
        }
        """
        
        while elapsed_time < max_wait_time:
            try:
                status_variables = {
                    "input": {
                        "inferenceIds": [inference_id]
                    }
                }
                
                # FIX: Add error handling for GraphQL requests
                status_result = await self._make_graphql_request(status_query, status_variables)
                
                # Validate response structure
                get_inferences_response = status_result.get("data", {}).get("getInferencesById")
                if not get_inferences_response:
                    raise Exception("Invalid response structure from getInferencesById")
                
                # Check for error response
                if "message" in get_inferences_response:
                    raise Exception(f"API error: {get_inferences_response['message']}")
                
                inferences = get_inferences_response.get("inferences", [])
                if not inferences:
                    return "❌ Inference not found."
                
                # Reset failure counter on successful request
                consecutive_failures = 0
                
                inference_data = inferences[0]
                current_status = inference_data.get("status", "UNKNOWN")
                
                if current_status == "COMPLETE":
                    response_text += f"✅ Completed in {elapsed_time} seconds!\n\n"
                    return response_text + await self._download_result_files(inference_data, save_path)
                    
                elif current_status == "FAILED":
                    return response_text + f"❌ Generation failed after {elapsed_time} seconds."
                    
                elif current_status == "CANCELLED":
                    return response_text + f"⚠️ Generation was cancelled after {elapsed_time} seconds."
                
                # Continue waiting for IN_PROGRESS status
                
            except Exception as e:
                consecutive_failures += 1
                logger.warning(f"Failed to check inference status (attempt {consecutive_failures}): {e}")
                
                if consecutive_failures >= max_consecutive_failures:
                    return response_text + f"❌ Failed to check status after {consecutive_failures} attempts. Last error: {str(e)}"
            
            # Wait before next check
            await asyncio.sleep(check_interval)
            elapsed_time += check_interval
        
        return response_text + f"⏰ Generation timed out after {max_wait_time} seconds."
    
    def _determine_file_extension(self, content_type: str, filename: str) -> str:
        """Determine proper file extension (BUG #6 FIX)."""
        # First try to get extension from content type
        content_type_lower = content_type.lower()
        
        if 'image' in content_type_lower:
            if 'png' in content_type_lower:
                return '.png'
            elif 'jpeg' in content_type_lower or 'jpg' in content_type_lower:
                return '.jpg'
            elif 'gif' in content_type_lower:
                return '.gif'
            elif 'svg' in content_type_lower:
                return '.svg'
            elif 'webp' in content_type_lower:
                return '.webp'
            else:
                return '.png'  # Default for images
                
        elif 'video' in content_type_lower:
            if 'mp4' in content_type_lower:
                return '.mp4'
            elif 'webm' in content_type_lower:
                return '.webm'
            elif 'avi' in content_type_lower:
                return '.avi'
            else:
                return '.mp4'  # Default for videos
                
        elif 'audio' in content_type_lower:
            if 'wav' in content_type_lower:
                return '.wav'
            elif 'mp3' in content_type_lower:
                return '.mp3'
            elif 'ogg' in content_type_lower:
                return '.ogg'
            else:
                return '.wav'  # Default for audio
                
        elif 'model' in content_type_lower or 'application/octet-stream' in content_type_lower:
            return '.glb'  # Default for 3D models
            
        else:
            # Try to get extension from filename
            file_ext = Path(filename).suffix
            if file_ext:
                return file_ext
            else:
                # Ultimate fallback based on common patterns
                return '.png'  # Most common case


# Example of how to apply these fixes to the main server class
def apply_critical_fixes():
    """Instructions for applying critical bug fixes."""
    print("""
🔧 CRITICAL BUG FIXES READY

To apply these fixes to your Layer.ai MCP Server:

1. Replace the buggy methods in fully_working_layer_ai_server.py with the fixed versions above
2. Update error handling throughout the codebase
3. Test thoroughly with edge cases (missing files, network issues, etc.)

Key improvements:
✅ Graceful error handling instead of sys.exit()
✅ File validation and size limits
✅ GraphQL response validation
✅ Retry logic for network issues
✅ Proper file extension detection
✅ Comprehensive error reporting

Priority: CRITICAL - Apply before production use!
""")


if __name__ == "__main__":
    apply_critical_fixes()