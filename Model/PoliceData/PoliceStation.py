from Model.PoliceData.PoliceReport import PoliceReport
from pydantic import BaseModel, ConfigDict, Field

class PoliceStation(BaseModel):
    model_config = ConfigDict(extra = "ignore", validate_by_name=True, validate_by_alias=True)

    dp_number: int = Field(alias="numero_dp")
    name: str = Field(alias="nome")
    address: str = Field(alias="endereco")
    station_type: str = Field(alias="classe")

    reports: list[PoliceReport] | None = Field(default=[], alias="casos")