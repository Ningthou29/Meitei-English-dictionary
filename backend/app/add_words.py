import asyncio
from datetime import datetime
from app.database import Database

# =============================================
# 👇 PUT YOUR NEW WORDS HERE
# =============================================

NEW_WORDS = [
    # Format: {"english": "word", "roman_latin": "roman", "meitei_mayek": "meitei"}
    
    # Add your words here...
    {"english": "computer", "roman_latin": "kompyutur", "meitei_mayek": "ꯀꯣꯝꯄ꯭ꯌꯨꯇꯨꯔ"},
    {"english": "phone", "roman_latin": "phon", "meitei_mayek": "ꯐꯣꯟ"},
]

# =============================================
# DON'T CHANGE BELOW THIS LINE
# =============================================

async def add_words():
    """Add new words WITHOUT deleting existing ones"""
    
    print("🔄 Connecting to MongoDB...")
    db = await Database.connect()
    collection = db.dictionary
    
    existing_count = await collection.count_documents({})
    print(f"📊 Existing words in database: {existing_count}")
    
    if len(NEW_WORDS) == 0:
        print("⚠️ No new words to add. Add words to NEW_WORDS list.")
        return
    
    added = 0
    skipped = 0
    
    for word in NEW_WORDS:
        existing = await collection.find_one({
            "english": word["english"].lower()
        })
        
        if existing:
            print(f" Skipping: {word['english']} (already exists)")
            skipped += 1
        else:
            word["english"] = word["english"].lower()
            word["created_at"] = datetime.utcnow()
            word["updated_at"] = datetime.utcnow()
            await collection.insert_one(word)
            print(f" Added: {word['english']}")
            added += 1
    
    print(f"\n Summary:")
    print(f"    Added: {added} words")
    print(f"    Skipped: {skipped} words (already existed)")
    print(f"    Total words now: {existing_count + added}")
    print("✨ Done!")

if __name__ == "__main__":
    asyncio.run(add_words())