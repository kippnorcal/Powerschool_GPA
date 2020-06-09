import os
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import data_map
from contextlib import AbstractContextManager


class BrowserSession(AbstractContextManager):
    def __init__(self):
        """Initialize session with needed variables"""
        host = os.getenv("PS_URL")
        self.LOGIN_URL = f"{host}/pw.html"
        self.QE_URL = f"{host}/importexport/exportstudents.html?dothisfor=selected"
        self.PS_USER = os.getenv("PS_USER")
        self.PS_PWD = os.getenv("PS_PWD")
        self.export_query = data_map.keys
        self.browser = self.create_driver()

    def __enter__(self):
        """Creates a context manager which starts the browser session"""
        self.browser.implicitly_wait(10)
        self.login()
        return self

    def __exit__(self, *exc_details):
        """Exit the context manger and close the browser session"""
        self.browser.close()

    def create_driver(self):
        """Set configuration options for browser session"""
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.dir", os.getcwd())
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference(
            "browser.helperApps.neverAsk.saveToDisk", "text/ps-export"
        )
        profile.set_preference("browser.download.usedownloaddir", False)
        return webdriver.Firefox(firefox_profile=profile)

    def login(self):
        """Log in to PowerSchool with provided credentials"""
        self.browser.get(self.LOGIN_URL)
        user_field = self.browser.find_element_by_id("fieldUsername")
        user_field.send_keys(self.PS_USER)
        pwd_field = self.browser.find_element_by_id("fieldPassword")
        pwd_field.send_keys(self.PS_PWD)
        submit_button = self.browser.find_element_by_id("btnEnter")
        submit_button.click()
        time.sleep(5)
        logging.info("logged in successfully")

    def search_students(self):
        """Use the PowerSchool student search to find the specified student types"""
        search_bar = WebDriverWait(self.browser, 30).until(
            EC.element_to_be_clickable((By.ID, "studentSearchInput"))
        )
        self.browser.save_screenshot("1-studentSearchInput.png")
        search_bar.clear()
        search_term = os.getenv("SEARCH")
        search_bar.send_keys(search_term)
        search_button = self.browser.find_element_by_id("searchButton")
        self.browser.save_screenshot("2-searchButton.png")
        search_button.click()
        time.sleep(5)
        logging.info("entered search query successfully")

    def _enter_text(self, element, line):
        """Type text into a field and press enter"""
        element.send_keys(line)
        element.send_keys(Keys.ENTER)

    def _quick_export_query(self, element):
        """Add a quick export query text to a browser element"""
        element.clear()
        for line in self.export_query:
            self._enter_text(element, line)

    def _wait_on_filestream(self):
        """Wait for the file to finish downloading"""
        time.sleep(20)
        while os.path.exists("student.export.text.part"):
            time.sleep(5)

    def quick_export_gpa(self):
        """Main function used to export the GPA data from PowerSchool to a file"""
        self.browser.get(self.QE_URL)
        text_box = self.browser.find_element_by_id("tt")
        self.browser.save_screenshot("3-tt.png")
        self._quick_export_query(text_box)
        time.sleep(5)
        submit_btn = self.browser.find_element_by_id("btnSubmit")
        submit_btn.click()
        self.browser.save_screenshot("4-btnSubmit.png")
        self._wait_on_filestream()
        self.browser.save_screenshot("5-wait_on_filestream.png")
        logging.info("finished downloading file")
