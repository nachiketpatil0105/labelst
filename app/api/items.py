from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.item import Item
from app.models.annotation import Annotation

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/")
def list_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return [{"id": item.id, "text": item.text} for item in items]


@router.get("/unlabeled")
def list_unlabeled_items(db: Session = Depends(get_db)):
    items = (
        db.query(Item)
        .outerjoin(Annotation, Item.id == Annotation.item_id)
        .filter(Annotation.item_id.is_(None))
        .all()
    )
    return [{"id": item.id, "text": item.text} for item in items]


@router.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item.id, "text": item.text}


@router.put("/{item_id}/annotation")
def save_annotation(item_id: int, label: str, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    annotation = db.query(Annotation).filter(Annotation.item_id == item_id).first()

    if annotation:
        annotation.label = label
    else:
        annotation = Annotation(item_id=item_id, label=label)
        db.add(annotation)

    db.commit()

    return {"item_id": item_id, "label": label, "status": "saved"}


@router.get("/{item_id}/annotation")
def get_annotation(item_id: int, db: Session = Depends(get_db)):
    annotation = db.query(Annotation).filter(Annotation.item_id == item_id).first()
    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    return {"item_id": item_id, "label": annotation.label}
