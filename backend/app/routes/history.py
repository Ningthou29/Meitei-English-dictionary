from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from app.database import get_db

router = APIRouter(prefix="/api/history", tags=["history"])

# POST: Add history entry
@router.post("/")
async def add_history_entry(
    source_text: str,
    source_language: str,
    translated_text: str,
    target_language: str,
    db=Depends(get_db)
):
    collection = db.history
    
    entry = {
        "source_text": source_text,
        "source_language": source_language,
        "translated_text": translated_text,
        "target_language": target_language,
        "created_at": datetime.utcnow()
    }
    
    result = await collection.insert_one(entry)
    
    return {
        "success": True,
        "message": "History entry added",
        "id": str(result.inserted_id)
    }

# GET: Get all history
@router.get("/")
async def get_history(limit: int = 50, db=Depends(get_db)):
    collection = db.history
    cursor = collection.find().sort("created_at", -1).limit(limit)
    history = await cursor.to_list(length=limit)
    
    for entry in history:
        entry["id"] = str(entry["_id"])
        del entry["_id"]
    
    return {
        "success": True,
        "total": len(history),
        "history": history
    }

# GET: Search history
@router.get("/search/{source_text}")
async def search_history(source_text: str, db=Depends(get_db)):
    collection = db.history
    cursor = collection.find({"source_text": {"$regex": source_text, "$options": "i"}})
    history = await cursor.to_list(length=50)
    
    for entry in history:
        entry["id"] = str(entry["_id"])
        del entry["_id"]
    
    return {
        "success": True,
        "total": len(history),
        "history": history
    }

# DELETE: Delete history entry
@router.delete("/{entry_id}")
async def delete_history_entry(entry_id: str, db=Depends(get_db)):
    collection = db.history
    
    if not ObjectId.is_valid(entry_id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    
    result = await collection.delete_one({"_id": ObjectId(entry_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    return {
        "success": True,
        "message": "History entry deleted"
    }

# DELETE: Clear all history
@router.delete("/")
async def clear_history(db=Depends(get_db)):
    collection = db.history
    await collection.delete_many({})
    
    return {
        "success": True,
        "message": "All history cleared"
    }