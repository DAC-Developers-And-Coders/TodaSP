from pydantic import BaseModel, ConfigDict, Field

class PoliceReport(BaseModel):
    model_config = ConfigDict(extra = "ignore", validate_by_name=True, validate_by_alias=True)

    nature_id: int = Field(alias="id_natureza")
    nature: str = Field(alias="natureza")
    last_month_reports: int = Field(alias="quantidade_ultimo_mes")
    year_reports: int = Field(alias="quantidade_ultimo_ano")
    year: int = Field(alias="ano")