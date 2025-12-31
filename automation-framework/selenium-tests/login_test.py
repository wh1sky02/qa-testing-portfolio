#!/usr/bin/env python3
"""
Selenium Test Suite - Login Functionality
Author: QA Team
Date: 2025-12-31
Framework: Selenium WebDriver with pytest
Pattern: Page Object Model (POM)
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPage:
    """
    Page Object Model for Login Page
    Encapsulates all elements and actions for the login page
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Locators
        self.username_input = (By.ID, "email")
        self.password_input = (By.ID, "password")
        self.login_button = (By.CSS_SELECTOR, "button[type='submit']")
        self.error_message = (By.CLASS_NAME, "error-message")
        self.forgot_password_link = (By.LINK_TEXT, "Forgot Password?")
        self.remember_me_checkbox = (By.ID, "rememberMe")

    def navigate_to_login(self, url):
        """Navigate to the login page"""
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located(self.username_input))

    def enter_username(self, username):
        """Enter username in the username field"""
        element = self.wait.until(
            EC.presence_of_element_located(self.username_input)
        )
        element.clear()
        element.send_keys(username)

    def enter_password(self, password):
        """Enter password in the password field"""
        element = self.wait.until(
            EC.presence_of_element_located(self.password_input)
        )
        element.clear()
        element.send_keys(password)

    def click_login(self):
        """Click the login button"""
        element = self.wait.until(EC.element_to_be_clickable(self.login_button))
        element.click()

    def click_remember_me(self):
        """Click the remember me checkbox"""
        element = self.driver.find_element(*self.remember_me_checkbox)
        element.click()

    def get_error_message(self):
        """Get the error message text"""
        try:
            element = self.wait.until(
                EC.presence_of_element_located(self.error_message)
            )
            return element.text
        except TimeoutException:
            return None

    def is_logged_in(self):
        """Check if user is logged in by checking URL change"""
        try:
            self.wait.until(EC.url_contains("/dashboard"))
            return True
        except TimeoutException:
            return False


class DashboardPage:
    """
    Page Object Model for Dashboard Page
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Locators
        self.user_profile = (By.CLASS_NAME, "user-profile")
        self.logout_button = (By.ID, "logout")

    def get_user_name(self):
        """Get the logged in user's name"""
        element = self.wait.until(
            EC.presence_of_element_located(self.user_profile)
        )
        return element.text

    def logout(self):
        """Click logout button"""
        element = self.wait.until(EC.element_to_be_clickable(self.logout_button))
        element.click()


