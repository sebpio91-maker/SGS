from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    customer_id: int
    article_number: str
    name: str
    category: str | None = None
    has_battery: bool = False
    has_manual: bool = False
    specification: dict | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    customer_id: int | None = None
    article_number: str | None = None
    name: str | None = None
    category: str | None = None
    has_battery: bool | None = None
    has_manual: bool | None = None
    specification: dict | None = None


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
