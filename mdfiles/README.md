# Chroma SaaS API Documentation

Complete API documentation for frontend integration.

## Documentation Files

- **[API Overview](./API_Overview.md)** - Base URL, authentication, pagination, error handling, and endpoint overview
- **[Authentication API](./Authentication.md)** - Login, refresh token, and current user endpoints
- **[Tenants API](./Tenants.md)** - Tenant registration, management, and locations
- **[Users API](./Users.md)** - User management and roles
- **[Customers API](./Customers.md)** - Customer management with search
- **[Products API](./Products.md)** - Global product catalog and tenant product catalog
- **[Inventory API](./Inventory.md)** - Inventory items, transactions, and low stock alerts
- **[Formulas API](./Formulas.md)** - Formula creation and management (auto-deducts inventory)

## Quick Start

1. **Base URL:** `http://localhost:8000/api/v1`
2. **Register Tenant:** `POST /tenants/register` (public endpoint)
3. **Login:** `POST /users/login` with email and password
4. **Use Access Token:** Include `Authorization: Bearer <token>` header in all requests

## Authentication Flow

```
1. Register Tenant → Get tenant, location, admin user info
2. Login → Get access_token and refresh_token
3. Use access_token → Include in Authorization header
4. Refresh Token → Use refresh_token to get new access_token when expired
```

## Common Patterns

### Pagination
All list endpoints support pagination:
```
GET /endpoint/?page=1&page_size=20
```

### Multi-Tenant
- All data is automatically filtered by tenant
- Users can only access their tenant's data
- Tenant ID is determined from authenticated user

### Inventory Tracking
- Quantities tracked in grams (G) or milliliters (ML)
- Creating formulas automatically deducts inventory
- All transactions are audited

## Testing

Use Swagger UI for interactive testing:
- **Swagger UI:** http://localhost:8000/swagger
- **ReDoc:** http://localhost:8000/redoc

In Swagger UI:
1. Click "Authorize" button
2. Paste your access token
3. Click "Authorize"
4. Test endpoints directly in the browser

## Support

For detailed endpoint documentation, see the individual API files listed above.




