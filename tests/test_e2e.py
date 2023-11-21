from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import unittest

class E2ELocalTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = Chrome()
        self.browser.get('http://localhost:5173/')

    def login(self):
        self.browser.find_element(By.ID, "username").send_keys("referee")
        self.browser.find_element(By.ID, "password").send_keys("referee123")
        self.browser.find_element(By.ID, "login").click()
        self.assertEqual(self.browser.current_url, "http://localhost:5173/homepage")