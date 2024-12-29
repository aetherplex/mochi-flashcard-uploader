from typing import Optional, Dict, List
import requests
from pathlib import Path
from .models import Card, Deck
import base64
import mimetypes
from rich.console import Console
from rich.progress import Progress

class MochiClient:
    def __init__(self, api_key: str, base_url: str = "https://app.mochi.cards/api"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.auth = (api_key, '')
        self.console = Console()

    def create_deck(self, deck: Deck) -> Dict:
        """Create a new deck in Mochi."""
        try:
            json = {
                "name": deck.name,
                "parent-id": deck.parent_id,
                "sort": deck.sort if deck.sort else 0,
                "archived?": deck.archived,
                "show-sides?": deck.show_sides,
                "sort-by-direction": deck.sort_by_direction,
                "review-reverse?": deck.review_reverse
            }
            if deck.trashed:
                json["trashed?"] = deck.trashed.isoformat()
            response = self.session.post(
                f"{self.base_url}/decks",
                json=json
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            print(f"Response: {response.text}")
            raise

    def create_card(self, card: Card) -> Dict:
        """Create a new card in Mochi."""
        # Convert the markdown to match Mochi's format
        content = card.content.replace("---", "***")  # Replace markdown divider with Mochi's divider

        payload = {
            "content": content,
            "deck-id": card.deck_id,
            "template-id": card.template_id,
            "archived?": card.archived,
            "review-reverse?": card.review_reverse,
        }

        if card.pos:
            payload["pos"] = card.pos

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

        try:
            response = self.session.post(f"{self.base_url}/cards", json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print("Error Response:", response.text)  # This will show the actual error message
            raise

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