class TestLoginFunctionality:
    """
    Test suite for login functionality
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup that runs before each test"""
        # Initialize WebDriver
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        # Test data
        self.base_url = "https://qa.example.com"
        self.valid_username = "testuser@example.com"
        self.valid_password = "Test@1234"

        # Initialize page objects
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)

        yield

        # Teardown - runs after each test
        self.driver.quit()

    def test_valid_login(self):
        """
        TC-AUTH-001: Valid User Login
        Verify that user can login with valid credentials
        """
        # Navigate to login page
        self.login_page.navigate_to_login(f"{self.base_url}/login")

        # Enter credentials
        self.login_page.enter_username(self.valid_username)
        self.login_page.enter_password(self.valid_password)

        # Click login
        self.login_page.click_login()

        # Verify login successful
        assert self.login_page.is_logged_in(), "Login failed with valid credentials"
        assert "/dashboard" in self.driver.current_url, "Not redirected to dashboard"

    def test_invalid_username(self):
        """
        TC-AUTH-002: Invalid Username Login Attempt
        Verify that login fails with invalid username
        """
        self.login_page.navigate_to_login(f"{self.base_url}/login")

        self.login_page.enter_username("invalid@example.com")
        self.login_page.enter_password(self.valid_password)
        self.login_page.click_login()

        # Verify error message appears
        error_msg = self.login_page.get_error_message()
        assert error_msg is not None, "No error message displayed"
        assert "invalid" in error_msg.lower(), "Error message not appropriate"

        # Verify still on login page
        assert "/login" in self.driver.current_url, "User was redirected unexpectedly"

    def test_invalid_password(self):
        """
        TC-AUTH-003: Invalid Password Login Attempt
        Verify that login fails with invalid password
        """
        self.login_page.navigate_to_login(f"{self.base_url}/login")

        self.login_page.enter_username(self.valid_username)
        self.login_page.enter_password("WrongPassword@123")
        self.login_page.click_login()

        error_msg = self.login_page.get_error_message()
        assert error_msg is not None, "No error message displayed"
        assert "/login" in self.driver.current_url, "User was redirected unexpectedly"

    def test_empty_username(self):
        """
        TC-AUTH-004: Empty Username Field
        Verify that login fails when username is empty
        """
        self.login_page.navigate_to_login(f"{self.base_url}/login")

        self.login_page.enter_password(self.valid_password)
        self.login_page.click_login()

        error_msg = self.login_page.get_error_message()
        assert error_msg is not None, "No validation error displayed"
        assert "required" in error_msg.lower() or "username" in error_msg.lower()

    def test_empty_password(self):
        """
        TC-AUTH-005: Empty Password Field
        Verify that login fails when password is empty
        """
        self.login_page.navigate_to_login(f"{self.base_url}/login")

        self.login_page.enter_username(self.valid_username)
        self.login_page.click_login()

        error_msg = self.login_page.get_error_message()
        assert error_msg is not None, "No validation error displayed"
        assert "required" in error_msg.lower() or "password" in error_msg.lower()

    def test_sql_injection_username(self):
        """
        TC-AUTH-006: SQL Injection in Username Field
        Verify that application prevents SQL injection
        """
        self.login_page.navigate_to_login(f"{self.base_url}/login")

        sql_injection_string = "admin' OR '1'='1"
        self.login_page.enter_username(sql_injection_string)
        self.login_page.enter_password("anything")
        self.login_page.click_login()

        # Should not be logged in
        assert not self.login_page.is_logged_in(), (
            "SQL injection was successful (SECURITY ISSUE!)"
        )

    def test_xss_attack_username(self):
        """
        TC-AUTH-007: XSS Attack in Username Field
        Verify that application prevents XSS attacks
        """
        self.login_page.navigate_to_login(f"{self.base_url}/login")

        xss_string = "<script>alert('XSS')</script>"
        self.login_page.enter_username(xss_string)
        self.login_page.enter_password(self.valid_password)
        self.login_page.click_login()

        # Verify no alert popup (script not executed)
        assert not self.login_page.is_logged_in(), "XSS input allowed login"

    def test_remember_me_functionality(self):
        """
        TC-AUTH-008: Remember Me Functionality
        Verify that remember me checkbox works
        """
        self.login_page.navigate_to_login(f"{self.base_url}/login")

        self.login_page.enter_username(self.valid_username)
        self.login_page.enter_password(self.valid_password)
        self.login_page.click_remember_me()
        self.login_page.click_login()

        assert self.login_page.is_logged_in(), "Login failed"

        # Check if persistent cookie exists
        cookies = self.driver.get_cookies()
        remember_cookie = [
            c for c in cookies if "remember" in c.get("name", "").lower()
        ]
        assert len(remember_cookie) > 0, "Remember me cookie not set"

    def test_logout_functionality(self):
        """
        TC-AUTH-010: Logout Functionality
        Verify that user can logout successfully
        """
        # First login
        self.login_page.navigate_to_login(f"{self.base_url}/login")
        self.login_page.enter_username(self.valid_username)
        self.login_page.enter_password(self.valid_password)
        self.login_page.click_login()

        assert self.login_page.is_logged_in(), "Login failed"

        # Now logout
        self.dashboard_page.logout()

        # Verify redirected to login page
        WebDriverWait(self.driver, 10).until(EC.url_contains("/login"))
        assert (
            "/login" in self.driver.current_url
        ), "Not redirected to login after logout"

    @pytest.mark.parametrize(
        "username,password",
        [
            ("", ""),
            ("test", "short"),
            ("invalid-email", "Test@1234"),
            ("test@example.com", " "),
        ],
    )
    def test_multiple_invalid_inputs(self, username, password):
        """
        Data-driven test for multiple invalid input combinations
        """
        self.login_page.navigate_to_login(f"{self.base_url}/login")

        if username:
            self.login_page.enter_username(username)
        if password:
            self.login_page.enter_password(password)

        self.login_page.click_login()

        # Should not be logged in
        assert not self.login_page.is_logged_in(), (
            f"Logged in with invalid inputs: {username}/{password}"
        )


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main(["-v", "--html=report.html", __file__])
