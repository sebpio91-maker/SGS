from pydantic import BaseModel, ConfigDict


class GenerateTestPlanRequest(BaseModel):
    product_id: int
    test_order_id: int | None = None
    selected_catalog_item_ids: list[int] = []
    selected_spec_requirement_ids: list[int] = []
    selected_special_item_eigenschaften: list[str] = []


class TestPlanItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    catalog_item_id: int | None
    category_name: str
    name: str
    norm_reference: str | None
    description: str | None
    result: str | None
    remarks: str | None
    lab_minutes: float | None
    lab_cost: float | None
    sale_price: float | None
    sort_order: int


class TestPlanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    product_id: int
    test_order_id: int | None
    status: str
    items: list[TestPlanItemOut]
    lab_minutes_total: float
    lab_cost_total: float
    sale_price_total: float

    @classmethod
    def from_model(cls, plan) -> "TestPlanOut":
        lab_minutes_total = sum((i.lab_minutes or 0) for i in plan.items)
        lab_cost_total = sum((i.lab_cost or 0) for i in plan.items)
        sale_price_total = sum((i.sale_price or 0) for i in plan.items)
        return cls(
            id=plan.id,
            customer_id=plan.customer_id,
            product_id=plan.product_id,
            test_order_id=plan.test_order_id,
            status=plan.status,
            items=[TestPlanItemOut.model_validate(i) for i in plan.items],
            lab_minutes_total=float(lab_minutes_total),
            lab_cost_total=float(lab_cost_total),
            sale_price_total=float(sale_price_total),
        )
