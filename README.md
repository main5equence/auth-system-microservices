# Authentication & Authorization System (JWT + MFA + Behavioral Auth)

## Project Overview
This project implements a secure authentication and authorization system simulating a microservices architecture.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Security](https://img.shields.io/badge/Security-MFA%20%7C%20JWT%20%7C%20RBAC-green)
![Behavioral Auth](https://img.shields.io/badge/Auth-Behavioral%20Auth-orange)
![Architecture](https://img.shields.io/badge/Architecture-Microservices-blueviolet)
![Purpose](https://img.shields.io/badge/Purpose-Educational-lightgrey)

It includes:

- Multi-factor authentication (2FA)
- Behavioral authentication (keystroke dynamics)
- JWT-based authentication
- Session-based authentication
- Role-Based Access Control (RBAC)
- Security mechanisms (token expiration, blacklist, replay detection)

The system is designed to reflect real-world SaaS security architecture.

---

## System Architecture Diagram (microservises)

### System Flow

```
User (Client)
   ↓
AuthService → authentication (login + 2FA) → issues JWT / session
   ↓
BehavioralAuth → optional keystroke verification (MFA)
   ↓
ResourceService → validates token / session
   ↓
RBAC → checks user role and permissions
   ↓
Access granted / denied
```

```mermaid
graph LR

Auth[Auth Service]
User[User Service]
Resource[Resource Service]
Behavior[Behavioral Auth]
RBAC[RBAC]
DB[(Database)]

Auth --> DB
User --> DB

Auth --> RBAC
Resource --> RBAC

Auth --> Behavior
Resource --> Auth
```



---

## Full Authentication Flow (MFA + Behavioral Auth + JWT)
This diagram represents a full multi-factor authentication flow including behavioral verification.

```mermaid
sequenceDiagram

participant U as User
participant A as AuthService
participant B as BehavioralAuth
participant R as ResourceService

U->>A: login (login + password)
A->>A: verify password

A->>U: request 2FA code
U->>A: TOTP code

A->>B: verify keystroke pattern
B-->>A: OK / FAIL

A->>U: JWT + Session

U->>R: request resource + token
R->>R: verify JWT + RBAC

R-->>U: access granted / denied
```

---

## Features

### Authentication
- Username & password login
- Secure password hashing (bcrypt)
- Two-Factor Authentication (TOTP via Google Authenticator)
- Behavioral authentication (keystroke dynamics)

<img width="217" height="110" alt="image" src="https://github.com/user-attachments/assets/d1d4523e-fe43-43c0-bde3-000f7830866e" />


### Authorization
Role-Based Access Control (RBAC)
Roles:
admin → full access
user → limited 

<img width="376" height="201" alt="image" src="https://github.com/user-attachments/assets/4f1c67f6-09d6-4bac-b3b0-3443d956d64b" />


### Token System
- JWT (short-lived access token)
- Refresh token
- Token expiration handling

<img width="235" height="94" alt="image" src="https://github.com/user-attachments/assets/58988f25-63a6-40e4-a593-e23d5d45adec" />


### Behavioral Authentication 
- Learns typing patterns during registration
- Measures time between keystrokes
- Verifies user behavior during login

<img width="345" height="226" alt="image" src="https://github.com/user-attachments/assets/5729690e-8fbc-4fa4-94a0-f2479dc977d5" />


### Session System
- Session-based authentication (alternative to JWT)
- Session storage in memory
- Session invalidation (logout)

<img width="360" height="387" alt="image" src="https://github.com/user-attachments/assets/f8ba24e1-55a5-448d-8cac-c0f8262ac81d" />


### Security Mechanisms
- Access denied without authentication
- Token expiration handling
- Role-based restrictions (RBAC)
- Replay attack detection
- Rate limiting (per user)
- Logout (JWT blacklist + session removal)
- Test Scenarios

<img width="415" height="74" alt="image" src="https://github.com/user-attachments/assets/04bd9ce8-c35e-47b3-8027-e8593bb6706f" />


---

### The system demonstrates:

- User login
- Valid token → OK
- Missing token → FAIL
- Wrong role → FORBIDDEN
- Token expiration → FAIL
- Refresh token → new access granted
- JWT vs Session differences
- Logout (JWT + session)
- Replay attack detection

```mermaid
graph TD

User --> AuthService
AuthService --> TokenService
AuthService --> SessionStore
AuthService --> UserService

User --> ResourceService

ResourceService --> TokenService
ResourceService --> SessionStore
ResourceService --> RBAC

TokenService --> Blacklist
ResourceService --> ReplayDetection
ResourceService --> RateLimit
```

---

### JWT vs Session diagram

```mermaid
flowchart LR

subgraph JWT Mode
A1[Client] -->|JWT| B1[Resource Service]
B1 -->|verify token| C1[Token Service]
end

subgraph Session Mode
A2[Client] -->|session_id| B2[Resource Service]
B2 -->|check session| C2[Session Store]
end
```
---

### Example Behavior
- Scenario	Result
- Valid admin token	ADMIN DATA
- Missing token	FAIL
- User accessing admin resource	FORBIDDEN
- Expired token	FAIL
- Replay attack	DETECTED

---

### Technologies
- Python 3
- bcrypt – password hashing
- pyotp – 2FA (TOTP)
- qrcode – QR generation
- pyjwt – JWT handling

---

### Project Structure

```
auth-system/
│
├── README.md
├── requirements.txt
│
├── auth_service/
│   ├── __init__.py
│   ├── auth.py
│   ├── token_service.py
│   └── session_store.py
│   └── token_blacklist.py   
│
├── user_service/
│   ├── __init__.py
│   └── user.py
│
├── resource_service/
│   ├── __init__.py
│   └── resource.py
│
├── behavioral_auth/
│   ├── __init__.py
│   └── keystroke.py
│
├── rbac/
│   ├── __init__.py
│   └── roles.py
│
├── database/
│   ├── __init__.py
│   └── db.py
│
├── rate_limit.py
│
├── replay_detection.py
│
└── main.py
```

---

### How to Run
1. Install dependencies

```
pip install -r requirements.txt
```

2. Run the application

```
python main.py
```

---

### Key Concepts
- Authentication → verifies identity (login, 2FA, keystroke)
- Authorization → determines access (RBAC)
- JWT vs Session → stateless vs stateful authentication

---

### Conclusion

This project demonstrates a complete authentication system combining:

- Traditional login
- Multi-factor authentication
- Behavioral biometrics
- Token-based security
- Microservice-like architecture

It reflects real-world security design principles used in modern cloud systems.

