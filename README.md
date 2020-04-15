# Propertyscraper
A webscraper that scrapes rental properties offered on the Zoopla website. It requires a specific text file with the areas that are required to be scraped to be input to the script. The scraper outputs a .CSV file with location data, address, number of bedrooms, bathrooms and reception rooms, url, as well as the monthly rental price.

The scraper has two scripts. The first, processinput.py, will take a list of suburbs in London and process them to make sure there is some data to be scraped on the other end. Once this pre-scraping check has been done, the output file can be fed through the zooploop.py script. This will scrape the required info from the website and feed it into an output CSV file that an then be added to a GIS program or analysed as needed. 
