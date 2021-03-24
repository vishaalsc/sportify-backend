import time
import random
import requests
from locust import HttpUser, task, between

class LocationData:
	def __init__(self):
		self.base_url = "http://localhost:5000/api"
		self.parks_url = self.base_url + "/parks/all"
		self.districts_url = self.base_url + "/districts/all"

	def get_random_park(self):
		res = requests.get(self.parks_url).json()
		if res:
			return random.choice(res)["park_name"]

	def get_random_district(self):
		res = requests.get(self.districts_url).json()
		if res:
			return random.choice(res)["district"]

class SportifyUser(HttpUser):
	wait_time = between(1, 2.5)

	locationData = LocationData()

	@task
	def lorem_ipsum(self):
		self.client.get("/")

	@task
	def get_all_locations(self):
		self.client.get("/api/locations/all")

	@task
	def get_park_location(self):
		park_name = self.locationData.get_random_park()
		self.client.get(
			"/api/locations/parks/?name={}"
			.format(park_name))

	@task
	def get_district_location(self):
		district = self.locationData.get_random_district()
		self.client.get(
			"/api/locations/districts?name={}"
			.format(district))