import io

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.lidl_pdf_parser import parse_pruefauftrag
from app.models.customer import Customer
from app.models.order import TestOrder
from app.models.product import Product
from app.schemas.test_order import LidlImportResult, TestOrderOut

router = APIRouter(
    prefix="/test-orders", tags=["test-orders"], dependencies=[Depends(get_current_user)]
)

LIDL_CUSTOMER_CODE = "LIDL"

# Diese Felder aus dem Parser-Ergebnis fließen in die Produkt-Spezifikation;
# raw_fields/raw_text sind nur für das Audit-Trail im TestOrder relevant.
_PRODUCT_SPEC_KEYS = [
    "auftraggeber",
    "datum",
    "artikelkategorie",
    "lieferant",
    "lieferant_ansprechpartner",
    "produktionsstaette",
    "herkunftsland",
    "maße",
    "gewicht",
    "material",
    "materialstaerke",
    "farbe",
    "zertifizierungen",
    "verpackung",
]


@router.get("", response_model=list[TestOrderOut])
def list_test_orders(
    customer_id: int | None = Query(default=None), db: Session = Depends(get_db)
):
    query = db.query(TestOrder)
    if customer_id is not None:
        query = query.filter(TestOrder.customer_id == customer_id)
    return query.order_by(TestOrder.created_at.desc()).all()


@router.get("/{test_order_id}", response_model=TestOrderOut)
def get_test_order(test_order_id: int, db: Session = Depends(get_db)):
    test_order = db.get(TestOrder, test_order_id)
    if test_order is None:
        raise HTTPException(status_code=404, detail="Prüfauftrag nicht gefunden")
    return test_order


@router.post("/import-lidl", response_model=LidlImportResult, status_code=status.HTTP_201_CREATED)
async def import_lidl_pruefauftrag(file: UploadFile, db: Session = Depends(get_db)):
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Nur PDF-Dateien werden unterstützt")

    content = await file.read()
    try:
        parsed = parse_pruefauftrag(io.BytesIO(content))
    except Exception as exc:  # PDF ist kein gültiges/lesbares PDF
        raise HTTPException(status_code=422, detail=f"PDF konnte nicht gelesen werden: {exc}")

    if not parsed.get("ian_charge"):
        raise HTTPException(
            status_code=422,
            detail="IAN/Charge konnte nicht aus dem PDF extrahiert werden – "
            "entspricht die Datei dem erwarteten Lidl-Prüfauftrags-Format?",
        )

    customer = db.query(Customer).filter_by(code=LIDL_CUSTOMER_CODE).one_or_none()
    if customer is None:
        raise HTTPException(
            status_code=500,
            detail="Kunde 'LIDL' nicht gefunden – bitte zuerst Seed-Skript ausführen",
        )

    article_number = parsed["ian_charge"]
    product = (
        db.query(Product)
        .filter_by(customer_id=customer.id, article_number=article_number)
        .one_or_none()
    )
    if product is None:
        product = Product(customer_id=customer.id, article_number=article_number, name="")
        db.add(product)

    product.name = parsed.get("artikelbezeichnung") or article_number
    product.category = parsed.get("warenbereich")
    product.has_battery = bool(parsed.get("has_battery"))
    product.has_manual = bool(parsed.get("has_manual"))
    product.specification = {k: parsed.get(k) for k in _PRODUCT_SPEC_KEYS}
    db.flush()

    test_order = TestOrder(
        customer_id=customer.id,
        product_id=product.id,
        order_number=article_number,
        source="upload_lidl",
        original_filename=file.filename,
        raw_data=parsed,
        status="geparst",
    )
    db.add(test_order)
    db.commit()
    db.refresh(product)
    db.refresh(test_order)

    return LidlImportResult(
        product=product,
        test_order=test_order,
        pruefumfang_kategorien=parsed.get("pruefumfang_kategorien", []),
        referenzpruefung=bool(parsed.get("referenzpruefung")),
        ngo_pruefung=bool(parsed.get("ngo_pruefung")),
        ffu_pruefung=bool(parsed.get("ffu_pruefung")),
    )
