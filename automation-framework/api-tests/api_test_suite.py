#!/usr/bin/env python3
"""
API Automation Test Suite
Author: QA Team
Date: 2025-12-31
Framework: pytest with requests library
"""

import pytest
import requests
import json
from datetime import datetime
import time


class APIClient:
    """
    Wrapper class for API requests with common functionality
    """
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None
        
    def set_auth_token(self, token):
        """Set authentication token for requests"""
        self.token = token
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })
        
    def get(self, endpoint, params=None):
        """Send GET request"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params)
        return response
        
    def post(self, endpoint, data=None, json_data=None):
        """Send POST request"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, data=data, json=json_data)
        return response
        
    def put(self, endpoint, data=None, json_data=None):
        """Send PUT request"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(url, data=data, json=json_data)
        return response
        
    def delete(self, endpoint):
        """Send DELETE request"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url)
        return response


class TestUserAPI:
    """
    Test suite for User API endpoints
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        self.base_url = "https://api.example.com/v1"
        self.client = APIClient(self.base_url)
        
        # Login to get auth token
        login_response = self.client.post("/auth/login", json_data={
            "email": "testuser@example.com",
            "password": "Test@1234"
        })
        
        if login_response.status_code == 200:
            token = login_response.json().get('accessToken')
            self.client.set_auth_token(token)
        
        yield
        
        # Cleanup if needed
        
    def test_get_user_by_id_success(self):
        """
        TC-API-001: GET User By ID - Success
        """
        user_id = 12345
        response = self.client.get(f"/users/{user_id}")
        
        # Assertions
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.headers['Content-Type'] == 'application/json'
        
        # Verify response time
        assert response.elapsed.total_seconds() < 0.5, "Response time exceeded 500ms"
        
        # Verify response body
        data = response.json()
        assert data['id'] == user_id
        assert 'email' in data
        assert 'firstName' in data
        assert 'lastName' in data
        assert 'password' not in data, "Password should not be exposed"
        
        # Verify data types
        assert isinstance(data['id'], int)
        assert isinstance(data['email'], str)
        assert '@' in data['email'], "Invalid email format"
        
    def test_get_user_not_found(self):
        """
        TC-API-002: GET User By ID - Not Found
        """
        non_existent_id = 999999
        response = self.client.get(f"/users/{non_existent_id}")
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        
        error = response.json()['error']
        assert error['code'] == 'USER_NOT_FOUND'
        assert 'message' in error
        assert 'timestamp' in error
        
    def test_create_user_success(self):
        """
        TC-API-003: POST Create User - Success
        """
        new_user = {
            "email": f"newuser_{int(time.time())}@example.com",
            "firstName": "Jane",
            "lastName": "Smith",
            "password": "SecurePass@123",
            "phone": "+1987654321"
        }
        
        response = self.client.post("/users", json_data=new_user)
        
        # Assertions
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        assert 'Location' in response.headers, "Location header missing"
        
        # Verify response time
        assert response.elapsed.total_seconds() < 1.0, "Response time exceeded 1000ms"
        
        # Verify response body
        data = response.json()
        assert 'id' in data
        assert data['email'] == new_user['email']
        assert data['firstName'] == new_user['firstName']
        assert 'password' not in data, "Password should not be returned"
        assert data['status'] == 'active'
        
        # Verify timestamps
        assert 'createdAt' in data
        assert 'updatedAt' in data
        
    def test_create_user_duplicate_email(self):
        """
        TC-API-004: POST Create User - Duplicate Email
        """
        duplicate_user = {
            "email": "existinguser@example.com",
            "firstName": "Test",
            "lastName": "User",
            "password": "SecurePass@123"
        }
        
        response = self.client.post("/users", json_data=duplicate_user)
        
        assert response.status_code == 409, f"Expected 409, got {response.status_code}"
        
        error = response.json()['error']
        assert error['code'] == 'EMAIL_ALREADY_EXISTS'
        assert 'field' in error
        assert error['field'] == 'email'
        
    def test_create_user_invalid_email(self):
        """
        TC-API-005: POST Create User - Invalid Email Format
        """
        invalid_user = {
            "email": "invalid-email",
            "firstName": "Test",
            "lastName": "User",
            "password": "SecurePass@123"
        }
        
        response = self.client.post("/users", json_data=invalid_user)
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        error = response.json()['error']
        assert error['code'] == 'VALIDATION_ERROR'
        assert 'details' in error
        assert any(d['field'] == 'email' for d in error['details'])
        
    def test_update_user_success(self):
        """
        TC-API-006: PUT Update User - Success
        """
        user_id = 12345
        update_data = {
            "firstName": "John",
            "lastName": "Updated",
            "phone": "+1111111111"
        }
        
        response = self.client.put(f"/users/{user_id}", json_data=update_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert data['firstName'] == update_data['firstName']
        assert data['lastName'] == update_data['lastName']
        assert data['phone'] == update_data['phone']
        
        # Verify updatedAt timestamp changed
        assert 'updatedAt' in data
        
    def test_delete_user_success(self):
        """
        TC-API-007: DELETE User - Success
        """
        # First create a user to delete
        new_user = {
            "email": f"todelete_{int(time.time())}@example.com",
            "firstName": "Delete",
            "lastName": "Me",
            "password": "SecurePass@123"
        }
        
        create_response = self.client.post("/users", json_data=new_user)
        user_id = create_response.json()['id']
        
        # Now delete the user
        delete_response = self.client.delete(f"/users/{user_id}")
        
        assert delete_response.status_code == 204, f"Expected 204, got {delete_response.status_code}"
        assert len(delete_response.content) == 0, "Response body should be empty"
        
        # Verify user is deleted
        get_response = self.client.get(f"/users/{user_id}")
        assert get_response.status_code == 404, "User should not exist after deletion"


class TestProductAPI:
    """
    Test suite for Product API endpoints
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        self.base_url = "https://api.example.com/v1"
        self.client = APIClient(self.base_url)
        yield
        
    def test_get_products_pagination(self):
        """
        TC-API-008: GET Products List - Pagination
        """
        params = {
            'page': 1,
            'limit': 10,
            'sort': 'name:asc'
        }
        
        response = self.client.get("/products", params=params)
        
        assert response.status_code == 200
        
        data = response.json()
        
        # Verify pagination structure
        assert 'data' in data
        assert 'pagination' in data
        assert 'links' in data
        
        # Verify pagination metadata
        pagination = data['pagination']
        assert pagination['page'] == 1
        assert pagination['limit'] == 10
        assert 'totalPages' in pagination
        assert 'totalItems' in pagination
        assert 'hasNext' in pagination
        assert 'hasPrevious' in pagination
        
        # Verify links
        links = data['links']
        assert 'self' in links
        
        # Verify data
        assert len(data['data']) <= 10, "Should not exceed limit"
        
        # Verify sorting (products should be sorted by name)
        products = data['data']
        if len(products) > 1:
            names = [p['name'] for p in products]
            assert names == sorted(names), "Products not sorted correctly"


