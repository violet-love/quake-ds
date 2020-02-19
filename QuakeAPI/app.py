from flask import Flask, jsonify
from .USGSetl import *


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return 'success, the flask API is running'

    @app.route('/lastQuake')
    def lastQuake():
        curs = CONN.cursor()
        response = curs.execute('''
            SELECT * FROM USGS
            ORDER BY Time Desc
            limit 1;
        ''')
        quake = curs.fetchone()[1:]
        response = {'id': quake[0],
                    'place': quake[1],
                    'lat': quake[2],
                    'lon': quake[3],
                    'mag': quake[4],
                    'Oceanic': quake[5]}
        return jsonify(response)

    @app.route('/last/<time>')
    def getTime(time):
        '''for now this is a super simple function that just uses the USGS API to
        get the last however many quakes. In a future release this will need to
        be improved to read out of our database'''
        if time.upper() not in ['HOUR', 'DAY', 'WEEK', 'MONTH']:
            return 'Please select from hour, day, week, or month'
        else:
            return jsonify(get_recent_quakes(os.environ[time.upper()]))

    @app.route('/history/<lat>,<lon>,<dist>')
    def history(lat, lon, dist):
        # oof I just googled it and this is gonna be rough
        pass

    return app