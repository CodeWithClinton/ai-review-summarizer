

# 🛒 Products & AI Review Summary API (DRF)

Base URL:

```
http://localhost:8000/
```

This API allows frontend applications to:

* List products
* View a single product with reviews
* Generate an **AI-powered summary of recent reviews** (rate-limited to once every 7 days per product)

---

## 📦 Data Models (What the Frontend Will See)

### Review Object

```json
{
  "id": 1,
  "product": 3,
  "rating": 4,
  "comment": "Great product, works well",
  "author": "John Doe",
  "created_at": "2026-01-10T14:22:01Z"
}
```

---

### Product (List View)

```json
{
  "id": 3,
  "name": "Wireless Headphones",
  "image_url": "https://example.com/image.jpg",
  "price": "59.99",
  "slug": "wireless-headphones",
  "reviews": [ ... ]
}
```

---

### Product (Detail View)

```json
{
  "id": 3,
  "name": "Wireless Headphones",
  "image_url": "https://example.com/image.jpg",
  "description": "High-quality wireless headphones",
  "price": "59.99",
  "slug": "wireless-headphones",
  "review_summary": "Overall sentiment is positive...",
  "summary_updated_at": "2026-01-09T10:30:00Z",
  "reviews": [ ... ]
}
```

---

## 🔍 Endpoints

---

## 1️⃣ List All Products

### **GET** `/products/`

Fetches all products with their associated reviews.

**Endpoint**

```
GET /api/products/
```

**Use case**

* Product listing page
* Store homepage
* Product cards grid

**Response**

```json
[
  {
    "id": 1,
    "name": "Smart Watch",
    "image_url": "...",
    "price": "120.00",
    "slug": "smart-watch",
    "reviews": []
  }
]
```

**Notes for frontend**

* `reviews` is included but can be ignored if not needed for listing.
* Use `slug` for routing to product detail pages.

---

## 2️⃣ Get Single Product Details

### **GET** `/products/{slug}/`

Fetches full details of a single product, including:

* Description
* Reviews
* AI-generated review summary (if available)

**Endpoint**

```
GET /api/products/{slug}/
```

**Example**

```
GET /api/products/wireless-headphones/
```

**Response**

```json
{
  "id": 3,
  "name": "Wireless Headphones",
  "image_url": "...",
  "description": "High-quality wireless headphones",
  "price": "59.99",
  "slug": "wireless-headphones",
  "review_summary": "Overall sentiment is positive...",
  "summary_updated_at": "2026-01-09T10:30:00Z",
  "reviews": [
    {
      "id": 12,
      "rating": 5,
      "comment": "Amazing sound quality",
      "author": "Jane",
      "created_at": "2026-01-08T11:00:00Z"
    }
  ]
}
```

**Notes for frontend**

* `review_summary` can be `null` if not yet generated.
* `summary_updated_at` tells when the summary was last created.
* Reviews are ordered by creation date (newest first).

---

## 3️⃣ Generate AI Review Summary

### **POST** `/products/{slug}/generate-summary/`

Generates an **AI-powered summary** of the **latest 10 reviews** for a product.

⚠️ **Important Rule**

* A summary can only be generated **once every 7 days per product**.

**Endpoint**

```
POST /api/products/{slug}/generate-summary/
```

**Example**

```
POST /api/products/wireless-headphones/generate-summary/
```

---

### ✅ Successful (New Summary Created)

**Status:** `201 CREATED`

```json
{
  "product": "Wireless Headphones",
  "summary": "Overall sentiment is positive. Customers love the sound quality...",
  "generated_at": "2026-01-11T09:15:00Z",
  "days_left": 7,
  "newly_created": true
}
```

**Frontend behavior**

* Update the UI with the new summary immediately
* Optionally show “Updated just now”

---

### 🔁 Summary Already Exists (Within 7 Days)

**Status:** `200 OK`

```json
{
  "detail": "Summary was recently generated",
  "summary": "Overall sentiment is positive...",
  "days_left": 3,
  "next_allowed_at": "2026-01-14T09:15:00Z",
  "generated_at": "2026-01-11T09:15:00Z",
  "newly_created": false
}
```

**Frontend behavior**

* Display the existing summary
* Disable the “Generate Summary” button
* Optionally show:
  *“You can regenerate this summary in 3 days”*

---

### ❌ No Reviews Available

**Status:** `400 BAD REQUEST`

```json
{
  "error": "No reviews available."
}
```

**Frontend behavior**

* Hide or disable the “Generate Summary” button
* Show a message like:

  > “This product doesn’t have enough reviews yet.”

---

## 🧠 How the AI Summary Works (High Level)

* Only the **latest 10 reviews** are used
* The AI generates:

  * Overall sentiment
  * Common pros
  * Common cons
  * A short final summary
* The result is stored and reused until the 7-day cooldown expires

---
