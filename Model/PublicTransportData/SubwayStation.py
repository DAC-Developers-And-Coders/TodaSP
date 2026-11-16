from pydantic import BaseModel, ConfigDict, Field

class SubwayStation(BaseModel):
    model_config = ConfigDict(extra = "ignore", validate_by_name=True, validate_by_alias=True)

    name: str = Field(alias="nome")
    address: str = Field(alias="endereco")
    operating_hours: str = Field(default="Não identificado", alias="horario_funcionamento")
    transfers: str = Field(default="Não identificado", alias="integracoes")
    info_date: str = Field(default="Não identificado", alias="data_informacoes")

    lines: list[str]= Field(default=[], alias="linhas")