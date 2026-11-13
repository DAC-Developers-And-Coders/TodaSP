from pydantic import BaseModel, ConfigDict

class Subprefecture(BaseModel):
    model_config = ConfigDict(extra = "ignore")

    name: str
    hydrological_risk_area: float
    data_years: list[int]