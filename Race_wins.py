from bs4 import BeautifulSoup as soup
import requests
import pandas as pd

venue = []
fname = []
lname = []
sname = []
car = []
laps = []
time = []
date = []

for year in range(1950, 2021):
    print('Fetching data for year', year, "...")
    url = r'https://www.formula1.com/en/results.html/{}/races.html'.format(str(year))
    r = requests.get(url)
    s = soup(r.text, 'html.parser')

    venue = venue + list(x.text.strip() for x in (s.find_all('a', class_='dark bold ArchiveLink')))
    fname = fname + list(x.text.strip() for x in (s.find_all('span', class_='hide-for-tablet')))
    lname = lname + list(x.text.strip() for x in (s.find_all('span', class_='hide-for-mobile')))
    sname = sname + list(x.text.strip() for x in (s.find_all('span', class_='uppercase hide-for-desktop')))
    car = car + list(x.text.strip() for x in (s.find_all('td', class_='semi-bold uppercase')))
    laps = laps + list(x.text.strip() for x in (s.find_all('td', class_='bold hide-for-mobile')))
    time = time + list(x.text.strip() for x in (s.find_all('td', class_='dark bold hide-for-tablet')))
    date = date + list(x.text.strip() for x in (s.find_all('td', class_='dark hide-for-mobile')))

pd.set_option('display.max_columns', None)

name = list(x + " " + y for x, y in zip(fname, lname))

df = pd.DataFrame(list(zip(venue, date, name, sname, car, laps, time)),
                  columns=['Venue', 'Date', 'Name', 'NameTag', 'Team', 'Laps', 'Time'])

print(df.head())

df.to_csv('D:\\race_wins_1950-2020.csv')
