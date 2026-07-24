"""Prüfplan-Generierungslogik.

Führt zusammen:
- den Normenfinder (Produktklassifikation → Norm, Laborzeit/-kosten,
  Preis; siehe `NormLookupRule`/`NormSpecialItem`)
- die (physikalische) Produktspezifikation (`ProductSpecRequirement`)
- bei Lidl: den geparsten Prüfauftrag (Prüfumfang-Kategorien,
  Batterie/Anleitung/Referenzprüfung/NGO/FFU) plus den festen
  Prüfpunkt-Baum (`TestCategory`/`TestCatalogItem`)
- bei anderen Kunden: die manuell aus dem Katalog ausgewählten
  Prüfpunkte (`selected_catalog_item_ids`)

zu einem persistierten `TestPlan` mit `TestPlanItem`-Positionen inkl.
Kosten-Snapshot.
"""

from dataclasses import dataclass, field

from sqlalchemy.orm import Session

from app.models.catalog import TestCatalogItem, TestCategory
from app.models.customer import Customer
from app.models.master_data import NormLookupRule, NormSpecialItem, ProductSpecRequirement
from app.models.order import TestOrder
from app.models.plan import TestPlan, TestPlanItem
from app.models.product import Product

LIDL_CUSTOMER_CODE = "LIDL"

# Bekannte Bedingungen für `TestCatalogItem.applicability_condition`,
# ausgewertet gegen die Flags des Produkts.
_APPLICABILITY_CHECKS = {
    "has_battery": lambda product: bool(product.has_battery),
    "has_manual": lambda product: bool(product.has_manual),
}

# Zuordnung der Lidl-Prüfkategorien (Namen im TestCategory-Baum) zu den
# Schlüsseln, die `lidl_pdf_parser.determine_scope_categories` liefert.
_LIDL_CATEGORY_SCOPE_KEYS = {
    "Sicherheit & Norm / Sonder- & Funktionsparameter": "sicherheit_norm",
    "(physikalische) Produktspezifikation": "produktspezifikation",
}


@dataclass
class DraftItem:
    category_name: str
    name: str
    norm_reference: str | None = None
    description: str | None = None
    catalog_item_id: int | None = None
    lab_minutes: float | None = None
    lab_cost: float | None = None
    sale_price: float | None = None


@dataclass
class GenerationResult:
    items: list[DraftItem] = field(default_factory=list)
    norm_rule: NormLookupRule | None = None


def _classification_matches(rule_value: str | None, product_value: str | None) -> bool:
    """Ein leeres Regel-Feld gilt als Platzhalter (passt auf alles),
    analog zur Normenfinder-Logik in Excel."""
    return rule_value is None or rule_value == product_value


def find_norm_rule(db: Session, product: Product) -> NormLookupRule | None:
    """Sucht die zutreffende Norm-Regel für die Produktklassifikation.

    Kategorie, Produktart und Produkt(-typ) müssen gesetzt sein – das
    sind die drei Pflichtdimensionen im Normenfinder. Zielgruppe/
    Einsatzort/Bereich sind optional; ist eine Regel dafür leer, passt
    sie auf jede Ausprägung. Bei mehreren Treffern gewinnt die
    spezifischste (die meisten gesetzten optionalen Felder).
    """
    if not (product.kategorie and product.produktart and product.produkt_typ):
        return None

    candidates = (
        db.query(NormLookupRule)
        .filter(
            NormLookupRule.kategorie == product.kategorie,
            NormLookupRule.produktart == product.produktart,
            NormLookupRule.produkt == product.produkt_typ,
        )
        .all()
    )

    matches = [
        rule
        for rule in candidates
        if _classification_matches(rule.zielgruppe, product.zielgruppe)
        and _classification_matches(rule.einsatzort, product.einsatzort)
        and _classification_matches(rule.bereich, product.bereich)
    ]
    if not matches:
        return None

    def specificity(rule: NormLookupRule) -> int:
        return sum(1 for v in (rule.zielgruppe, rule.einsatzort, rule.bereich) if v is not None)

    return max(matches, key=specificity)


def find_special_item(
    db: Session, product: Product, eigenschaft: str
) -> NormSpecialItem | None:
    candidates = db.query(NormSpecialItem).filter(NormSpecialItem.eigenschaft == eigenschaft).all()
    matches = [
        item
        for item in candidates
        if _classification_matches(item.kategorie, product.kategorie)
        and _classification_matches(item.produktart, product.produktart)
        and _classification_matches(item.zielgruppe, product.zielgruppe)
        and _classification_matches(item.einsatzort, product.einsatzort)
    ]
    if not matches:
        return None

    def specificity(item: NormSpecialItem) -> int:
        return sum(
            1
            for v in (item.kategorie, item.produktart, item.zielgruppe, item.einsatzort)
            if v is not None
        )

    return max(matches, key=specificity)


def _norm_rule_to_item(rule: NormLookupRule) -> DraftItem:
    return DraftItem(
        category_name="Sicherheit & Norm / Sonder- & Funktionsparameter",
        name="Sicherheit-/Normprüfung",
        norm_reference=rule.normen,
        description=rule.verweise,
        lab_minutes=rule.zeit_labor_min,
        lab_cost=rule.kosten_labor,
        sale_price=rule.preis,
    )


