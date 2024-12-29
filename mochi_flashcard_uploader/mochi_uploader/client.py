from typing import Dict
import requests
from pathlib import Path
from .models import Card, Deck
import mimetypes
from rich.console import Console

class MochiClient:
    def __init__(self, api_key: str, base_url: str = "https://app.mochi.cards/api"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.auth = (api_key, '')
        self.console = Console()

    def create_deck(self, deck: Deck) -> Dict:
        """Create a new deck in Mochi."""
        response = self.session.post(
            f"{self.base_url}/decks",
            json={
                "name": deck.name,
                "parent-id": deck.parent_id,
                "sort": deck.sort,
                "archived?": deck.archived,
                "trashed?": deck.trashed.isoformat() if deck.trashed else None,
                "show-sides?": deck.show_sides,
                "sort-by-direction": deck.sort_by_direction,
                "review-reverse?": deck.review_reverse
            }
        )
        response.raise_for_status()
        return response.json()

    def create_card(self, card: Card) -> Dict:
        """Create a new card in Mochi."""
        payload = {
            "content": card.content,
            "deck-id": card.deck_id,
            "template-id": card.template_id,
            "archived?": card.archived,
            "review-reverse?": card.review_reverse,
            "pos": card.pos,
        }

        if card.fields:
            payload["fields"] = {
                k: {"id": k, "value": v.value}
                for k, v in card.fields.items()
            }

        if card.attachments:
            payload["attachments"] = [
                {
                    "file-name": att.file_name,
                    "content-type": att.content_type,
                    "data": att.data
                }
                for att in card.attachments
            ]

        response = self.session.post(f"{self.base_url}/cards", json=payload)
        response.raise_for_status()
        return response.json()

    def add_attachment(self, card_id: str, file_path: Path, attachment_id: str) -> None:
        """Add an attachment to a card."""
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if not mime_type:
            mime_type = 'application/octet-stream'

        with open(file_path, 'rb') as f:
            files = {'file': (attachment_id, f, mime_type)}
            response = self.session.post(
                f"{self.base_url}/cards/{card_id}/attachments/{attachment_id}",
                files=files
            )
        response.raise_for_status()