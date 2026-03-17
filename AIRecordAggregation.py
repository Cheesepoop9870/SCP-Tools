import requests
import bs4
import time
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt

AI = "https://05command.wikidot.com/forum/c-7852401/p/1"

def get_last_page(url):
   body = requests.get(url)
   soup = bs4.BeautifulSoup(body.text, 'html.parser')
   lastpage = soup.find('div', class_='pager')
   lastpage = lastpage.find('span', class_='pager-no').text.strip()
   return int(lastpage.strip('page 1 of '))

pageNum = get_last_page(AI)
rowlist = []
datelist = []
authorlist = []
for x in range(1, pageNum):
   body = requests.get(f'https://05command.wikidot.com/forum/c-7852401/p/{x}')
   soup = bs4.BeautifulSoup(body.text, 'html.parser')
   main_content = soup.find('div', id='page-content')
   table = main_content.find('table')
   rows = table.find_all('tr', class_='')
   for row in rows: 
     dates = row.find('td', class_='started')
     datelist.append(dates)
     author = row.find('td', class_='started').find('span', class_='printuser').find_all('a')
     author = author[1].text
     authorlist.append(author)
   rowlist.append(rows)
   print(f"Page {x} done.")
actual_datelist = []
for date in datelist:
  actual_datelist.append(date.find('span', class_='odate'))
print("Done.")
# print("\n"+str([x.text for x in actual_datelist]))

date_data = [] #day month year hour minute

for actual_date in actual_datelist:
  # print(actual_date.text.split(" "))
  date_data.append(actual_date.text.split(" "))
# print("\n"+str(date_data))
# print(authorlist)
data = []
for x in range(0, len(date_data)):
  data.append([*date_data[x], authorlist[x]]) #add authors to date data
actual_authors = []

for author2 in authorlist: #get unique authors
  if author2 not in actual_authors:
    actual_authors.append(author2)
    
for x in range(0, len(actual_authors)): #add number of contributions
  actual_authors[x] = [actual_authors[x],authorlist.count(actual_authors[x])]
print(actual_authors)

short_date = [] #day month year
for date in data:
  short_date.append(" ".join(date[1:3]))
  # print(" ".join(date[1:3]))

unique_dates = []
unique_dates2 = []
for x in range(0, len(short_date)):
  if short_date[x] not in unique_dates:
    unique_dates.append(short_date[x])
for x in range(0, len(unique_dates)):
  # print([unique_dates[x], short_date.count(unique_dates[x])])
  unique_dates2.append([unique_dates[x], short_date.count(unique_dates[x])])
  unique_dates[x] = [dt.strptime(unique_dates[x], "%b %Y"), short_date.count(unique_dates[x])]
  # print(unique_dates[x])
# for data2 in data:
#    print(data2)

dates = plt.plot([x[0] for x in sorted(unique_dates)], [x[1] for x in sorted(unique_dates)])
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.savefig('graph.png')
print("file saved as graph.png")
output = []
print("\n\n\n")
for date_temp in unique_dates2:
  output.append(date_temp[0])
print(", ".join(output))
output = []
for date_temp in unique_dates2:
  output.append(date_temp[1])
print(output)
print("\n"+str([x[0] for x in actual_authors]))
print("\n"+str([x[1] for x in actual_authors]))
