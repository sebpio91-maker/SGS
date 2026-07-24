from pydantic import BaseModel, ConfigDict


class CustomerBase(BaseModel):
    name: str
    code: str
    notes: str | None = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    notes: str | None = None


class CustomerOut(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
