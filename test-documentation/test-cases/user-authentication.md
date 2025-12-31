# Test Cases - User Authentication Module

## Module Information

| Field | Value |
|-------|-------|
| Module | User Authentication |
| Version | 1.0 |
| Created By | QA Team |
| Created Date | 2025-12-31 |
| Total Test Cases | 15 |

---

## TC-AUTH-001: Valid User Login

**Priority:** High  
**Severity:** Critical  
**Type:** Functional  
**Automation Status:** Automated

### Objective
Verify that a registered user can successfully login with valid credentials.

### Preconditions
- User account exists in the system
- User credentials: username = "testuser@example.com", password = "Test@1234"
- User is not already logged in

### Test Data
| Field | Value |
|-------|-------|
| Username | testuser@example.com |
| Password | Test@1234 |

### Test Steps

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to login page | Login page is displayed |
| 2 | Enter valid username | Username is entered in the field |
| 3 | Enter valid password | Password is entered and masked |
| 4 | Click 'Login' button | User is redirected to dashboard |
| 5 | Verify user name displayed | User name appears in header |

### Expected Results
- User successfully logs in
- Redirected to user dashboard
- Session token created
- User name displayed in header

### Postconditions
- User is logged in
- Session is active
- Login timestamp recorded in database

---

## TC-AUTH-002: Invalid Username Login Attempt

**Priority:** High  
**Severity:** High  
**Type:** Functional  
**Automation Status:** Automated

### Objective
Verify that login fails with an invalid username.

### Preconditions
- Login page is accessible
- User is not logged in

### Test Data
| Field | Value |
|-------|-------|
| Username | invaliduser@example.com |
| Password | Test@1234 |

### Test Steps

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to login page | Login page is displayed |
| 2 | Enter invalid username | Username is entered in the field |
| 3 | Enter any password | Password is entered and masked |
| 4 | Click 'Login' button | Error message is displayed |
| 5 | Verify error message | "Invalid username or password" message shown |

### Expected Results
- Login attempt fails
- Appropriate error message displayed
- User remains on login page
- No session created
- Failed login attempt logged

### Postconditions
- User is not logged in
- Failed attempt recorded in system logs

---

## TC-AUTH-003: Invalid Password Login Attempt

**Priority:** High  
**Severity:** High  
**Type:** Functional  
**Automation Status:** Automated

### Objective
Verify that login fails with an invalid password.

### Preconditions
- User account exists in the system
- Login page is accessible

### Test Data
| Field | Value |
|-------|-------|
| Username | testuser@example.com |
| Password | WrongPassword@123 |

### Test Steps

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to login page | Login page is displayed |
| 2 | Enter valid username | Username is entered in the field |
| 3 | Enter invalid password | Password is entered and masked |
| 4 | Click 'Login' button | Error message is displayed |
| 5 | Verify error message | "Invalid username or password" message shown |

### Expected Results
- Login attempt fails
- Generic error message displayed (security best practice)
- User remains on login page
- No session created
- Failed login attempt logged

### Postconditions
- User is not logged in
- Failed attempt counter incremented
- Security log entry created

---

## TC-AUTH-004: Empty Username Field

**Priority:** Medium  
**Severity:** Medium  
**Type:** Functional  
**Automation Status:** Automated

### Objective
Verify that login fails when username field is empty.

### Preconditions
- Login page is accessible

### Test Data
| Field | Value |
|-------|-------|
| Username | (empty) |
| Password | Test@1234 |

### Test Steps

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to login page | Login page is displayed |
| 2 | Leave username field empty | Username field is empty |
| 3 | Enter password | Password is entered |
| 4 | Click 'Login' button | Validation error is displayed |
| 5 | Verify error message | "Username is required" message shown |

### Expected Results
- Login button click triggers validation
- Error message displayed under username field
- Form is not submitted
- User remains on login page

---

## TC-AUTH-005: Empty Password Field

**Priority:** Medium  
**Severity:** Medium  
**Type:** Functional  
**Automation Status:** Automated

### Objective
Verify that login fails when password field is empty.

### Preconditions
- Login page is accessible

### Test Data
| Field | Value |
|-------|-------|
| Username | testuser@example.com |
| Password | (empty) |

### Test Steps

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to login page | Login page is displayed |
| 2 | Enter username | Username is entered |
| 3 | Leave password field empty | Password field is empty |
| 4 | Click 'Login' button | Validation error is displayed |
| 5 | Verify error message | "Password is required" message shown |

### Expected Results
- Login button click triggers validation
- Error message displayed under password field
- Form is not submitted
- User remains on login page

---

## TC-AUTH-006: SQL Injection in Username Field

