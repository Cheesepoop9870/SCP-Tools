# SCP Tools
Some tools for the SCP wiki

----
## 05 Record searcher:
Run: ```python3 05recordsearch.py```

It will ask for Record type:
* **D**: Disc record
* **AI**: AI usage record
* **ND**: Non-Disc record

Next it will ask for username (case-sensitive)

After, it will ask for how many pages to search back, e.g if you write '5', it will search pages 1-5. You can also set this to '-1' to search all availible pages

### Example:
Input:
```
Enter record type (AI, D, ND):D
Enter username of record to find (case sensitive):MrCoolCool
Enter # of pages to go back (set to -1 for all):10
```

Output: 
```
AI Record - MrCoolCool http://05command.wikidot.com/forum/t-17486839/ai-record-mrcoolcool: Posted AI page, admitted they "used ai to fix my wording" (page 1)
```

### Dependincies:
* python
* beautifulsoup4==4.14.3
* requests==2.32.5
----
## AI Record Aggregation

Fetches data from 05command and returns stats.

note: prints out a bunch of stuff, can probably ignore it (too lazy to remove)

Makes 3 files
* graph.png
* pie.png
* hours.png

graph.png is a graphing of AI records over time, per month

pie.png is a graphing of authors of AI record posts

hours.png is a graphing of the average time of day a record has been started

### Dependinies:
* python
* beatifulsoup4
* requests
* httpx
* re
* datetime
* asyncio
* matplotlib
* numpy
* fake_useragent (recommended)
----
### Preview Regex

Python flavored regex to match preview text in an SCP page
