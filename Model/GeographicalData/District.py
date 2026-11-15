from pydantic import BaseModel, ConfigDict, Field

class District(BaseModel):
    model_config = ConfigDict(extra = "ignore", validate_by_name=True, validate_by_alias=True)

    name: str = Field(alias="nome")
    population: int | None = Field(default=None, alias="populacao")
    old_population: int | None = Field(default=None, alias="populacao_idosa")
    children_population: int | None = Field(default=None, alias="populacao_criancas")

    flood_reports: int | None = Field(default=None, alias="casos_alagamentos")
    hydrological_risk: float | None = Field(default=None, alias="risco_hidrologico")
    hydrological_risk_level: str = Field(default="Não Identificado", alias="nivel_risco_hidrologico")

    data_years: list[int] = Field(default=[], alias="anos_informacoes")