import json
from typing import Dict, List, Union

from langchain.tools import BaseTool
from pathlib import Path


class BibleSearchTool(BaseTool):
    name = "BibleSearchTool"
    description = "Searches for Bible verses by keyword or by specific book/chapter/verse reference."

    def __init__(self, bible_path: Union[str, Path] = "src/data/kjv.json"):
        super().__init__()
        self.bible_path = Path(bible_path)
        self.verses = self._load_bible()

    def _load_bible(self) -> List[Dict]:
        try:
            with self.bible_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                return data["verses"]
        except Exception as e:
            raise RuntimeError(f"Failed to load Bible: {e}")

    def _format_verse(self, verse: Dict) -> str:
        return f"{verse['book_name']} {verse['chapter']}:{verse['verse']} - {verse['text']}"

    def run(self, query: str) -> str:
        query = query.strip().lower()

        if any(char.isdigit() for char in query):
            matched = [
                verse
                for verse in self.verses
                if query
                in f"{verse['book_name'].lower()} {verse['chapter']}:{verse['verse']}"
            ]
        else:
            matched = [verse for verse in self.verses if query in verse["text"].lower()]

        if not matched:
            return "No matching Bible verses found."

        return "\n".join(self._format_verse(v) for v in matched[:5])
