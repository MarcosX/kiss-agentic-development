# FastAPI Password Reset Implementation Plan

**Goal**: Create a new FastAPI web application that implements a password reset request endpoint following existing patterns (User model with email and password_hash, in-memory user store) as specified in the requirements.

**Architecture**: A standalone FastAPI application with modular structure (models, schemas, stores/services, routers). The app will define the User model as specified, implement an in-memory user store with the same pattern as described, and expose POST /auth/password-reset. For a password reset request flow (even in this minimal form), the endpoint will accept an email, validate it against known users, and generate a reset token (stored in-memory) while following security best practices (generic success response to avoid user enumeration). The implementation will be test-driven per the practicing-tdd skill.

**Acceptance Criteria:**

- AC-1: The app exposes POST /auth/password-reset accepting {"user_email": "string"} and returns a well-formed response. [owned by: Task 1]
- AC-2: When a valid registered email is provided, the system generates and stores a password reset token associated with that user. [owned by: Task 3]
- AC-3: When an unknown email is provided, the system returns the same generic success response (no user enumeration) and does not create a token. [owned by: Task 4]
- AC-4: The app includes the specified User model (email: EmailStr, password_hash: str) and an in-memory user store following the required pattern. [owned by: Task 2]
- AC-5: Invalid/malformed email format is rejected with appropriate validation error (422) per Pydantic validation. [owned by: Task 1]
- AC-6: The application can start and the endpoint is reachable under /auth/password-reset. [owned by: Task 1]

---

## Task 1: Set up project structure, basic endpoint skeleton, validation

**Category:** Coding  
**Type:** AFK  
**Satisfies:** AC-1, AC-5, AC-6

**Files:**

- Create: `pyproject.toml`
- Create: `requirements.txt`
- Create: `app/__init__.py`
- Create: `app/main.py`
- Create: `app/schemas/auth.py`
- Create: `app/api/__init__.py`
- Create: `app/api/routes_auth.py`
- Create: `app/core/config.py`
- Test: `tests/test_auth_password_reset.py`

**Contract** (REQUIRED):

- **Schemas** (`app/schemas/auth.py`): `PasswordResetRequest` with `user_email` (EmailStr), `PasswordResetResponse` with consistent fields.
- **API endpoint** (`app/api/routes_auth.py`): Define `POST /auth/password-reset` accepting `PasswordResetRequest` body. Return generic success response with HTTP 200.
- **App setup** (`app/main.py`): FastAPI app instance, include auth router so endpoint is at `/auth/password-reset`. App must be importable as `app`.
- **Dependencies**: FastAPI, uvicorn[standard], pydantic[email].
- **Behavior**: Valid email → 200 with generic message; invalid email → validation error (422 by FastAPI default).

**Done when**:
- Contract behavior verified through test-first loop (per practicing-tdd)
- Full test suite passes with no regressions
- Lint shows no errors or warnings
- Application builds/runs locally

---

## Task 2: Implement User model and in-memory user store

**Category:** Coding  
**Type:** AFK  
**Satisfies:** AC-4

**Files:**

- Create: `app/models/user.py`
- Create: `app/stores/user_store.py`
- Test: `tests/test_user_store.py`

**Contract** (REQUIRED):

- **User model** (`app/models/user.py`): `User` with `email: EmailStr` and `password_hash: str` (Pydantic BaseModel).
- **In-memory user store** (`app/stores/user_store.py`): Module-level store supporting add, get_by_email (case-insensitive), clear. Keyed by normalized lowercase email.

**Done when**:
- Contract behavior verified through test-first loop
- Full test suite passes with no regressions
- Lint shows no errors or warnings

---

## Task 3: Generate and store reset tokens for existing users

**Category:** Coding  
**Type:** AFK  
**Satisfies:** AC-2

**Files:**

- Create: `app/core/security.py`
- Create: `app/stores/token_store.py`
- Modify: `app/api/routes_auth.py`
- Test: `tests/test_auth_password_reset.py`

**Contract** (REQUIRED):

- **Token generation** (`app/core/security.py`): `generate_reset_token()` returns URL-safe token using secrets.
- **Token store** (`app/stores/token_store.py`): In-memory store mapping token → email, supports store/retrieve/query by email.
- **Endpoint**: When user exists (case-insensitive lookup), generate token and store it; response is identical generic success (200). Token must not be returned.

**Done when**:
- Contract behavior verified through test-first loop
- Full test suite passes with no regressions
- Lint shows no errors or warnings

---

## Task 4: Handle unknown emails with generic response (no enumeration)

**Category:** Coding  
**Type:** AFK  
**Satisfies:** AC-3

**Files:**

- Modify: `app/api/routes_auth.py`
- Test: `tests/test_auth_password_reset.py`

**Contract** (REQUIRED):

- Unknown email (valid format) returns identical generic success (200), no token created. Lookup is case-insensitive.

**Done when**:
- Contract behavior verified through test-first loop
- Full test suite passes with no regressions
- Lint shows no errors or warnings
