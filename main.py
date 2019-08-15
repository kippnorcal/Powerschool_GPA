import os
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from db import Connection
import data_map
import logging
from timer import elapsed
from mailer import notify
import sys

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S%p",
)


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
    user_field = browser.find_element_by_id("fieldUsername")
    user_field.send_keys(os.getenv("PS_USER"))
    pwd_field = browser.find_element_by_id("fieldPassword")
    pwd_field.send_keys(os.getenv("PS_PWD"))
    submit_button = browser.find_element_by_id("btnEnter")
    submit_button.click()
    time.sleep(5)
    logging.info("logged in successfully")


def search_bar(browser):
    search_bar = browser.find_element_by_id("studentSearchInput")
    search_bar.clear()
    search_bar.send_keys(os.getenv("SEARCH"))
    search_button = browser.find_element_by_id("searchButton")
    search_button.click()
    time.sleep(5)
    logging.info("entered search query successfully")


def enter_text(element, browser, line):
    element.send_keys(line)
    element.send_keys(Keys.ENTER)


@elapsed
def direct_quickExport(browser):
    QE_URL = (
        f"{os.getenv('PS_URL')}/importexport/exportstudents.html?dothisfor=selected"
    )
    browser.get(QE_URL)

    export_query = list(data_map.columns.keys())
    text_box = browser.find_element_by_id("tt")
    text_box.clear()
    for line in export_query:
        enter_text(text_box, browser, line)

    logging.info("entered quick export query successfully")
    time.sleep(5)
    submit_btn = browser.find_element_by_id("btnSubmit")
    submit_btn.click()
    while os.path.exists("student.export.text.part"):
        time.sleep(5)
    logging.info("finished downloading file")


def close(browser):
    browser.close()


def main():
    try:
        browser = create_driver()
        browser.implicitly_wait(10)
        login(browser)
        search_bar(browser)
        direct_quickExport(browser)
        os.rename("student.export.text", "student_export.txt")
        df = pd.read_csv("student_export.txt", sep="\t")
        column_names = data_map.columns
        df.rename(columns=column_names, inplace=True)
        df_len = len(df.index)
        conn = Connection()
        conn.insert_into("PS_GPA", df)
        logging.info(f"Loaded {df_len} students into PS_GPA table")
        with open("app.log") as f:
            log_info = f.read()
        notify(success_message=log_info)
    except Exception as e:
        html_page = browser.page_source
        logging.info(html_page)
        logging.error(e)
        stack_trace = traceback.format_exc()
        with open("app.log") as f:
            log_info = f.read()
        stack_trace = f"{stack_trace}\n{log_info}"
        notify(error=True, error_message=stack_trace)
    finally:
        close(browser)


if __name__ == "__main__":
    main()
