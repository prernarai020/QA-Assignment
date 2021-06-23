import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class JabaTalksSignup(unittest.TestCase):
    # Declare the global const variables
    Base_Url = "http://jt-dev.azurewebsites.net/#/SignUp"

    # Testing it only in Chrome Browser
    Chrome_Web_Driver_Path = "./drivers/Chrome/chromedriver"

    def setUp(self):
        # Initializing the Chrome Web Driver
        self.driver = webdriver.Chrome(executable_path=self.Chrome_Web_Driver_Path)

        # Setting the Browser to Maximum Screen Size View
        self.driver.maximize_window()

    def test_a_loadSignupPage(self):
        """User should be able to load the page"""
        self.driver.get(self.Base_Url)
        self.assertIn("Jabatalks", self.driver.title)

    def test_b_languageAvailable(self):
        """User should be able to see English and Dutch in Language drop down"""
        self.driver.get(self.Base_Url)

        self.driver.find_element(By.ID, "language").click()
        time.sleep(2)

        languageItems = self.driver.find_elements(By.CLASS_NAME, "ui-select-choices-row-inner")
        languageCount = 0
        for item in languageItems:
            if item.text == "English" or item.text == "Dutch":
                languageCount += 1

        self.assertTrue(languageCount == 2)  # English and Dutch is present

    def test_c_fillTheSignupFormAndSubmit(self):
        """User should be able to fill the form and submit."""
        self.driver.get(self.Base_Url)
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//*[@id='name']").send_keys("Prerna Rai")
        self.driver.find_element(By.XPATH, "//*[@id='orgName']").send_keys("Prerna Rai")
        self.driver.find_element(By.XPATH, "//*[@id='singUpEmail']").send_keys("testmeti01@gmail.com")
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div/div[3]/div/section/div[1]/form/fieldset/div[4]/label/span").click()
        self.driver.find_element(By.XPATH,
                                 "//*[@id='content']/div/div[3]/div/section/div[1]/form/fieldset/div[5]/button").click()
        time.sleep(10)
        emailSentAlert = self.driver.find_element(By.CLASS_NAME, "alert-danger")
        self.assertTrue(emailSentAlert.text == "A welcome email has been sent. Please check your email.")

    def test_d_emailReceivedVerification(self):
        """Checking the email received as verification in Gmail"""
        self.driver.get("https://mail.google.com/mail")

        self.driver.find_element(By.XPATH, "//*[@id='identifierId']").send_keys("testmeti01@gmail.com")
        self.driver.find_element(By.XPATH, "//*[@id='identifierNext']/div/button/span").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//*[@id='password']/div[1]/div/div[1]/input").send_keys("8800312325@1")
        self.driver.find_element(By.XPATH, "//*[@id='passwordNext']/div/button/span").click()
        time.sleep(10)
        emailReceived = False
        spanElement = self.driver.find_elements_by_tag_name("span")
        for item in spanElement:
            if item.get_attribute('email') == 'donotreply-dev@jabatalks.com':
                emailReceived = True
        self.assertTrue(emailReceived == True)

    def tearDown(self):
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