class TestAuthenticationAPI:
    """
    Test suite for Authentication API endpoints
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        self.base_url = "https://api.example.com/v1"
        self.client = APIClient(self.base_url)
        yield
        
    def test_login_success(self):
        """
        TC-API-009: POST Login - Success
        """
        credentials = {
            "email": "testuser@example.com",
            "password": "Test@1234"
        }
        
        response = self.client.post("/auth/login", json_data=credentials)
        
        assert response.status_code == 200
        assert response.elapsed.total_seconds() < 1.0
        
        data = response.json()
        assert 'accessToken' in data
        assert 'refreshToken' in data
        assert 'tokenType' in data
        assert data['tokenType'] == 'Bearer'
        assert 'expiresIn' in data
        assert 'user' in data
        
        # Verify token format (should be JWT)
        token = data['accessToken']
        assert token.count('.') == 2, "Invalid JWT format"
        
        # Verify user info
        user = data['user']
        assert user['email'] == credentials['email']
        assert 'password' not in user
        
    def test_login_invalid_credentials(self):
        """
        TC-API-010: POST Login - Invalid Credentials
        """
        invalid_credentials = {
            "email": "testuser@example.com",
            "password": "WrongPassword"
        }
        
        response = self.client.post("/auth/login", json_data=invalid_credentials)
        
        assert response.status_code == 401
        
        error = response.json()['error']
        assert error['code'] == 'INVALID_CREDENTIALS'
        
        # Verify generic error message (security best practice)
        message = error['message'].lower()
        assert 'invalid' in message
        
    def test_unauthorized_access(self):
        """
        TC-API-011: Unauthorized Access - No Token
        """
        # Try to access protected endpoint without token
        response = self.client.get("/users/12345")
        
        assert response.status_code == 401
        assert 'WWW-Authenticate' in response.headers
        
        error = response.json()['error']
        assert error['code'] == 'UNAUTHORIZED'


class TestRateLimiting:
    """
    Test suite for API rate limiting
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        self.base_url = "https://api.example.com/v1"
        self.client = APIClient(self.base_url)
        yield
        
    def test_rate_limit_exceeded(self):
        """
        TC-API-012: Rate Limiting - Too Many Requests
        """
        endpoint = "/products"
        max_requests = 100
        
        # Send requests until rate limit is hit
        responses = []
        for i in range(max_requests + 10):
            response = self.client.get(endpoint)
            responses.append(response)
            
            if response.status_code == 429:
                break
                
            time.sleep(0.1)  # Small delay between requests
        
        # Find first 429 response
        rate_limited_response = next((r for r in responses if r.status_code == 429), None)
        
        if rate_limited_response:
            assert rate_limited_response.status_code == 429
            
            # Verify rate limit headers
            headers = rate_limited_response.headers
            assert 'X-RateLimit-Limit' in headers
            assert 'X-RateLimit-Remaining' in headers
            assert 'X-RateLimit-Reset' in headers
            assert 'Retry-After' in headers
            
            # Verify error response
            error = rate_limited_response.json()['error']
            assert error['code'] == 'RATE_LIMIT_EXCEEDED'
            assert 'retryAfter' in error


class TestAPIPerformance:
    """
    Performance tests for API endpoints
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        self.base_url = "https://api.example.com/v1"
        self.client = APIClient(self.base_url)
        yield
    
    def test_response_time_under_load(self):
        """
        Verify API response times under simulated load
        """
        endpoint = "/products?page=1&limit=10"
        num_requests = 50
        response_times = []
        
        for _ in range(num_requests):
            start_time = time.time()
            response = self.client.get(endpoint)
            end_time = time.time()
            
            response_times.append(end_time - start_time)
            
            assert response.status_code == 200, "Request failed"
        
        # Calculate statistics
        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)
        min_response_time = min(response_times)
        
        print(f"\nPerformance Metrics:")
        print(f"Average Response Time: {avg_response_time:.3f}s")
        print(f"Max Response Time: {max_response_time:.3f}s")
        print(f"Min Response Time: {min_response_time:.3f}s")
        
        # Assertions
        assert avg_response_time < 0.5, f"Average response time {avg_response_time:.3f}s exceeds 500ms"
        assert max_response_time < 2.0, f"Max response time {max_response_time:.3f}s exceeds 2s"


if __name__ == "__main__":
    pytest.main(["-v", "--html=api_test_report.html", "--self-contained-html", __file__])
