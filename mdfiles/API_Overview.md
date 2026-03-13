# Chroma SaaS API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All protected endpoints require Bearer token authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Getting an Access Token

1. **Register a new tenant** (if you don't have an account):
   - `POST /tenants/register` - See [Tenants API](./Tenants.md)

2. **Login** to get access and refresh tokens:
   - `POST /users/login` - See [Authentication API](./Authentication.md)

3. **Use the access token** in subsequent requests

## Pagination

All list endpoints use page-based pagination:

**Query Parameters:**
- `page` (integer, default: 1, min: 1) - Page number
- `page_size` (integer, default: 20, min: 1, max: 100) - Items per page

**Response Format:**
```json
{
  "items": [...],
  "page": 1,
  "page_size": 20,
  "total": 100,
  "total_pages": 5
}
```

## Error Responses

### Standard Error Format

```json
{
  "detail": "Error message description"
}
```

### Common HTTP Status Codes

- `200 OK` - Success
- `201 Created` - Resource created successfully
- `204 No Content` - Success (no response body)
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid authentication token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource already exists or conflict
- `422 Unprocessable Entity` - Validation error

## Multi-Tenant Architecture

This API follows a multi-tenant architecture where:
- Each tenant (salon business) has isolated data
- Users can only access data from their tenant
- All endpoints automatically filter by tenant_id based on the authenticated user

## API Endpoints Overview

### Public Endpoints (No Authentication)
- `POST /tenants/register` - Register a new tenant

### Authentication Endpoints
- `POST /users/login` - Login with email/password
- `POST /users/refresh` - Refresh access token
- `GET /users/me` - Get current user info

### Tenant Management
- `GET /tenants/` - List tenants (ADMIN only)
- `GET /tenants/{tenant_id}` - Get tenant details
- `POST /tenants/` - Create tenant (ADMIN only)
- `PATCH /tenants/{tenant_id}` - Update tenant (ADMIN only)
- `DELETE /tenants/{tenant_id}` - Delete tenant (ADMIN only)
- `GET /tenants/{tenant_id}/locations` - List locations
- `POST /tenants/{tenant_id}/locations` - Create location
- `PATCH /tenants/{tenant_id}/locations/{location_id}` - Update location
- `DELETE /tenants/{tenant_id}/locations/{location_id}` - Delete location

### User Management
- `GET /users/` - List users (ADMIN/MANAGER)
- `POST /users/` - Create user (ADMIN/MANAGER)
- `GET /users/{user_id}` - Get user details
- `PATCH /users/{user_id}` - Update user (ADMIN/MANAGER)
- `DELETE /users/{user_id}` - Delete user (ADMIN)

### Customer Management
- `GET /customers/` - List customers (with search)
- `POST /customers/` - Create customer
- `GET /customers/{customer_id}` - Get customer details
- `PATCH /customers/{customer_id}` - Update customer
- `DELETE /customers/{customer_id}` - Delete customer

### Product Catalog
- `GET /products/brands` - List brands
- `POST /products/brands` - Create brand (ADMIN)
- `PATCH /products/brands/{brand_id}` - Update brand (ADMIN)
- `GET /products/lines` - List product lines
- `POST /products/lines` - Create product line (ADMIN)
- `PATCH /products/lines/{line_id}` - Update product line (ADMIN)
- `GET /products/` - List products
- `POST /products/` - Create product (ADMIN)
- `PATCH /products/{product_id}` - Update product (ADMIN)
- `GET /products/tenant-catalog` - List tenant products
- `POST /products/tenant-catalog` - Add product to tenant catalog
- `PATCH /products/tenant-catalog/{tp_id}` - Update tenant product
- `DELETE /products/tenant-catalog/{tp_id}` - Remove tenant product

### Inventory Management
- `GET /inventory/items` - List inventory items by location
- `GET /inventory/items/low-stock` - Get low stock alerts
- `POST /inventory/items` - Create inventory item (ADMIN/MANAGER)
- `GET /inventory/items/{item_id}` - Get inventory item
- `PATCH /inventory/items/{item_id}` - Update inventory item (ADMIN/MANAGER)
- `GET /inventory/transactions` - List transactions
- `GET /inventory/transactions/{item_id}` - List item transactions
- `POST /inventory/transactions` - Create transaction (ADMIN/MANAGER)

### Formula Management
- `GET /formulas/` - List formulas
- `POST /formulas/` - Create formula (auto-deducts inventory)
- `GET /formulas/{formula_id}` - Get formula details
- `PATCH /formulas/{formula_id}` - Update formula
- `DELETE /formulas/{formula_id}` - Delete formula (ADMIN/MANAGER)

## User Roles

- **ADMIN** - Full access to all features
- **MANAGER** - Can manage inventory, users, and locations
- **EMPLOYEE** - Can create formulas and view data

## Data Types

### UUID
All IDs are UUID strings (e.g., `"958aaa38-af27-4c73-b8ae-42b3ca8e2a9b"`)

### DateTime
All timestamps are ISO 8601 format (e.g., `"2024-01-15T10:30:00Z"`)

### Decimal
Quantities and costs are decimal numbers (e.g., `123.45`)

## Rate Limiting

Currently no rate limiting is implemented. Consider implementing rate limiting in production.

## Swagger UI

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/swagger
- **ReDoc**: http://localhost:8000/redoc

## Support

For API support, refer to the individual API documentation files:
- [Authentication API](./Authentication.md)
- [Tenants API](./Tenants.md)
- [Users API](./Users.md)
- [Customers API](./Customers.md)
- [Products API](./Products.md)
- [Inventory API](./Inventory.md)
- [Formulas API](./Formulas.md)




