from datetime import date, timedelta
import time
import urllib2

def scrape_site():
    production_url = 'https://campus-meal-scraper.herokuapp.com/locations/'
    dev_url = 'http://localhost:5000/locations/'

    url = production_url

    current_date = date.today()
    td = timedelta(days=1)
    dates = []
    days_to_refresh = 9

    dates.append(current_date.isoformat())
    print(current_date.isoformat())
    for i in range(days_to_refresh):
        new_date = current_date + td
        print(new_date.isoformat())
        dates.append(new_date.isoformat())
        current_date = new_date

    for day in dates:
        print('Requesting ' + url + day + '/')
        urllib2.urlopen(url + day + '/')

if __name__ ==  "__main__":
    scrape_site()
