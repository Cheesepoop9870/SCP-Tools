import sys
try:
  import requests
  import bs4
except ImportError as ie:
  print(f"module not found. Please install requests and bs4. ({ie})")
  install = input("Would you like to install them? (y/n):")
  if install == "y":
    import os
    os.system("python3 -m pip install requests && python3 -m pip install bs4")
    print("please rerun")
    sys.exit()
  else:
    print("Terminating")
    sys.exit()
record_type = input("Enter record type (AI, D, ND):")
if record_type == "AI":
  record_ID = "7852401"
  striptext = "AI Record - "
elif record_type == "D":
  record_ID = "82386"
  striptext = "Disciplinary - "
elif record_type == "ND":
  record_ID = "798754"
  striptext = "Non-Disc Record - "
else:
  print("Invalid record type.")
  sys.exit()
username = input("Enter username of record to find (case sensitive):")
pagesBack = int(input("Enter # of pages to go back (set to -1 for all):"))
record = []
found = False
# what_to_strip = ["AI Record - ", "Disciplinary - ", "Non-Disc Record - "]
# record_category = ["7852401", "82386", "798754"]


if pagesBack == -1:
  temp_body = requests.get(f'https://05command.wikidot.com/forum/c-{record_ID}/p/1')
  if temp_body.status_code != 200:
    print(f"Error: Could not connect to 05command.wikidot.com ({temp_body.status_code})")
    sys.exit()
  temp_soup = bs4.BeautifulSoup(temp_body.text, 'html.parser')
  lastpage = temp_soup.find('div', class_='pager')
  lastpage = lastpage.find('span', class_='pager-no').text.strip()
  # print(f"Last page is {lastpage.strip('page 1 of ')}")
  pagesBack = int(lastpage.strip('page 1 of '))
elif pagesBack == 0 or pagesBack < -1:
  print("Invalid number of pages.")
  sys.exit()

for x in range(1, pagesBack+1):
  #note: you may get rate limited/ip banned. this is not my fault.
  body = requests.get(f'https://05command.wikidot.com/forum/c-{record_ID}/p/{x}')
  if body.status_code != 200 and body.status_code != 404:
    print(f"Error: Could not connect to 05command.wikidot.com ({body.status_code})")
    sys.exit()
  elif body.status_code == 404:
    found = True
    break
  # print(x)
  soup = bs4.BeautifulSoup(body.text, 'html.parser')
  main_content = soup.find('div', id='page-content')
  # print(main_content)
  urls = []
  titles = main_content.find_all('div', class_="title")
  descriptions = main_content.find_all('div', class_="description")
  for title in titles:
    urls.append(title.find('a')['href'])
  for y in range(0, len(titles)):
    username_key = titles[y].text.strip().replace(striptext, "")
    record.append({username_key: {"title": titles[y].text.strip(), "url": urls[y], "desc": descriptions[y].text.strip(), "page": x}})
    if username in username_key:
      # print("AI record found.")
      found = True
      break
  if found:
    break

records2 = {}
  
for dict in record:
   records2.update(dict)
# print(records2)

keylist = []
try:
  for key in records2.keys():
    if username in key:
      keylist.append(key)
      # print(f"{records2[key]['title']} http://05command.wikidot.com{records2[key]['url']}: {records2[key]['desc']}")
      break
  if len(keylist) == 0:
    raise KeyError
  for key in keylist:
    print(f"{records2[key]['title']} http://05command.wikidot.com{records2[key]['url']}: {records2[key]['desc']} (page {records2[key]['page']})")
except KeyError:
   print("Record not found. (try going back more pages)")

