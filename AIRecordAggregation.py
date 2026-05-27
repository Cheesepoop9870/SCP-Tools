import requests
import bs4
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt
import asyncio
import httpx
try:
  import fake_useragent
except ImportError:
  print("Warning: fake_useragent is reccomended but not nessasarry")
AI = "https://05command.wikidot.com/forum/c-7852401/p/1"



async def get_page(client, url,sem): # fetch page
  async with sem: #limit requests
    try:
      ua = fake_useragent.UserAgent()
      headers = {'User-Agent': ua.random}
    except ModuleNotFoundError:
      headers = {'User-Agent': 'python-httpx/x.y.z'}
    response = await client.get(url, headers=headers)
    print(f'Fetched {url}')
  return response
def get_last_page(url): #get last page num
   body = requests.get(url)
   soup = bs4.BeautifulSoup(body.text, 'html.parser')
   lastpage = soup.find('div', class_='pager')
   lastpage = lastpage.find('span', class_='pager-no').text.strip() #type: ignore
   return int(lastpage.strip('page 1 of '))

pageNum = get_last_page(AI)
rowlist = []
# datelist = []
authorlist = []
datelist_unix = []
postlist = []
async def parse_page(page,pages): #get data out of page async
  soup = bs4.BeautifulSoup(page.text, 'html.parser')
  main_content = soup.find('div', id='page-content')
  table = main_content.find('table')  # type: ignore
  rows = table.find_all('tr', class_='')  # type: ignore
  for row in rows:
    # dates = row.find('span', class_='odate').text  
    # datelist.append(dates)
    datelist_unix.append(dt.fromtimestamp(int(row.find('span', class_='odate').get('class')[1].strip("time_")))) # type: ignore
    author = row.find('td', class_='started').find('span', class_='printuser').find_all('a')  # type: ignore
    author = author[1].text
    authorlist.append(author)
    posts=row.find('td', class_='posts').text.strip()
    postlist.append(posts)
  rowlist.append(rows)
  print(f"Page {pages.index(page)+1} done.")
  
async def scrape_pages(): #scrape all pages
  urls = [f'https://05command.wikidot.com/forum/c-7852401/p/{x}' for x in range(1, pageNum+1)]
  sem = asyncio.Semaphore(7) #nessasarry or wikidot murders ur tls handshake
  async with httpx.AsyncClient() as client: #async client
    tasks = [get_page(client, url,sem) for url in urls] #fetch page
    pages = await asyncio.gather(*tasks)
    tasks = [parse_page(page,pages) for page in pages] #parse page
    await asyncio.gather(*tasks)
asyncio.run(scrape_pages()) #run async
# print(datelist_unix)
print()
# print(authorlist)
# all_dates = np.array([dt.strptime(x, r'%d %b %Y %H:%M') for x in datelist]) #convert to datetime
all_dates = np.array(datelist_unix)
all_authors = np.array(authorlist)
date_author = np.stack((all_dates,all_authors),axis=1) #combine dates and authors
date_author = date_author[date_author[:,0].argsort()] #sort by date
unique_months =  np.unique(np.array([x.replace(hour=0,minute=0,second=0,microsecond=0,day=1) for x in all_dates.copy()]), return_counts=True) # remove day and time, add to list
unique_authors = np.unique(all_authors, return_counts=True)
print(unique_authors)
print(unique_months)
for month in unique_months[0]: 
  print(month.strftime("%b %Y"))
plt.figure(1,figsize=(10,5)) #figure 1 (cases over time/month)
dates =  plt.plot(unique_months[0], unique_months[1]) #plot dates and counts
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y')) #format dates to readable format
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2)) # make all dates show
plt.gcf().autofmt_xdate() #fix date overlap

plt.axvline(x=dt(2025, 10, 1), color='r', linestyle='--', label="AI is now Perma") #type: ignore add line for when AI is perma
plt.legend() #add legend
plt.grid() #add grid
plt.savefig('graph.png', dpi=300) #save graph
print("file saved as graph.png")

plt.figure(2, figsize=(10,5)) #author of record
other_count=0
unique_authors_trimmed = np.vstack((unique_authors[0],unique_authors[1])).T.tolist()
# unique_authors_trimmed = [list(x) for x in  list(zip(unique_authors[0],unique_authors[1]))]
print(unique_authors_trimmed)
other_count = sum(int(count) for author, count in unique_authors_trimmed if int(count) <= 10) #total um of authors <= 10
unique_authors_trimmed = [[author, count] for author, count in unique_authors_trimmed if int(count) > 10] #list of authors > 10
unique_authors_trimmed.append(["Other",other_count]) #add others
print()
print(unique_authors_trimmed)
plt.pie([x[1] for x in unique_authors_trimmed], labels=[x[0] for x in unique_authors_trimmed], autopct='%1.1f%%', radius=1.5,pctdistance=0.7)
plt.savefig('pie.png', dpi=300)
print('flie saved as pie.png')

hours = np.unique(np.array([x.replace(year=2000,month=1,day=1,minute=0,second=0) for x in all_dates.copy()]), return_counts=True) # remove 
hours = np.vstack((hours[0],hours[1])).T
print(hours)
plt.figure(3, figsize=(10,5))
plt.plot([x[0] for x in hours], [x[1] for x in hours])
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
plt.gcf().autofmt_xdate()
plt.grid()
plt.xlabel('Time of day (UTC)')
plt.ylabel('Number of posts')
plt.savefig('hours.png', dpi=300)
print('file saved as hours.png')

unique_posts = np.unique(np.array(postlist), return_counts=True)
unique_posts = np.vstack((unique_posts[0],unique_posts[1])).T
unique_posts = sorted(unique_posts, key=lambda x: int(x[0]))
print(unique_posts)
posts1 = sum(int(count) for post, count in unique_posts if int(post) <=1)
posts2 = sum(int(count) for post, count in unique_posts if int(post) == 2)
posts3 = sum(int(count) for post, count in unique_posts if int(post) == 3)
posts4to6 = sum(int(count) for post, count in unique_posts if int(post) >= 4 and int(post) <= 6)
posts7to9 = sum(int(count) for post, count in unique_posts if int(post) >= 7 and int(post) <= 9)
plus_ten = sum(int(count) for post, count in unique_posts if int(post) >= 10)
adj_unique_posts = [["1",posts1],["2",posts2],["3",posts3],["4-6",posts4to6],["7-9",posts7to9],["10+",plus_ten]]
print(adj_unique_posts)
plt.figure(4, figsize=(7,7))
plt.bar([x[0] for x in adj_unique_posts], [x[1] for x in adj_unique_posts])
plt.savefig('posts.png', dpi=300)
print("\n\n\ndone")
