# Customers API

## List Customers

List all customers for the current tenant with optional search.

**Endpoint:** `GET /customers/`

**Authentication:** Required

**Query Parameters:**
- `page` (integer, default: 1) - Page number
- `page_size` (integer, default: 20, max: 100) - Items per page
- `search` (string, optional) - Search by name or phone

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "customer-uuid-here",
      "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
      "full_name": "Sarah Johnson",
      "phone": "+1-555-0101",
      "email": "sarah@example.com",
      "notes": "Prefers natural colors",
      "home_location_id": "abc123-def456-ghi789",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "page": 1,
  "page_size": 20,
  "total": 1,
  "total_pages": 1
}
```

**Example with search:**
```bash
curl -X GET "http://localhost:8000/api/v1/customers/?search=Sarah&page=1&page_size=20" \
  -H "Authorization: Bearer <token>"
```

**Example without search:**
```bash
curl -X GET "http://localhost:8000/api/v1/customers/?page=1&page_size=20" \
  -H "Authorization: Bearer <token>"
```

---

## Create Customer

Create a new customer.

**Endpoint:** `POST /customers/`

**Authentication:** Required

**Request Body:**
```json
{
  "full_name": "Sarah Johnson",
  "phone": "+1-555-0101",
  "email": "sarah@example.com",
  "notes": "Prefers natural colors",
  "home_location_id": "abc123-def456-ghi789"
}
```

**Required Fields:**
- `full_name` (string) - Customer's full name

**Optional Fields:**
- `phone` (string) - Phone number
- `email` (string, email) - Email address
- `notes` (string) - Notes about the customer
- `home_location_id` (UUID) - Default location ID

**Response:** `201 Created`
```json
{
  "id": "customer-uuid-here",
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "full_name": "Sarah Johnson",
  "phone": "+1-555-0101",
  "email": "sarah@example.com",
  "notes": "Prefers natural colors",
  "home_location_id": "abc123-def456-ghi789",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/customers/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Sarah Johnson",
    "phone": "+1-555-0101",
    "email": "sarah@example.com",
    "home_location_id": "abc123-def456-ghi789"
  }'
```

---

## Get Customer

Get customer details by ID.

**Endpoint:** `GET /customers/{customer_id}`

**Authentication:** Required

**Path Parameters:**
- `customer_id` (UUID) - Customer ID

**Response:** `200 OK`
```json
{
  "id": "customer-uuid-here",
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "full_name": "Sarah Johnson",
  "phone": "+1-555-0101",
  "email": "sarah@example.com",
  "notes": "Prefers natural colors",
  "home_location_id": "abc123-def456-ghi789",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `404 Not Found` - Customer not found or belongs to different tenant

---

## Update Customer

Update customer information.

**Endpoint:** `PATCH /customers/{customer_id}`

**Authentication:** Required

**Path Parameters:**
- `customer_id` (UUID) - Customer ID

**Request Body:**
```json
{
  "full_name": "Sarah Johnson-Smith",
  "phone": "+1-555-0102",
  "email": "sarah.new@example.com",
  "notes": "Updated notes",
  "home_location_id": "xyz789-abc123-def456"
}
```

**All fields are optional.** Only include fields you want to update.

**Response:** `200 OK`
```json
{
  "id": "customer-uuid-here",
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "full_name": "Sarah Johnson-Smith",
  "phone": "+1-555-0102",
  "email": "sarah.new@example.com",
  "notes": "Updated notes",
  "home_location_id": "xyz789-abc123-def456",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Example:**
```bash
curl -X PATCH "http://localhost:8000/api/v1/customers/customer-uuid-here" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+1-555-0102"
  }'
```

---

## Delete Customer

Delete a customer.

**Endpoint:** `DELETE /customers/{customer_id}`

**Authentication:** Required

**Path Parameters:**
- `customer_id` (UUID) - Customer ID

**Response:** `204 No Content`

**Error Responses:**
- `404 Not Found` - Customer not found or belongs to different tenant

**Note:** Deleting a customer will also delete all associated formulas.

---

## Search Functionality

The search parameter searches across:
- Customer full name (case-insensitive partial match)
- Phone number (case-insensitive partial match)

**Example:**
```bash
# Search for customers with "Sarah" in name or phone
GET /customers/?search=Sarah

# Search for phone number
GET /customers/?search=555-0101
```

## Notes

- Customers are automatically associated with the authenticated user's tenant
- Customers can have a home location, but formulas can be created at any location
- Customer history (formulas) is preserved even if customer is deleted (formulas remain but customer_id becomes orphaned)