def _catalog_item_to_draft(item: TestCatalogItem) -> DraftItem:
    return DraftItem(
        category_name=item.category.name,
        name=item.name,
        norm_reference=item.norm.reference if item.norm else None,
        description=item.description,
        catalog_item_id=item.id,
    )


def build_lidl_items(db: Session, product: Product, test_order: TestOrder) -> list[DraftItem]:
    """Leitet die Prüfplan-Positionen aus dem Lidl-Prüfpunkt-Baum und dem
    geparsten Prüfauftrag ab (Prüfumfang-Kategorien, Batterie/Anleitung/
    Referenzprüfung/NGO/FFU)."""
    raw = test_order.raw_data or {}
    scope_keys = set(raw.get("pruefumfang_kategorien") or [])

    categories = (
        db.query(TestCategory)
        .filter(TestCategory.customer_id == product.customer_id, TestCategory.parent_id.is_(None))
        .all()
    )

    items: list[DraftItem] = []
    for category in categories:
        scope_key = _LIDL_CATEGORY_SCOPE_KEYS.get(category.name)
        if scope_key is not None:
            if scope_key not in scope_keys:
                continue
            for catalog_item in category.items:
                condition = catalog_item.applicability_condition
                if condition and not _APPLICABILITY_CHECKS.get(condition, lambda p: False)(
                    product
                ):
                    continue
                items.append(_catalog_item_to_draft(catalog_item))
        elif category.name == "FFU/Fitting" and raw.get("ffu_pruefung"):
            items.append(DraftItem(category_name=category.name, name="FFU-Prüfung"))
        elif category.name == "Referenzprüfung" and raw.get("referenzpruefung"):
            items.append(DraftItem(category_name=category.name, name="Referenzprüfung"))
        elif category.name == "NGO" and raw.get("ngo_pruefung"):
            items.append(DraftItem(category_name=category.name, name="NGO-Prüfung"))

    return items


def generate_test_plan(
    db: Session,
    *,
    product: Product,
    test_order: TestOrder | None = None,
    selected_catalog_item_ids: list[int] | None = None,
    selected_spec_requirement_ids: list[int] | None = None,
    selected_special_item_eigenschaften: list[str] | None = None,
    created_by_id: int | None = None,
) -> TestPlan:
    customer = db.get(Customer, product.customer_id)
    draft_items: list[DraftItem] = []

    if customer is not None and customer.code == LIDL_CUSTOMER_CODE and test_order is not None:
        draft_items.extend(build_lidl_items(db, product, test_order))

    existing_catalog_item_ids = {i.catalog_item_id for i in draft_items if i.catalog_item_id}
    for catalog_item_id in selected_catalog_item_ids or []:
        if catalog_item_id in existing_catalog_item_ids:
            continue
        catalog_item = db.get(TestCatalogItem, catalog_item_id)
        if catalog_item is not None:
            draft_items.append(_catalog_item_to_draft(catalog_item))

    for spec_id in selected_spec_requirement_ids or []:
        spec = db.get(ProductSpecRequirement, spec_id)
        if spec is None:
            continue
        draft_items.append(
            DraftItem(
                category_name="(physikalische) Produktspezifikation",
                name=f"{spec.parameter} – {spec.produkt}" if spec.produkt else spec.parameter,
                norm_reference=spec.norm,
                description=spec.materialverkaufstext,
                lab_cost=spec.kosten,
                sale_price=spec.vk_preis,
            )
        )

    norm_rule = find_norm_rule(db, product)
    if norm_rule is not None:
        norm_item = next(
            (i for i in draft_items if i.name == "Sicherheit-/Normprüfung"), None
        )
        if norm_item is not None:
            norm_item.norm_reference = norm_rule.normen
            norm_item.description = norm_rule.verweise
            norm_item.lab_minutes = norm_rule.zeit_labor_min
            norm_item.lab_cost = norm_rule.kosten_labor
            norm_item.sale_price = norm_rule.preis
        else:
            draft_items.append(_norm_rule_to_item(norm_rule))

    for eigenschaft in selected_special_item_eigenschaften or []:
        special = find_special_item(db, product, eigenschaft)
        if special is not None:
            draft_items.append(
                DraftItem(
                    category_name="Sicherheit & Norm / Sonder- & Funktionsparameter",
                    name=f"Sonderposten: {special.eigenschaft}",
                    description=special.kommentar,
                    sale_price=special.zusatzkosten,
                )
            )

    test_plan = TestPlan(
        customer_id=product.customer_id,
        product_id=product.id,
        test_order_id=test_order.id if test_order else None,
        created_by_id=created_by_id,
        status="entwurf",
    )
    db.add(test_plan)
    db.flush()

    for sort_order, draft in enumerate(draft_items, start=1):
        db.add(
            TestPlanItem(
                test_plan_id=test_plan.id,
                catalog_item_id=draft.catalog_item_id,
                category_name=draft.category_name,
                name=draft.name,
                norm_reference=draft.norm_reference,
                description=draft.description,
                lab_minutes=draft.lab_minutes,
                lab_cost=draft.lab_cost,
                sale_price=draft.sale_price,
                sort_order=sort_order,
            )
        )

    db.commit()
    db.refresh(test_plan)
    return test_plan
