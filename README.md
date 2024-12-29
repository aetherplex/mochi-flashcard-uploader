# Mochi Flashcard Uploader

A command-line tool to upload markdown-formatted flashcards to [Mochi](https://mochi.cards/).

## Features

- Upload flashcards from markdown files to Mochi
- Support for nested decks
- Simple markdown format for card creation
- Environment variable support for API key
- Rich console output with progress indicators

## Installation

### Using pip

```bash
pip install mochi-flashcard-uploader
```

### Using poetry

```bash
poetry add mochi-flashcard-uploader
```

## Configuration

1. Get your Mochi API key from [Mochi Settings](https://app.mochi.cards/settings)

2. Set up your API key in one of two ways:

   a. Create a `.env` file in your project directory:

   ```
   MOCHI_API_KEY=your_api_key_here
   ```

   b. Pass it directly via the command line with `--api-key`

## Usage

### Basic Usage

```bash
mochi-upload path/to/cards.md "Deck Name"
```

### With Parent Deck

```bash
mochi-upload path/to/cards.md "Deck Name" --parent-deck-id your_parent_deck_id
```

### With API Key Override

```bash
mochi-upload path/to/cards.md "Deck Name" --api-key your_api_key
```

## Markdown Format

Your markdown file should follow this format:

```markdown
## Card 1

Front content of the card

---

Back content of the card

## Card 2

Question on the front

---

Answer on the back
```

Each card should:

- Start with `## Card N` where N is a number
- Have front and back content separated by `---`
- Have a blank line between cards

## Development

### Requirements

- Python 3.12+
- Poetry

### Setting Up Development Environment

1. Clone the repository:

```bash
git clone https://github.com/yourusername/mochi-flashcard-uploader.git
cd mochi-flashcard-uploader
```

2. Install dependencies:

```bash
poetry install
```

3. Copy the example environment file:

```bash
cp .env.example .env
```

4. Add your Mochi API key to `.env`

### Code Style

This project uses:

- Black for code formatting
- Mypy for type checking
- Ruff for linting

Run all checks:

```bash
poetry run black .
poetry run mypy .
poetry run ruff check .
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add some amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/aetherplex/mochi-flashcard-uploader/issues).
