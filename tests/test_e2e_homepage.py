from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import unittest
from tests.utils import browser_login

class HomepageE2ELocalTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = Chrome()
        browser_login(self.browser, "referee", "referee123")

    def test_redirect_to_record_page(self):
        """Test redirect to record page"""
        self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/table/tbody/tr[2]/td[5]/a/img').click() # click medals at XPATH
        self.browser.implicitly_wait(30)
        self.assertEqual(self.browser.current_url, "http://localhost:5173/record/1")

    def test_redirect_to_record_page_without_login(self):
        """Test redirect to record page without_login"""
        self.browser.get("http://localhost:5173/record/1")
        self.browser.implicitly_wait(30)
        self.assertEqual(self.browser.current_url, "http://localhost:5173/login")

    def test_redirect_of_record_medal_workflow(self):
        """Test redirect of record medal workflow and record medal"""
        self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/table/tbody/tr[5]/td[14]/a/img').click() # click medals at XPATH
        self.browser.implicitly_wait(30)
        self.assertEqual(self.browser.current_url, "http://localhost:5173/record/4")
        self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div[1]/select').click()
        self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div[1]/select/option[2]').click()
        self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div').click() # 1st select country
        self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div[2]').click() # select Azerbaijan
        self.browser.find_element(By.XPATH, '//*[@id="input1-1"]').send_keys("1") # add gold medal to 1
        self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div').click() # 2nd select country
        self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[3]').click() # select latvia
        self.browser.find_element(By.XPATH, '//*[@id="input2-2"]').send_keys("1") # add silver medal to 1
        self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div/div[3]/div/div/div').click() # 3rd select country
        self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div[6]').click() # select nigeria
        self.browser.find_element(By.XPATH, '//*[@id="input3-3"]').send_keys("1") # add bronze medal to 1
        self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/input[2]').click() # click record medal button
        self.browser.implicitly_wait(30)
        self.browser.find_element(By.XPATH, '/html/body/div[2]/div/div[6]/button[1]').click() # click confirm button
        self.assertEqual(self.browser.current_url, "http://localhost:5173/record/4")