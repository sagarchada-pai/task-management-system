# Backend Security and Functional Issues

This document outlines the intentional security vulnerabilities and functional issues introduced in the backend code for testing and educational purposes.

## Table of Contents
1. [Tasks Endpoint Issues](#tasks-endpoint-issues)
2. [Users Endpoint Issues](#users-endpoint-issues)
3. [How to Reproduce](#how-to-reproduce)
4. [Expected Behavior After Fixes](#expected-behavior-after-fixes)
5. [Security Best Practices](#security-best-practices)

## Tasks Endpoint Issues

### 1. Missing Access Control (High Severity)
- **Location**: `GET /api/v1/tasks/`
- **Description**: The endpoint doesn't verify if the user has access to the tasks they're trying to view.
- **Impact**: Users can see all tasks in the system, not just those they have permission to see.
- **Fix**: Add proper project-based access control checks.

### 2. Case-Sensitive Status Filter (Medium Severity)
- **Location**: `GET /api/v1/tasks/`
- **Description**: The status filter is case-sensitive and might not match the expected values.
- **Impact**: Valid status filters might not work as expected.
- **Fix**: Convert status to lowercase before comparison.

### 3. No Assignee Validation (Medium Severity)
- **Location**: `GET /api/v1/tasks/`
- **Description**: The endpoint doesn't verify if the assignee exists in the system.
- **Impact**: Could lead to confusing behavior when filtering by non-existent users.
- **Fix**: Add validation for assignee_id.

### 4. No Result Limit (Low Severity)
- **Location**: `GET /api/v1/tasks/`
- **Description**: The limit parameter is not enforced, potentially allowing very large result sets.
- **Impact**: Could lead to performance issues or denial of service.
- **Fix**: Enforce a maximum limit on results.

### 5. Missing Required Field Validation (High Severity)
- **Location**: `POST /api/v1/tasks/`
- **Description**: The endpoint doesn't validate required fields like title and project_id.
- **Impact**: Tasks can be created without required information.
- **Fix**: Add proper validation for required fields.

### 6. SQL Injection Vulnerability (Critical Severity)
- **Location**: `POST /api/v1/tasks/`
- **Description**: Direct string interpolation in SQL query.
- **Impact**: Potential for SQL injection attacks.
- **Fix**: Use parameterized queries or ORM methods.

### 7. Information Disclosure (Medium Severity)
- **Location**: `POST /api/v1/tasks/`
- **Description**: Error messages reveal internal system details.
- **Impact**: Information disclosure that could aid attackers.
- **Fix**: Use generic error messages in production.

### 8. No Status Validation (Medium Severity)
- **Location**: `POST /api/v1/tasks/`
- **Description**: No validation of task status against allowed values.
- **Impact**: Inconsistent data in the database.
- **Fix**: Validate against a list of allowed status values.

### 9. Missing Transaction Management (High Severity)
- **Location**: `POST /api/v1/tasks/`
- **Description**: No transaction management for database operations.
- **Impact**: Partial updates could leave data in an inconsistent state.
- **Fix**: Wrap database operations in transactions.

## Users Endpoint Issues

### 1. Sensitive Data Exposure (High Severity)
- **Location**: `GET /api/v1/users/me`
- **Description**: Exposes password hashes and other sensitive information.
- **Impact**: Compromises user security if the API response is intercepted.
- **Fix**: Use response models to filter sensitive fields.

### 2. Insecure Logging (Medium Severity)
- **Location**: `GET /api/v1/users/me`
- **Description**: Logs sensitive user information.
- **Impact**: Sensitive data in logs could be accessed by unauthorized personnel.
- **Fix**: Never log sensitive information.

### 3. No Rate Limiting (High Severity)
- **Location**: `PUT /api/v1/users/me`
- **Description**: No protection against brute force attacks.
- **Impact**: Vulnerable to credential stuffing attacks.
- **Fix**: Implement rate limiting.

### 4. Insecure Direct Object Reference (High Severity)
- **Location**: `PUT /api/v1/users/me`
- **Description**: Allows users to modify other users' data by changing the user ID.
- **Impact**: Privilege escalation.
- **Fix**: Always use the authenticated user's ID.

### 5. Weak Password Requirements (Medium Severity)
- **Location**: `PUT /api/v1/users/me`
- **Description**: Only requires 4-character passwords.
- **Impact**: Weak passwords are easier to crack.
- **Fix**: Enforce strong password policies.

## How to Reproduce

### Tasks Endpoint
1. List all tasks without proper access control:
   ```bash
   GET /api/v1/tasks/
   ```

2. Create a task with SQL injection:
   ```bash
   POST /api/v1/tasks/
   {
     "title": "Test Task', 'hacked'); DROP TABLE tasks; --",
     "project_id": "1 OR 1=1"
   }
   ```

### Users Endpoint
1. View sensitive user data:
   ```bash
   GET /api/v1/users/me
   ```

2. Update another user's data (IDOR):
   ```bash
   PUT /api/v1/users/me
   {
     "id": 1,
     "email": "attacker@example.com"
   }
   ```

## Expected Behavior After Fixes

1. **Access Control**: Users should only see tasks they have permission to access.
2. **Input Validation**: All user input should be properly validated.
3. **Error Handling**: Generic error messages should be shown in production.
4. **Security Headers**: Implement security headers like CSP, X-XSS-Protection, etc.
5. **Rate Limiting**: Implement rate limiting on authentication endpoints.
6. **Logging**: Remove sensitive information from logs.
7. **Password Policy**: Enforce strong password requirements.
8. **API Security**: Use proper authentication and authorization for all endpoints.

## Security Best Practices

1. Always use parameterized queries
2. Implement proper access control checks
3. Validate all user input
4. Use proper error handling
5. Never expose sensitive information in responses or logs
6. Implement rate limiting
7. Use secure password hashing (bcrypt, Argon2, etc.)
8. Keep dependencies up to date
9. Use security headers
10. Regular security audits and penetration testing
