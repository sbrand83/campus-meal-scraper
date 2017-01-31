from bs4 import BeautifulSoup
import json
import re
from selenium import webdriver

def get_all_locations(date):
    locations = [
        {"name": "Union Cafe", "url_path": "cafe/"},
        {"name": "Logan's", "url_path": "logans/"},
        {"name": "Faculty Dining Room", "url_path": "faculty-dining-room/"},
        {"name": "C-Store", "url_path": "c-store/"},
        {"name": "Moench", "url_path": "moench/"},
        {"name": "Subway", "url_path": "subway/"},
    ]

    location_data = []

    for location in locations:
        mealtimes = get_location_meal_times(location['url_path'], date)
        loc = {"name": location['name'], "mealTimes": mealtimes}
        location = {"location": loc}
        location_data.append(location)

    return location_data

def get_location_meal_times(url_path, date):
    url = "http://rose-hulman.cafebonappetit.com/cafe/"
    url = url + url_path + date

    menu_page = get_page_html(url)
    soup = BeautifulSoup(menu_page, 'html.parser')

    daypart_menu_panels = list()
    for i in range(1, 5):
        daypart_menu_panels.append("#panel-daypart-menu-{}".format(i))

    items_selector = "article .daypart-menu .column article"
    hours_selector = "#panel-cafe-hours .cafe-details ul"

    meal_panels = list()
    for meal_panel in daypart_menu_panels:
        panel = (soup.select(meal_panel + " " + items_selector))
        if len(panel) != 0:
            meal_panels.append(panel)

    # get the hours of each meal
    meal_info = get_meal_name_and_hours(hours_selector, soup)

    meals = []
    print(len(meal_info))
    for i in range(len(meal_info)):
        meal_dict = {"name": "", "hours": "", "items": []}

        meal_dict['hours'] = meal_info[i]['hours']
        meal_dict['name'] = meal_info[i]['name']

        # may not find meal on site, if so do nothing,
        # and return with empty items array
        try:
            panel = meal_panels[i]
        except IndexError:
            print("Number of meal hours don't match number of meal panels")
            meals.append(meal_dict)
            continue

        # get each item's name, icons, and calories
        for item in meal_panels[i]:
            item = BeautifulSoup(str(item), 'html.parser')
            item_name = item.span
            item_icons = item.select(".station-item-title .cor-icons")

            icons = BeautifulSoup(str(item_icons), 'html.parser')
            icon_titles = list(img.get('title') for img in icons.find_all('img'))

            calories = item.select('ul .nutrition span')
            calories = BeautifulSoup(str(calories), 'html.parser')
            calories = calories.get_text()

            item_name = item_name.get_text().strip()
            item = {"name": item_name, "icons": icon_titles, "calories": calories}
            meal_dict["items"].append(item)
        meals.append(meal_dict)

    return meals

def get_page_html(url):
    driver = webdriver.PhantomJS()

    print("Requesting " + url)
    driver.get(url)
    print("Retrieving page...")

    print("Scraping meal information...")
    menu_page = driver.page_source
    driver.close()
    return menu_page



def get_meal_name_and_hours(selector, page):
    hours_list = page.select(selector)
    hours_json = BeautifulSoup(str(hours_list), 'html.parser')
    hours_json = hours_json.ul.find_all('li')
    meal_info = []
    for element in hours_json:
        spans = element.find_all('span')
        meal = dict({"name": spans[0].get_text(), "hours": spans[1].get_text()})
        match = re.search('\d{1,2}:\d{2}.*-.*\d{1,2}:\d{2} \D{2}', meal['hours'])

        if match:
            hours = match.string[match.start():match.end()]
            meal['hours'] = hours
        meal_info.append(meal)
    return meal_info
