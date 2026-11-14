from pydantic import BaseModel, ConfigDict
from Model.PoliceReport import PoliceReport

class PoliceStation(BaseModel):
    model_config = ConfigDict(extra = "ignore")

    dp_number: int
    name: str
    address: str
    station_type: str

    reports = list[PoliceReport]