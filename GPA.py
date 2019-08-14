import os
import time
import traceback
from selenium import webdriver
import pandas as pd
from db import Connection


def create_driver():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", os.getcwd())
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/ps-export")
    profile.set_preference("browser.download.usedownloaddir", False)
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
    time.sleep(120)

def close(browser):
    browser.close()

def main():
    try:
        # browser = create_driver()
        # browser.implicitly_wait(10)
        # login(browser)
        # search_bar(browser)
        # direct_quickExport(browser)
        df = pd.read_csv('student_export.txt', sep="\t") # Read csv file on args.filepath
        data_map = {
            'student_number':'student_number',
            'lastfirst':'lastfirst',
            'grade_level':'grade_level',
            '[39]name':'School',
            '^(*gpa method="KSJC Simple Transcripts Only" format=##0.00)':'Cumulative_GPA',
            '^(*gpa method="Weighted" format=##0.00 grade="9,10,11,12")':'Cumulative_Weighted_GPA',
        }
        df.rename(columns=data_map, inplace=True)
        conn = Connection() # Send commands and receive back information
        conn.insert_into("PS_GPA", df) # Insert coonections to the PS_GPA table
        print("success")
    except Exception as e:
        print(e)
    # finally:
    #     close(browser)


if __name__ == "__main__":
    main()
