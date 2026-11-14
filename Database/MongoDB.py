from pymongo import MongoClient
from Model.District import District
from Model.PoliceReport import PoliceReport
from Model.Subprefecture import Subprefecture
from Model.PoliceStation import PoliceStation
from Model.HealthFacility import HealthFacility

class MongoDB:
    def __init__(self):
        self.uri = "mongodb://localhost:27017"

        self.client = MongoClient(self.uri)
        self.database = self.client['todasp']

        self.database['health_facilities'].create_index("cnes_id", unique=True)
        self.database['police_stations'].create_index("numero_dp", unique=True)
        self.database['subprefectures'].create_index("nome", unique=True)
        self.database['districts'].create_index("nome", unique=True)

    def insert_health_facility(self, health_facility: HealthFacility):
        collection = self.database['health_facilities']
        facility = health_facility.model_dump(by_alias=True)

        collection.update_one({"cnes_id": facility["cnes_id"]}, {"$set": facility}, upsert=True)

    def insert_police_station(self, police_station: PoliceStation):
        collection = self.database['police_stations']
        station = police_station.model_dump(by_alias=True, exclude={"reports"})

        collection.update_one({"numero_dp": station["numero_dp"]}, {"$set": station}, upsert=True)

    def insert_police_station_reports(self, number: int, reports: list[PoliceReport]):
        collection = self.database['police_stations']

        collection.update_one({"numero_dp": number}, {"$set": {"casos": [
            report.model_dump(by_alias=True) for report in reports
        ]}}, upsert=False)

    def insert_district(self, district: District):
        collection = self.database['districts']
        data = district.model_dump(by_alias=True)

        collection.update_one({"nome": data["nome"]}, {"$set": data}, upsert=True)

    def insert_subprefecture(self, subprefecture: Subprefecture):
        collection = self.database['subprefectures']
        data = subprefecture.model_dump(by_alias=True)

        collection.update_one({"nome": data["nome"]}, {"$set": data}, upsert=True)