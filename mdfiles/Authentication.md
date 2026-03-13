# Authentication API

## Login

Authenticate a user with email and password.

**Endpoint:** `POST /users/login`

**Authentication:** Not required

**Request Body:**
```json
{
  "email": "admin@salonone.com",
  "password": "password123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized` - Incorrect email or password
- `403 Forbidden` - User account is inactive

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@salonone.com",
    "password": "password123"
  }'
```

---

## Refresh Token

Get a new access token using a refresh token.

**Endpoint:** `POST /users/refresh`

**Authentication:** Not required

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or expired refresh token

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/users/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

---

## Get Current User

Get information about the currently authenticated user.

**Endpoint:** `GET /users/me`

**Authentication:** Required (Bearer token)

**Response:** `200 OK`
```json
{
  "id": "958aaa38-af27-4c73-b8ae-42b3ca8e2a9b",
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "full_name": "Alice Admin",
  "email": "admin@salonone.com",
  "role": "ADMIN",
  "is_active": true,
  "default_location_id": "abc123...",
  "last_login_at": "2024-01-15T10:30:00Z",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Error Responses:**
- `401 Unauthorized` - Missing or invalid token

**Example:**
```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Token Expiration

- **Access Token:** 60 minutes (configurable)
- **Refresh Token:** 7 days (configurable)

## Using Tokens

Include the access token in the Authorization header for all protected endpoints:

```
Authorization: Bearer <access_token>
```

## Swagger UI Authorization

In Swagger UI:
1. Click the "Authorize" button (lock icon)
2. Paste your access token in the "Value" field
3. Click "Authorize"
4. Click "Close"

All subsequent requests will include the token automatically.




