# API Test Cases - E-Commerce Platform

## Module Information

| Field | Value |
|-------|-------|
| Module | REST API Endpoints |
| Version | 1.0 |
| Created By | QA Team |
| Created Date | 2025-12-31 |
| Total Test Cases | 12 |
| Base URL | https://api.example.com/v1 |

---

## TC-API-001: GET User By ID - Success

**Endpoint:** GET /users/{id}  
**Priority:** High  
**Type:** Functional  
**Authentication:** Required

### Objective
Verify that API returns correct user details when valid user ID is provided.

### Preconditions
- Valid authentication token available
- User with ID=12345 exists in database

### Request Details

**Method:** GET  
**URL:** /users/12345  
**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
Accept: application/json
```

### Expected Response

**Status Code:** 200 OK  
**Response Time:** < 500ms

**Response Body:**
```json
{
  "id": 12345,
  "email": "testuser@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "phone": "+1234567890",
  "status": "active",
  "createdAt": "2025-01-15T10:30:00Z",
  "updatedAt": "2025-12-30T14:20:00Z"
}
```

### Validation Points
- Status code is 200
- Response contains all required fields
- Data types are correct
- User ID matches requested ID
- Email format is valid
- Timestamps are in ISO 8601 format
- No sensitive data (password) is exposed

---

## TC-API-002: GET User By ID - Not Found

**Endpoint:** GET /users/{id}  
**Priority:** High  
**Type:** Negative Testing  
**Authentication:** Required

### Objective
Verify that API returns appropriate error when non-existent user ID is requested.

### Request Details

**Method:** GET  
**URL:** /users/999999  
**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

### Expected Response

**Status Code:** 404 Not Found  
**Response Time:** < 300ms

**Response Body:**
```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with ID 999999 does not exist",
    "timestamp": "2025-12-31T10:30:00Z"
  }
}
```

### Validation Points
- Status code is 404
- Error message is descriptive
- Error code is consistent
- Timestamp is present
- No sensitive system information leaked

---

## TC-API-003: POST Create User - Success

**Endpoint:** POST /users  
**Priority:** Critical  
**Type:** Functional  
**Authentication:** Required

### Objective
Verify that new user can be created successfully with valid data.

### Request Details

**Method:** POST  
**URL:** /users  
**Headers:**
```
Authorization: Bearer {admin_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "firstName": "Jane",
  "lastName": "Smith",
  "password": "SecurePass@123",
  "phone": "+1987654321"
}
```

### Expected Response

**Status Code:** 201 Created  
**Response Time:** < 1000ms

**Response Body:**
```json
{
  "id": 12346,
  "email": "newuser@example.com",
  "firstName": "Jane",
  "lastName": "Smith",
  "phone": "+1987654321",
  "status": "active",
  "createdAt": "2025-12-31T10:30:00Z",
  "updatedAt": "2025-12-31T10:30:00Z"
}
```

**Response Headers:**
```
Location: /users/12346
```

### Validation Points
- Status code is 201
- Response includes generated user ID
- Location header contains new resource URL
- Password is not returned in response
- Timestamps are set correctly
- User is created in database
- Email confirmation sent (if applicable)

### Postconditions
- User record exists in database
- User can login with provided credentials
- Audit log entry created

---

## TC-API-004: POST Create User - Duplicate Email

**Endpoint:** POST /users  
**Priority:** High  
**Type:** Negative Testing  
**Authentication:** Required

### Objective
Verify that API rejects user creation with duplicate email address.

### Request Details

**Method:** POST  
**URL:** /users  
**Headers:**
```
Authorization: Bearer {admin_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "existinguser@example.com",
  "firstName": "Test",
  "lastName": "User",
  "password": "SecurePass@123",
  "phone": "+1234567890"
}
```

### Expected Response

**Status Code:** 409 Conflict  
**Response Time:** < 500ms

**Response Body:**
```json
{
  "error": {
    "code": "EMAIL_ALREADY_EXISTS",
    "message": "User with email existinguser@example.com already exists",
    "field": "email",
    "timestamp": "2025-12-31T10:30:00Z"
  }
}
```

### Validation Points
- Status code is 409
- Error clearly indicates duplicate email
- Field causing error is specified
- No user record is created
- No duplicate entries in database

---

## TC-API-005: POST Create User - Invalid Email Format

**Endpoint:** POST /users  
**Priority:** Medium  
**Type:** Validation Testing  
**Authentication:** Required

### Objective
Verify that API validates email format and rejects invalid emails.

### Request Details

**Method:** POST  
**URL:** /users

**Request Body:**
```json
{
  "email": "invalid-email",
  "firstName": "Test",
  "lastName": "User",
  "password": "SecurePass@123"
}
```

### Expected Response

**Status Code:** 400 Bad Request

**Response Body:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": [
      {
        "field": "email",
        "message": "Email format is invalid",
        "rejectedValue": "invalid-email"
      }
    ],
    "timestamp": "2025-12-31T10:30:00Z"
  }
}
```

