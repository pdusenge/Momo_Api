# MoMo Transaction API - Endpoint Documentation

## Base Information
- **Base URL:** `http://localhost:8000`
- **Authentication:** Basic Authentication (admin:secret)
- **Content-Type:** `application/json`
- **Response Format:** JSON

---

## 1. GET /transactions - Retrieve All Transactions

### Endpoint & Method
- **Method:** `GET`
- **URL:** `/transactions`
- **Authentication:** Required (Basic Auth)

### Description
Retrieves a list of all mobile money transactions in the system.

### Request Example
```http
GET http://localhost:8000/transactions
Authorization: Basic YWRtaW46c2VjcmV0
```

**cURL Command:**
```bash
curl -u admin:secret "http://localhost:8000/transactions"
```

### Response Example (200 OK)
```json
[
  {
    "transaction_id": "7666202170",
    "type": "receive",
    "amount": "2000",
    "sender": "Jane Smith",
    "receiver": null,
    "timestamp": "2024-05-10 16:30:51",
    "balance": "2000",
    "fee": null,
    "raw_body": "You have received 2000 RWF from Jane Smith (***********013) on your mobile money account at 2024-05-10 16:30:51. Message from sender: . Your new balance:2000 RWF."
  }
]
```

### Error Codes
- **200 OK:** Successfully retrieved transactions
- **401 Unauthorized:** Invalid or missing authentication credentials
- **500 Internal Server Error:** Server error occurred

---

## 2. GET /transactions/{id} - Retrieve Single Transaction

### Endpoint & Method
- **Method:** `GET`
- **URL:** `/transactions/{id}`
- **Authentication:** Required (Basic Auth)
- **Parameters:** 
  - `id` (path parameter): Transaction ID

### Description
Retrieves a specific transaction by its ID.

### Request Example
```http
GET http://localhost:8000/transactions/1692
Authorization: Basic YWRtaW46c2VjcmV0
```

**cURL Command:**
```bash
curl -u admin:secret "http://localhost:8000/transactions/1692"
```

### Response Example (200 OK)
```json
{
  "transaction_id": "10264064542",
  "type": "receive",
  "amount": "50000",
  "sender": "Vivine",
  "receiver": "Peggy",
  "timestamp": "2024-10-23 09:59:01",
  "balance": "81022",
  "fee": 0,
  "raw_body": "You have received 50000 RWF from Jane Smith (25079596306) on your mobile money account at 2024-10-23 09:59:01. Message from sender: . Your new balance:81022 RWF. Financial Transaction Id: 80264064542."
}
```

### Error Codes
- **200 OK:** Transaction found and returned
- **401 Unauthorized:** Invalid or missing authentication credentials
- **404 Not Found:** Transaction with specified ID does not exist
- **500 Internal Server Error:** Server error occurred

---

## 3. POST /transactions - Create New Transaction

### Endpoint & Method
- **Method:** `POST`
- **URL:** `/transactions`
- **Authentication:** Required (Basic Auth)
- **Content-Type:** `application/json`

### Description
Creates a new transaction record in the system.

### Request Body Schema
```json
{
  "transaction_id": "string (required)",
  "type": "string (required)",
  "amount": "string/number (required)",
  "sender": "string (optional)",
  "receiver": "string (optional)",
  "timestamp": "string (optional)",
  "balance": "string/number (optional)",
  "fee": "number (optional)",
  "raw_body": "string (optional)"
}
```

### Request Example
```http
POST http://localhost:8000/transactions
Authorization: Basic YWRtaW46c2VjcmV0
Content-Type: application/json

{
  "transaction_id": "10264064542",
  "type": "receive",
  "amount": "50000",
  "sender": "Jane Smith",
  "receiver": "Peggy",
  "timestamp": "2024-10-23 09:59:01",
  "balance": "81022",
  "fee": 0,
  "raw_body": "You have received 50000 RWF from Jane Smith (25079596306) on your mobile money account at 2024-10-23 09:59:01. Message from sender: . Your new balance:81022 RWF. Financial Transaction Id: 80264064542."
}
```

**cURL Command:**
```bash
curl -u admin:secret -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "10264064542",
    "type": "receive",
    "amount": "50000",
    "sender": "Jane Smith",
    "receiver": "Peggy",
    "timestamp": "2024-10-23 09:59:01",
    "balance": "81022",
    "fee": 0
  }' \
  "http://localhost:8000/transactions"
```

### Response Example (201 Created)
```json
{
  "id": 1692,
  "transaction_id": "10264064542",
  "type": "receive",
  "amount": "50000",
  "sender": "Jane Smith",
  "receiver": "Peggy",
  "timestamp": "2024-10-23 09:59:01",
  "balance": "81022",
  "fee": 0,
  "raw_body": "You have received 50000 RWF from Jane Smith (25079596306) on your mobile money account at 2024-10-23 09:59:01. Message from sender: . Your new balance:81022 RWF. Financial Transaction Id: 80264064542."
}
```

### Error Codes
- **201 Created:** Transaction successfully created
- **400 Bad Request:** Invalid JSON format or missing required fields
- **401 Unauthorized:** Invalid or missing authentication credentials
- **500 Internal Server Error:** Server error occurred

---

## 4. PUT /transactions/{id} - Update Existing Transaction

### Endpoint & Method
- **Method:** `PUT`
- **URL:** `/transactions/{id}`
- **Authentication:** Required (Basic Auth)
- **Content-Type:** `application/json`
- **Parameters:** 
  - `id` (path parameter): Transaction ID to update

### Description
Updates an existing transaction record with new data.

### Request Body Schema
All fields are optional for updates:
```json
{
  "transaction_id": "string",
  "type": "string",
  "amount": "string/number",
  "sender": "string",
  "receiver": "string",
  "timestamp": "string",
  "balance": "string/number",
  "fee": "number",
  "raw_body": "string"
}
```

