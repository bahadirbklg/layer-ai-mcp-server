#!/usr/bin/env python3
"""Setup secure credentials for Layer.ai MCP server."""

import sys

from auth import LayerTokenManager


def main():
    """Interactive credential setup."""
    print("🔐 Layer.ai MCP Server - Secure Credential Setup")
    print("=" * 55)
    print("This will securely store your Layer.ai credentials using encryption.")
    print("Your API token will be encrypted and stored locally.\n")

    try:
        manager = LayerTokenManager()

        # Check if credentials already exist
        existing = manager.get_credentials()
        if existing:
            print("✅ Existing credentials found!")
            print(f"🏢 Workspace ID: {existing['workspace_id']}")
            print(f"🔑 API Token: [CONFIGURED]\n")

            overwrite = (
                input("Do you want to update these credentials? (y/N): ")
                .strip()
                .lower()
            )
            if overwrite not in ["y", "yes"]:
                print("👍 Keeping existing credentials.")
                return

        # Get new credentials
        print("\n📝 Enter your Layer.ai credentials:")
        print("You can find these at: https://app.layer.ai/settings/api-keys\n")

        api_token = input("🔑 API Token (starts with 'pat_'): ").strip()
        if not api_token:
            print("❌ API token is required")
            sys.exit(1)

        workspace_id = input("🏢 Workspace ID: ").strip()
        if not workspace_id:
            print("❌ Workspace ID is required")
            sys.exit(1)

        # Store credentials
        print("\n🔒 Encrypting and storing credentials...")
        if manager.store_credentials(api_token, workspace_id):
            print("✅ Credentials stored securely!")
            print("\n🎉 Setup complete! Your Layer.ai MCP server is ready to use.")
            print("🔐 Your API token is encrypted and stored in .layer-mcp/secure/")
            print("🚀 You can now use the MCP server without exposing your token.")
        else:
            print("❌ Failed to store credentials")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
