# Security Guide - Layer.ai MCP Server

## 🔐 Overview

This Layer.ai MCP Server implements enterprise-grade security practices to protect your API credentials and ensure safe operation in development and production environments.

## 🛡️ Security Features

### 1. Encrypted Credential Storage
- **AES-256 Encryption**: Industry-standard encryption for API tokens
- **PBKDF2 Key Derivation**: Secure key generation from passwords
- **Salt-based Security**: Unique salts prevent rainbow table attacks
- **No Plain Text Storage**: Credentials never stored in readable format

### 2. File System Security
- **Restricted Permissions**: Credential files set to 600 (owner read-only)
- **Secure Directory**: Credentials stored in `.layer-mcp/secure/` directory
- **Automatic Cleanup**: Temporary files securely deleted
- **Path Validation**: Input paths validated to prevent directory traversal

### 3. Network Security
- **HTTPS Only**: All API communications use TLS encryption
- **Token Validation**: API tokens validated before use
- **Request Timeouts**: Prevents hanging connections
- **Error Sanitization**: Sensitive data removed from error messages

## 🔑 Credential Management

### Initial Setup
```bash
python layer-mcp-server/setup.py
```

This interactive script:
1. Prompts for your Layer.ai API token
2. Validates token format and accessibility
3. Encrypts credentials using AES-256
4. Stores encrypted data with restricted permissions
5. Provides setup confirmation

### Token Requirements
- **Format**: Must start with `pat_` (Personal Access Token)
- **Length**: Minimum 32 characters
- **Characters**: Alphanumeric and underscores only
- **Scope**: Must have appropriate workspace permissions

### Credential Storage Location
```
.layer-mcp/secure/
├── credentials.enc    # Encrypted credentials
├── salt.bin          # Encryption salt
└── key.bin           # Derived key (password-protected)
```

## 🔒 Encryption Details

### Algorithm: AES-256-CBC
- **Key Size**: 256 bits
- **Block Size**: 128 bits
- **Mode**: Cipher Block Chaining (CBC)
- **Padding**: PKCS7

### Key Derivation: PBKDF2
- **Hash Function**: SHA-256
- **Iterations**: 100,000
- **Salt Length**: 32 bytes
- **Key Length**: 32 bytes

### Implementation
```python
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, padding

# Key derivation
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
)

# AES encryption
cipher = Cipher(
    algorithms.AES(key),
    modes.CBC(iv)
)
```

## 🚨 Security Best Practices

### 1. Token Management
- **Regular Rotation**: Rotate API tokens every 90 days
- **Principle of Least Privilege**: Use tokens with minimal required permissions
- **Environment Separation**: Use different tokens for dev/staging/production
- **Monitoring**: Monitor token usage for unusual activity

### 2. File Permissions
```bash
# Verify secure permissions
ls -la .layer-mcp/secure/
# Should show: -rw------- (600)

# Fix permissions if needed
chmod 600 .layer-mcp/secure/*
chmod 700 .layer-mcp/secure/
```

### 3. Environment Variables
If using environment variables as fallback:
```bash
# Set with restricted scope
export LAYER_API_TOKEN="pat_your_token_here"
export LAYER_WORKSPACE_ID="your_workspace_id"

# Unset after use
unset LAYER_API_TOKEN
unset LAYER_WORKSPACE_ID
```

### 4. Version Control
The `.gitignore` file prevents accidental commits of:
- Credential files (`.layer-mcp/secure/`)
- Environment files (`.env*`)
- Token files (`*.token`, `*.credentials`)
- Backup directories with sensitive data

## 🔍 Security Validation

### Self-Check Commands
```bash
# Check file permissions
python -c "
import os, stat
path = '.layer-mcp/secure/credentials.enc'
if os.path.exists(path):
    mode = oct(stat.S_IMODE(os.stat(path).st_mode))
    print(f'Permissions: {mode}')
    print('✅ Secure' if mode == '0o600' else '❌ Insecure')
else:
    print('❌ Credentials not found')
"

# Validate token format
python -c "
import os
token = os.getenv('LAYER_API_TOKEN', '')
if token.startswith('pat_') and len(token) >= 32:
    print('✅ Token format valid')
else:
    print('❌ Invalid token format')
"
```

### Security Audit Checklist
- [ ] Credentials encrypted with AES-256
- [ ] File permissions set to 600
- [ ] No plain text tokens in config files
- [ ] `.gitignore` prevents credential commits
- [ ] API tokens rotated regularly
- [ ] Network communications use HTTPS
- [ ] Error messages don't expose sensitive data
- [ ] Temporary files cleaned up properly

## 🚨 Incident Response

### If Credentials Are Compromised
1. **Immediate Actions**:
   - Revoke the compromised API token in Layer.ai dashboard
   - Generate a new API token
   - Update credentials using setup script
   - Review access logs for unauthorized usage

2. **Investigation**:
   - Check git history for accidental commits
   - Review file system permissions
   - Audit network traffic logs
   - Verify backup security

3. **Prevention**:
   - Implement additional monitoring
   - Review security practices
   - Update documentation
   - Train team members

### Emergency Contacts
- **Layer.ai Support**: support@layer.ai
- **Security Issues**: security@layer.ai

## 🔧 Advanced Security Configuration

### Custom Encryption Password
```python
# Use custom password for encryption
token_manager = LayerTokenManager(password="your_secure_password")
```

### Network Proxy Support
```python
# Configure proxy for corporate environments
import httpx

client = httpx.AsyncClient(
    proxies="http://proxy.company.com:8080",
    verify="/path/to/ca-bundle.crt"
)
```

### Logging Security
```python
import logging

# Configure secure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('layer_mcp.log', mode='a'),
        logging.StreamHandler()
    ]
)

# Sanitize sensitive data in logs
logger.info(f"Token: {token[:8]}...")  # Only log first 8 chars
```

## 📋 Compliance

### Standards Compliance
- **OWASP**: Follows OWASP secure coding practices
- **NIST**: Implements NIST cybersecurity framework guidelines
- **SOC 2**: Compatible with SOC 2 Type II requirements
- **GDPR**: Supports data protection requirements

### Audit Trail
The server maintains logs of:
- Authentication attempts
- API requests and responses (sanitized)
- File operations
- Error conditions
- Security events

## 🔗 Additional Resources

- [Layer.ai Security Documentation](https://docs.layer.ai/security)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Python Cryptography Documentation](https://cryptography.io/)

---

**Remember**: Security is an ongoing process. Regularly review and update your security practices to protect against evolving threats.