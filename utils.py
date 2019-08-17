from selenium import webdriver
import time

def scroll_down(driver):
    '''Scroll down the dynamically loading page until the end of friend list is loaded.'''
    while True:
        if driver.find_elements_by_css_selector('div.mbm') == []:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
        else:
            break

def fb_login(driver,email,password):
    '''Automate Facebook log-in process.'''
    driver.get('https://www.facebook.com/')
    email_input = driver.find_element_by_id('email')
    password_input = driver.find_element_by_id('pass')
    button = driver.find_element_by_id('loginbutton')
    email_input.send_keys(email)
    password_input.send_keys(password)
    button.click()
