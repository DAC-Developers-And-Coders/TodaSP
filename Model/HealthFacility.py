from pydantic import BaseModel, ConfigDict

class HealthFacility(BaseModel):
    model_config = ConfigDict(extra = "ignore")

    cnes_id: int
    legal_name: str | None = "Não identificado"
    trade_name: str | None = "Não identificado"
    desc_administrative_sphere: str
    facility_code: int | None = None
    facility_type: str | None = "Não identificado"
    cep: str
    address: str
    number: str | None = None
    neighborhood: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    desc_legal_nature: str | None = None
    legal_nature: str | None = "Não identificado"
    update_date: str | None = None