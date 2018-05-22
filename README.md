Scrapy log analyzer
==

Get logs from specific job and create some helpful reports. 

So far the script gets all errors from a log for given job and creates

convenient report to insert into a code for debugging
  
Uses https://github.com/scrapinghub/python-scrapinghub

Example
--

**From command line:**

```
$ python3 scrapy_la.py errors 16014/2/8207 -a <APIKEY> 

```

```
Errors in the log: 1151
With different scrapy types: 45
With different description: 3
With different url: 108
With different response_url: 60
With different python types of errors: 2
With different python messages: 2
--------- Part for code debugging -----------
test_urls = [
    # Inconsistent 'products_on_page' (5 from 947 different 59)
    "http://www.example.com/no7/no7-lift-luminate-range",
    "http://www.example.com/heinz/heinz-finger-food",
    "http://www.example.com/electrical-dental/electric-flossers",
    # Spider error processing (5 from 59 different 43)
    "https://example.com/execute?__debug_kwid=id245&__debug_page_number=1",
    "https://example.com/execute?__debug_kwid=id6&__debug_page_number=1",
    "https://example.com/execute?__debug_kwid=id132&__debug_page_number=1",
    # duplicated field(s): 'page_item_number' (5 from 145 different 9)
    "http://www.example.com/no7-make-up/no7-mascaras",
    "http://www.example.com/centrum/centrum-50",
    "http://www.example.com/electrical-dental/dental-brush-heads",
]
```

Requirements
--

- at least python 3.5
- scrapinghub (2.0.3)
- pandas (0.22.0)
 

Installation
--

just clone the project and install the requirements:

```
$ git clone https://github.com/PyExplorer/scrapy_log_analyzer.git
$ cd scrapy_log_analyzer
$ pip3 install -r requirements.txt
```

Docs
--
The script has one command "errors" and 2 required and 1 optional parameters. 
  
**Required parameters**:

**job** - job key string in format project_id/spider_id/job_id, where all the components are integers.

**-a (--apikey)** - APIKEY for ScrapinghubClient (Your Scrapinghub API key is 

available at https://app.scrapinghub.com/account/apikey after you sign up with the service.)

APIKEY also can be set with as SH_APIKEY in your environment so not necessary to set it with -a in the future

```
$ python3 scrapy-la.py errors 10/10/10 -a <APIKEY>'
```

**Optional parameters for errors**

**-m (--max)** - Set max urls to output for each type of log (errors)
  
*default:* 3

```
$ python3 scrapy-la.py errors 10/10/10 -a <APIKEY> -m 5
```

Contributing
--

To contribute, pick an issue to work on and leave a comment saying that you've taken the issue. 

Don't forget to mention when you want to submit the pull request.


Launch tests
--

*$ python3 -m unittest*

Next features:
--
 
- get statistic for all errors from a project (not only one job) - types, counts, etc;

- find specific error's message (or scrapy/python types) in all spiders for project

- add command 'warnings' for warning's analyze

- and more



