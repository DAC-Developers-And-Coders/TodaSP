from pymongo import MongoClient
from Model.HealthFacility import HealthFacility

class MongoDB:
    def __init__(self):
        self.uri = "mongodb://localhost:27017"

        self.client = MongoClient(self.uri)
        self.database = self.client['todasp']

        self.database['health_facilities'].create_index("cnes_id", unique=True)

    def insert_health_facility(self, health_facility: HealthFacility):
        collection = self.database['health_facilities']
        facility = health_facility.model_dump(by_alias=True)

        collection.update_one({"cnes_id": facility["cnes_id"]}, {"$set": facility}, upsert=True)