# Chroma SaaS — FastAPI Backend

Multi-tenant SaaS platform for professional hair salons to track color formulas and inventory.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Seed Database

```bash
python -m src.seed.seed_data
```

This creates:
- Two demo tenants (Salon One - Premium, Salon Two - Basic)
- Three users:
  - `admin@salonone.com` / `password123` (ADMIN)
  - `mike@salonone.com` / `password123` (EMPLOYEE)
  - `admin@salontwo.com` / `password123` (ADMIN)
- Product catalog (Redken Shades EQ, Wella Color Touch)
- Sample inventory items

### 3. Start the Server

```bash
uvicorn src.main:app --reload
```

### 4. Access Swagger UI

Open your browser to:
- **Swagger UI**: http://localhost:8000/swagger
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Tenant Registration

New salons can register themselves using the public registration endpoint:

**Request:**
```json
POST /api/v1/tenants/register
{
  "tenant_name": "My Salon",
  "plan": "premium",
  "admin_email": "owner@mysalon.com",
  "admin_password": "secure_password123",
  "admin_full_name": "John Owner",
  "location_name": "Main Branch",
  "location_address": "123 Main St, City, State",
  "location_timezone": "America/New_York"
}
```

**Response:**
```json
{
  "tenant": {
    "id": "...",
    "name": "My Salon",
    "plan": "premium",
    "status": "trial",
    "created_at": "..."
  },
  "location": {
    "id": "...",
    "name": "Main Branch",
    "tenant_id": "...",
    "created_at": "..."
  },
  "admin_user_id": "...",
  "admin_email": "owner@mysalon.com",
  "message": "Tenant registered successfully. You can now login with your admin credentials."
}
```

After registration, use the admin email and password to login.

## Authentication

### Login

Simply use email and password:

**Request:**
```json
POST /api/v1/users/login
{
  "email": "admin@salonone.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### Token Response

Login returns both access and refresh tokens:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### Using Tokens

Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### Refresh Token

Use `/api/v1/users/refresh` endpoint with the refresh token to get a new access token:
```json
{
  "refresh_token": "eyJ..."
}
```

## API Endpoints

All endpoints are prefixed with `/api/v1`:

- `/tenants` - Tenant management
- `/users` - User management and authentication
- `/customers` - Customer management
- `/products` - Product catalog (brands, lines, products, tenant products)
- `/inventory` - Inventory items and transactions
- `/formulas` - Color formulas

## Pagination

All list endpoints use **page-based pagination**:

- `page` (default: 1, min: 1)
- `page_size` (default: 20, min: 1, max: 100)

Response format:
```json
{
  "items": [...],
  "page": 1,
  "page_size": 20,
  "total": 100,
  "total_pages": 5
}
```

## Environment Variables

Create a `.env` file (see `env.example`):

```env
DATABASE_URL=sqlite:///./chroma.db
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Development

- Database: SQLite (default) or PostgreSQL
- Auto-reload: Use `--reload` flag with uvicorn
- Database tables: Auto-created on startup (use Alembic for production)

## Project Structure

```
src/
├── main.py           # FastAPI app entry point
├── config.py         # Settings
├── database.py       # SQLAlchemy setup
├── models/           # ORM models
├── schemas/          # Pydantic schemas
├── crud/             # Database operations
├── routers/          # API endpoints
├── utils/            # Utilities (security, pagination)
└── seed/             # Seed scripts
```

