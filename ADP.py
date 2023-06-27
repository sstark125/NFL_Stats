from bs4 import BeautifulSoup
import requests
import re
import urllib3
import os
import pandas as pd
def ConsoleClear():
    os.system('cls' if os.name == 'nt' else 'clear')
ConsoleClear()



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url = "https://www.fantasypros.com/nfl/adp/overall.php"
result = requests.get(url, verify=False)
doc = BeautifulSoup(result.text, "html.parser")

tbody = doc.tbody
trs = tbody.contents

players = {}

for tr in trs:
    if tr.name == 'tr':
        tds = tr.find_all('td')
        name, position, adp = tds[1], tds[2], tds[7]
        fixed_name = name.a.string
        fixed_pos = position.string
        fixed_adp = adp.string
        
        players[fixed_name] = (fixed_pos, fixed_adp)

# for player, values in players.items():
#     position, adp = values
#     print(f"{player}: {position}, {adp}")


df = pd.DataFrame.from_dict(players, orient='index', columns=['Position','ADP'])
df.index.name = 'Player'

# Save the DataFrame to an Excel file
excel_filename = 'players.xlsx'
df.to_excel(excel_filename)

print(f"Data has been saved to {excel_filename} successfully.")