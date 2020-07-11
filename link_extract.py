from bs4 import BeautifulSoup as soup
import requests

l = []
for year in range(1950, 2021):
    print("Link for year ", year)
    url = 'https://www.formula1.com/en/results.html/{}/races.html'.format(str(year))
    r = requests.get(url)
    s = soup(r.text, 'html.parser')

    links = list(str(link.get('href')) for link in s.find_all('a'))

    # links for race pages
    link = list(i for i in filter(lambda x: x.find('race-result') != -1, links))
    for i in link:
        if i not in l:
            l.append(i)

f = open("D:\\f1links.txt", "w")
for j in l:
    f.writelines("https://www.formula1.com" + j + "\n")
f.close()

# links for fastest laps
f = open('D:\\f1links.txt', 'r')
lines = f.readlines()
f.close()

f = open('D:\\fastlaps.txt', 'w')
for l in lines:
    f.writelines(l.replace('race-result', 'fastest-laps') + "\n")
f.close()

# links for qualifying
f = open('D:\\f1links.txt', 'r')
lines = f.readlines()
lines = list(l.replace('\n', '') for l in lines)
f.close()

f = open('D:\\quali.txt', 'w')
for l in lines:
    if l[41:45] < '2006':
        f.writelines(l.replace('race-result', 'qualifying-0') + "\n")
    else:
        f.writelines(l.replace('race-result', 'qualifying') + "\n")
f.close()
