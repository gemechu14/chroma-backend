# Formulas API

Formulas represent color mixing recipes used on customers. Creating a formula automatically deducts inventory.

## List Formulas

List formulas for the tenant, optionally filtered by customer.

**Endpoint:** `GET /formulas/`

**Authentication:** Required

**Query Parameters:**
- `customer_id` (UUID, optional) - Filter by customer ID
- `page` (integer, default: 1) - Page number
- `page_size` (integer, default: 20, max: 100) - Items per page

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "formula-uuid-here",
      "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
      "location_id": "abc123-def456-ghi789",
      "customer_id": "customer-uuid-here",
      "created_by_user_id": "user-uuid-here",
      "formula_name": "Sarah's Winter Color",
      "service_type": "Full Color",
      "notes": "Customer prefers cooler tones",
      "created_at": "2024-01-15T10:30:00Z",
      "formula_items": [
        {
          "id": "item-uuid-here",
          "formula_id": "formula-uuid-here",
          "tenant_product_id": "tenant-product-uuid-here",
          "amount_used": 30.0,
          "cost_at_time": 0.35,
          "created_at": "2024-01-15T10:30:00Z"
        },
        {
          "id": "item-uuid-here-2",
          "formula_id": "formula-uuid-here",
          "tenant_product_id": "tenant-product-uuid-here-2",
          "amount_used": 15.0,
          "cost_at_time": 0.35,
          "created_at": "2024-01-15T10:30:00Z"
        }
      ]
    }
  ],
  "page": 1,
  "page_size": 20,
  "total": 1,
  "total_pages": 1
}
```

**Example - All formulas:**
```bash
curl -X GET "http://localhost:8000/api/v1/formulas/?page=1&page_size=20" \
  -H "Authorization: Bearer <token>"
```

**Example - Customer formulas:**
```bash
curl -X GET "http://localhost:8000/api/v1/formulas/?customer_id=customer-uuid-here&page=1&page_size=20" \
  -H "Authorization: Bearer <token>"
