import sqlite3
import csv

conn = sqlite3.connect('locations.db')

c = conn.cursor()

with open('toronto-courts-facilities-data.csv', 'r') as file:
	csv_reader = csv.reader(file, delimiter=',')
	records = 0
	for row in csv_reader:
		if records:
			c.execute('''
				INSERT INTO locations(court_id, name, tennis_court_area, park_name, address, district,
				ward, primary_permitting_status, asset_category, lights, surface_material, GIS_coordinate)
				VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
				'''	, row)
			conn.commit()
		records += 1

conn.close()
print(f'\n{records} Records Transferred')
