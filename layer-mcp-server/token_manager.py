#!/usr/bin/env python3
"""Secure API token management for Layer.ai MCP server."""

import os
import json
import base64
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class SecureTokenManager:
    """Secure token management with encryption and validation."""
    
    def __init__(self, config_dir: str = ".kiro/secure"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.token_file = self.config_dir / "layer_tokens.enc"
        self.key_file = self.config_dir / ".key"
        
    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key."""
        if self.key_file.exists():
            return self.key_file.read_bytes()
        
        # Generate new key from system entropy
        key = Fernet.generate_key()
        self.key_file.write_bytes(key)
        self.key_file.chmod(0o600)  # Read-only for owner
        return key
    
    def _encrypt_data(self, data: str) -> bytes:
        """Encrypt sensitive data."""
        key = self._get_or_create_key()
        f = Fernet(key)
        return f.encrypt(data.encode())
    
    def _decrypt_data(self, encrypted_data: bytes) -> str:
        """Decrypt sensitive data."""
        key = self._get_or_create_key()
        f = Fernet(key)
        return f.decrypt(encrypted_data).decode()
    
    def store_token(self, token: str, workspace_id: str) -> bool:
        """Store API token securely."""
        try:
            # Validate token format
            if not self._validate_token(token):
                raise ValueError("Invalid Layer.ai token format")
            
            # Prepare data
            token_data = {
                "api_token": token,
                "workspace_id": workspace_id,
                "token_hash": hashlib.sha256(token.encode()).hexdigest()[:16]
            }
            
            # Encrypt and store
            encrypted_data = self._encrypt_data(json.dumps(token_data))
            self.token_file.write_bytes(encrypted_data)
            self.token_file.chmod(0o600)  # Read-only for owner
            
            return True
        except Exception as e:
            print(f"❌ Failed to store token: {e}")
            return False
    
    def get_token(self) -> Optional[Dict[str, str]]:
        """Retrieve API token securely."""
        try:
            if not self.token_file.exists():
                return None
            
            encrypted_data = self.token_file.read_bytes()
            decrypted_data = self._decrypt_data(encrypted_data)
            token_data = json.loads(decrypted_data)
            
            # Validate token is still valid format
            if not self._validate_token(token_data["api_token"]):
                print("⚠️ Stored token appears invalid")
                return None
            
            return {
                "api_token": token_data["api_token"],
                "workspace_id": token_data["workspace_id"]
            }
        except Exception as e:
            print(f"❌ Failed to retrieve token: {e}")
            return None
    
    def _validate_token(self, token: str) -> bool:
        """Validate Layer.ai token format."""
        if not token:
            return False
        
        # Layer.ai tokens start with 'pat_' and are ~100 chars
        if not token.startswith("pat_"):
            return False
        
        if len(token) < 50 or len(token) > 200:
            return False
        
        # Check for valid base64-like characters after prefix
        import re
        if not re.match(r'^pat_[A-Za-z0-9_-]+$', token):
            return False
        
        return True
    
    def clear_token(self) -> bool:
        """Clear stored token."""
        try:
            if self.token_file.exists():
                self.token_file.unlink()
            return True
        except Exception as e:
            print(f"❌ Failed to clear token: {e}")
            return False


class EnvironmentTokenManager:
    """Fallback token manager using environment variables with validation."""
    
    @staticmethod
    def get_token() -> Optional[Dict[str, str]]:
        """Get token from environment variables."""
        api_token = os.getenv("LAYER_API_TOKEN", "").strip()
        workspace_id = os.getenv("LAYER_WORKSPACE_ID", "").strip()
        
        if not api_token or not workspace_id:
            return None
        
        # Validate token format
        if not api_token.startswith("pat_") or len(api_token) < 50:
            print("⚠️ Invalid LAYER_API_TOKEN format")
            return None
        
        # Validate workspace ID format (UUID-like)
        import re
        if not re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', workspace_id):
            print("⚠️ Invalid LAYER_WORKSPACE_ID format")
            return None
        
        return {
            "api_token": api_token,
            "workspace_id": workspace_id
        }


class LayerTokenManager:
    """Main token manager with multiple fallback strategies."""
    
    def __init__(self):
        self.secure_manager = SecureTokenManager()
        self.env_manager = EnvironmentTokenManager()
    
    def get_credentials(self) -> Optional[Dict[str, str]]:
        """Get credentials using best available method."""
        # Try secure storage first
        credentials = self.secure_manager.get_token()
        if credentials:
            print("🔐 Using securely stored credentials")
            return credentials
        
        # Fallback to environment variables
        credentials = self.env_manager.get_token()
        if credentials:
            print("🔑 Using environment variable credentials")
            return credentials
        
        print("❌ No valid credentials found")
        return None
    
    def store_credentials(self, api_token: str, workspace_id: str) -> bool:
        """Store credentials securely."""
        return self.secure_manager.store_token(api_token, workspace_id)
    
    def setup_interactive(self) -> bool:
        """Interactive setup for credentials."""
        print("🔐 Layer.ai MCP Server - Secure Credential Setup")
        print("=" * 50)
        
        # Get API token
        api_token = input("Enter your Layer.ai API token (pat_...): ").strip()
        if not api_token:
            print("❌ API token is required")
            return False
        
        # Get workspace ID
        workspace_id = input("Enter your Layer.ai workspace ID: ").strip()
        if not workspace_id:
            print("❌ Workspace ID is required")
            return False
        
        # Store securely
        if self.store_credentials(api_token, workspace_id):
            print("✅ Credentials stored securely!")
            print("🔒 Your API token is encrypted and stored locally")
            return True
        else:
            print("❌ Failed to store credentials")
            return False


if __name__ == "__main__":
    # Interactive setup
    manager = LayerTokenManager()
    manager.setup_interactive()