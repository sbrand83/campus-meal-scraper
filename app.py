from flask import Flask
from flask import json
from flask import Response
from menu_scraper import get_all_locations

app = Flask(__name__)

@app.route('/locations/<date>/')
def get_todays_menu(date=""):
    data = get_all_locations(date)
    return Response(json.dumps(data), mimetype='application/json')

if __name__ == "__main__":
    app.run()
