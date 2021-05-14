# USING SELENIUM
# Instagram Automation which can perform following tasks:
# 1. Logging in Instagram
# 2. Handling the pop-ups
# 3. Searching for a hashtag
# 4. Scrolling the feed of the hashtag
# 5. Downloading the resulted images to our desktop

import os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import wget
import time

# Link to chromedriver
url = "C:/Users/91707/Downloads/chromedriver_win32/chromedriver.exe"

# Web Driver is a tool that connects between your code and your web browser
# and essentially allows the automation process.
driver = webdriver.Chrome(url)

# To start the website
driver.get("http://www.instagram.com/")

#  WebDriverWait() is literally asking your webdriver to wait before
#  it executes the command specified inside .until().
# WebDriverWait accepts 2 arguments:
# driver: represents the webdriver object we initialized earlier (driver)
# timeout: represents the number of seconds that would pass before a Timeout Exception is triggered (10).
# An integer data type is expected (int).

# EC.element_to_be_clickable() has 2 parts:
# EC is specifying a condition for the wait.
# Simply speaking, it asks our software "don't run the command until my condition is met!"
# element_to_be_clickable() is one of the available methods you can choose as condition.
# It not only waits until the element is loaded on the page,
# but also waits until the browser allows clicking on that element.
# These methods take-in the element you'd like to select as an argument.

# By.CSS_SELECTOR also has 2 components,
# it represents the means you'd use to locate the desired element on the page.
# Selecting by CSS selector is fast, convenient and very popular.
# You can target all the attributes of a given DOM element and even specify their properties.

# "input[name='password']" represents the element we are selecting in a string.
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name = 'username']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name = 'password']")))

# To clear the input fields
username.clear()
password.clear()

# Entering Login Credentials of Instagram
username.send_keys("enter_d_username")
password.send_keys("enter_d_password")

# Clicking the submit button to get log in
log_in = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

# XPATH helps us to search within the text of elements or within any of their attributes,
# and allows us not to be to be specific with our search terms.
pop_up = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]"))).click()
pop_up1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]"))).click()

# To select the Searchbox and clearing it and
searchBox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
searchBox.clear()
keyword = '#dog'
searchBox.send_keys(keyword)

# Moving to the link after searching the hashtag
driver.get("https://www.instagram.com/explore/tags/" + keyword[1:] + "/")

# Scrolling to the bottom of the page
# n_scrolls represents the number of times our browser will scroll to the bottom of the page
# (document.body.scrollHeight) and we will run this with the help of Javascript

# window.scrollTo() takes in 2 parameters:
# the first represents the y value to begin scrolling from (0 in our case, top of the page)
# second parameter represents the y value where the scrolling ends
# (in our case document.body.scrollHeight which represents the bottom of the page).
n_scrolls = 3
for i in range(1, n_scrolls):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

# Extract Instagram Thumbnails
# images = driver.find_elements_by_tag_name("img")
# images = [image.get_attribute('src') for image in images]
# We will also slice-off the last 2 images consist of your profile picture and Instagram’s logo.
# images = images[:-2]

# Extract Instagram Images
anchors = driver.find_elements_by_tag_name('a')
anchors = [a.get_attribute('href') for a in anchors]
anchors = [a for a in anchors if str(a).startswith("https://www.instagram.com/p/")]
print('Found ' + str(len(anchors)) + ' links to images')

# we will navigate to each of these anchors and extract the second image element of each page,
# which represents the full-size image (the first image in the DOM is always our profile picture)
images = []
for a in anchors:
    driver.get(a)
    img = driver.find_elements_by_tag_name('img')
    img = [i.get_attribute('src') for i in img]
    images.append(1)

# creating a directory to download the images
path = os.getcwd()
path = os.path.join(path, keyword[1:] + "s")
os.mkdir(path)
print(path)
counter = 0
for image in images:
    save_as = os.path.join(path + keyword[1:] + str(counter) + ".jpg")
    wget.download(image, save_as)
    counter += 1
