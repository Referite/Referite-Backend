    def test_record(self):
        """Test record page"""
        self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/table/tbody/tr[2]/td[5]/a/img').click() # click medals at XPATH
        self.browser.implicitly_wait(30)
        self.assertEqual(self.browser.current_url, "http://localhost:5173/record/1")