### Validation Points
- Status code is 400
- Validation error is detailed
- Field name is specified
- Invalid value is shown
- No database record created

---

## TC-API-006: PUT Update User - Success

**Endpoint:** PUT /users/{id}  
**Priority:** High  
**Type:** Functional  
**Authentication:** Required

### Objective
Verify that user information can be updated successfully.

### Request Details

**Method:** PUT  
**URL:** /users/12345

**Request Body:**
```json
{
  "firstName": "John",
  "lastName": "Updated",
  "phone": "+1111111111"
}
```

### Expected Response

**Status Code:** 200 OK

**Response Body:**
```json
{
  "id": 12345,
  "email": "testuser@example.com",
  "firstName": "John",
  "lastName": "Updated",
  "phone": "+1111111111",
  "status": "active",
  "createdAt": "2025-01-15T10:30:00Z",
  "updatedAt": "2025-12-31T10:35:00Z"
}
```

### Validation Points
- Status code is 200
- Updated fields reflect new values
- Unchanged fields remain same
- updatedAt timestamp is updated
- createdAt timestamp unchanged
- Changes persisted in database

---

## TC-API-007: DELETE User - Success

**Endpoint:** DELETE /users/{id}  
**Priority:** High  
**Type:** Functional  
**Authentication:** Required (Admin)

### Objective
Verify that user can be deleted successfully by admin.

### Request Details

**Method:** DELETE  
**URL:** /users/12345  
**Headers:**
```
Authorization: Bearer {admin_token}
```

### Expected Response

**Status Code:** 204 No Content  
**Response Time:** < 500ms  
**Response Body:** Empty

### Validation Points
- Status code is 204
- Response body is empty
- User record deleted/marked as deleted in database
- Subsequent GET request returns 404
- User cannot login after deletion
- Audit log entry created

---

## TC-API-008: GET Products List - Pagination

**Endpoint:** GET /products  
**Priority:** High  
**Type:** Functional  
**Authentication:** Optional

### Objective
Verify that products API supports pagination correctly.

### Request Details

**Method:** GET  
**URL:** /products?page=1&limit=10&sort=name:asc

### Expected Response

**Status Code:** 200 OK

**Response Body:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Product A",
      "price": 29.99,
      "stock": 100
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "totalPages": 15,
    "totalItems": 150,
    "hasNext": true,
    "hasPrevious": false
  },
  "links": {
    "self": "/products?page=1&limit=10",
    "next": "/products?page=2&limit=10",
    "last": "/products?page=15&limit=10"
  }
}
```

### Validation Points
- Status code is 200
- Returns exactly 10 items (limit)
- Pagination metadata is correct
- Navigation links are provided
- Items are sorted by name ascending
- Total count is accurate

---

## TC-API-009: POST Login - Success

**Endpoint:** POST /auth/login  
**Priority:** Critical  
**Type:** Functional  
**Authentication:** None

### Objective
Verify successful authentication with valid credentials.

### Request Details

**Method:** POST  
**URL:** /auth/login

**Request Body:**
```json
{
  "email": "testuser@example.com",
  "password": "Test@1234"
}
```

### Expected Response

**Status Code:** 200 OK  
**Response Time:** < 1000ms

**Response Body:**
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIs...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIs...",
  "tokenType": "Bearer",
  "expiresIn": 3600,
  "user": {
    "id": 12345,
    "email": "testuser@example.com",
    "firstName": "John",
    "lastName": "Doe"
  }
}
```

