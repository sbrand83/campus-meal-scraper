import menu_scraper
import time
from datetime import date, timedelta

def scrape_site():
    current_date = date.today()
    td = timedelta(days=1)
    dates = []

    dates.append(current_date.isoformat())
    for i in range(6):
        new_date = current_date + td
        print(new_date.isoformat())
        dates.append(new_date.isoformat())
        current_date = new_date

    for day in dates:
        data = menu_scraper.get_all_locations(day)
        menu_scraper.write_data_to_file(data, day)

if __name__ ==  "__main__":
    scrape_site()