**Priority:** Critical  
**Severity:** Critical  
**Type:** Security  
**Automation Status:** Automated

### Objective
Verify that application is protected against SQL injection attacks via username field.

### Preconditions
- Login page is accessible

### Test Data
| Field | Value |
|-------|-------|
| Username | admin' OR '1'='1 |
| Password | anything |

### Test Steps

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to login page | Login page is displayed |
| 2 | Enter SQL injection string in username | SQL injection string entered |
| 3 | Enter any password | Password is entered |
| 4 | Click 'Login' button | Login fails with error message |
| 5 | Verify no unauthorized access | User is not logged in |
| 6 | Check security logs | Injection attempt is logged |

### Expected Results
- SQL injection attempt is blocked
- No unauthorized access granted
- Generic error message displayed
- Security team alerted
- Incident logged in security logs

---

## TC-AUTH-007: XSS Attack in Username Field

**Priority:** Critical  
**Severity:** Critical  
**Type:** Security  
**Automation Status:** Automated

### Objective
Verify that application is protected against XSS attacks.

### Preconditions
- Login page is accessible

### Test Data
| Field | Value |
|-------|-------|
| Username | <script>alert('XSS')</script> |
| Password | Test@1234 |

### Test Steps

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to login page | Login page is displayed |
| 2 | Enter XSS script in username | Script entered as text |
| 3 | Enter password | Password is entered |
| 4 | Click 'Login' button | Login fails |
| 5 | Verify no script execution | No alert popup appears |
| 6 | Verify input sanitization | Script tags are escaped/removed |

### Expected Results
- XSS attack is prevented
- Script is not executed
- Input is properly sanitized
- Error message displayed
- Security log entry created

---

## TC-AUTH-008: Remember Me Functionality

**Priority:** Medium  
**Severity:** Low  
**Type:** Functional  
**Automation Status:** Manual

### Objective
Verify that "Remember Me" functionality works correctly.

### Preconditions
- User account exists
- User is not logged in
- Browser cookies are enabled

### Test Data
| Field | Value |
|-------|-------|
| Username | testuser@example.com |
| Password | Test@1234 |
| Remember Me | Checked |

### Test Steps

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to login page | Login page is displayed |
| 2 | Enter valid credentials | Credentials entered |
| 3 | Check "Remember Me" checkbox | Checkbox is checked |
| 4 | Click 'Login' button | User is logged in |
| 5 | Close browser completely | Browser closed |
| 6 | Reopen browser and navigate to site | User is still logged in |

### Expected Results
- User remains logged in after browser restart
- Persistent cookie is created
- Cookie expiration set appropriately (e.g., 30 days)
- User can access protected pages without re-login

---

## TC-AUTH-009: Account Lockout After Multiple Failed Attempts

**Priority:** High  
**Severity:** High  
**Type:** Security  
**Automation Status:** Automated

### Objective
Verify that account is locked after specified number of failed login attempts.

### Preconditions
- User account exists and is active
- Account lockout threshold is set to 5 attempts

### Test Data
| Field | Value |
|-------|-------|
| Username | testuser@example.com |
| Password | WrongPassword |

### Test Steps

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Attempt login with wrong password | Login fails |
| 2 | Repeat step 1 four more times | Each login fails |
| 3 | Attempt 6th login with wrong password | Account locked message displayed |
| 4 | Try login with correct password | Account locked message displayed |
| 5 | Verify lockout notification | Email sent to user |

### Expected Results
- Account is locked after 5 failed attempts
- "Account locked" message displayed
- User cannot login even with correct password
- Security notification sent to user email
- Admin can unlock the account
- Automatic unlock after specified duration

---

## TC-AUTH-010: Logout Functionality

**Priority:** High  
**Severity:** High  
**Type:** Functional  
**Automation Status:** Automated

### Objective
Verify that user can successfully logout.

### Preconditions
- User is logged in

### Test Steps

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | User is on dashboard | Dashboard is displayed |
| 2 | Click 'Logout' button | Logout confirmation or immediate logout |
| 3 | Verify redirect to login page | Login page is displayed |
| 4 | Try to access protected page | Redirected to login page |
| 5 | Use browser back button | Still on login page or shows logout state |

### Expected Results
- User is logged out successfully
- Session is terminated
- Session cookie is deleted
- User redirected to login page
- Cannot access protected pages without re-login
- Logout timestamp recorded

---

## TC-AUTH-011: Session Timeout

**Priority:** High  
**Severity:** Medium  
**Type:** Functional  
**Automation Status:** Automated

### Objective
Verify that user session expires after inactivity period.

### Preconditions
- User is logged in
- Session timeout is set to 30 minutes

