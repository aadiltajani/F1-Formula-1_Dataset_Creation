from bs4 import BeautifulSoup as soup
import requests
import pandas as pd

pos = []
no = []
y = []
venue = []
fname = []
lname = []
sname = []
car = []
laps = []
time = []
pts = []
dno = []

f = open("D:\\f1links.txt", "r")
for line in f.readlines():
    print('Fetching data for race ' + line.split("/")[8], line[41:45], "...")

    url = line
    r = requests.get(url)
    s = soup(r.text, 'html.parser')

    po = list(x.text.strip() for x in (s.find_all('td', class_='dark')))
    p = list(x.text.strip() for x in (s.find_all('td', class_='bold')))
    t = list(x.text.strip() for x in (s.find_all('td', class_='dark bold')))

    pos = pos + po[0:len(po):4]
    time = time + t[1:len(t):2]
    pts = pts + p[3:len(p):4]

    dno = dno + list(x.text.strip() for x in (s.find_all('td', class_='dark hide-for-mobile')))
    fn = list(x.text.strip() for x in (s.find_all('span', class_='hide-for-tablet')))
    fname = fname + fn
    lname = lname + list(x.text.strip() for x in (s.find_all('span', class_='hide-for-mobile')))
    sname = sname + list(x.text.strip() for x in (s.find_all('span', class_='uppercase hide-for-desktop')))
    car = car + list(x.text.strip() for x in (s.find_all('td', class_='semi-bold uppercase hide-for-tablet')))
    laps = laps + list(x.text.strip() for x in (s.find_all('td', class_='bold hide-for-mobile')))
    venue = venue + list(line.split("/")[8] for i in range(0, len(fn)))
    y = y + list(line[41:45] for i in range(0, len(fn)))

pd.set_option('display.max_columns', None)
name = list(x + " " + y for x, y in zip(fname, lname))

df = pd.DataFrame(list(zip(y, pos, dno, venue, name, sname, car, laps, time, pts)),
                  columns=['Year', 'Position', 'Driver No.', 'Venue', 'Name', 'NameTag', 'Team', 'Laps', 'Time',
                           'Points'])
print(df.head())
df.to_csv('D:\\race_results_1950-2020.csv')
f.close()
