from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import Literal
import json
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

app = FastAPI()

class AnnotationIn(BaseModel):
    label: Literal["POS", "NEG", "NEU"]


with open("data/items.json") as f:
    ITEMS = json.load(f)

@app.get("/items")
def list_items():
    return ITEMS

@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in ITEMS:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}

@app.put("/items/{item_id}/annotation")
def save_annot(item_id: int, annotation: AnnotationIn):
    label = annotation.label

    conn = get_db()
    cursor = conn.cursor()

    query = """
    INSERT INTO annotations (item_id, label)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE label = %s
    """

    try:
        cursor.execute(query, (item_id, label, label))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        cursor.close()
        conn.close()

    return {
        "item_id": item_id,
        "label": label,
        "status": "saved"
    }

@app.get("/items/{item_id}/annotation")
def get_annotation(item_id: int):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT label FROM annotations WHERE item_id = %s",
        (item_id,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if not result:
        return {"error": "Annotation not found"}

    return {
        "item_id": item_id,
        "annotation": result
    }