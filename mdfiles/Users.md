# Users API

## List Users

List all users for the current tenant.

**Endpoint:** `GET /users/`

**Authentication:** Required (ADMIN or MANAGER role)

**Query Parameters:**
- `page` (integer, default: 1) - Page number
- `page_size` (integer, default: 20, max: 100) - Items per page

**Response:** `200 OK`
```json
{
  "items": [
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
  ],
  "page": 1,
  "page_size": 20,
  "total": 1,
  "total_pages": 1
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/api/v1/users/?page=1&page_size=20" \
  -H "Authorization: Bearer <token>"
```

---

## Create User

Create a new user for the tenant.

**Endpoint:** `POST /users/`

**Authentication:** Required (ADMIN or MANAGER role)

**Request Body:**
```json
{
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "full_name": "John Stylist",
  "email": "john@salonone.com",
  "password": "password123",
  "role": "EMPLOYEE",
  "is_active": true,
  "default_location_id": "abc123-def456-ghi789"
}
```

**Required Fields:**
- `tenant_id` (UUID) - Tenant ID (must match current user's tenant)
- `full_name` (string) - User's full name
- `email` (string, email) - User's email address
- `password` (string) - User's password

**Optional Fields:**
- `role` (string) - User role: "ADMIN", "MANAGER", "EMPLOYEE" (default: "EMPLOYEE")
- `is_active` (boolean) - Whether user is active (default: true)
- `default_location_id` (UUID) - Default location ID

**Response:** `201 Created`
```json
{
  "id": "new-user-uuid-here",
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "full_name": "John Stylist",
  "email": "john@salonone.com",
  "role": "EMPLOYEE",
  "is_active": true,
  "default_location_id": "abc123-def456-ghi789",
  "last_login_at": null,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `403 Forbidden` - Cannot create user for different tenant
- `409 Conflict` - Email already registered for this tenant

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
    "full_name": "John Stylist",
    "email": "john@salonone.com",
    "password": "password123",
    "role": "EMPLOYEE"
  }'
```

---

## Get User

Get user details by ID.

**Endpoint:** `GET /users/{user_id}`

**Authentication:** Required

**Path Parameters:**
- `user_id` (UUID) - User ID

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
- `404 Not Found` - User not found or belongs to different tenant

---

## Update User

Update user information.

**Endpoint:** `PATCH /users/{user_id}`

**Authentication:** Required (ADMIN or MANAGER role)

**Path Parameters:**
- `user_id` (UUID) - User ID

**Request Body:**
```json
{
  "full_name": "Updated Name",
  "email": "newemail@salonone.com",
  "role": "MANAGER",
  "is_active": true,
  "default_location_id": "xyz789...",
  "password": "newpassword123"
}
```

**All fields are optional.** Only include fields you want to update.

**Response:** `200 OK`
```json
{
  "id": "958aaa38-af27-4c73-b8ae-42b3ca8e2a9b",
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "full_name": "Updated Name",
  "email": "newemail@salonone.com",
  "role": "MANAGER",
  "is_active": true,
  "default_location_id": "xyz789...",
  "last_login_at": "2024-01-15T10:30:00Z",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Example:**
```bash
curl -X PATCH "http://localhost:8000/api/v1/users/958aaa38-af27-4c73-b8ae-42b3ca8e2a9b" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "MANAGER"
  }'
```

---

## Delete User

Delete a user (ADMIN only).

**Endpoint:** `DELETE /users/{user_id}`

**Authentication:** Required (ADMIN role)

**Path Parameters:**
- `user_id` (UUID) - User ID

**Response:** `204 No Content`

**Error Responses:**
- `404 Not Found` - User not found or belongs to different tenant

---

## User Roles

- **ADMIN** - Full access to all features
  - Can manage tenants, users, locations
  - Can manage inventory
  - Can delete formulas
  - Can access all endpoints

- **MANAGER** - Management access
  - Can manage users (create, update)
  - Can manage locations
  - Can manage inventory
  - Can delete formulas
  - Cannot delete users or tenants

- **EMPLOYEE** - Basic access
  - Can create and view formulas
  - Can view customers
  - Can view inventory
  - Cannot manage users or inventory

## Notes

- Users can only access data from their own tenant
- Email addresses must be unique within a tenant
- Password updates require providing the new password in the update request
- Deactivated users (`is_active: false`) cannot login




