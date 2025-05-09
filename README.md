# Revela: AI-Powered Devotional Generator

Revela is an AI-powered system that generates devotionals based on specific themes. Using a crew of specialized AI agents, Revela researches relevant Bible passages, provides theological analysis, and crafts structured spiritual messages.

## Features

- **Bible Research Agent**: Locates precise scripture passages based on references or thematic keywords
- **Theological Analyst**: Provides deep historical, literary, and spiritual interpretation of passages
- **Sermon Writer**: Crafts well-structured, Christ-centered messages for spiritual edification
- **Local LLM Support**: Works with local models via Ollama (default: Gemma 3 1B)
- **Bible Search Tool**: Efficiently searches through scripture with both reference and keyword lookup

## Bible Data
The application uses a JSON file (bible.json) that contains the complete text of the Bible in a specific format. The expected structure is:
```json{
  "metadata": {
    "name": "Authorized King James Version",
    "shortname": "KJV"
  },
  "verses": [
    {
      "book_name": "Genesis",
      "book": 1,
      "chapter": 1,
      "verse": 1,
      "text": "In the beginning God created the heaven and the earth."
    },
    ...
  ]
}
```
Make sure this file is placed in the `src/data` directory.

## Installation

1. Clone this repository:
```bash
  git clone https://github.com/yourusername/revela.git
  cd revela
```
2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Set up your environment:
- Copy .env.example to .env and modify as needed
- Ensure you have a `bible.json` file in the `src/data/` directory
5. Set up Ollama (*if you want to run with local LLM*):
```bash
ollama pull gemma3:1b
```

## Usage
Run the main script:
```bash
python src/main.py
```
You will be prompted to enter a **theme** for your devotional or sermon. The system will then:
1. Search for relevant Bible passages
2. Analyze them theologically
3. Generate a complete devotional message
4. The output will be saved as a **markdown** file with today's date (e.g., `devotional-2025-05-10.md`).

## Project Structure
```
revela/
├── src/
│   ├── agents.py          # AI agent definitions
│   ├── crew.py            # Crew orchestration
│   ├── main.py            # Main execution script
│   ├── tasks.py           # Task definitions
│   ├── tools/             # Custom tools
│   │   └── search.py      # Bible search tool
│   └── data/
│       └── bible.json     # Bible data
├── .env                   # Environment configuration
└── requirements.txt       # Python dependencies
```

## Requirements
- Python 3.10+
- Ollama (for local LLM) or OpenAI API Key
- Bible data in JSON format (see `src/data/bible.json`)

---

### Support this project by giving it a star in the repository ⭐
