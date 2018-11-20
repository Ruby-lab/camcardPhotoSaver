#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
import os

def get_image(driver, image_url, save_to_dir):
    '''save image file to specific directory from URL.

    driver:webdriver
    image_url:image url to save
    save_to_dir: directory for saving image
    '''

    mainTab = driver.current_window_handle
    driver.execute_script('window.open("{}", "_blank");'.format(image_url))

    # Get new tab ID
    new_window = [window for window in driver.window_handles if window != mainTab][0]

    # Switch to new window/tab
    driver.switch_to.window(new_window)

    # Get the dimensions of the browser and image.
    orig_h = driver.execute_script("return window.outerHeight")
    orig_w = driver.execute_script("return window.outerWidth")
    margin_h = orig_h - driver.execute_script("return window.innerHeight")
    margin_w = orig_w - driver.execute_script("return window.innerWidth")
    new_h = driver.execute_script('return document.getElementsByTagName("img")[0].height')
    new_w = driver.execute_script('return document.getElementsByTagName("img")[0].width')

    # Resize the browser window as image size.
    driver.set_window_size(new_w + margin_w, new_h + margin_h)

    # Get the image by taking a screenshot.
    img_val = driver.get_screenshot_as_png()

    # Set the window size back to what it was.
    driver.set_window_size(orig_w, orig_h)

    # Save the image
    parsed_url = urlparse(image_url)
    fileName = os.path.basename(parsed_url.path)
    f = open(save_to_dir+fileName, 'wb')
    f.write(img_val)
    f.close()

    # Close new tab
    driver.close()
    # Focus back
    driver.switch_to.window(mainTab)


# Init chrome driver and login to camcard
driver = webdriver.Chrome('./libs/chromedriver')
driver\
    .get('https://www.camcard.com/user/login?l=ja-jp')

driver\
    .find_element_by_xpath('//*[(@id = "input_email")]')\
    .send_keys('ID')
driver\
    .find_element_by_xpath('//*[(@id = "input_pwd")]')\
    .send_keys('PASSWORD')
driver\
    .find_element_by_xpath('//*[(@id = "btn_login")]')\
    .click()

next_page = True
pic_urls = []
page_count = 1
timeout = 10

while next_page == True:

    # Wait for loading page
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'card_front_pic'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timeout to load page.")

    # Get every card image in page
    page_count += 1
    card_pics = driver.find_elements_by_class_name('card_front_pic')
    for card_pic_el in card_pics:
        print('Class: '+driver.find_element_by_class_name('next_page').find_element_by_tag_name('span').get_attribute('class'))
        try:
            imgEl = card_pic_el.find_element_by_tag_name('img')
            pic_urls.append(imgEl.get_attribute('data-src'))
        except NoSuchElementException:
            continue
    #end for

    # Check next page existence
    if driver.find_element_by_class_name('next_page').get_attribute('class').find('disable') < 0:
        # If next page exist, move to next page.
        next_page = True
        driver.find_element_by_class_name('next_page').click()
    else :
        next_page = False
        print('End!')
        break
#end while

print('URL Count: ' + str(len(pic_urls)))

# Get image from URLs
for pic_url in pic_urls:
    get_image(driver, pic_url, 'SAVE TO DIRECTORY')
