import os
import time
import traceback
from selenium import webdriver
import bs4
import pandas as pdpi
import argparse
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
        browser = create_driver()
        browser.implicitly_wait(10)
        login(browser)
        search_bar(browser)
        direct_quickExport(browser)
    except Exception as e:
        print(e)
    finally:
        close(browser) 

    parser = argparse.ArgumentParser() # Holds all information necessary to parse the command line into data types
    parser.add_argument("--filepath", help="file path of csv to parse") # Information about filepath to file path of csv to parse
    parser.add_argument("--tablename", help="name of the destination sql table") # Information about tablename to name of the destination sql table
    args = parser.parse_args()# Stores information on filepath and tablename when parse_args() is called
    file = args.filepath # Put all filepath information to file 
    table = args.tablename # Put all tablename information to table 

    df = pd.read_csv(file, sep="\t") # Read csv file on args.filepath 
    conn = Connection() # Send commands and receive back information
    conn.insert_into("PS_GPA", df) # Insert coonections to the PS_GPA table 

if __name__ == "__main__":
    main() 