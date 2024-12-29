import typer
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from .client import MochiClient
from .models import Card, Deck
import re
from dotenv import load_dotenv
import os
from pathlib import Path

app = typer.Typer()
console = Console()

def process_markdown_file(file_path: Path) -> List[Card]:
    """Process a markdown file and extract cards."""
    print(f"Processing markdown file: {file_path}")
    cards = []
    with open(file_path) as f:
        content = f.read()

    # Split content into individual cards
    # This is a basic implementation - you might want to enhance the parsing logic
    card_sections = re.split(r'\n## Card \d+\n', content)

    for section in card_sections:
        if not section.strip():
            continue

        # Extract front and back
        parts = section.split('\n---\n', 1)
        if len(parts) != 2:
            continue

        front, back = parts

        cards.append(Card(
            content=f"{front.strip()}\n---\n{back.strip()}",
            deck_id=""  # This will be set later
        ))

    return cards

def load_api_key() -> Optional[str]:
    """Load API key from .env file or environment"""
    # Try to load from .env file
    env_file = Path(".env")
    if env_file.exists():
        load_dotenv(env_file)
    return os.getenv("MOCHI_API_KEY")

@app.command()
def upload(
    markdown_file: Path,  # First positional argument
    deck_name: str,      # Second positional argument
    api_key: Optional[str] = typer.Option(None, help="Mochi API key"),
    parent_deck_id: Optional[str] = typer.Option(None, help="Parent deck ID if creating a nested deck")
):
    print(f"Uploading {markdown_file} to deck {deck_name} with parent deck ID {parent_deck_id}")
    # Try to get API key from .env if not provided
    api_key = api_key or load_api_key()
    if not api_key:
        console.print("[red]Error: API key not found. Please provide it via --api-key or set MOCHI_API_KEY in .env file[/red]")
        raise typer.Exit(1)
    """Upload flashcards from a markdown file to Mochi."""
    try:
        client = MochiClient(api_key)

        # Create or get deck
        deck = Deck(
            name=deck_name,
            parent_id=parent_deck_id
        )

        with console.status(f"Creating deck '{deck_name}'..."):
            print(f"Deck: {deck}")
            deck_response = client.create_deck(deck)
            deck_id = deck_response['id']
            console.print(f"Created deck with ID: {deck_id}")

        print(f"Deck ID: {deck_id}")
        # Process markdown file
        cards = process_markdown_file(markdown_file)
        print(f"Cards: {cards}")
        with console.status(f"Uploading {len(cards)} cards...") as status:
            for i, card in enumerate(cards, 1):
                card.deck_id = deck_id
                status.update(f"Uploading card {i}/{len(cards)}...")
                client.create_card(card)

        console.print(f"Successfully uploaded {len(cards)} cards to deck '{deck_name}'")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()