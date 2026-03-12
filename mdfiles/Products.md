# Products API

The Products API manages the global product catalog (brands, product lines, products) and tenant-specific product catalogs.

## Global Product Catalog

### List Brands

List all brands in the global catalog.

**Endpoint:** `GET /products/brands`

**Authentication:** Required

**Query Parameters:**
- `page` (integer, default: 1) - Page number
- `page_size` (integer, default: 20, max: 100) - Items per page

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "brand-uuid-here",
      "name": "Redken",
      "website_url": "https://www.redken.com",
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

### Create Brand

Create a new brand (ADMIN only).

**Endpoint:** `POST /products/brands`

**Authentication:** Required (ADMIN role)

**Request Body:**
```json
{
  "name": "Wella",
  "website_url": "https://www.wella.com"
}
```

**Response:** `201 Created`
```json
{
  "id": "brand-uuid-here",
  "name": "Wella",
  "website_url": "https://www.wella.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### Update Brand

Update brand information (ADMIN only).

**Endpoint:** `PATCH /products/brands/{brand_id}`

**Authentication:** Required (ADMIN role)

**Request Body:**
```json
{
  "name": "Updated Brand Name",
  "website_url": "https://new-url.com"
}
```

---

### List Product Lines

List product lines for a brand.

**Endpoint:** `GET /products/lines`

**Authentication:** Required

**Query Parameters:**
- `brand_id` (UUID, required) - Brand ID
- `page` (integer, default: 1) - Page number
- `page_size` (integer, default: 20, max: 100) - Items per page

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "line-uuid-here",
      "brand_id": "brand-uuid-here",
      "name": "Shades EQ",
      "category": "COLOR",
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

### Create Product Line

Create a new product line (ADMIN only).

**Endpoint:** `POST /products/lines`

**Authentication:** Required (ADMIN role)

**Request Body:**
```json
{
  "brand_id": "brand-uuid-here",
  "name": "Shades EQ",
  "category": "COLOR"
}
```

**Category Values:**
- `COLOR` - Color products
- `DEVELOPER` - Developer products
- `TONER` - Toner products
- `TREATMENT` - Treatment products

---

### List Products

List products in the global catalog.

**Endpoint:** `GET /products/`

**Authentication:** Required

**Query Parameters:**
- `product_line_id` (UUID, optional) - Filter by product line
- `page` (integer, default: 1) - Page number
- `page_size` (integer, default: 20, max: 100) - Items per page

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "product-uuid-here",
      "product_line_id": "line-uuid-here",
      "sku": "SKU123",
      "code": "09N",
      "name": "Shades EQ 09N — Platinum",
      "tone_family": "N",
      "pack_size_value": 60.0,
      "pack_size_unit": "G",
      "is_active": true,
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

### Create Product

Create a new product (ADMIN only).

**Endpoint:** `POST /products/`

**Authentication:** Required (ADMIN role)

**Request Body:**
```json
{
  "product_line_id": "line-uuid-here",
  "sku": "SKU123",
  "code": "09N",
  "name": "Shades EQ 09N — Platinum",
  "tone_family": "N",
  "pack_size_value": 60.0,
  "pack_size_unit": "G",
  "is_active": true
}
```

**Pack Size Unit Values:**
- `G` - Grams
- `ML` - Milliliters

---

## Tenant Product Catalog

### List Tenant Products

List products in the tenant's catalog.

**Endpoint:** `GET /products/tenant-catalog`

**Authentication:** Required

**Query Parameters:**
- `enabled_only` (boolean, default: false) - Only return enabled products
- `page` (integer, default: 1) - Page number
- `page_size` (integer, default: 20, max: 100) - Items per page

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "tenant-product-uuid-here",
      "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
      "product_id": "product-uuid-here",
      "custom_name": "My Custom Name",
      "is_enabled": true,
      "tracking_unit": "G",
      "default_unit_cost": 0.35,
      "currency": "USD",
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

### Add Product to Tenant Catalog

Add a product to the tenant's catalog.

**Endpoint:** `POST /products/tenant-catalog`

**Authentication:** Required (ADMIN or MANAGER role)

**Request Body:**
```json
{
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "product_id": "product-uuid-here",
  "custom_name": "My Custom Name",
  "is_enabled": true,
  "tracking_unit": "G",
  "default_unit_cost": 0.35,
  "currency": "USD"
}
```

**Required Fields:**
- `tenant_id` (UUID) - Tenant ID (must match current user's tenant)
- `product_id` (UUID) - Product ID from global catalog

**Optional Fields:**
- `custom_name` (string) - Custom name for the product
- `is_enabled` (boolean) - Whether product is enabled (default: true)
- `tracking_unit` (string) - Unit for tracking: "G" or "ML" (default: "G")
- `default_unit_cost` (decimal) - Default cost per unit
- `currency` (string) - Currency code (e.g., "USD")

**Response:** `201 Created`
```json
{
  "id": "tenant-product-uuid-here",
  "tenant_id": "79dcbe8c-b004-4705-a5ad-767223660e75",
  "product_id": "product-uuid-here",
  "custom_name": "My Custom Name",
  "is_enabled": true,
  "tracking_unit": "G",
  "default_unit_cost": 0.35,
  "currency": "USD",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### Update Tenant Product

Update tenant product configuration.

**Endpoint:** `PATCH /products/tenant-catalog/{tp_id}`

**Authentication:** Required (ADMIN or MANAGER role)

**Path Parameters:**
- `tp_id` (UUID) - Tenant Product ID

**Request Body:**
```json
{
  "custom_name": "Updated Custom Name",
  "is_enabled": false,
  "tracking_unit": "ML",
  "default_unit_cost": 0.40,
  "currency": "USD"
}
```

**All fields are optional.**

---

### Remove Tenant Product

Remove a product from the tenant catalog.

**Endpoint:** `DELETE /products/tenant-catalog/{tp_id}`

**Authentication:** Required (ADMIN or MANAGER role)

**Path Parameters:**
- `tp_id` (UUID) - Tenant Product ID

**Response:** `204 No Content`

---

## Notes

- Global catalog (brands, product lines, products) is shared across all tenants
- Tenant products link global products to tenant-specific settings (cost, tracking unit, custom name)
- Only enabled tenant products can be used in formulas and inventory
- Tracking unit (G or ML) determines how inventory is measured for that product

