from pydantic import BaseModel, ConfigDict

from app.schemas.product import ProductOut


class TestOrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    product_id: int | None
    order_number: str | None
    source: str
    original_filename: str | None
    status: str
    raw_data: dict | None


class LidlImportResult(BaseModel):
    product: ProductOut
    test_order: TestOrderOut
    pruefumfang_kategorien: list[str]
    referenzpruefung: bool
    ngo_pruefung: bool
    ffu_pruefung: bool
