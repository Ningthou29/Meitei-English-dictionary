from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from app.database import get_db
from app.models import WordCreate, WordResponse

router = APIRouter(prefix="/api/dictionary", tags=["dictionary"])

# GET: Get all words
@router.get("/")
async def get_all_words(limit: int = 100, skip: int = 0, db=Depends(get_db)):
    collection = db.dictionary
    cursor = collection.find().skip(skip).limit(limit)
    words = await cursor.to_list(length=limit)
    
    for word in words:
        word["id"] = str(word["_id"])
        del word["_id"]
    
    total = await collection.count_documents({})
    
    return {
        "success": True,
        "total": total,
        "limit": limit,
        "skip": skip,
        "words": words
    }

# GET: Search word
@router.get("/search/{word}")
async def search_word(word: str, db=Depends(get_db)):
    collection = db.dictionary
    result = await collection.find_one({"english": word.lower()})
    
    if not result:
        raise HTTPException(status_code=404, detail="Word not found")
    
    result["id"] = str(result["_id"])
    del result["_id"]
    
    return {
        "success": True,
        "word": result
    }

# POST: Add new word
@router.post("/")
async def add_word(word: WordCreate, db=Depends(get_db)):
    collection = db.dictionary
    
    existing = await collection.find_one({"english": word.english.lower()})
    if existing:
        raise HTTPException(status_code=400, detail="Word already exists")
    
    word_data = word.dict()
    word_data["english"] = word_data["english"].lower()
    word_data["created_at"] = datetime.utcnow()
    word_data["updated_at"] = datetime.utcnow()
    
    result = await collection.insert_one(word_data)
    
    return {
        "success": True,
        "message": "Word added successfully",
        "id": str(result.inserted_id)
    }

# PUT: Update word
@router.put("/{word_id}")
async def update_word(word_id: str, word: WordCreate, db=Depends(get_db)):
    collection = db.dictionary
    
    if not ObjectId.is_valid(word_id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    
    existing = await collection.find_one({"_id": ObjectId(word_id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Word not found")
    
    word_data = word.dict()
    word_data["english"] = word_data["english"].lower()
    word_data["updated_at"] = datetime.utcnow()
    
    await collection.update_one(
        {"_id": ObjectId(word_id)},
        {"$set": word_data}
    )
    
    return {
        "success": True,
        "message": "Word updated successfully"
    }

# DELETE: Delete word
@router.delete("/{word_id}")
async def delete_word(word_id: str, db=Depends(get_db)):
    collection = db.dictionary
    
    if not ObjectId.is_valid(word_id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    
    result = await collection.delete_one({"_id": ObjectId(word_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Word not found")
    
    return {
        "success": True,
        "message": "Word deleted successfully"
    }

# POST: Add multiple words
@router.post("/bulk")
async def add_multiple_words(words: List[WordCreate], db=Depends(get_db)):
    collection = db.dictionary
    added = []
    failed = []
    
    for word in words:
        existing = await collection.find_one({"english": word.english.lower()})
        if existing:
            failed.append({"english": word.english, "reason": "Already exists"})
            continue
        
        word_data = word.dict()
        word_data["english"] = word_data["english"].lower()
        word_data["created_at"] = datetime.utcnow()
        word_data["updated_at"] = datetime.utcnow()
        
        result = await collection.insert_one(word_data)
        added.append({"english": word.english, "id": str(result.inserted_id)})
    
    return {
        "success": True,
        "added": len(added),
        "failed": len(failed),
        "details": {
            "added": added,
            "failed": failed
        }
    }