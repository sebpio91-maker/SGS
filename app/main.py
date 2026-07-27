import io
from datetime import datetime

from fastapi import FastAPI, Request, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import or_
from sqlalchemy.orm import Session
import openpyxl

from .database import Base, engine, get_db
from .models import Norm, Pruefpunkt, STATUS_OPTIONEN, RELEVANZ_OPTIONEN
from .seed import seed_if_empty
from . import extraction

Base.metadata.create_all(bind=engine)

_db = next(get_db())
try:
    seed_if_empty(_db)
finally:
    _db.close()

app = FastAPI(title="Normen-Datenbank")

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# ---------- Seiten ----------

@app.get("/")
def index(request: Request, q: str = "", db: Session = Depends(get_db)):
    query = db.query(Norm)
    if q:
        like = f"%{q}%"
        norm_ids = (
            db.query(Pruefpunkt.norm_id)
            .filter(
                or_(
                    Pruefpunkt.kapitel.ilike(like),
                    Pruefpunkt.ueberschrift.ilike(like),
                    Pruefpunkt.inhalt.ilike(like),
                )
            )
            .distinct()
        )
        query = query.filter(
            or_(
                Norm.kurzbezeichnung.ilike(like),
                Norm.vollbezeichnung.ilike(like),
                Norm.titel.ilike(like),
                Norm.kategorie.ilike(like),
                Norm.id.in_(norm_ids),
            )
        )
    normen = query.order_by(Norm.kurzbezeichnung).all()
    return templates.TemplateResponse(
        request, "index.html", {"normen": normen, "q": q}
    )


@app.get("/normen/neu")
def neue_norm_form(request: Request):
    return templates.TemplateResponse(
        request,
        "norm_form.html",
        {"norm": None, "status_optionen": STATUS_OPTIONEN},
    )


@app.post("/normen/neu")
def neue_norm_anlegen(
    kurzbezeichnung: str = Form(...),
    vollbezeichnung: str = Form(""),
    titel: str = Form(""),
    status: str = Form("aktiv"),
    kategorie: str = Form(""),
    notiz: str = Form(""),
    db: Session = Depends(get_db),
):
    norm = Norm(
        kurzbezeichnung=kurzbezeichnung.strip(),
        vollbezeichnung=vollbezeichnung.strip() or None,
        titel=titel.strip() or None,
        status=status,
        kategorie=kategorie.strip() or None,
        notiz=notiz.strip() or None,
    )
    db.add(norm)
    db.commit()
    db.refresh(norm)
    return RedirectResponse(f"/normen/{norm.id}", status_code=303)


@app.get("/normen/{norm_id}")
def norm_detail(norm_id: int, request: Request, db: Session = Depends(get_db)):
    norm = db.get(Norm, norm_id)
    if not norm:
        raise HTTPException(404, "Norm nicht gefunden")
    return templates.TemplateResponse(
        request,
        "norm_detail.html",
        {
            "norm": norm,
            "status_optionen": STATUS_OPTIONEN,
            "relevanz_optionen": RELEVANZ_OPTIONEN,
        },
    )


@app.post("/normen/{norm_id}/bearbeiten")
def norm_bearbeiten(
    norm_id: int,
    kurzbezeichnung: str = Form(...),
    vollbezeichnung: str = Form(""),
    titel: str = Form(""),
    status: str = Form("aktiv"),
    kategorie: str = Form(""),
    notiz: str = Form(""),
    db: Session = Depends(get_db),
):
    norm = db.get(Norm, norm_id)
    if not norm:
        raise HTTPException(404, "Norm nicht gefunden")
    norm.kurzbezeichnung = kurzbezeichnung.strip()
    norm.vollbezeichnung = vollbezeichnung.strip() or None
    norm.titel = titel.strip() or None
    norm.status = status
    norm.kategorie = kategorie.strip() or None
    norm.notiz = notiz.strip() or None
    norm.updated_at = datetime.utcnow()
    db.commit()
    return RedirectResponse(f"/normen/{norm_id}", status_code=303)


@app.post("/normen/{norm_id}/loeschen")
def norm_loeschen(norm_id: int, db: Session = Depends(get_db)):
    norm = db.get(Norm, norm_id)
    if norm:
        db.delete(norm)
        db.commit()
    return RedirectResponse("/", status_code=303)


# ---------- Prüfpunkte JSON-API (Tabelle auf der Detailseite) ----------

def _pruefpunkt_to_dict(p: Pruefpunkt):
    return {
        "id": p.id,
        "kapitel": p.kapitel,
        "ueberschrift": p.ueberschrift,
        "pruefungsrelevant": p.pruefungsrelevant,
        "inhalt": p.inhalt,
        "sortierung": p.sortierung,
    }


@app.get("/api/normen/{norm_id}/pruefpunkte")
def api_liste(norm_id: int, db: Session = Depends(get_db)):
    punkte = (
        db.query(Pruefpunkt)
        .filter(Pruefpunkt.norm_id == norm_id)
        .order_by(Pruefpunkt.sortierung)
        .all()
    )
    return [_pruefpunkt_to_dict(p) for p in punkte]


