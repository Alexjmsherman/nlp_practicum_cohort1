"""
Refactoring Lesson
Author: Alex Sherman | alsherman@deloitte.com

Goal: Refactor the data scraping homework solution. 
      Convert the code into functions.

"""
import boto3
import json
import os
import requests
import time
from bs4 import BeautifulSoup
from configparser import ConfigParser, ExtendedInterpolation

# configuration
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('config.ini')
BUCKET_NAME = config['LAMBDA']['BUCKET_NAME']
BASE_URL = config['LAMBDA']['BASE_URL']
COMPANY = config['LAMBDA']['COMPANY']


def main(event, context):
    print('start annual reports for {}'.format(COMPANY))
    urls = get_company_annual_report_urls(COMPANY)
    output_paths = create_output_paths(urls, COMPANY)
    download_annual_reports(urls, output_paths)


def get_company_annual_report_urls(COMPANY):
    """ collect all of the urls for the numerous pdf annual reports
    of a specified COMPANY

    :param COMPANY: COMPANY name, used to search for annual reports
    :return urls: list of urls for the annual report pdfs for the COMPANY
    """

    company_url = r'{}/Company/{}'.format(BASE_URL, COMPANY)

    # find all links on page
    r = requests.get(company_url)
    b = BeautifulSoup(r.text, 'html.parser')
    annual_reports = b.find_all('ul', attrs={'class':'links'})

    urls = []
    for report in annual_reports:
        try:
            # create the report_url to download the pdf
            report_name = report.find('a')['href']
            report_url = ''.join([BASE_URL, report_name])
            urls.append(report_url)
        # handle expected errors for links on the page that are not for pdfs
        except (TypeError, KeyError):
            continue

    return urls

def create_output_paths(urls, COMPANY):
    """ create a mapping a file paths for the report_names and
    directory paths to store each annual report locally

    NOTE:annual_report/raw_data/[COMPANY_name]

    :param urls: list of annual report urls
    :param COMPANY: name of COMPANY
    :return output_paths: dict with mapping - {'report name': 'directory_path'}
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
            previous_year = urls[1].split('_')[-1].split('.')[0] 
            year = str(int(previous_year) + 1)

        # create a file path to identify how to name a file
        # and where to store it locally
        filename = '{}_annual_report_{}.pdf'.format(COMPANY, year)
        output_paths[url] = filename

    return output_paths


def download_annual_reports(urls, output_paths):
    """ Download all of the specified annual reports to a local directory

    :param urls: annual report urls
    :param output_paths: local directory file names to write annual reports
    """
    
    # S3 Connect to load new files
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)

    # access bucket resources to check for existing files
    items = []
    try:
        for item in bucket.objects.all():
            items.append(item.key)
    except KeyError:
        pass

    for ind, url in enumerate(urls):
        # break after 3 pdfs
        if ind > 3:
            break
        
        # get directory to store annual report
        filename = output_paths[url]

        # ignore existing files
        if filename in items:
            print('file already downloaded: {}'.format(filename))
            continue
                
        # download pdf
        r = requests.get(url)
        print('downloaded: {}'.format(filename))

        # write pdf to s3 bucket
        bucket.put_object(Body=r.content, Bucket=BUCKET_NAME, Key=filename)

        # required delay, stated in the robots.txt
        time.sleep(5)  # five seconds

if __name__ == "__main__": main(event=None, context=None)



