# Security Policy

## Overview

This project implements a secure authentication and authorization system that simulates real-world security practices.

It includes:
- Multi-Factor Authentication (MFA)
- Behavioral authentication (keystroke dynamics)
- JWT-based authentication
- Session-based authentication
- Role-Based Access Control (RBAC)

---

## Authentication
- Passwords are hashed using bcrypt
- Two-Factor Authentication (2FA) via TOTP (pyotp)
- QR codes for authenticator apps (e.g. Google Authenticator)
- Additional behavioral verification (keystroke dynamics)

---

## Token Security
JWT tokens contain:
- user_id
- role
- exp (expiration time)

Short-lived access tokens (security best practice)
Refresh tokens used to obtain new access tokens

Token validation includes:
- signature verification
- expiration check

---

## Session Security
- Session-based authentication supported
- Sessions stored in memory
- Sessions can be invalidated (logout)

---

## Authorization (RBAC)
Role-Based Access Control implemented
Roles:
admin → full access
user → limited access
Permissions checked on each request

---

## Security Features
- Access denied without authentication
- Token expiration handling
- JWT blacklist (logout)
- Replay attack detection
- Rate limiting per user
- Behavioral MFA verification

---

## Replay Attack Detection

The system prevents token reuse.

Example:

First request: ADMIN DATA
Second request: REPLAY ATTACK DETECTED

---

## Logout
JWT → added to blacklist
Session → removed from session store

---

## Reporting a Vulnerability

If you discover a potential security issue, please report it responsibly.

You can:

Open an issue on GitHub

Please include:

- Description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Potential impact

---

##Limitations

This project is a simplified simulation:

- Uses local file storage (users.json)
- No real HTTP/HTTPS communication
- No persistent database
- Behavioral authentication is simplified

---

## Responsible Use

This project is intended for:

Education
- Demonstration of security concepts

It should not be used for malicious purposes.

---

## Disclaimer

This software is provided "as is" without any warranties.

The author is not responsible for misuse of this project.

---

## Summary

This system demonstrates a layered security approach:

- Authentication (login + 2FA)
- Authorization (RBAC)
- Behavioral verification
- Token-based security
