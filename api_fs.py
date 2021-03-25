import os
import flask
from flask import request, jsonify
from firebase_admin import credentials, firestore, initialize_app

"""
Setup Flask app and Firestore DB
"""
app = flask.Flask(__name__)
app.config['DEBUG'] = True

cred = credentials.Certificate(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
sportify_app = initialize_app(cred)
db = firestore.client()
locations_ref = db.collection('Locations')

"""
API routing for location data
"""
@app.route('/', methods=['GET'])
def home():
	return 'Lorem ipsum'

@app.route('/api/locations/all', methods=['GET'])
def locations_all():
	locations = [doc.to_dict() for doc in locations_ref.stream()]
	return jsonify(locations), 200

@app.route('/api/locations/parks/', methods=['GET'])
def locations_parks():
	if request.args:
		park_name = request.args.get('name')
		docs = locations_ref.where(u'parkName', u'==', park_name)
		parks = [doc.to_dict() for doc in docs.stream()]
		return jsonify(parks), 200
	return "No park name specified"

@app.route('/api/parks/all', methods=['GET'])
def parks_all():
	docs = [doc.to_dict() for doc in locations_ref.stream()]
	parks = {}
	if docs:
		for d in docs:
			name = d['parkName']
			if name in parks:
				parks[name] += 1
			else:
				parks[name] = 0
	return jsonify(parks), 200

@app.route('/api/locations/districts/', methods=['GET'])
def locations_districts():
	if request.args:
		district = request.args.get('name')
		docs = locations_ref.where(u'district', u'==', district)
		districts = [doc.to_dict() for doc in doc.stream()]
		return jsonify(districts), 200

@app.route('/api/districts/all', methods=['GET'])
def districts_all():
	docs = [doc.to_dict() for doc in locations_ref.stream()]
	districts = {}
	if docs:
		for d in docs:
			name = d['district']
			if name in districts:
				districts[name] += 1
			else:
				districts[name] = 0
	return jsonify(districts), 200

"""
Run Flask app
"""
app.run(host='0.0.0.0', port=5001)
