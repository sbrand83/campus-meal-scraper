from bs4 import BeautifulSoup
import json
import re
import sys
from selenium import webdriver

def get_cafe_menu(date):
    url = "http://rose-hulman.cafebonappetit.com/cafe/cafe/"

    driver = webdriver.PhantomJS()

    url = url + date
    print("Requesting " + url)
    driver.get(url)
    print("Retrieving page...")

    print("Scraping meal information...")
    menu_page = driver.page_source
    driver.close()
    soup = BeautifulSoup(menu_page, 'html.parser')

    daypart_menu_panels = list()
    for i in range(1, 5):
        daypart_menu_panels.append("#panel-daypart-menu-{}".format(i))

    heading_selector = ".daypart-header .panel-title"
    items_selector = "article .daypart-menu .column article"
    hours_selector = "#panel-cafe-hours .cafe-details ul"

    meal_panels = list()
    headers = list()
    for meal_panel in daypart_menu_panels:
        meal_panels.append(soup.select(meal_panel + " " + items_selector))
        headers.append(soup.select(meal_panel + " " +  heading_selector))

    # get the hours of each meal
    meal_info = get_meal_name_and_hours(hours_selector, soup)

    meals = []
    for i in range(len(meal_panels)):
        if meal_panels[i] == []:
            continue;

        meal_dict = {"name": "", "hours": "", "items": []}

        meal_dict['hours'] = meal_info[i]['hours']
        meal_dict['name'] = meal_info[i]['name']

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
