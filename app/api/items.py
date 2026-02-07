"""Items API routes for listing items and managing annotations."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.item import Item
from app.models.annotation import Annotation

# Router for item-related endpoints under /api/items
router = APIRouter(prefix="/api/items", tags=["items"])


@router.get("/")
def list_items(db: Session = Depends(get_db)):
    """Return all items with basic fields."""
    items = db.query(Item).all()

    return [
        {
            "id": item.id,
            "text": item.text
        }
        for item in items
    ]


@router.get("/unlabeled")
def list_unlabeled_items(db: Session = Depends(get_db)):
    """Return items that do not have any annotation."""
    items = (
        db.query(Item)
        .outerjoin(Annotation, Item.id == Annotation.item_id)
        .filter(Annotation.item_id.is_(None))
        .all()
    )

    return [
        {
            "id": item.id,
            "text": item.text
        }
        for item in items
    ]


@router.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Fetch a single item by its ID."""
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return {
        "id": item.id,
        "text": item.text
    }


@router.put("/{item_id}/annotation")
def save_annotation(
    item_id: int,
    label: str,
    db: Session = Depends(get_db)
):
    """Create or update an annotation label for an item."""
    # Check if item exists
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Check for existing annotation
    annotation = (
        db.query(Annotation)
        .filter(Annotation.item_id == item_id)
        .first()
    )

    # Update existing or create new annotation
    if annotation:
        annotation.label = label
    else:
        annotation = Annotation(item_id=item_id, label=label)
        db.add(annotation)

    # Commit changes to database
    db.commit()

    return {
        "item_id": item_id,
        "label": label,
        "status": "saved"
    }


@router.get("/{item_id}/annotation")
def get_annotation(item_id: int, db: Session = Depends(get_db)):
    """Retrieve the annotation label for a specific item."""
    annotation = (
        db.query(Annotation)
        .filter(Annotation.item_id == item_id)
        .first()
    )

    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")

    return {
        "item_id": item_id,
        "label": annotation.label
    }
