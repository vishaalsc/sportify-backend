import sqlite3
import flask
from flask import g, request, jsonify

"""
Setup Flask app and SQLite DB
"""
app = flask.Flask(__name__)
app.config['DEBUG'] = True

DATABASE = 'locations.db'

def dict_factory(cursor, row):
	return dict((cursor.description[idx][0], value)
		for idx, value in enumerate(row))

def get_db():
	db = getattr(g, '_database', None)
	if not db:
		db = g._database = sqlite3.connect(DATABASE)
	db.row_factory = dict_factory
	return db

"""
API routing for location data
"""
@app.route('/', methods=['GET'])
def home():
	return 'Lorem ipsum'

@app.route('/api/locations/all', methods=['GET'])
def locations_all():
	c = get_db().cursor()
	locations = c.execute('SELECT * FROM locations;').fetchall()
	return jsonify(locations)

@app.route('/api/locations/parks/', methods=['GET'])
def locations_parks():
	c = get_db().cursor()
	if request.args:
		park_name = request.args.get('name')
		parks = c.execute('''
			SELECT * FROM locations WHERE park_name LIKE ?;
		''', (f'%{park_name}%',)).fetchall()
		return jsonify(parks)
	return "No park name specified"

@app.route('/api/parks/all', methods=['GET'])
def parks_all():
	c = get_db().cursor()
	parks = c.execute('SELECT DISTINCT park_name FROM locations;').fetchall()
	return jsonify(parks)

@app.route('/api/locations/districts/', methods=['GET'])
def locations_districts():
	c = get_db().cursor()
	if request.args:
		district = request.args.get('district')
		districts = c.execute('''
			SELECT * FROM locations WHERE district LIKE ?;
		''', (f'%{district}%',)).fetchall()
		return jsonify(districts)
	return "No district specified"

@app.route('/api/districts/all', methods=['GET'])
def districts_all():
	c = get_db().cursor()
	districts = c.execute('SELECT DISTINCT district FROM locations;').fetchall()
	return jsonify(districts)

"""
DB close and app error handling
"""
@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db:
		db.close()

@app.errorhandler(404)
def page_not_found(e):
	return "Resource not found", 404

app.run()
