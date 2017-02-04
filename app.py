from flask import Flask
from flask import json
from flask import Response
from menu_scraper import (
    check_if_cached,
    get_all_locations,
    read_data_file,
    write_data_to_file,
)

app = Flask(__name__)

@app.route('/locations/<date>/')
def get_todays_menu(date=""):
    data = None
    if (check_if_cached(date)):
        data = read_data_file(date)
    else:
        data = get_all_locations(date)
        write_data_to_file(data, date)
    return Response(json.dumps(data), mimetype='application/json')

if __name__ == "__main__":
    app.run()
