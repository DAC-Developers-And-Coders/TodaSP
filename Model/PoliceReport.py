from pydantic import BaseModel, ConfigDict

class PoliceReport(BaseModel):
    model_config = ConfigDict(extra = "ignore")

    id: int
    last_month_reports: int
    year_reports: int
    year: int