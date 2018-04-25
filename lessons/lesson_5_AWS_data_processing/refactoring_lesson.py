"""
Refactoring Lesson
Author: Alex Sherman | alsherman@deloitte.com

Goal: Refactor the data scraping homework solution. 
      Convert the code into functions.
"""

import os
import requests
import time
from bs4 import BeautifulSoup
import configparser
from configparser import ConfigParser, ExtendedInterpolation

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('../../config.ini')
OUTPUT_DIR_PATH = config['AUTOMATION']['OUTPUT_DIR_PATH']
BASE_URL = config['AUTOMATION']['BASE_URL']
COMPANY = config['AUTOMATION']['COMPANY']


"""
1. collect all of the urls for the numerous annual reports
"""

# find all the html that stores the pdf urls
company_url = r'{}/Company/{}'.format(BASE_URL, COMPANY)
r = requests.get(company_url)
b = BeautifulSoup(r.text, 'lxml')
annual_reports = b.find_all('ul', attrs={'class':'links'})

# collect/store all annual report pdf urls
urls = []
for report in annual_reports:
    try:
        # create the report_url to download the pdf
        report_name = report.find('a')['href']
        report_url = ''.join([BASE_URL, report_name])
        urls.append(report_url)
    # handle expected errors for links on the page that are not for pdfs
    except TypeError:
        continue
    except KeyError:
        continue



"""
2. Create a mapping a file paths for how you want to name and where you want to
    store each file locally

    a. store all files in a folder on your desktop called
       annual_report/raw_data/[COMPANY_name]
       -NOTE: replace [COMPANY_name] with the selected companies name
"""

output_paths = {}
for ind, url in enumerate(urls):
    # parse the year from the annual report report_name
    year = url.split('_')[-1].split('.')[0]

    # The first annual report on a page is stored in different html
    # and does not have the year in the report name
    # e.g. ('Click/[#]') instead of ('NYSE_ORCL_2015.pdf')
    # add one to the year of the last annual report to get the correct year
    if ind == 0:
        year = str(int(urls[1].split('_')[-1].split('.')[0])+1)

    # create a file path to identify how to name a file
    # and where to store it locally
    filename = '{}_annual_report_{}.pdf'.format(COMPANY, year)
    filepath = os.path.join(OUTPUT_DIR_PATH,filename)
    output_paths[url] = filepath



"""
3. Download all of the annual reports

    a. make sure to check the http://www.annualreports.com/robots.txt
       to ascertain any data collection restrictions
"""

for url in urls:
    # get directory to store annual report
    filepath = output_paths[url]
    filename = filepath.split('\\')[-1]

    # skip files that have already been downloaded
    if filename in os.listdir(OUTPUT_DIR_PATH):
        print('file already downloaded: {}'.format(url))
        continue
        
    # download pdf
    r = requests.get(url)
    print('downloaded: {}'.format(url))

    # write pdf to local directory
    with open(filepath, 'wb') as f:
        f.write(r.content)

    # required delay, stated in the robots.txt
    time.sleep(5)  # five seconds


