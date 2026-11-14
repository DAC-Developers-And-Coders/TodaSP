from pydantic import BaseModel, ConfigDict, Field

class HealthFacility(BaseModel):
    model_config = ConfigDict(extra="ignore", validate_by_name=True, validate_by_alias=True)

    cnes_id: int
    legal_name: str | None = Field(default="Não identificado", alias="razao_social")
    trade_name: str | None = Field(default="Não identificado", alias="nome_fantasia")
    desc_administrative_sphere: str = Field(alias="esfera_administrativa")
    facility_code: int | None = Field(default=None, alias="codigo_tipo")
    facility_type: str | None = Field(default="Não identificado", alias="tipo")
    cep: str
    address: str = Field(alias="endereco")
    number: str | None = Field(default=None, alias="numero")
    neighborhood: str | None = Field(default=None, alias="bairro")
    latitude: float | None = Field(default=None, alias="latitude")
    longitude: float | None = Field(default=None, alias="longitude")
    desc_legal_nature: str | None = Field(default=None, alias="codigo_natureza_juridica")
    legal_nature: str | None = Field(default="Não identificado", alias="natureza_juridica")
    update_date: str | None = Field(default=None, alias="data_informacoes")