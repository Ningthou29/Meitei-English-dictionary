from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WordCreate(BaseModel):
    english: str
    roman_latin: str
    meitei_mayek: str

class WordResponse(BaseModel):
    id: str
    english: str
    roman_latin: str
    meitei_mayek: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class HistoryResponse(BaseModel):
    id: str
    source_text: str
    source_language: str
    translated_text: str
    target_language: str
    created_at: datetime