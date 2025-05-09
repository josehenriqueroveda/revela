import os
import json
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr


class BibleSearchToolInput(BaseModel):
    """Input schema for BibleSearchTool."""

    query: str = Field(..., description="Keyword or biblical reference to search for.")


class BibleSearchTool(BaseTool):
    name: str = "BibleSearchTool"
    description: str = "Searches for biblical verses by keyword or specific reference."
    args_schema: Type[BaseModel] = BibleSearchToolInput

    _verses: list = PrivateAttr()
    _bible_data_path: str = PrivateAttr()

    def __init__(self, bible_data_path: str = "src/data/bible.json"):
        super().__init__()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._bible_data_path = os.path.join(base_dir, "data", "bible.json")
        self._verses = self._load_bible()

    def _load_bible(self):
        try:
            with open(self._bible_data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "verses" not in data or not isinstance(data["verses"], list):
                    raise ValueError(
                        "Bible data is not in the expected format (missing 'verses' list)."
                    )
                return data["verses"]
        except FileNotFoundError:
            raise RuntimeError(
                f"Bible data file not found at {self._bible_data_path}. "
                f"Please ensure the path is correct. Current working directory: {os.getcwd()}"
            )
        except json.JSONDecodeError:
            raise RuntimeError(
                f"Error decoding JSON from Bible data file at {self._bible_data_path}."
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to load Bible from {self._bible_data_path}: {e}"
            )

    def _run(self, query: str) -> str:
        query_str = query.strip().lower()

        if not self._verses:
            return "Bible data not loaded. Cannot perform search."

        matched_verses = []
        if any(char.isdigit() for char in query_str):
            matched_verses = [
                verse
                for verse in self._verses
                if query_str
                in f"{verse.get('book_name', '').lower()} {verse.get('chapter', '')}:{verse.get('verse', '')}"
            ]
        else:
            matched_verses = [
                verse
                for verse in self._verses
                if query_str in verse.get("text", "").lower()
            ]

        if not matched_verses:
            return f"No matching Bible verses found for '{query}'."

        results = []
        for v in matched_verses[:5]:
            results.append(
                f"{v.get('book_name', 'N/A')} {v.get('chapter', 'N/A')}:{v.get('verse', 'N/A')} - {v.get('text', 'N/A')}"
            )
        return "\n".join(results)
