from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.order import TestOrder
from app.models.plan import TestPlan
from app.models.product import Product
from app.models.user import User
from app.schemas.test_plan import GenerateTestPlanRequest, TestPlanOut
from app.services.plan_generator import generate_test_plan

router = APIRouter(
    prefix="/test-plans", tags=["test-plans"], dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=list[TestPlanOut])
def list_test_plans(
    customer_id: int | None = Query(default=None),
    product_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(TestPlan)
    if customer_id is not None:
        query = query.filter(TestPlan.customer_id == customer_id)
    if product_id is not None:
        query = query.filter(TestPlan.product_id == product_id)
    plans = query.order_by(TestPlan.created_at.desc()).all()
    return [TestPlanOut.from_model(p) for p in plans]


@router.get("/{test_plan_id}", response_model=TestPlanOut)
def get_test_plan(test_plan_id: int, db: Session = Depends(get_db)):
    plan = db.get(TestPlan, test_plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Prüfplan nicht gefunden")
    return TestPlanOut.from_model(plan)


@router.post("/generate", response_model=TestPlanOut, status_code=201)
def generate(
    payload: GenerateTestPlanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = db.get(Product, payload.product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden")

    test_order = None
    if payload.test_order_id is not None:
        test_order = db.get(TestOrder, payload.test_order_id)
        if test_order is None:
            raise HTTPException(status_code=404, detail="Prüfauftrag nicht gefunden")
        if test_order.product_id != product.id:
            raise HTTPException(
                status_code=400, detail="Prüfauftrag gehört nicht zu diesem Produkt"
            )

    plan = generate_test_plan(
        db,
        product=product,
        test_order=test_order,
        selected_catalog_item_ids=payload.selected_catalog_item_ids,
        selected_spec_requirement_ids=payload.selected_spec_requirement_ids,
        selected_special_item_eigenschaften=payload.selected_special_item_eigenschaften,
        created_by_id=current_user.id,
    )
    return TestPlanOut.from_model(plan)
