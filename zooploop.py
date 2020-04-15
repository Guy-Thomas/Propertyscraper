import math
import csv
import requests
from bs4 import BeautifulSoup as bs

global counter
counter = 1


def zooplaScrape():
    with open('processedAreas_remains.txt', 'r') as fh:
        #Outer loop through subBouroughs file
        pathdict = {
            "page_size": "100",
            "price_frequency": "per_month",
            "include_shared_accommodation": "false"
        }
        pathbase = 'http://www.zoopla.co.uk/to-rent/property/'


        for i in fh:
            rpath = pathbase + str(i).replace('\n', '') + '/'
            print(rpath)
            src = requests.get(rpath, params=pathdict)
            pageLength = scrapeLengths(src)
            for listLen in range(1, pageLength+1):
                pathdict2 = {
                    "pn" : listLen,
                    "page_size": "100",
                    "price_frequency": "per_month",
                    "include_shared_accommodation": "false"
                }
                pageLists = requests.get(rpath, params=pathdict2)
                scrape(pageLists.url)



#get listing lengths
def scrapeLengths(path):
    #scrape the urls here
    result = path.content
    soup = bs(result, 'lxml')
    count = soup.find_all('span', class_="listing-results-utils-count")
    #count = soup.body.find_all('span', class_="listing-results-utils-count")
    #print(path.url)
    print(count)
    try:
        x = count[0].get_text()
    except:
        x = '100'
        print('error: set to 100')
    #print(x)
    v = x.split(' ')
    t = str(v[-1]).strip('+')
    no = t.replace(',', '')
    #print(no)
    pRange = math.ceil(float(no)/100)
    print(pRange)
    return pRange
#loop through the listing range

#scrape each list

def scrape(path):
    result = requests.get(path)
    src = result.content
    soup = bs(src, 'lxml')

    listing = soup.body.find('ul', class_="listing-results clearfix js-gtm-list")
    prop = listing.find_all('li', class_="srp clearfix")

    result = []

    for i in prop:
        # Address
        addresssoup = i.div.find_all('a', class_="listing-results-address")
        address = addresssoup[0].text
        addresssplit = address.split(', ', 3)


        #address1 = addresssplit[-3]
        #address2 = addresssplit[-2]
        #address3 = addresssplit[-1]

        rooms = i.find_all('h3', class_="listing-results-attr")
        # bedrooms
        bedssoup = i.find('span', class_="num-icon num-beds")
        if bedssoup is not None:
            beds = bedssoup.text
            # baths = bathssoup.text
        else:
            beds = 'None'

        # bathrooms
        bathssoup = i.find('span', class_="num-icon num-baths")
        if bathssoup is not None:
            baths = bathssoup.text
        else:
            baths = None

        # reception rooms
        recepsoup = i.find('span', class_="num-icon num-reception")
        if recepsoup is not None:
            recep = recepsoup.text
        else:
            recep = None

        # Price pm
        pricesoup = i.find('a', class_="listing-results-price text-price")
        price = pricesoup.get_text(",", strip=True)
        price_Int = (price.split(' ')[0].strip('£,')).replace(',', '')

        # co-ordinates
        listsoup = i.find('a', class_="listing-results-price text-price")['href']
        base = 'http://www.zoopla.co.uk'
        XY = base + str(listsoup)
        xypage = requests.get(XY)
        XYsrc = xypage.content
        # html.body.main.div[2].div[1].div[3].section[2].div[1].div[2].div.div.div[2].a
        spatialsoup = bs(XYsrc, 'lxml')
        #link = spatialsoup.find('img', class_="js-lazy ui-static-map__img")['data-src']
        link = tryscrape(spatialsoup)
        #print(link)
        linkstring = str((str(link).split('&')[0]).split('=')[-1])
        xy = linkstring.split(',')
        long = xy[0]
        lat = xy[1]




        roomdict = {
            'address1': addresssplit,
            #'address2': address2,
            #'address3': address3,
            'bedrooms': beds,
            'bathrooms': baths,
            'reception': recep,
            'price': price_Int,
            'lat': lat,
            'long': long,
            'page_url': xypage.url,
        }

        print(roomdict)
        result.append(roomdict)
    write2CSV(result, roomdict)

def write2CSV(testCSV, dict):

    testCSVKeys = dict.keys()
    with open('resultsRaw/CENTRAL_RAW/resultsremains.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=testCSVKeys)
        writer.writeheader()
        for i in testCSV:
            writer.writerow(i)
def tryscrape(url):
    try:
        link = url.find('img', class_="js-lazy ui-static-map__img")['data-src']
        return link
    except:
        link = '=0,0&'
        return link

zooplaScrape()