# Tenants API

## Register Tenant

Register a new tenant (salon business). This is a public endpoint that creates a tenant, default location, and admin user.

**Endpoint:** `POST /tenants/register`

**Authentication:** Not required

**Request Body:**
```json
{
  "tenant_name": "Elite Hair Salon",
  "plan": "premium",
  "admin_email": "owner@elitehair.com",
  "admin_password": "secure_password123",
  "admin_full_name": "Jane Smith",
  "location_name": "Downtown Location",
  "location_address": "456 Main St, City, State 12345",
  "location_timezone": "America/New_York"
}
```

**Required Fields:**
- `tenant_name` (string) - Name of the salon business
- `admin_email` (string, email) - Email for the admin user
- `admin_password` (string) - Password for the admin user
- `admin_full_name` (string) - Full name of the admin user
- `location_name` (string) - Name of the default location

**Optional Fields:**
- `plan` (string) - Plan type: "trial", "basic", "premium" (default: "trial")
- `location_address` (string) - Address of the location
- `location_timezone` (string) - Timezone (e.g., "America/New_York")

**Response:** `201 Created`
```json
{
  "tenant": {
    "id": "79dcbe8c-b004-4705-a5ad-767223660e75",
    "name": "Elite Hair Salon",
    "plan": "premium",
    "status": "trial",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "location": {
    "id": "abc123-def456-ghi789",
    "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
    "name": "Downtown Location",
    "address": "456 Main St, City, State 12345",
    "timezone": "America/New_York",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "admin_user_id": "958aaa38-af27-4c73-b8ae-42b3ca8e2a9b",
  "admin_email": "owner@elitehair.com",
  "message": "Tenant registered successfully. You can now login with your admin credentials."
}
```

**Error Responses:**
- `409 Conflict` - Email already registered

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/tenants/register" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_name": "Elite Hair Salon",
    "plan": "premium",
    "admin_email": "owner@elitehair.com",
    "admin_password": "secure_password123",
    "admin_full_name": "Jane Smith",
    "location_name": "Downtown Location",
    "location_address": "456 Main St",
    "location_timezone": "America/New_York"
  }'
```

---

## List Tenants

List all tenants (ADMIN only).

**Endpoint:** `GET /tenants/`

**Authentication:** Required (ADMIN role)

**Query Parameters:**
- `page` (integer, default: 1) - Page number
- `page_size` (integer, default: 20, max: 100) - Items per page

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "79dcbe8c-b004-4705-a5ad-767223660e75",
      "name": "Elite Hair Salon",
      "plan": "premium",
      "status": "active",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "page": 1,
  "page_size": 20,
  "total": 1,
  "total_pages": 1
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/api/v1/tenants/?page=1&page_size=20" \
  -H "Authorization: Bearer <token>"
```

---

## Get Tenant

Get tenant details.

**Endpoint:** `GET /tenants/{tenant_id}`

**Authentication:** Required (must be tenant member or ADMIN)

**Path Parameters:**
- `tenant_id` (UUID) - Tenant ID

**Response:** `200 OK`
```json
{
  "id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "name": "Elite Hair Salon",
  "plan": "premium",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `403 Forbidden` - Not a member of this tenant
- `404 Not Found` - Tenant not found

---

## Create Tenant

Create a new tenant (ADMIN only).

**Endpoint:** `POST /tenants/`

**Authentication:** Required (ADMIN role)

**Request Body:**
```json
{
  "name": "New Salon",
  "plan": "basic",
  "status": "trial"
}
```

**Response:** `201 Created`
```json
{
  "id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "name": "New Salon",
  "plan": "basic",
  "status": "trial",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## Update Tenant

Update tenant information (ADMIN only).

**Endpoint:** `PATCH /tenants/{tenant_id}`

**Authentication:** Required (ADMIN role)

**Path Parameters:**
- `tenant_id` (UUID) - Tenant ID

**Request Body:**
```json
{
  "name": "Updated Salon Name",
  "plan": "premium",
  "status": "active"
}
```

**Response:** `200 OK`
```json
{
  "id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "name": "Updated Salon Name",
  "plan": "premium",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## Delete Tenant

Delete a tenant (ADMIN only).

**Endpoint:** `DELETE /tenants/{tenant_id}`

**Authentication:** Required (ADMIN role)

**Path Parameters:**
- `tenant_id` (UUID) - Tenant ID

**Response:** `204 No Content`

---

## List Locations

List all locations for a tenant.

**Endpoint:** `GET /tenants/{tenant_id}/locations`

**Authentication:** Required (must be tenant member or ADMIN)

**Path Parameters:**
- `tenant_id` (UUID) - Tenant ID

**Query Parameters:**
- `page` (integer, default: 1) - Page number
- `page_size` (integer, default: 20, max: 100) - Items per page

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "abc123-def456-ghi789",
      "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
      "name": "Downtown Location",
      "address": "456 Main St",
      "timezone": "America/New_York",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "page": 1,
  "page_size": 20,
  "total": 1,
  "total_pages": 1
}
```

---

## Create Location

Create a new location for a tenant.

**Endpoint:** `POST /tenants/{tenant_id}/locations`

**Authentication:** Required (ADMIN or MANAGER role)

**Path Parameters:**
- `tenant_id` (UUID) - Tenant ID

**Request Body:**
```json
{
  "name": "Uptown Location",
  "address": "789 Park Ave",
  "timezone": "America/New_York"
}
```

**Response:** `201 Created`
```json
{
  "id": "xyz789-abc123-def456",
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "name": "Uptown Location",
  "address": "789 Park Ave",
  "timezone": "America/New_York",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## Update Location

Update location information.

**Endpoint:** `PATCH /tenants/{tenant_id}/locations/{location_id}`

**Authentication:** Required (ADMIN or MANAGER role)

**Path Parameters:**
- `tenant_id` (UUID) - Tenant ID
- `location_id` (UUID) - Location ID

**Request Body:**
```json
{
  "name": "Updated Location Name",
  "address": "New Address",
  "timezone": "America/Los_Angeles"
}
```

**Response:** `200 OK`
```json
{
  "id": "xyz789-abc123-def456",
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "name": "Updated Location Name",
  "address": "New Address",
  "timezone": "America/Los_Angeles",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## Delete Location

Delete a location (ADMIN only).

**Endpoint:** `DELETE /tenants/{tenant_id}/locations/{location_id}`

**Authentication:** Required (ADMIN role)

**Path Parameters:**
- `tenant_id` (UUID) - Tenant ID
- `location_id` (UUID) - Location ID

**Response:** `204 No Content`

---

## Tenant Status Values

- `trial` - Trial period
- `active` - Active subscription
- `suspended` - Suspended account

## Plan Values

- `trial` - Trial plan
- `basic` - Basic plan
- `premium` - Premium plan




