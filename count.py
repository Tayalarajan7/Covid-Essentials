from requests import get
import bs4

url = 'https://www.mohfw.gov.in/'
res = get(url)
#print(res.text[:10000])

soup = bs4.BeautifulSoup(res.text, 'lxml')

a = soup.select('.bg-blue')
r = soup.select('.bg-green')
d = soup.select('.bg-red')

ac = a[0].text
re = r[0].text
de = d[0].text

active = ac[2:8]
recovered = re[2:8]
death = de[2:6]

#print('Active cases: ' + active)
#print('Recovered cases: ' + recovered)
#print('Deaths: ' + death)

