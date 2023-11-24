from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import unittest
from tests.utils import browser_login

class LoginE2ELocalTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = Chrome()
    def test_login_valid_username_password_and_logout(self):
        """Test login with valid username and password, then logout"""
        browser_login(self.browser, "referee", "referee123")
        self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[3]/a/img').click() # logout button
        self.browser.implicitly_wait(30)
        self.browser.find_element(By.XPATH, '//*[@id="root"]/div/img').is_displayed() # check if referite icon is shown on login page

    def test_login_valid_username_invalid_password(self):
        """Test login with valid username and invalid password"""
        browser_login(self.browser, "referee", "referee")
        self.browser.implicitly_wait(30)
        self.browser.find_element(By.XPATH, '//*[@id="swal2-html-container"]').is_displayed() # check if Pop-up text Wrong user id or password is shown.
        self.assertEqual(self.browser.current_url, "http://localhost:5173/login")

    def test_login_invalid_username_valid_password(self):
        """Test login with invalid username and valid password"""
        browser_login(self.browser, "tester", "referee123")
        self.browser.implicitly_wait(30)
        self.assertEqual(self.browser.current_url, "http://localhost:5173/login")

    def test_login_invalid_username_invalid_password(self):
        """Test login with invalid username and invalid password"""
        browser_login(self.browser, "tester", "referee")
        self.browser.implicitly_wait(30)
        self.assertEqual(self.browser.current_url, "http://localhost:5173/login")

    def test_login_empty_username_empty_password(self):
        """Test login with empty username and empty password"""
        browser_login(self.browser, "", "")
        self.browser.implicitly_wait(30)
        self.assertEqual(self.browser.current_url, "http://localhost:5173/login")
        

    