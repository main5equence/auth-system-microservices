# auth-system-microservices
Multi-factor authentication system with RBAC, JWT, sessions and behavioral biometrics (keystroke dynamics) implemented in microservices-style architecture.





---

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
└── main.py
```

---

## 1. Architecture Diagram (microservises)


```
main.py
   ↓
AuthService → login → JWT / session
   ↓
ResourceService → sprawdza token / sesję
   ↓
RBAC → sprawdza role
   ↓
BehavioralAuth → opcjonalna dodatkowa weryfikacja
```


```mermaid
graph TD

A[Client / main.py] --> B[Auth Service]
A --> C[Resource Service]
A --> D[User Service]

B --> E[Token Service JWT]
B --> F[Session Store]

C --> E
C --> F

C --> G[RBAC]

B --> H[Database]
D --> H
```

---

## 2. Login Diagram (2FA + MFA)

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


## 3. JWT vs Session diagram


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

## 4. System Structure

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

## How to run 

```
pip install -r requirements.txt
```

```
python main.py
```










