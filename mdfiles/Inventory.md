# Inventory API

## List Inventory Items

List inventory items for a specific location.

**Endpoint:** `GET /inventory/items`

**Authentication:** Required

**Query Parameters:**
- `location_id` (UUID, required) - Location ID

**Response:** `200 OK`
```json
[
  {
    "id": "inventory-item-uuid-here",
    "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
    "location_id": "abc123-def456-ghi789",
    "tenant_product_id": "tenant-product-uuid-here",
    "on_hand_qty": 360.0,
    "reorder_level_qty": 60.0,
    "updated_at": "2024-01-15T10:30:00Z",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

**Example:**
```bash
curl -X GET "http://localhost:8000/api/v1/inventory/items?location_id=abc123-def456-ghi789" \
  -H "Authorization: Bearer <token>"
```

---

## Low Stock Alerts

Get inventory items that are at or below reorder level.

**Endpoint:** `GET /inventory/items/low-stock`

**Authentication:** Required

**Response:** `200 OK`
```json
[
  {
    "id": "inventory-item-uuid-here",
    "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
    "location_id": "abc123-def456-ghi789",
    "tenant_product_id": "tenant-product-uuid-here",
    "on_hand_qty": 45.0,
    "reorder_level_qty": 60.0,
    "updated_at": "2024-01-15T10:30:00Z",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

---

## Create Inventory Item

Create a new inventory item for a location and product.

**Endpoint:** `POST /inventory/items`

**Authentication:** Required (ADMIN or MANAGER role)

**Request Body:**
```json
{
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "location_id": "abc123-def456-ghi789",
  "tenant_product_id": "tenant-product-uuid-here",
  "on_hand_qty": 360.0,
  "reorder_level_qty": 60.0
}
```

**Required Fields:**
- `tenant_id` (UUID) - Tenant ID (must match current user's tenant)
- `location_id` (UUID) - Location ID
- `tenant_product_id` (UUID) - Tenant Product ID

**Optional Fields:**
- `on_hand_qty` (decimal) - Current quantity on hand (default: 0.0)
- `reorder_level_qty` (decimal) - Reorder level threshold

**Response:** `201 Created`
```json
{
  "id": "inventory-item-uuid-here",
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "location_id": "abc123-def456-ghi789",
  "tenant_product_id": "tenant-product-uuid-here",
  "on_hand_qty": 360.0,
  "reorder_level_qty": 60.0,
  "updated_at": "2024-01-15T10:30:00Z",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `409 Conflict` - Inventory item already exists for this location and product

---

## Get Inventory Item

Get inventory item details.

**Endpoint:** `GET /inventory/items/{item_id}`

**Authentication:** Required

**Path Parameters:**
- `item_id` (UUID) - Inventory Item ID

**Response:** `200 OK`
```json
{
  "id": "inventory-item-uuid-here",
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "location_id": "abc123-def456-ghi789",
  "tenant_product_id": "tenant-product-uuid-here",
  "on_hand_qty": 360.0,
  "reorder_level_qty": 60.0,
  "updated_at": "2024-01-15T10:30:00Z",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## Update Inventory Item

Update inventory item quantities.

**Endpoint:** `PATCH /inventory/items/{item_id}`

**Authentication:** Required (ADMIN or MANAGER role)

**Path Parameters:**
- `item_id` (UUID) - Inventory Item ID

**Request Body:**
```json
{
  "on_hand_qty": 400.0,
  "reorder_level_qty": 80.0
}
```

**All fields are optional.**

**Response:** `200 OK`
```json
{
  "id": "inventory-item-uuid-here",
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "location_id": "abc123-def456-ghi789",
  "tenant_product_id": "tenant-product-uuid-here",
  "on_hand_qty": 400.0,
  "reorder_level_qty": 80.0,
  "updated_at": "2024-01-15T11:00:00Z",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## List Transactions

List all inventory transactions for the tenant.

**Endpoint:** `GET /inventory/transactions`

**Authentication:** Required

**Query Parameters:**
- `page` (integer, default: 1) - Page number
- `page_size` (integer, default: 20, max: 100) - Items per page

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "txn-uuid-here",
      "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
      "inventory_item_id": "inventory-item-uuid-here",
      "user_id": "user-uuid-here",
      "formula_id": "formula-uuid-here",
      "txn_type": "CONSUME",
      "qty_delta": -30.0,
      "unit_cost_at_time": 0.35,
      "note": "Used in formula",
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

## List Item Transactions

List transactions for a specific inventory item.

**Endpoint:** `GET /inventory/transactions/{item_id}`

**Authentication:** Required

**Path Parameters:**
- `item_id` (UUID) - Inventory Item ID

**Query Parameters:**
- `page` (integer, default: 1) - Page number
- `page_size` (integer, default: 20, max: 100) - Items per page

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "txn-uuid-here",
      "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
      "inventory_item_id": "inventory-item-uuid-here",
      "user_id": "user-uuid-here",
      "formula_id": "formula-uuid-here",
      "txn_type": "CONSUME",
      "qty_delta": -30.0,
      "unit_cost_at_time": 0.35,
      "note": "Used in formula",
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

## Create Transaction

Create a manual inventory transaction (ADMIN/MANAGER only).

**Endpoint:** `POST /inventory/transactions`

**Authentication:** Required (ADMIN or MANAGER role)

**Request Body:**
```json
{
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "inventory_item_id": "inventory-item-uuid-here",
  "user_id": "user-uuid-here",
  "txn_type": "PURCHASE",
  "qty_delta": 100.0,
  "unit_cost_at_time": 0.35,
  "note": "Restocked inventory",
  "formula_id": null
}
```

**Required Fields:**
- `tenant_id` (UUID) - Tenant ID (must match current user's tenant)
- `inventory_item_id` (UUID) - Inventory Item ID
- `user_id` (UUID) - User ID (automatically set to current user)
- `txn_type` (string) - Transaction type
- `qty_delta` (decimal) - Quantity change (positive = stock in, negative = stock out)

**Optional Fields:**
- `unit_cost_at_time` (decimal) - Cost per unit at time of transaction
- `note` (string) - Transaction note
- `formula_id` (UUID) - Associated formula ID (if applicable)

**Transaction Types:**
- `PURCHASE` - Stock received/purchased (positive qty_delta)
- `CONSUME` - Stock consumed/used (negative qty_delta)
- `ADJUST` - Manual adjustment (can be positive or negative)
- `WASTE` - Stock wasted/spoiled (negative qty_delta)
- `RETURN` - Stock returned (positive qty_delta)

**Response:** `201 Created`
```json
{
  "id": "txn-uuid-here",
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "inventory_item_id": "inventory-item-uuid-here",
  "user_id": "user-uuid-here",
  "formula_id": null,
  "txn_type": "PURCHASE",
  "qty_delta": 100.0,
  "unit_cost_at_time": 0.35,
  "note": "Restocked inventory",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Note:** Creating a transaction automatically updates the inventory item's `on_hand_qty`.

---

## Notes

- Inventory quantities are tracked in grams (G) or milliliters (ML) based on the tenant product's `tracking_unit`
- Each location can have separate inventory for the same product
- Transactions create an audit trail of all inventory movements
- Formulas automatically create CONSUME transactions when created
- Low stock alerts are based on `on_hand_qty <= reorder_level_qty`
- `qty_delta` is positive for stock increases, negative for decreases




