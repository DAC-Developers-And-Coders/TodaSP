from pydantic import BaseModel, ConfigDict, Field, field_validator

class HealthFacility(BaseModel):
    model_config = ConfigDict(extra="ignore", validate_by_name=True, validate_by_alias=True)

    cnes_id: int
    legal_name: str = Field(default="Não identificado", alias="razao_social")
    trade_name: str = Field(default="Não identificado", alias="nome_fantasia")
    desc_administrative_sphere: str = Field(alias="esfera_administrativa")
    facility_code: int | None = Field(default=None, alias="codigo_tipo")
    facility_type: str = Field(default="Não identificado", alias="tipo")
    cep: str
    address: str = Field(alias="endereco")
    number: str | None = Field(default=None, alias="numero")
    neighborhood: str = Field(default="Não identificado", alias="bairro")
    latitude: float | None = Field(default=None, alias="latitude")
    longitude: float | None = Field(default=None, alias="longitude")
    desc_legal_nature: str | None = Field(default=None, alias="codigo_natureza_juridica")
    legal_nature: str = Field(default="Não identificado", alias="natureza_juridica")
    update_date: str | None = Field(default=None, alias="data_informacoes")

    @field_validator(
        "legal_name",
        "trade_name",
        "facility_type",
        "neighborhood",
        "legal_nature",
        mode="before",
    )

    @classmethod
    def set_default_if_none(cls, value):
        return value if value is not None else "Não identificado"