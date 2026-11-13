from pydantic import BaseModel, ConfigDict

class District(BaseModel):
    model_config = ConfigDict(extra = "ignore")

    name: str
    population: int
    old_population: int
    children_population: int

    flood_reports: int
    hydrological_risk: float
    hydrological_risk_level: str

    data_years: list[int]