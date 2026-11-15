from pydantic import BaseModel, ConfigDict, Field

class BusStation(BaseModel):
    model_config = ConfigDict(extra = "ignore", validate_by_name=True, validate_by_alias=True)

    stop_id: str = Field(alias="id_ponto")
    name: str = Field(alias="nome")
    latitude: float
    longitude: float

    lines: list[dict] = Field(default=[], alias="linhas")