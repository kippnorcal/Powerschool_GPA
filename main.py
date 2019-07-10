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
    search_bar = browser.find_element_by_id('searchBar')
    #search_bar.send_keys(
    search_bar.send_keys('grade_level > 8')



'''
def html_to_df(html, school, grade): # Creating a virtual data table from the website table 
    df_list = pd.read_html(html, header=0) # Importing a list  
    df = df_list[0] # Retrun the first value inside the dataframe list 
    df['school'] = school # Passing variable school into the dataframe
    df['grade'] = grade # Passing variable grade into the dataframe 
    return df # Return dataframe 
''' 

def select_school(school_name): # Selecting the School through school_name parameter 
    school_link = browser.find_element_by_id('schoolContext') # Finding the web element for school button (elements matching id attribute)
    school_link.click() # Send key strokes to fill in the web element for the school button 
    time.sleep(1) # Button pause for 1 second

    school_select = browser.find_element_by_name('Schoolid') # Finding the web element for school id (elements matching name)
    options = school_select.find_elements_by_tag_name('option') # Finding the web element for option (elements matching tag name)
    for option in options: # Using a for loop to loop through every option in options 
        if option.text == school_name: # If the text option equals to the school name then click that text option 
            option.click()
            break # Stops the execution of the loop and starts executing the next line of the code after the block
    time.sleep(1) # Button pause for 1 second


def report_options(grade): # Report options function through the grade parameter 
    grade_level = browser.find_element_by_name('gradelevel') # Finding web element for Grade Level 
    for option in grade_level.find_elements_by_tag_name('option'): # Using for loop for every option Within the Option button 
        if option.text == str(grade): # If the text option equals to a grade in string type then click that text option 
            option.click()
            break # Stops the execution of the loop and starts executing the next line of the code after the block

    # Set Ranking Method to KKC Weighted - NEW
    rank_method = browser.find_element_by_name('rankmethod') # Finding web element for ranking method 
    for option in rank_method.find_elements_by_tag_name('option'): # Using for loop for every option Within the Option button 
        if option.text == 'KKC Weighted - NEW': # If the text option equals to the KKC Weighted strng then click that text button
            option.click()
            break # Stops the execution of the loop and starts executing the next line of the code after the block

    # Show only 3.0+ GPAs
    min_gpa = browser.find_element_by_name('mingpa') # Find the web element for min gpa 
    min_gpa.send_keys("3.0") # Send keys in min gpa to "3.0"

    report_submit = browser.find_element_by_id('btnSubmit') # Finding web element for Submit button 
    report_submit.click() # Click on the Submit Button 


def class_ranking_report(): # Class Ranking Report function 
    report_url = f"{os.getenv('PS_URL')}/reports/classranking1.html" # Returning the value of the environment variable
    browser.get(report_url) # Go to the browser (Firefox) to get the reports url
    report_options(10) # Report options value 10 
    time.sleep(1) # Button pause for 1 second


def parse_table(): # Parse table function  
    table = browser.find_element_by_id("content-main") # Finding the web element for the main content 
    return table.find_element_by_tag_name("table").get_attribute('outerHTML') # Returning the main content web element for table and to get the outer HTML 


def main(): # Main function 
    try: # Correcting assertion errors to ensure that the grades dataframe consists of 4 schools
        grades_df = pd.DataFrame() 
        schools = [                       
            'KIPP King Collegiate',
            'KIPP San Jose Collegiate',
            'KIPP SF College Prepatory',
            'KIPP Navigate College Prep',
        ] # A list of schools named schools 

        login() # Call the Login function 

        for school in schools: # For loop for every school in schools 
            select_school(school) # Select school in select school 
            for grade in range(9,13): # Nested for loop for grades from 9 to 12 in school, do the following inside for loop and then repeat with the next school in the list untill all schools in the list of schools applied
                class_ranking_report() # Calling the class ranking report function 
                gpa_table = parse_table() # Making the parse table function to a variable called gpa table 
                df = html_to_df(gpa_table, school, grade) # Making the html_to_df function to a variable calle df 
                grades_df = grades_df.append(df, ignore_index=True) # Appending the dataframe of the html_to_df into the grades dataframe 

        grades_df.to_csv("class_ranking.csv", index=False) # Turn grades dataframe to class_ranking.csv URL

    except Exception as e: # try and except, expecting e to continue the program 
        print(e) # Print e 
        stack_trace = traceback.format_exc() # Returns a string called stack_trace 
        print(stack_trace) # Print the traceback (string type)

    finally: # End the code with quitting the browser (Firefox)
        browser.quit() 


if __name__ == "__main__":
    main() # Calling the main function 
