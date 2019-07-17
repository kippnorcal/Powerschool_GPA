import os
import time
import traceback
from selenium import webdriver
import bs4
import pandas as pdpi

browser = webdriver.Firefox()

def login():
    PS_URL = f"{os.getenv('PS_URL')}/pw.html"
    browser.get(PS_URL) 
    user_field = browser.find_element_by_id('fieldUsername') 
    user_field.send_keys(os.getenv("USER")) 
    pwd_field = browser.find_element_by_id('fieldPassword') 
    pwd_field.send_keys(os.getenv("PWD")) 
    submit_button = browser.find_element_by_id('btnEnter')
    submit_button.click() 
    time.sleep(5) 

def search_bar():       
    search_bar = browser.find_element_by_id('studentSearchInput')
    search_bar.send_keys(os.getenv("SEARCH"))
    search_button = browser.find_element_by_id('searchButton') 
    search_button.click() 
    time.sleep(5)

def direct_quickExport(): 
    QE_URL = f"{os.getenv('PS_URL')}/importexport/exportstudents.html?dothisfor=selected"
    browser.get(QE_URL)
    #text_box = browser.find_element_by_id('tt')
    #text_box.send_keys(os.getenv("QUICK_EXPORT"))
    time.sleep(5)
    submit_btn = browser.find_element_by_id('btnSubmit')
    submit_btn.click()
    time.sleep(5)

def main():
        try:
            login()
            search_bar()
            direct_quickExport()
            
        except Exception as e:
            print(e)
        finally:
            browser.quit() 

if __name__ == "__main__":
        main() 