### Validation Points
- Status code is 200
- Access token is returned
- Refresh token is returned
- Token expiry time is specified
- User information is included
- Tokens are valid JWT format
- Session created in database

---

## TC-API-010: POST Login - Invalid Credentials

**Endpoint:** POST /auth/login  
**Priority:** Critical  
**Type:** Security Testing  
**Authentication:** None

### Objective
Verify that login fails with invalid credentials and no sensitive info is leaked.

### Request Details

**Method:** POST  
**URL:** /auth/login

**Request Body:**
```json
{
  "email": "testuser@example.com",
  "password": "WrongPassword"
}
```

### Expected Response

**Status Code:** 401 Unauthorized  
**Response Time:** < 1000ms

**Response Body:**
```json
{
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password",
    "timestamp": "2025-12-31T10:30:00Z"
  }
}
```

### Validation Points
- Status code is 401
- Generic error message (doesn't reveal which field is wrong)
- No token is returned
- Failed attempt is logged
- Rate limiting is applied (if configured)
- No session created

---

## TC-API-011: Unauthorized Access - No Token

**Endpoint:** GET /users/12345  
**Priority:** Critical  
**Type:** Security Testing  
**Authentication:** None provided

### Objective
Verify that protected endpoints reject requests without authentication token.

### Request Details

**Method:** GET  
**URL:** /users/12345  
**Headers:**
```
Content-Type: application/json
```

### Expected Response

**Status Code:** 401 Unauthorized

**Response Body:**
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required",
    "timestamp": "2025-12-31T10:30:00Z"
  }
}
```

**Response Headers:**
```
WWW-Authenticate: Bearer realm="API"
```

### Validation Points
- Status code is 401
- WWW-Authenticate header is present
- Clear error message
- No data is returned
- Request is logged

---

## TC-API-012: Rate Limiting - Too Many Requests

**Endpoint:** Any endpoint  
**Priority:** Medium  
**Type:** Performance/Security  
**Authentication:** Optional

### Objective
Verify that API implements rate limiting to prevent abuse.

### Test Scenario
Send 100+ requests within 1 minute from same IP/user.

### Expected Response (after limit exceeded)

**Status Code:** 429 Too Many Requests

**Response Body:**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "retryAfter": 60,
    "timestamp": "2025-12-31T10:30:00Z"
  }
}
```

**Response Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1704016260
Retry-After: 60
```

### Validation Points
- Status code is 429
- Rate limit headers are present
- Retry-After header indicates wait time
- Limit is enforced correctly
- Normal requests resume after wait period

---

## Test Summary

| Category | Count |
|----------|-------|
| Total API Test Cases | 12 |
| Critical Priority | 3 |
| High Priority | 7 |
| Medium Priority | 2 |
| Functional Tests | 7 |
| Negative Tests | 3 |
| Security Tests | 2 |

## API Testing Checklist

- [ ] Status codes are correct
- [ ] Response times are within SLA
- [ ] Response schema matches documentation
- [ ] Error messages are descriptive
- [ ] Authentication is enforced
- [ ] Authorization is validated
- [ ] Input validation is working
- [ ] Rate limiting is implemented
- [ ] CORS headers are configured
- [ ] API versioning is supported
- [ ] Pagination works correctly
- [ ] Filtering and sorting work
- [ ] No sensitive data exposure
- [ ] SQL injection prevented
- [ ] Proper HTTP methods used

---

Document End