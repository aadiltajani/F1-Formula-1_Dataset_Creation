from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
pos = []
fname = []
lname = []
sname = []
nation = []
car = []
pts = []
plist = []
y = []

for year in range(1950, 2021):
    print('Fetching drivers championship data for year', year, "...")
    url = r'https://www.formula1.com/en/results.html/{}/drivers.html'.format(str(year))
    r = requests.get(url)
    s = soup(r.text, 'html.parser')

    plist = list(x.text.strip() for x in (s.find_all('td', class_='dark')))
    pos = pos + plist[0:len(plist):3]
    y = y + [year for i in range(0,len(plist),3)]
    fname = fname + list(x.text.strip() for x in (s.find_all('span', class_='hide-for-tablet')))
    lname = lname + list(x.text.strip() for x in (s.find_all('span', class_='hide-for-mobile')))
    sname = sname + list(x.text.strip() for x in (s.find_all('span', class_='uppercase hide-for-desktop')))
    nation = nation + list(x.text.strip() for x in (s.find_all('td', class_='dark semi-bold uppercase')))
    car = car + list(x.text.strip() for x in (s.find_all('a', class_='grey semi-bold uppercase ArchiveLink')))
    pts = pts + list(x.text.strip() for x in (s.find_all('td', class_='dark bold')))
pd.set_option('display.max_columns', None)
name = list(x + " " + z for x, z in zip(fname, lname))
df = pd.DataFrame(list(zip(y, pos, name, sname, nation, car, pts)),
                  columns=['Year', 'Position', 'Name', 'Driver Tag', 'Nationality', 'Team', 'Points'])

print(df.head())

df.to_csv('D:\\drivers_championship_1950-2020.csv')