import os
import csv
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
firebase_admin.initialize_app(cred, {
	'projectId': 'sportify-ab845'
})

db = firestore.client()

def getRowValues(row):
	items = ['court_id', 'name', 'tennis_court_area', 'park_name', 'address', 'district', 'ward',
	'primary_permitting_status', 'asset_category', 'lights', 'surface_material', 'GIS_coordinate']
	return {items[i]: row[i] for i in range(len(items))}

with open('toronto-courts-facilities-data.csv', 'r') as file:
	csv_reader = csv.reader(file, delimiter=',')
	docs = 0
	for row in csv_reader:
		if docs:
			values = getRowValues(row)
			doc_ref = db.collection(u'Locations').document(f'{values["court_id"]}')
			doc_ref.set({
				u'name': f'{values["name"]}',
				u'tennisCourtArea': f'{values["tennis_court_area"]}',
				u'parkName': f'{values["park_name"]}',
				u'address': f'{values["address"]}',
				u'district': f'{values["district"]}',
				u'ward': f'{values["ward"]}',
				u'primaryPermittingStatus': f'{values["primary_permitting_status"]}',
				u'assetCategory': f'{values["asset_category"]}',
				u'lights': f'{values["lights"]}',
				u'surfaceMaterial': f'{values["surface_material"]}',
				u'GISCoordinate': f'{values["GIS_coordinate"]}'
			})
		docs += 1

print(f'{docs} Documents Created')
