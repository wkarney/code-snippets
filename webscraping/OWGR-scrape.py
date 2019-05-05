# Package imports
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Defining the url
url = 'http://www.owgr.com/en/Ranking.aspx?pageNo=1&pageSize=300&country=All'

# Make HTTP request to URL
res = requests.get(url)

# Generate BeautifulSoup object
soup = BeautifulSoup(res.content, 'lxml')

# Find the first table element on the page
table = soup.find('table')

# Instantiate a blank list and a counter for ranking position
rankings = []
curr_rank = 1

# Iterate over all rows in the table, starting with the 2nd row
for rows in table.find_all('tr')[1:]:
    # Instatiate dictionary for each row
    player = {}
    
    # Assign the name, country, and rank for each player/row of the table
    player['name'] = rows.find('td',{'class':'name'}).text
    player['country'] = rows.find('td',{'class':'ctry'}).find('img')['title']
    player['rank'] = curr_rank
    curr_rank += 1
    
    # Append each player to the ranking list
    rankings.append(player)

# Create OWGR dataframe with ranking as index
owgr = pd.DataFrame(rankings).set_index('rank')

# Export to CSV file
owgr.to_csv('./current-OWGR.csv')