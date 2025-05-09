import json
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr


class BibleSearchToolInput(BaseModel):
    """Esquema de entrada para a ferramenta BibleSearchTool."""

    query: str = Field(
        ..., description="Palavra-chave ou referência para buscar na Bíblia."
    )


class BibleSearchTool(BaseTool):
    name: str = "BibleSearchTool"
    description: str = (
        "Busca versículos bíblicos por palavra-chave ou referência específica."
    )
    args_schema: Type[BaseModel] = BibleSearchToolInput

    _verses: list = PrivateAttr()

    def __init__(self):
        super().__init__()
        self._verses = self._load_bible()

    def _load_bible(self):
        try:
            with open("src/data/bible.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data["verses"]
        except Exception as e:
            raise RuntimeError(f"Falha ao carregar a Bíblia: {e}")

    def _run(self, query: str) -> str:
        query = query.strip().lower()

        if any(char.isdigit() for char in query):
            matched = [
                verse
                for verse in self._verses
                if query
                in f"{verse['book_name'].lower()} {verse['chapter']}:{verse['verse']}"
            ]
        else:
            matched = [
                verse for verse in self._verses if query in verse["text"].lower()
            ]

        if not matched:
            return "No matching Bible verses found."

        return "\n".join(
            f"{v['book_name']} {v['chapter']}:{v['verse']} - {v['text']}"
            for v in matched[:5]
        )
