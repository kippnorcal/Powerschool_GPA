import os
import time
import traceback
from selenium import webdriver
import bs4
import pandas as pdpi

def create_driver():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", CWD)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    profile.set_preference("pdfjs.disabled", True)
    # options = Options()
    # options.headless = True
    # return webdriver.Firefox(options=options, firefox_profile=profile)
    return webdriver.Firefox(firefox_profile=profile)

def login(browser):
    PS_URL = f"{os.getenv('PS_URL')}/pw.html"
    browser.get(PS_URL) 
    user_field = browser.find_element_by_id('fieldUsername') 
    user_field.send_keys(os.getenv("USER")) 
    pwd_field = browser.find_element_by_id('fieldPassword') 
    pwd_field.send_keys(os.getenv("PWD")) 
    submit_button = browser.find_element_by_id('btnEnter')
    submit_button.click() 
    time.sleep(5) 

def search_bar(browser):       
    search_bar = browser.find_element_by_id('studentSearchInput')
    search_bar.send_keys(os.getenv("SEARCH"))
    search_button = browser.find_element_by_id('searchButton') 
    search_button.click() 
    time.sleep(5)

def direct_quickExport(browser): 
    QE_URL = f"{os.getenv('PS_URL')}/importexport/exportstudents.html?dothisfor=selected"
    browser.get(QE_URL)
    #text_box = browser.find_element_by_id('tt')
    #text_box.send_keys(os.getenv("QUICK_EXPORT"))
    time.sleep(5)
    submit_btn = browser.find_element_by_id('btnSubmit')
    submit_btn.click()
    time.sleep(5)

def close(browser):
    browser.close()

def main():
        try:
            browser = create_driver()
            browser.implicitly_wait(10)
            login(browser)
            search_bar(browser)
            direct_quickExport(browser)

        except Exception as e:
            print(e)
        finally:
            close(browser) 

if __name__ == "__main__":
        main() 