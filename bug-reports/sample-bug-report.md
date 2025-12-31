# Bug Report - Login Page Timeout Error

## Bug Information

| Field | Value |
|-------|-------|
| Bug ID | BUG-2145 |
| Title | Login page shows timeout error on valid credentials |
| Reported By | QA Engineer |
| Reported Date | 2025-12-31 |
| Environment | QA |
| Priority | High |
| Severity | High |
| Status | Assigned |
| Assigned To | Backend Team |
| Module | User Authentication |
| Version | 2.3.5 |

## Summary

Login page displays a timeout error when users attempt to login with valid credentials during peak hours, preventing legitimate users from accessing the system.

## Description

During load testing and peak usage hours (9 AM - 10 AM), the login functionality fails with a gateway timeout error (HTTP 504). Users enter valid credentials, click the login button, and after approximately 30 seconds, receive a timeout error message. This issue affects multiple users simultaneously and has significant business impact as it prevents users from accessing the platform during high-traffic periods.

The issue appears to be related to backend authentication service performance under load. Database query logs show slow response times exceeding 25 seconds for authentication queries during peak periods.

## Environment Details

### Application Environment
- Application URL: https://qa.example.com
- Build Number: 2.3.5-20251231
- Release Version: 2.3.5
- Server: AWS EC2 - QA Environment
- Database: PostgreSQL 14.5

### Test Environment
- Operating System: Windows 11 Pro
- Browser: Chrome 120.0.6099.130
- Screen Resolution: 1920x1080
- Mobile Device: Not applicable
- Network Conditions: Standard broadband (100 Mbps)

## Steps to Reproduce

1. Navigate to https://qa.example.com/login
2. Wait for peak usage hours (9:00 AM - 10:00 AM) or simulate load with 100+ concurrent users
3. Enter valid username: testuser@example.com
4. Enter valid password: Test@1234
5. Click the "Login" button
6. Wait for response
7. Observe timeout error after ~30 seconds

## Actual Results

After clicking the login button, the page shows a loading spinner for approximately 30 seconds, then displays:
- Error message: "Gateway Timeout - The server is taking too long to respond. Please try again later."
- HTTP Status Code: 504
- User remains on the login page
- No session is created
- Error is logged in browser console: "POST /api/auth/login net::ERR_EMPTY_RESPONSE"

## Expected Results

- User should be authenticated within 2-3 seconds
- User should be redirected to the dashboard
- Session token should be created
- Welcome message should be displayed
- No timeout errors should occur
- System should handle peak load gracefully

## Test Data

| Field | Value |
|-------|-------|
| Username | testuser@example.com |
| Password | Test@1234 |
| Account Type | Standard User |
| Account Status | Active |
| Concurrent Users | 150+ during test |
| Load Condition | Peak hours simulation |

## Attachments

### Screenshots
- timeout_error.png - Shows the timeout error message on login page
- network_tab.png - Browser network tab showing 504 error
- loading_state.png - Page stuck in loading state

### Videos
- login_timeout_recording.mp4 - Screen recording of the entire login attempt

### Logs
- backend_error_log.txt - Backend service error logs showing slow queries
- browser_console_log.txt - Browser console errors
- network_har_file.har - Complete network traffic capture
- database_slow_query_log.txt - PostgreSQL slow query log

## Additional Information

### Frequency
- [X] Always reproducible (during peak hours)
- [ ] Intermittent (occurs randomly)
- [X] Reproducible with specific conditions (100+ concurrent users)

### Workaround Available
- [X] Yes (describe below)
- [ ] No

Workaround Description:
Users can successfully login during off-peak hours (after 10:30 AM or before 8:30 AM) when server load is lower. Alternatively, increasing timeout settings on the load balancer to 60 seconds allows some requests to complete, though performance is still degraded.

### Related Issues
- Related to: BUG-2098 (Slow database queries under load)
- Related to: BUG-2134 (Connection pool exhaustion)
- Blocks: STORY-456 (Mobile app login integration)

### Performance Metrics

| Metric | Normal Load | Peak Load |
|--------|-------------|----------|
| Response Time | 1.2s | 30s+ |
| Concurrent Users | 20-30 | 150+ |
| Database Query Time | 100ms | 25s |
| CPU Usage | 45% | 95% |
| Memory Usage | 60% | 85% |
| Active Connections | 50 | 200+ |

### Root Cause (filled by developer)

Date: 2025-12-31
Analyzed by: Backend Team Lead

Root cause identified as:
1. Missing database index on user_authentication table for email lookups
2. N+1 query problem in user role permission loading
3. Insufficient database connection pool size (max 50 connections)
4. Lack of query caching for frequently accessed user data
5. Authentication service not horizontally scaled

Database explain analysis shows full table scan on 500,000+ user records during authentication. Each login triggers 15+ additional queries to load user permissions and preferences.

### Fix Description (filled by developer)

Implemented the following fixes:

1. Added composite index on (email, status) columns in user_authentication table
2. Implemented eager loading for user roles and permissions (eliminated N+1 queries)
3. Increased database connection pool from 50 to 200 connections
4. Added Redis caching layer for user session data and permissions (15-minute TTL)
5. Configured horizontal pod autoscaling for authentication service (2-6 replicas based on CPU)
6. Optimized authentication query from 15 queries to 2 queries
7. Added query result caching for user lookup operations

Performance improvements:
- Login response time reduced from 30s to 800ms under peak load
- Database query time reduced from 25s to 150ms
- Can now handle 300+ concurrent users without degradation

Fix deployed in build 2.3.6-20251231

## Testing Notes

Retested on build 2.3.6 with following scenarios:
1. Single user login: PASSED (response time: 1.1s)
2. 100 concurrent users: PASSED (avg response time: 1.8s)
3. 200 concurrent users: PASSED (avg response time: 2.3s)
4. 300 concurrent users: PASSED (avg response time: 3.1s)
5. Peak hour simulation: PASSED (no timeouts observed)

Recommendation: Move to Verified status pending regression testing.

## Comments

### Comment 1 - 2025-12-31 09:15 - QA Engineer
Also noticed similar timeout issues on the registration page. Might be related to the same root cause. Created separate bug report BUG-2146 for tracking.

### Comment 2 - 2025-12-31 11:30 - Backend Team Lead
Confirmed the issue. Database profiling shows severely degraded query performance. Working on optimization and indexing strategy. ETA for fix: EOD today.

### Comment 3 - 2025-12-31 15:45 - Database Administrator
Added indexes and verified query performance improvement in staging environment. Query time reduced from 25s to 120ms. Ready for deployment to QA.

### Comment 4 - 2025-12-31 17:00 - DevOps Engineer
Build 2.3.6 deployed to QA environment with all optimizations. Ready for retest.

### Comment 5 - 2025-12-31 18:30 - QA Engineer
Retested with load simulation. All scenarios passed. No timeouts observed. Performance significantly improved. Moving to Verified status.

---

Document End