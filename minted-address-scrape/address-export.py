import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import re

# driver = webdriver.Chrome(executable_path='/path-to-google-chromedriver')
driver = webdriver.Chrome(executable_path='./chromedriver')

# URL for minted addressbook
url = 'https://www.minted.com/addressbook/my-account/finalize/0?it=utility_nav'

driver.get(url)

# Login form
emailElem = driver.find_element_by_name('email')
emailElem.send_keys('your-email-here') # replace with your actual email for login
passwordElem = driver.find_element_by_name('password')
passwordElem.send_keys('your-password-here') # replace with your actual password for login
loginSubmit = driver.find_element_by_class_name('loginButton')
loginSubmit.click()

sleep(5) # to load JS and be nice

driver.get('https://addressbook.minted.com/api/contacts/contacts/print/?')

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
listings = soup.find('main')

address_book = pd.DataFrame()
addressees = listings.find_all('span',{'class':'contact-name'})
address_book['name'] = [name.text.strip() for name in addressees]
addresses = listings.find_all('span',{'class':'contact-address'})
street_details = [''.join(street.text.strip().split('\n')[:-1]).strip() for street in addresses]
address_book['address'] = [' '.join(street.split()) for street in street_details]
city_details = [street.text.strip().split('\n')[-1].strip() for street in addresses]
address_book['locality'] = [_ for _ in city_details]

def pull_state(address):
    try:
        state = re.findall(r'([A-Z]{2}) (\d{5})',address)[0][0]
    except:
        state = ''
    return state

def pull_zip(address):
    try:
        zipcode = re.findall(r'([A-Z]{2}) (\d{5})',address)[0][1]
    except:
        zipcode = ''
    return zipcode

address_book['state'] = address_book['locality'].apply(pull_state)
address_book['zipcode'] = address_book['locality'].apply(pull_zip)
address_book['town'] = address_book['locality'].map(lambda x: x.split(',')[0])

columnsTitles = ['name', 'address', 'town', 'state','zipcode']

address_book = address_book.reindex(columns=columnsTitles)

address_book.to_excel('./minted-addresses.xlsx')

driver.close()