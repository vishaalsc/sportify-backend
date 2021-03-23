import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config['DEBUG'] = True

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

@app.route('/', methods=['GET'])
def home():
	return 'Lorem ipsum'

@app.route('/api/locations/all', methods=['GET'])
def locations_all():
	conn = sqlite3.connect('locations.db')
	conn.row_factory = dict_factory

	c = conn.cursor()
	locations = c.execute('SELECT * FROM locations;').fetchall()

	return jsonify(locations)

@app.errorhandler(404)
def page_not_found(e):
	return "Resource not found"

app.run()