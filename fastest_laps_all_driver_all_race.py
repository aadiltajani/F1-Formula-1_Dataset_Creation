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
dno = []
speed = []

f = open("D:\\fastlaps.txt", "r")
lines = f.readlines()

for line in lines[0:len(lines):2]:
    print('Fetching data for race ' + line.split("/")[8], line[41:45], "...")

    url = line
    r = requests.get(url)
    s = soup(r.text, 'html.parser')
    po = list(x.text.strip() for x in (s.find_all('td', class_='dark')))
    lp = list(x.text.strip() for x in (s.find_all('td', class_='bold')))
    t = list(x.text.strip() for x in (s.find_all('td', class_='dark bold')))

    if int(line[41:45]) < 1998:
        pos = pos + po[0:len(po):4]
        laps = laps + lp[1:len(lp):3]

        if int(line[41:45]) < 1980:
            for b in laps:
                if len(b)==0:
                    laps[laps.index(b)]='N/A'
        time = time + t[1:len(t):2]
        speed = speed + list('N/A' for i in range(0,len(po[0:len(po):4])))

    elif int(line[41:45]) < 2014:
        pos = pos + po[0:len(po):5]
        laps = laps + lp[1:len(lp):4]
        time = time + t[1:len(t):3]
        speed = speed + t[2:len(t):3]

    else:
        pos = pos + po[0:len(po):6]
        laps = laps + lp[1:len(lp):5]
        time = time + t[2:len(t):4]
        speed = speed + t[3:len(t):4]

    dno = dno + list(x.text.strip() for x in (s.find_all('td', class_='dark hide-for-mobile')))
    fn = list(x.text.strip() for x in (s.find_all('span', class_='hide-for-tablet')))
    fname = fname + fn
    lname = lname + list(x.text.strip() for x in (s.find_all('span', class_='hide-for-mobile')))
    sname = sname + list(x.text.strip() for x in (s.find_all('span', class_='uppercase hide-for-desktop')))
    car = car + list(x.text.strip() for x in (s.find_all('td', class_='semi-bold uppercase hide-for-tablet')))
    venue = venue + list(line.split("/")[8] for i in range(0, len(fn)))
    y = y + list(line[41:45] for i in range(0, len(fn)))

pd.set_option('display.max_columns', None)

name = list(x + " " + y for x, y in zip(fname, lname))

df = pd.DataFrame(list(zip(y, pos, dno, venue, name, sname, car, laps, time, speed)),
                  columns=['Year', 'Position', 'Driver No.', 'Venue', 'Name', 'NameTag', 'Team', 'Lap No.', 'Time', 'Avg Speed'])

print(df.head())
df.to_csv('D:\\fastest_laps_all_drivers_all_race_1950-2020.csv')

f.close()
