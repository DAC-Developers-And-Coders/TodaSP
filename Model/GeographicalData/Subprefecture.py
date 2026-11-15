from pydantic import BaseModel, ConfigDict, Field

class Subprefecture(BaseModel):
    model_config = ConfigDict(extra = "ignore", validate_by_name=True, validate_by_alias=True)

    name: str = Field(alias="nome")
    hydrological_risk_area: float | None = Field(default=None, alias="area_risco_hidrologico")
    data_years: list[int] = Field(default=[], alias="anos_informacoes")