@app.post("/api/normen/{norm_id}/pruefpunkte")
def api_neu(norm_id: int, db: Session = Depends(get_db)):
    norm = db.get(Norm, norm_id)
    if not norm:
        raise HTTPException(404, "Norm nicht gefunden")
    max_sort = db.query(Pruefpunkt).filter(Pruefpunkt.norm_id == norm_id).count()
    p = Pruefpunkt(
        norm_id=norm_id,
        kapitel="",
        ueberschrift="",
        pruefungsrelevant="Nein",
        inhalt="",
        sortierung=max_sort,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return _pruefpunkt_to_dict(p)


@app.patch("/api/pruefpunkte/{punkt_id}")
async def api_update(punkt_id: int, request: Request, db: Session = Depends(get_db)):
    p = db.get(Pruefpunkt, punkt_id)
    if not p:
        raise HTTPException(404, "Prüfpunkt nicht gefunden")
    data = await request.json()
    for feld in ("kapitel", "ueberschrift", "pruefungsrelevant", "inhalt"):
        if feld in data:
            setattr(p, feld, data[feld])
    p.updated_at = datetime.utcnow()
    db.commit()
    return _pruefpunkt_to_dict(p)


@app.delete("/api/pruefpunkte/{punkt_id}")
def api_loeschen(punkt_id: int, db: Session = Depends(get_db)):
    p = db.get(Pruefpunkt, punkt_id)
    if p:
        db.delete(p)
        db.commit()
    return {"ok": True}


@app.post("/api/pruefpunkte/{punkt_id}/verschieben")
async def api_verschieben(punkt_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    richtung = data.get("richtung")
    p = db.get(Pruefpunkt, punkt_id)
    if not p:
        raise HTTPException(404, "Prüfpunkt nicht gefunden")
    nachbarn = (
        db.query(Pruefpunkt)
        .filter(Pruefpunkt.norm_id == p.norm_id)
        .order_by(Pruefpunkt.sortierung)
        .all()
    )
    idx = next((i for i, n in enumerate(nachbarn) if n.id == p.id), None)
    if idx is None:
        return {"ok": False}
    ziel = idx - 1 if richtung == "hoch" else idx + 1
    if 0 <= ziel < len(nachbarn):
        a, b = nachbarn[idx], nachbarn[ziel]
        a.sortierung, b.sortierung = b.sortierung, a.sortierung
        db.commit()
    return {"ok": True}


# ---------- PDF-Upload (Entwurf-Extraktion) ----------

@app.get("/normen/{norm_id}/upload")
def upload_form(norm_id: int, request: Request, db: Session = Depends(get_db)):
    norm = db.get(Norm, norm_id)
    if not norm:
        raise HTTPException(404, "Norm nicht gefunden")
    return templates.TemplateResponse(request, "upload_form.html", {"norm": norm})


@app.post("/normen/{norm_id}/upload")
async def upload_verarbeiten(
    norm_id: int, request: Request, db: Session = Depends(get_db), datei: UploadFile = File(...)
):
    norm = db.get(Norm, norm_id)
    if not norm:
        raise HTTPException(404, "Norm nicht gefunden")
    inhalt_bytes = await datei.read()
    text = extraction.extract_text(inhalt_bytes)
    entwuerfe = extraction.parse_kapitel_entwurf(text)
    return templates.TemplateResponse(
        request,
        "upload_review.html",
        {
            "norm": norm,
            "entwuerfe": entwuerfe,
            "relevanz_optionen": RELEVANZ_OPTIONEN,
            "anzahl": len(entwuerfe),
        },
    )


@app.post("/normen/{norm_id}/upload/uebernehmen")
async def upload_uebernehmen(norm_id: int, request: Request, db: Session = Depends(get_db)):
    norm = db.get(Norm, norm_id)
    if not norm:
        raise HTTPException(404, "Norm nicht gefunden")
    form = await request.form()
    indizes = sorted(
        {key.split("_", 1)[1] for key in form.keys() if key.startswith("uebernehmen_")},
        key=int,
    )
    max_sort = db.query(Pruefpunkt).filter(Pruefpunkt.norm_id == norm_id).count()
    hinzugefuegt = 0
    for idx in indizes:
        if form.get(f"uebernehmen_{idx}") != "on":
            continue
        kapitel = (form.get(f"kapitel_{idx}") or "").strip()
        ueberschrift = (form.get(f"ueberschrift_{idx}") or "").strip()
        relevanz = form.get(f"relevanz_{idx}") or "Nein"
        inhalt_text = (form.get(f"inhalt_{idx}") or "").strip()
        db.add(
            Pruefpunkt(
                norm_id=norm_id,
                kapitel=kapitel,
                ueberschrift=ueberschrift,
                pruefungsrelevant=relevanz,
                inhalt=inhalt_text or None,
                sortierung=max_sort + hinzugefuegt,
            )
        )
        hinzugefuegt += 1
    db.commit()
    return RedirectResponse(f"/normen/{norm_id}", status_code=303)


# ---------- Export ----------

@app.get("/export/excel")
def export_excel(db: Session = Depends(get_db)):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "NORMEN"
    ws.append(["Norm", "Kapitel", "Überschrift", "Prüfungsrelevant", "Inhalt"])

    normen = db.query(Norm).order_by(Norm.kurzbezeichnung).all()
    for norm in normen:
        for p in sorted(norm.pruefpunkte, key=lambda x: x.sortierung):
            ws.append(
                [
                    norm.kurzbezeichnung,
                    p.kapitel,
                    p.ueberschrift,
                    p.pruefungsrelevant,
                    p.inhalt,
                ]
            )

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=normen_export.xlsx"},
    )
