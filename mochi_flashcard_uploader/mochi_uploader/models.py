from typing import Dict, Optional, List
from pydantic import BaseModel
from datetime import datetime

class Field(BaseModel):
    id: str
    value: str

class Attachment(BaseModel):
    file_name: str
    content_type: str
    data: str

class Card(BaseModel):
    content: str
    deck_id: str
    template_id: Optional[str] = None
    archived: bool = False
    review_reverse: bool = False
    pos: Optional[str] = None
    fields: Optional[Dict[str, Field]] = None
    attachments: Optional[List[Attachment]] = None

class Deck(BaseModel):
    name: str
    parent_id: Optional[str] = None
    sort: Optional[int] = None
    trashed: Optional[datetime] = None
    archived: bool = False
    sort_by: Optional[str] = None
    cards_view: Optional[str] = None
    show_sides: bool = False
    sort_by_direction: bool = False
    review_reverse: bool = False