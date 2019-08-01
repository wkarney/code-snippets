from seleniumrequests import Chrome
import os
from time import sleep
import pandas as pd

driver = Chrome()

# URL for minted addressbook
url = 'https://www.minted.com/login'

# Set your minted.com email and password as the env vars:
# minted_email and minted_password
try:
    minted_email = os.environ['minted_email']
except KeyError:
    minted_email = input("Enter your minted.com email address:")
try:
    minted_password = os.environ['minted_password']
except KeyError:
    minted_password = input("Enter your minted.com password:")

driver.get(url)

# Selenium deals with lgin form
emailElem = driver.find_element_by_name('email')
emailElem.send_keys(minted_email)
passwordElem = driver.find_element_by_name('password')
passwordElem.send_keys(minted_password) 
loginSubmit = driver.find_element_by_class_name('loginButton')
loginSubmit.click()

sleep(5) # to load JS and be nice

# Request address book contents as json
response = driver.request('GET','https://addressbook.minted.com/api/contacts/contacts/?format=json')
listings = response.json()

# Create dataframe to hold addresses
address_book = pd.DataFrame(listings)

# Export to excel
address_book.to_excel('./minted-addresses-api.xlsx')

# Close selenium webdriver
driver.close()