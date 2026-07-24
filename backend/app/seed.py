"""Seed-Daten für den Lidl-Prüfpunkt-Baum.

Idempotent ausführbar: bereits vorhandene Datensätze (nach `code` bzw.
`name`) werden nicht doppelt angelegt. Aufruf: `python -m app.seed`.
"""

from app.db.session import SessionLocal
from app.models.catalog import TestCatalogItem, TestCategory
from app.models.customer import Customer

LIDL_TOP_LEVEL_CATEGORIES = [
    "Sicherheit & Norm / Sonder- & Funktionsparameter",
    "(physikalische) Produktspezifikation",
    "FFU/Fitting",
    "Referenzprüfung",
    "NGO",
]

LIDL_SICHERHEIT_NORM_ITEMS = [
    {
        "name": "Sicherheit-/Normprüfung",
        "description": None,
        "applicability_condition": None,
    },
    {
        "name": "Akkusicherheitskurzcheck",
        "description": "bei elektrischen Produkten mit Batterie- oder Akkukomponente",
        "applicability_condition": "has_battery",
    },
    {
        "name": "Kennzeichnungsprüfung",
        "description": "Verpackung und Produkt",
        "applicability_condition": None,
    },
    {
        "name": "Bedienungsanleitungsprüfung",
        "description": "falls es eine gibt",
        "applicability_condition": "has_manual",
    },
    {
        "name": "Optischer Abgleich",
        "description": None,
        "applicability_condition": None,
    },
]


def seed() -> None:
    db = SessionLocal()
    try:
        customer = db.query(Customer).filter_by(code="LIDL").one_or_none()
        if customer is None:
            customer = Customer(name="Lidl", code="LIDL")
            db.add(customer)
            db.flush()

        for sort_order, category_name in enumerate(LIDL_TOP_LEVEL_CATEGORIES, start=1):
            category = (
                db.query(TestCategory)
                .filter_by(customer_id=customer.id, name=category_name, parent_id=None)
                .one_or_none()
            )
            if category is None:
                category = TestCategory(
                    customer_id=customer.id,
                    name=category_name,
                    sort_order=sort_order,
                )
                db.add(category)
                db.flush()

            if category_name == "Sicherheit & Norm / Sonder- & Funktionsparameter":
                for item_sort_order, item_data in enumerate(LIDL_SICHERHEIT_NORM_ITEMS, start=1):
                    exists = (
                        db.query(TestCatalogItem)
                        .filter_by(category_id=category.id, name=item_data["name"])
                        .one_or_none()
                    )
                    if exists is None:
                        db.add(
                            TestCatalogItem(
                                category_id=category.id,
                                name=item_data["name"],
                                description=item_data["description"],
                                applicability_condition=item_data["applicability_condition"],
                                sort_order=item_sort_order,
                            )
                        )

        db.commit()
        print("Seed abgeschlossen: Kunde 'Lidl' mit Prüfpunkt-Baum angelegt/aktualisiert.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