### Request Example
```http
PUT http://localhost:8000/transactions/1692
Authorization: Basic YWRtaW46c2VjcmV0
Content-Type: application/json

{
  "transaction_id": "10264064542",
  "type": "receive",
  "amount": "50000",
  "sender": "Vivine",
  "receiver": "Peggy",
  "timestamp": "2024-10-23 09:59:01",
  "balance": "81022",
  "fee": 0,
  "raw_body": "You have received 50000 RWF from Jane Smith (25079596306) on your mobile money account at 2024-10-23 09:59:01. Message from sender: . Your new balance:81022 RWF. Financial Transaction Id: 80264064542."
}
```

**cURL Command:**
```bash
curl -u admin:secret -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "Vivine",
    "amount": "55000",
    "balance": "86022"
  }' \
  "http://localhost:8000/transactions/1692"
```

### Response Example (200 OK)
```json
{
  "id": 1692,
  "transaction_id": "10264064542",
  "type": "receive",
  "amount": "50000",
  "sender": "Vivine",
  "receiver": "Peggy",
  "timestamp": "2024-10-23 09:59:01",
  "balance": "81022",
  "fee": 0,
  "raw_body": "You have received 50000 RWF from Jane Smith (25079596306) on your mobile money account at 2024-10-23 09:59:01. Message from sender: . Your new balance:81022 RWF. Financial Transaction Id: 80264064542."
}
```

### Error Codes
- **200 OK:** Transaction successfully updated
- **400 Bad Request:** Invalid JSON format
- **401 Unauthorized:** Invalid or missing authentication credentials
- **404 Not Found:** Transaction with specified ID does not exist
- **500 Internal Server Error:** Server error occurred

---

## 5. DELETE /transactions/{id} - Delete Transaction

### Endpoint & Method
- **Method:** `DELETE`
- **URL:** `/transactions/{id}`
- **Authentication:** Required (Basic Auth)
- **Parameters:** 
  - `id` (path parameter): Transaction ID to delete

### Description
Permanently removes a transaction record from the system.

### Request Example
```http
DELETE http://localhost:8000/transactions/5
Authorization: Basic YWRtaW46c2VjcmV0
```

**cURL Command:**
```bash
curl -u admin:secret -X DELETE "http://localhost:8000/transactions/5"
```

### Response Example (200 OK)
```json
{
  "deleted": {
    "transaction_id": "17818959211",
    "type": "codePay",
    "amount": "2,000",
    "sender": null,
    "receiver": "Samuel Carter 14965",
    "timestamp": "2024-05-11 18:48:42",
    "balance": "38,400",
    "fee": 0,
    "raw_body": "TxId: 17818959211. Your payment of 2,000 RWF to Samuel Carter 14965 has been completed at 2024-05-11 18:48:42. Your new balance: 38,400 RWF. Fee was 0 RWF.Kanda*182"
  }
}
```

### Error Codes
- **200 OK:** Transaction successfully deleted
- **401 Unauthorized:** Invalid or missing authentication credentials
- **404 Not Found:** Transaction with specified ID does not exist
- **500 Internal Server Error:** Server error occurred

---

## Authentication Details

### Basic Authentication
All endpoints require HTTP Basic Authentication with the following credentials:

- **Username:** `admin`
- **Password:** `secret`

### Authentication Header Format
```
Authorization: Basic YWRtaW46c2VjcmV0
```

Where `YWRtaW46c2VjcmV0` is the Base64 encoding of `admin:secret`.

### Authentication Failure Response (401)
```json
HTTP/1.0 401 Unauthorized
WWW-Authenticate: Basic realm="MoMoAPI"
```

---

## Common Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid JSON"
}
```

### 401 Unauthorized
```json
HTTP/1.0 401 Unauthorized
WWW-Authenticate: Basic realm="MoMoAPI"
```

### 404 Not Found
```json
{
  "error": "Not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Data Models

### Transaction Object
```json
{
  "id": "integer (auto-generated)",
  "transaction_id": "string (unique identifier)",
  "type": "string (receive, send, codePay, etc.)",
  "amount": "string/number (transaction amount)",
  "sender": "string|null (sender name/identifier)",
  "receiver": "string|null (receiver name/identifier)",
  "timestamp": "string (YYYY-MM-DD HH:MM:SS format)",
  "balance": "string/number (account balance after transaction)",
  "fee": "number|null (transaction fee)",
  "raw_body": "string (original SMS message body)"
}
```

---

## Rate Limiting & Performance

- **Concurrent Requests:** Supported with thread-safe file operations
- **Response Time:** Typically under 100ms for single operations
- **File Storage:** JSON file-based persistence (`data/transactions.json`)
- **Memory Usage:** Loads full dataset into memory for fast access

---

## Testing Examples

### Complete Test Sequence
```bash
# 1. Get all transactions
curl -u admin:secret "http://localhost:8000/transactions"

# 2. Create a new transaction
curl -u admin:secret -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "TEST123456",
    "type": "send",
    "amount": "10000",
    "sender": "Test User",
    "receiver": "Test Recipient",
    "balance": "90000"
  }' \
  "http://localhost:8000/transactions"

# 3. Get the created transaction (assuming ID 1693)
curl -u admin:secret "http://localhost:8000/transactions/1693"

# 4. Update the transaction
curl -u admin:secret -X PUT \
  -H "Content-Type: application/json" \
  -d '{"amount": "15000", "balance": "85000"}' \
  "http://localhost:8000/transactions/1693"

# 5. Delete the transaction
curl -u admin:secret -X DELETE "http://localhost:8000/transactions/1693"

# 6. Test authentication failure
curl "http://localhost:8000/transactions"
```

---
