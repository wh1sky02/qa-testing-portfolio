# Requirements Traceability Matrix

## Document Information

| Field | Value |
|-------|-------|
| Project | E-Commerce Platform |
| Module | User Authentication |
| Version | 1.0 |
| Date | 2025-12-31 |
| Author | QA Team |

---

## Purpose

This Requirements Traceability Matrix (RTM) maps business requirements to test cases, ensuring complete test coverage and traceability throughout the software development lifecycle.

---

## User Authentication Requirements

| Req ID | Requirement Description | Priority | Test Cases | Status | Coverage |
|--------|------------------------|----------|------------|--------|----------|
| REQ-001 | User shall be able to login with valid email and password | High | TC-AUTH-001, TC-AUTH-010 | Pass | 100% |
| REQ-002 | System shall validate email format during login | Medium | TC-AUTH-005, TC-API-005 | Pass | 100% |
| REQ-003 | System shall mask password input | Low | TC-AUTH-012 | Pass | 100% |
| REQ-004 | System shall display error on invalid credentials | High | TC-AUTH-002, TC-AUTH-003 | Pass | 100% |
| REQ-005 | System shall prevent SQL injection attacks | Critical | TC-AUTH-006 | Pass | 100% |
| REQ-006 | System shall prevent XSS attacks | Critical | TC-AUTH-007 | Pass | 100% |
| REQ-007 | System shall support "Remember Me" functionality | Medium | TC-AUTH-008 | Pass | 100% |
| REQ-008 | System shall lock account after 5 failed login attempts | High | TC-AUTH-009 | Pass | 100% |
| REQ-009 | User shall be able to logout successfully | High | TC-AUTH-010 | Pass | 100% |
| REQ-010 | System shall timeout inactive sessions after 30 minutes | High | TC-AUTH-011 | Pass | 100% |
| REQ-011 | System shall support password visibility toggle | Low | TC-AUTH-012 | Pass | 100% |
| REQ-012 | System shall provide forgot password functionality | High | TC-AUTH-013 | Pass | 100% |
| REQ-013 | System shall handle concurrent sessions per policy | Medium | TC-AUTH-014 | Pass | 100% |
| REQ-014 | System shall enforce password complexity rules | Medium | TC-AUTH-015 | Pass | 100% |
| REQ-015 | System shall validate required fields before submission | Medium | TC-AUTH-004, TC-AUTH-005 | Pass | 100% |

---

## API Requirements

| Req ID | Requirement Description | Priority | Test Cases | Status | Coverage |
|--------|------------------------|----------|------------|--------|----------|
| API-001 | GET /users/{id} shall return user details | High | TC-API-001 | Pass | 100% |
| API-002 | GET /users/{id} shall return 404 for invalid ID | High | TC-API-002 | Pass | 100% |
| API-003 | POST /users shall create new user | Critical | TC-API-003 | Pass | 100% |
| API-004 | POST /users shall reject duplicate email | High | TC-API-004 | Pass | 100% |
| API-005 | POST /users shall validate email format | Medium | TC-API-005 | Pass | 100% |
| API-006 | PUT /users/{id} shall update user details | High | TC-API-006 | Pass | 100% |
| API-007 | DELETE /users/{id} shall delete user | High | TC-API-007 | Pass | 100% |
| API-008 | GET /products shall support pagination | High | TC-API-008 | Pass | 100% |
| API-009 | POST /auth/login shall return JWT token | Critical | TC-API-009 | Pass | 100% |
| API-010 | POST /auth/login shall reject invalid credentials | Critical | TC-API-010 | Pass | 100% |
| API-011 | Protected endpoints shall require authentication | Critical | TC-API-011 | Pass | 100% |
| API-012 | API shall implement rate limiting | Medium | TC-API-012 | Pass | 100% |

---

## Performance Requirements

| Req ID | Requirement Description | Target | Test Cases | Status | Result |
|--------|------------------------|--------|------------|--------|--------|
| PERF-001 | Login response time shall be < 3s (95th percentile) | 3s | PERF-LOGIN-001 | Pass | 2.3s |
| PERF-002 | System shall support 5000 concurrent users | 5000 | PERF-LOAD-001 | Pass | 5500 |
| PERF-003 | API response time shall be < 500ms | 500ms | PERF-API-001 | Pass | 420ms |
| PERF-004 | Page load time shall be < 2s | 2s | PERF-UI-001 | Pass | 1.8s |
| PERF-005 | System shall handle 500 requests/second | 500 | PERF-THROUGHPUT-001 | Pass | 650 |

---

## Security Requirements

| Req ID | Requirement Description | Priority | Test Cases | Status | Coverage |
|--------|------------------------|----------|------------|--------|----------|
| SEC-001 | System shall prevent SQL injection | Critical | TC-AUTH-006, SEC-001 | Pass | 100% |
| SEC-002 | System shall prevent XSS attacks | Critical | TC-AUTH-007, SEC-002 | Pass | 100% |
| SEC-003 | System shall prevent CSRF attacks | Critical | SEC-003 | Pass | 100% |
| SEC-004 | Passwords shall be encrypted in database | Critical | SEC-004 | Pass | 100% |
| SEC-005 | System shall use HTTPS for all communications | Critical | SEC-005 | Pass | 100% |
| SEC-006 | System shall implement account lockout | High | TC-AUTH-009 | Pass | 100% |
| SEC-007 | System shall invalidate sessions on logout | High | TC-AUTH-010 | Pass | 100% |
| SEC-008 | Password reset tokens shall expire | High | SEC-008 | Pass | 100% |
| SEC-009 | System shall implement rate limiting | Medium | TC-API-012 | Pass | 100% |
| SEC-010 | System shall log security events | Medium | SEC-010 | Pass | 100% |

---

## Compatibility Requirements

| Req ID | Browser/Device | Version | Test Cases | Status |
|--------|----------------|---------|------------|--------|
| COMP-001 | Google Chrome | 120+ | COMP-CHROME-001 | Pass |
| COMP-002 | Mozilla Firefox | 121+ | COMP-FIREFOX-001 | Pass |
| COMP-003 | Apple Safari | 17+ | COMP-SAFARI-001 | Fail |
| COMP-004 | Microsoft Edge | 120+ | COMP-EDGE-001 | Pass |
| COMP-005 | iOS Mobile | 14+ | COMP-IOS-001 | Pass |
| COMP-006 | Android Mobile | 10+ | COMP-ANDROID-001 | Pass |

---

## Test Coverage Summary

| Category | Total Requirements | Tested | Passed | Failed | Coverage |
|----------|-------------------|--------|--------|--------|----------|
| Functional | 15 | 15 | 15 | 0 | 100% |
| API | 12 | 12 | 12 | 0 | 100% |
| Performance | 5 | 5 | 5 | 0 | 100% |
| Security | 10 | 10 | 10 | 0 | 100% |
| Compatibility | 6 | 6 | 5 | 1 | 83% |
| **Total** | **48** | **48** | **47** | **1** | **98%** |

---

## Defect Mapping

| Req ID | Requirement | Defects | Status |
|--------|-------------|---------|--------|
| REQ-012 | Forgot password functionality | BUG-2156 | Fixed & Verified |
| REQ-001 | User login | BUG-2145 | Fixed & Verified |
| COMP-003 | Safari compatibility | BUG-2190 | Open |

---

## Change History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-12-31 | Initial RTM creation | QA Team |

---

## Notes

- Safari compatibility issue (COMP-003) under investigation - BUG-2190
- All critical and high priority requirements have 100% test coverage
- Automated test coverage: 92%
- Manual test coverage: 8%

---

Document End