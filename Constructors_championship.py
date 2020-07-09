from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
pos = []
team = []
pts = []
plist = []
y = []

for year in range(1958, 2021):
    print('Fetching constructors championship data for year', year, "...")
    url = r'https://www.formula1.com/en/results.html/{}/team.html'.format(str(year))
    r = requests.get(url)
    s = soup(r.text, 'html.parser')

    plist = list(x.text.strip() for x in (s.find_all('td', class_='dark')))
    pos = pos + plist[0:len(plist):2]
    y = y + [year for i in range(0,len(plist),2)]
    team = team + list(x.text.strip() for x in (s.find_all('a', class_='dark bold uppercase ArchiveLink')))
    pts = pts + list(x.text.strip() for x in (s.find_all('td', class_='dark bold')))
pd.set_option('display.max_columns', None)
df = pd.DataFrame(list(zip(y, pos, team, pts)),
                  columns=['Year', 'Position', 'Team', 'Points'])
print(df.head())

df.to_csv('D:\\constructors_championship_1958-2020.csv')