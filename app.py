from flask import Flask
from flask import json
from flask import Response
from menu_scraper import get_cafe_menu


app = Flask(__name__)

@app.route('/cafe/<date>/')
def get_todays_menu(date=""):
    data = get_cafe_menu(date)
    return Response(json.dumps(data), mimetype='application/json')

app.run()
