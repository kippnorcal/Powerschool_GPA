import os
import time
import traceback
from selenium import webdriver
import bs4
import pandas as pd


browser = webdriver.Firefox()

def login():
    browser.get(f"{os.getenv('PS_URL')}/pw.html") 
    user_field = browser.find_element_by_id('fieldUsername') 
    user_field.send_keys(os.getenv("USER")) 
    pwd_field = browser.find_element_by_id('fieldPassword') 
    pwd_field.send_keys(os.getenv("PWD")) 
    submit_button = browser.find_element_by_id('btnEnter')
    submit_button.click() 
    time.sleep(1) 

def search_bar():       
    search_bar = browser.find_element_by_id('studentSearchInput')
    search_bar.send_keys(os.getenv("SEARCH"))
    search_bar.click() 
    time.sleep(1)

def direct_quickExport(): 
    browser.get(f"{os.getenv('QE_URL')}/importexport/exportstudents.html?dothisfor=selected")
    text_box = browser.find_element_by_id('tt')
    text_box.send_keys(os.getenv("QUICK_EXPORT"))
    submit_btn = browser.find_element_by_id('btnSubmit')
    submit_btn.click()
    time.sleep(1)

def main():
        login() 

        browser.quit() 


if __name__ == "__main__":
    main() 