```

---

## Create Formula

Create a new formula. This automatically:
1. Creates the formula and formula items
2. Deducts inventory for each product used
3. Creates CONSUME inventory transactions

**Endpoint:** `POST /formulas/`

**Authentication:** Required

**Request Body:**
```json
{
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "location_id": "abc123-def456-ghi789",
  "customer_id": "customer-uuid-here",
  "created_by_user_id": "user-uuid-here",
  "formula_name": "Sarah's Winter Color",
  "service_type": "Full Color",
  "notes": "Customer prefers cooler tones",
  "items": [
    {
      "tenant_product_id": "tenant-product-uuid-here",
      "amount_used": 30.0,
      "cost_at_time": 0.35
    },
    {
      "tenant_product_id": "tenant-product-uuid-here-2",
      "amount_used": 15.0,
      "cost_at_time": 0.35
    },
    {
      "tenant_product_id": "developer-product-uuid",
      "amount_used": 45.0,
      "cost_at_time": 0.02
    }
  ]
}
```

**Required Fields:**
- `tenant_id` (UUID) - Tenant ID (automatically set from current user)
- `location_id` (UUID) - Location where formula is used
- `customer_id` (UUID) - Customer ID
- `created_by_user_id` (UUID) - User ID (automatically set from current user)
- `items` (array) - Array of formula items

**Formula Item Required Fields:**
- `tenant_product_id` (UUID) - Tenant Product ID
- `amount_used` (decimal) - Amount used in grams or milliliters

**Optional Fields:**
- `formula_name` (string) - Name for the formula
- `service_type` (string) - Type of service (e.g., "Full Color", "Highlights", "Toner")
- `notes` (string) - Additional notes
- `cost_at_time` (decimal) - Cost per unit at time of use (for each item)

**Response:** `201 Created`
```json
{
  "id": "formula-uuid-here",
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "location_id": "abc123-def456-ghi789",
  "customer_id": "customer-uuid-here",
  "created_by_user_id": "user-uuid-here",
  "formula_name": "Sarah's Winter Color",
  "service_type": "Full Color",
  "notes": "Customer prefers cooler tones",
  "created_at": "2024-01-15T10:30:00Z",
  "formula_items": [
    {
      "id": "item-uuid-here",
      "formula_id": "formula-uuid-here",
      "tenant_product_id": "tenant-product-uuid-here",
      "amount_used": 30.0,
      "cost_at_time": 0.35,
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "item-uuid-here-2",
      "formula_id": "formula-uuid-here",
      "tenant_product_id": "tenant-product-uuid-here-2",
      "amount_used": 15.0,
      "cost_at_time": 0.35,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/formulas/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "location_id": "abc123-def456-ghi789",
    "customer_id": "customer-uuid-here",
    "formula_name": "Sarah'\''s Winter Color",
    "service_type": "Full Color",
    "items": [
      {
        "tenant_product_id": "tenant-product-uuid-here",
        "amount_used": 30.0,
        "cost_at_time": 0.35
      },
      {
        "tenant_product_id": "tenant-product-uuid-here-2",
        "amount_used": 15.0,
        "cost_at_time": 0.35
      }
    ]
  }'
```

**Note:** The `tenant_id` and `created_by_user_id` are automatically set from the authenticated user.

**Error Responses:**

**400 Bad Request - Insufficient Inventory:**
```json
{
  "detail": {
    "error": "Insufficient inventory",
    "message": "One or more products do not have sufficient inventory",
    "insufficient_items": [
      {
        "tenant_product_id": "tenant-product-uuid-here",
        "product_name": "Shades EQ 09N — Platinum",
        "tracking_unit": "G",
        "amount_needed": 50.0,
        "available": 30.0,
        "reason": "Insufficient inventory. Need 50.0 G, have 30.0 G"
      },
      {
        "tenant_product_id": "tenant-product-uuid-here-2",
        "product_name": "Developer 10 Vol",
        "tracking_unit": "ML",
        "amount_needed": 100.0,
        "available": 0.0,
        "reason": "Inventory item not found for this location"
      }
    ]
  }
}
```

The system validates inventory sufficiency **before** creating the formula. If any product has insufficient inventory, the entire formula creation is rejected and no inventory is deducted.

**Example Error Response:**
```bash
# Request with insufficient inventory
curl -X POST "http://localhost:8000/api/v1/formulas/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "location_id": "abc123-def456-ghi789",
    "customer_id": "customer-uuid-here",
    "items": [
      {
        "tenant_product_id": "tenant-product-uuid-here",
        "amount_used": 50.0
      }
    ]
  }'

# Response: 400 Bad Request
{
  "detail": {
    "error": "Insufficient inventory",
    "message": "One or more products do not have sufficient inventory",
    "insufficient_items": [...]
  }
}
```

---

## Get Formula

Get formula details including all formula items.

**Endpoint:** `GET /formulas/{formula_id}`

**Authentication:** Required

**Path Parameters:**
- `formula_id` (UUID) - Formula ID

**Response:** `200 OK`
```json
{
  "id": "formula-uuid-here",
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "location_id": "abc123-def456-ghi789",
  "customer_id": "customer-uuid-here",
  "created_by_user_id": "user-uuid-here",
  "formula_name": "Sarah's Winter Color",
  "service_type": "Full Color",
  "notes": "Customer prefers cooler tones",
  "created_at": "2024-01-15T10:30:00Z",
  "formula_items": [
    {
      "id": "item-uuid-here",
      "formula_id": "formula-uuid-here",
      "tenant_product_id": "tenant-product-uuid-here",
      "amount_used": 30.0,
      "cost_at_time": 0.35,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**Error Responses:**
- `404 Not Found` - Formula not found or belongs to different tenant

---

## Update Formula

Update formula information (items cannot be updated).

**Endpoint:** `PATCH /formulas/{formula_id}`

**Authentication:** Required

**Path Parameters:**
- `formula_id` (UUID) - Formula ID

**Request Body:**
```json
{
  "formula_name": "Updated Formula Name",
  "service_type": "Highlights",
  "notes": "Updated notes"
}
```

**All fields are optional.** Note: Formula items cannot be updated after creation.

**Response:** `200 OK`
```json
{
  "id": "formula-uuid-here",
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "location_id": "abc123-def456-ghi789",
  "customer_id": "customer-uuid-here",
  "created_by_user_id": "user-uuid-here",
  "formula_name": "Updated Formula Name",
  "service_type": "Highlights",
  "notes": "Updated notes",
  "created_at": "2024-01-15T10:30:00Z",
  "formula_items": [...]
}
```

---

## Delete Formula

Delete a formula (ADMIN/MANAGER only).

**Endpoint:** `DELETE /formulas/{formula_id}`

**Authentication:** Required (ADMIN or MANAGER role)

**Path Parameters:**
- `formula_id` (UUID) - Formula ID

**Response:** `204 No Content`

**Error Responses:**
- `404 Not Found` - Formula not found or belongs to different tenant

**Note:** Deleting a formula does NOT restore inventory. Inventory transactions remain in the audit log.

---

## Formula Workflow

1. **Stylist creates formula** with products and amounts used
2. **System automatically:**
   - Saves the formula and formula items
   - Deducts inventory from the location's inventory items
   - Creates CONSUME inventory transactions
   - Records cost at time of use
3. **Formula is saved** for customer history
4. **Future visits** can reference past formulas

## Example Formula Structure

A typical formula might look like:

```json
{
  "formula_name": "Sarah's Winter Color",
  "service_type": "Full Color",
  "items": [
    {
      "tenant_product_id": "product-7n-uuid",
      "amount_used": 30.0,
      "cost_at_time": 0.35
    },
    {
      "tenant_product_id": "product-7a-uuid",
      "amount_used": 15.0,
      "cost_at_time": 0.35
    },
    {
      "tenant_product_id": "developer-uuid",
      "amount_used": 45.0,
      "cost_at_time": 0.02
    }
  ]
}
```

This represents:
- 30g of 7N color
- 15g of 7A color
- 45ml of developer

## Notes

- **Inventory Validation:** The system validates inventory sufficiency **before** creating the formula. If any product has insufficient inventory, the entire formula creation is rejected with a 400 Bad Request error and no inventory is deducted.
- Formulas automatically deduct inventory when created (only if validation passes)
- Amounts are tracked in grams (G) or milliliters (ML) based on the tenant product's tracking unit
- Cost at time is recorded for accurate cost calculation
- Formulas are linked to customers for history tracking
- Formula items cannot be modified after creation (delete and recreate if needed)
- Inventory must exist at the location for products used in formulas
- The validation checks all items before processing any, ensuring atomicity (all or nothing)

