from bs4 import BeautifulSoup
import json
import re
import sys
from selenium import webdriver

def get_cafe_menu(date):
    url = "http://rose-hulman.cafebonappetit.com/cafe/"

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
    hours_selector = "#panel-cafe-hours .all-cafe-hours li"

    meal_panels = list()
    headers = list()
    for meal_panel in daypart_menu_panels:
        meal_panels.append(soup.select(meal_panel + " " + items_selector))
        headers.append(soup.select(meal_panel + " " +  heading_selector))

    # get the hours of each meal
    hours_panel = soup.select(hours_selector)
    hours_json = BeautifulSoup(str(hours_panel), 'html.parser')
    hours_json = hours_json.li['data-json']

    hours_json = json.loads(hours_json)

    meal_hours = list()
    for i in range(len(meal_panels)):
        if meal_panels[i] == [] or not date == "":
            continue;

        # only want the HH:MM am - HH:MM pm part
        hours_text = hours_json['dayparts'][i]['status']
        match = re.search('\d{1,2}:\d{2}.*-.*\d{1,2}:\d{2}_\D{2}', hours_text)

        if match:
            hours = match.string[match.start():match.end()]
            hours = hours.replace("_", " ")
            meal_hours.append(hours)

    meals = []
    for i in range(len(meal_panels)):
        if meal_panels[i] == []:
            continue;

        # get meal name
        meal_dict = {"name": "", "hours": "", "items": []}
        meal_name = BeautifulSoup(str(headers[i]), 'html.parser')
        meal_dict["name"] = meal_name.h2.get_text()

        if len(meal_hours) != 0:
            meal_dict['hours'] = meal_hours[i]
        else:
            meal_dict['hours'] = ""

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
