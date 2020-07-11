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
q1 = []
q2 = []
q3 = []

f = open("D:\\quali.txt", "r")
lines = f.readlines()
f.close()

# 1950 to 2005
for b in range(0,750):
    line = lines[b]

    print('Fetching data for race ' + line.split("/")[8], line[41:45], "...")

    url = line
    r = requests.get(url)
    s = soup(r.text, 'html.parser')
    po = list(x.text.strip() for x in (s.find_all('td', class_='dark')))
    lp = list(x.text.strip() for x in (s.find_all('td', class_='semi-bold hide-for-mobile')))
    t = list(x.text.strip() for x in (s.find_all('td', class_='dark bold')))

    if int(line[41:45]) < 1994:
        pos = pos + po[0:len(po):4]
        laps = laps + list('N/A' for i in range(0,len(po[0:len(po):4])))
        time = time + t[1:len(t):2]

    else:
        pos = pos + po[0:len(po):4]
        laps = laps + lp
        time = time + t[1:len(t):2]

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

df = pd.DataFrame(list(zip(y, pos, dno, venue, name, sname, car, time, laps)),
                  columns=['Year', 'Position', 'Driver No.', 'Venue', 'Name', 'NameTag', 'Team', 'Lap Time', 'Laps'])

print(df.head())

df.to_csv('D:\\qualifying_times_1950-2005.csv')


# 2006 to 2020
for b in range(750, len(lines)):
    line = lines[b]

    print('Fetching data for race ' + line.split("/")[8], line[41:45], "...")

    url = line
    r = requests.get(url)
    s = soup(r.text, 'html.parser')
    po = list(x.text.strip() for x in (s.find_all('td', class_='dark')))
    t = list(x.text.strip() for x in (s.find_all('td', class_='dark bold')))
    pos = pos + po[0:len(po):6]
    laps = laps + list(x.text.strip() for x in (s.find_all('td', class_='semi-bold hide-for-mobile')))
    q1 = q1 + t[1:len(t):4]
    q2 = q2 + t[2:len(t):4]
    q3 = q3 + t[3:len(t):4]
    dno = dno + list(x.text.strip() for x in (s.find_all('td', class_='dark hide-for-mobile')))
    fn = list(x.text.strip() for x in (s.find_all('span', class_='hide-for-tablet')))
    fname = fname + fn
    lname = lname + list(x.text.strip() for x in (s.find_all('span', class_='hide-for-mobile')))
    sname = sname + list(x.text.strip() for x in (s.find_all('span', class_='uppercase hide-for-desktop')))
    car = car + list(x.text.strip() for x in (s.find_all('td', class_='semi-bold uppercase hide-for-tablet')))
    venue = venue + list(line.split("/")[8] for i in range(0, len(fn)))
    y = y + list(line[41:45] for i in range(0, len(fn)))

pd.set_option('display.max_columns', None)

for i in range(0, len(q3)):
    if len(q3[i]) == 0:
        q3[i] = 'N/A'
        if len(q2[i]) == 0:
            q2[i] = 'N/A'

name = list(x + " " + y for x, y in zip(fname, lname))
df = pd.DataFrame(list(zip(y, pos, dno, venue, name, sname, car, q1, q2, q3, laps)),
                  columns=['Year', 'Position', 'Driver No.', 'Venue', 'Name', 'NameTag', 'Team', 'Q1', 'Q2', 'Q3',
                           'Laps'])

print(df.head())

df.to_csv('D:\\qualifying_times_2006-2020.csv')
