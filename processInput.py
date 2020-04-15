import requests
from bs4 import BeautifulSoup as bs

def input(file):
    with open(file, 'r') as In_Put:
        pathdict = {
            "page_size": "100",
            "price_frequency": "per_month",
            "include_shared_accommodation": "false"
        }
        pathbase = 'http://www.zoopla.co.uk/to-rent/property/'
        for i in In_Put:
            url = ((str(i).strip("'")).replace('\n', '')).replace(' ', '-')
            rpath = pathbase + url + '/'
            result = requests.get(rpath, params=pathdict)
            srs = result.content
            soup = bs(srs, 'lxml')
            count = soup.find_all('span', class_="listing-results-utils-count")
            print(count)
            if count == []:
                r = 'london/' + url
                writeOutput(r)
                print(r)
            else:
                writeOutput(url)
                print(url)

def writeOutput(r):
    with open('processedAreas_' + x + '.txt', 'a') as output:
        output.write(r + '\n')


x = 'remains'

input((x + '.txt'))