### Test Steps

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Login to application | User is logged in |
| 2 | Leave application idle for 30 minutes | No activity for 30 minutes |
| 3 | Try to perform any action | Session timeout warning appears |
| 4 | Wait or ignore warning | Redirected to login page |
| 5 | Verify session ended | Must login again to access system |

### Expected Results
- Session expires after 30 minutes of inactivity
- User receives timeout warning (1-2 minutes before expiry)
- User is redirected to login page
- Session data is cleared
- User must re-authenticate

---

## TC-AUTH-012: Password Visibility Toggle

**Priority:** Low  
**Severity:** Low  
**Type:** Functional  
**Automation Status:** Automated

### Objective
Verify that password visibility toggle works correctly.

### Preconditions
- Login page is accessible

### Test Steps

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to login page | Login page displayed |
| 2 | Enter password in password field | Password appears as dots/asterisks |
| 3 | Click eye icon to show password | Password is displayed in plain text |
| 4 | Click eye icon again to hide | Password is masked again |

### Expected Results
- Password field has visibility toggle icon
- Toggle shows/hides password correctly
- Icon changes to indicate current state
- Functionality works smoothly

---

## TC-AUTH-013: Forgot Password Functionality

**Priority:** High  
**Severity:** High  
**Type:** Functional  
**Automation Status:** Automated

### Objective
Verify that forgot password functionality works correctly.

### Preconditions
- User account exists with registered email

### Test Data
| Field | Value |
|-------|-------|
| Email | testuser@example.com |

### Test Steps

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to login page | Login page displayed |
| 2 | Click "Forgot Password" link | Forgot password page displayed |
| 3 | Enter registered email address | Email entered in field |
| 4 | Click 'Submit' button | Success message displayed |
| 5 | Check email inbox | Password reset email received |
| 6 | Click reset link in email | Password reset page opens |
| 7 | Enter new password | New password entered |
| 8 | Confirm new password | Confirmation entered |
| 9 | Submit new password | Password changed successfully |
| 10 | Login with new password | Login successful |

### Expected Results
- Password reset email sent to registered email
- Reset link is unique and time-limited (e.g., 1 hour)
- New password meets complexity requirements
- Old password is invalidated
- User can login with new password
- Reset link can only be used once

---

## TC-AUTH-014: Concurrent Session Management

**Priority:** Medium  
**Severity:** Medium  
**Type:** Functional  
**Automation Status:** Automated

### Objective
Verify system behavior when user logs in from multiple devices.

### Preconditions
- User account exists
- Multiple devices/browsers available

### Test Steps

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Login from Device A | User logged in on Device A |
| 2 | Login from Device B with same credentials | User logged in on Device B |
| 3 | Check Device A session | Based on policy: either logged out or remains active |
| 4 | Perform action on Device A | Based on policy: works or requires re-login |
| 5 | Logout from Device B | Device B logged out |
| 6 | Verify Device A status | Device A session status verified |

### Expected Results
- System handles concurrent sessions as per security policy
- Option 1: Previous session terminated when new login occurs
- Option 2: Multiple active sessions allowed with limit
- Option 3: User notified of concurrent login
- All sessions properly tracked in database

---

## TC-AUTH-015: Password Complexity Validation

**Priority:** Medium  
**Severity:** Medium  
**Type:** Functional  
**Automation Status:** Automated

### Objective
Verify that password complexity requirements are enforced during registration/password change.

### Preconditions
- Password requirements:
  - Minimum 8 characters
  - At least 1 uppercase letter
  - At least 1 lowercase letter
  - At least 1 number
  - At least 1 special character

### Test Data
| Password | Expected Result |
|----------|----------------|
| test | Failed - too short |
| testtest | Failed - no uppercase, number, special char |
| Testtest | Failed - no number, special char |
| Testtest1 | Failed - no special char |
| Test@123 | Success - meets all requirements |
| Password@123 | Success - meets all requirements |

### Test Steps

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to registration/change password | Page displayed |
| 2 | Enter weak password | Real-time validation shows errors |
| 3 | Attempt to submit | Submission blocked |
| 4 | Enter password meeting requirements | Validation passes |
| 5 | Submit form | Form submitted successfully |

### Expected Results
- Password complexity requirements clearly displayed
- Real-time validation feedback provided
- Weak passwords are rejected
- Strong passwords are accepted
- Clear error messages guide user

---

## Test Summary

| Category | Count |
|----------|-------|
| Total Test Cases | 15 |
| Automated | 13 |
| Manual | 2 |
| Critical Priority | 3 |
| High Priority | 7 |
| Medium Priority | 4 |
| Low Priority | 1 |

---

Document End