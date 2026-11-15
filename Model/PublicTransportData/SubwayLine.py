from pydantic import BaseModel, ConfigDict, Field

class SubwayLine(BaseModel):
    model_config = ConfigDict(extra = "ignore", validate_by_name=True, validate_by_alias=True)

    line_number: int = Field(alias="numero_linha")
    name: str = Field(alias="nome")
    label: str = Field(alias="rotulo")
    color: str = Field(alias="cor")
    status: str
    operator: str = Field(alias="operadora")
    update_date: str = Field(alias="data_atualizacao")

    route: list[dict] = Field(default=[], alias="rota")