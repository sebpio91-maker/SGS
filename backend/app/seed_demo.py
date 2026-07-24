"""Demo-Daten zum Ausprobieren der App: ein Beispielprodukt mit passender
Normenfinder-Regel, einem simulierten Lidl-Prüfauftrag und einem daraus
generierten Prüfplan.

Nutzt generische, öffentlich unbedenkliche Beispieldaten (Campingtisch,
DIN EN 581), keine echten Kunden-/Auftragsdaten. Idempotent: bereits
vorhandene Demo-Datensätze werden nicht doppelt angelegt.

Aufruf: `python -m app.seed_demo` (setzt voraus, dass `python -m app.seed`
bereits gelaufen ist bzw. führt es bei Bedarf selbst aus).
"""

from app.db.session import SessionLocal
from app.models.customer import Customer
from app.models.master_data import NormLookupRule, NormSpecialItem, ProductSpecRequirement
from app.models.order import TestOrder
from app.models.plan import TestPlan
from app.models.product import Product
from app.seed import seed as seed_lidl_catalog
from app.services.plan_generator import generate_test_plan

DEMO_ARTICLE_NUMBER = "DEMO-001"


def seed_demo() -> None:
    seed_lidl_catalog()

    db = SessionLocal()
    try:
        lidl = db.query(Customer).filter_by(code="LIDL").one()

        rule = db.query(NormLookupRule).filter_by(code="DEMO_CAMPINGTISCH").one_or_none()
        if rule is None:
            rule = NormLookupRule(
                kategorie="Möbel",
                produktart="Tisch",
                zielgruppe="Privat",
                einsatzort="Outdoor",
                bereich="Camping",
                produkt="Campingtisch",
                code="DEMO_CAMPINGTISCH",
                normen="DIN EN 581-1 / DIN EN 581-3",
                verweise="EN 1730 (Standsicherheit, Festigkeit und Dauerhaltbarkeit)",
                preis=570,
                zeit_labor_min=360,
                kosten_labor=432,
            )
            db.add(rule)

        special = (
            db.query(NormSpecialItem)
            .filter_by(kategorie="Möbel", produktart="Tisch", eigenschaft="Glas")
            .one_or_none()
        )
        if special is None:
            special = NormSpecialItem(
                kategorie="Möbel", produktart="Tisch", eigenschaft="Glas", zusatzkosten=100
            )
            db.add(special)

        spec = (
            db.query(ProductSpecRequirement)
            .filter_by(parameter="UV-Beständigkeit", produkt="Kunststoffe")
            .one_or_none()
        )
        if spec is None:
            spec = ProductSpecRequirement(
                parameter="UV-Beständigkeit",
                produkt="Kunststoffe",
                norm="DIN EN ISO 4892-3",
                kosten=1700,
                vk_preis=1900,
                materialverkaufstext="UV-Beständigkeit / Kunststoffe",
            )
            db.add(spec)

        db.flush()

        product = (
            db.query(Product)
            .filter_by(customer_id=lidl.id, article_number=DEMO_ARTICLE_NUMBER)
            .one_or_none()
        )
        if product is None:
            product = Product(
                customer_id=lidl.id,
                article_number=DEMO_ARTICLE_NUMBER,
                name="Demo-Campingtisch",
                category="Hartware",
                has_battery=False,
                has_manual=True,
                kategorie="Möbel",
                produktart="Tisch",
                zielgruppe="Privat",
                einsatzort="Outdoor",
                bereich="Camping",
                produkt_typ="Campingtisch",
            )
            db.add(product)
            db.flush()

        test_order = (
            db.query(TestOrder).filter_by(product_id=product.id, order_number=DEMO_ARTICLE_NUMBER)
            .one_or_none()
        )
        if test_order is None:
            test_order = TestOrder(
                customer_id=lidl.id,
                product_id=product.id,
                order_number=DEMO_ARTICLE_NUMBER,
                source="manual",
                status="geparst",
                raw_data={
                    "pruefumfang_kategorien": ["sicherheit_norm", "produktspezifikation"],
                    "has_battery": False,
                    "has_manual": True,
                    "referenzpruefung": True,
                    "ngo_pruefung": False,
                    "ffu_pruefung": True,
                },
            )
            db.add(test_order)
            db.commit()
            db.refresh(test_order)
        else:
            db.commit()

        db.refresh(product)

        existing_plan = (
            db.query(TestPlan)
            .filter_by(product_id=product.id, test_order_id=test_order.id)
            .one_or_none()
        )
        if existing_plan is None:
            plan = generate_test_plan(
                db,
                product=product,
                test_order=test_order,
                selected_spec_requirement_ids=[spec.id],
                selected_special_item_eigenschaften=["Glas"],
            )
            print(f"Demo-Prüfplan #{plan.id} für Produkt '{product.name}' erzeugt "
                  f"({len(plan.items)} Positionen).")
        else:
            print(f"Demo-Prüfplan #{existing_plan.id} existiert bereits, überspringe.")

        print("Öffne die App, logge dich ein und schau ihn dir auf der Seite "
              "'Prüfpläne' an (Produkt: 'Demo-Campingtisch').")
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo()
