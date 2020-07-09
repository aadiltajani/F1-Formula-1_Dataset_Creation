from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
fname = []
lname = []
sname = []
venue = []
car = []
time = []
y = []

for year in range(1950, 2021):
    print('Fetching fastest laps data for year', year, "...")
    url = r'https://www.formula1.com/en/results.html/{}/fastest-laps.html'.format(str(year))
    r = requests.get(url)
    s = soup(r.text, 'html.parser')

    y = y + [year for i in range(0,len(list(s.find_all('span', class_='hide-for-tablet'))))]
    fname = fname + list(x.text.strip() for x in (s.find_all('span', class_='hide-for-tablet')))
    lname = lname + list(x.text.strip() for x in (s.find_all('span', class_='hide-for-mobile')))
    sname = sname + list(x.text.strip() for x in (s.find_all('span', class_='uppercase hide-for-desktop')))
    venue = venue + list(x.text.strip() for x in (s.find_all('td', class_='width30 dark')))
    car = car + list(x.text.strip() for x in (s.find_all('td', class_='width25 semi-bold uppercase')))
    time = time + list(x.text.strip() for x in (s.find_all('td', class_='dark bold')))

pd.set_option('display.max_columns', None)
name = list(x + " " + z for x, z in zip(fname, lname))
df = pd.DataFrame(zip(y, venue, name, sname, car, time),
                  columns=['Year', 'Venue', 'Name', 'Driver Tag', 'Team', 'Lap Time'])
print(df.head())

df.to_csv('D:\\fastest_laps_1950-2020.csv')