import os
import time
import traceback
from selenium import webdriver
import bs4
import pandas as pd


browser = webdriver.Firefox() # Defining Firefox as a browser 

def login():
    browser.get(f"{os.getenv('PS_URL')}/pw.html") # Directing browser to specified URL
    user_field = browser.find_element_by_id('fieldUsername') # Finding web element for Username 
    user_field.send_keys(os.getenv("USER")) # Send key strokes to fill in the web element for Username
    pwd_field = browser.find_element_by_id('fieldPassword') # Finding web element for Password
    pwd_field.send_keys(os.getenv("PWD")) # Send key strokes to fill in the web element for Password
    submit_button = browser.find_element_by_id('btnEnter') # Finding the Submit Button (Enter button)
    submit_button.click() # Clicking the submit button 
    time.sleep(1) # Button pause for 1 second

def search_bar():       
    search_bar = browser.find_element_by_id('studentSearchInput')
    search_bar.send_keys(os.getenv("SEARCH"))
    search_bar.click() 
    time.sleep(1)

def direct_quickExport(): 
    browser.get(f"{os.getenv('QE_URL')}/importexport/exportstudents.html?dothisfor=selected"))
    text_box = browser.find_element_by_id('tt')
    text_box.send_keys(os.getenv("QUICK_EXPORT"))
    submit_btn = browser.find_element_by_id('btnSubmit')
    submit_btn.click()
    time.sleep(1)

def main(): # Main function 
        login() # Call the Login function 

        browser.quit() 


if __name__ == "__main__":
    main() # Calling the main function 