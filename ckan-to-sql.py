import sqlite3
import csv

conn = sqlite3.connect('locations.db')

c = conn.cursor()

def get_values_for_row(row):
	return [row[x] for x in range(len(row))]

with open('toronto-courts-facilities-data.csv', 'r') as file:
	csv_reader = csv.reader(file, delimiter=',')
	records = 0
	for row in csv_reader:
		values = get_values_for_row(row)
		c.execute('''
			INSERT INTO locations(court_id, name, tennis_court_area, park_name, address, district, ward,
					primary_permitting_status, asset_category, lights, surface_material, GIS_coordinate)
			VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
			'''	, (values[0], values[1], values[2], values[3], values[4], values[5],
				values[6], values[7], values[8], values[9], values[10], values[11]))
		conn.commit()
		records += 1

conn.close()
print('\n{} Records Transferred'.format(records))