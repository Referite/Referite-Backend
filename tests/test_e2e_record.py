from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import unittest
from tests.utils import browser_login
from db import sport_schedule_connection

class RecordPageE2ELocalTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = Chrome()
        browser_login(self.browser, "referee", "referee123")

    def test_default_record_medal_workflow(self):
        """Test record medal workflow of default standard olympics"""
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
        # change status back to trophy
        query = {"sport.sport_id": 4, "sport.sport_type.type_id": 39, "sport.sport_type.status": "RECORDED"}
        update = {"$set": {"sport.$.sport_type.$[typeElem].status": "TROPHY"}}
        sport_schedule_connection.update_one(query, update, array_filters=[{"typeElem.type_id": 39, "typeElem.status": "RECORDED"}])

    def test_invalid_medal_record_workflow(self):
        """Test invalid medal record workflow"""
        pass

    def test_special_case_medal_record_workflow(self):
        """Test special case medal record workflow"""
        pass

    def test_impossible_medal_quantity_record_workflow(self):
        """Test impossible medal quantity record workflow"""
        pass

    def test_invalid_countries_selection_of_record_workflow(self):
        """Test invalid countries selection"""
        pass

