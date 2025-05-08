import json
import os
import re
from typing import Dict, List, Union, Optional

from langchain.tools import BaseTool, tool
from pathlib import Path


class BibleSearchTool(BaseTool):
    """Tool for search and retrieving Bible passages."""

    name = "bible_search_tool"
    description = """
    Useful for searching the Bible by reference (e.g., "John 3:16", "Genesis 1:1-10") 
    or by keywords/themes. Returns the full text of the specified verses or passages 
    containing the search terms.
    """

    def __init__(self):
        super.__init__()
        self.bible_data = self._load_bible_data()

    def _load_bible_data(self) -> Dict:
        current_dir = Path(__file__).parent.parent
        bible_path = current_dir / "data/kjv.json"

        try:
            with open(bible_path, "r", encoding="utf-8") as file:
                bible_json = json.load(file)
                return bible_json
        except FileNotFoundError:
            raise FileNotFoundError(f"Bible JSON file not found at {bible_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in Bible file at {bible_path}")

    def _parse_reference(self, reference: str) -> Dict:
        """
        Parse a Bible reference into its components.
        Examples:
        - "John 3:16" -> {"book": "John", "chapter": 3, "verse_start": 16, "verse_end": 16}
        - "Genesis 1:1-10" -> {"book": "Genesis", "chapter": 1, "verse_start": 1, "verse_end": 10}
        - "Psalms 23" -> {"book": "Psalms", "chapter": 23, "verse_start": None, "verse_end": None}
        """

        pattern = r"([\w\s]+)\s+(\d+)(?::(\d+)(?:-(\d+))?)?"
        match = re.match(pattern, reference.strip())

        if not match:
            return {}

        book = match.group(1).strip()
        chapter = int(match.group(2))
        verse_start = int(match.group(3)) if match.group(3) else None
        verse_end = int(match.group(4)) if match.group(4) else verse_start

        return {
            "book": book,
            "chapter": chapter,
            "verse_start": verse_start,
            "verse_end": verse_end,
        }

    def _get_passage_by_reference(self, ref_parts: Dict) -> Dict:
        """
        Retrieve Bible text based on parsed reference parts.
        Returns a dictionary with the reference and text.
        """
        book = ref_parts["book"]
        chapter = ref_parts["chapter"]
        verse_start = ref_parts["verse_start"]
        verse_end = ref_parts["verse_end"]

        matching_verses = [
            verse
            for verse in self.bible_data["verses"]
            if verse["book_name"].lower() == book.lower()
            and verse["chapter"] == chapter
        ]

        if not matching_verses:
            return {
                "error": f"Book '{book}' chapter {chapter} not found in the Bible data."
            }

        if verse_start is None:
            verses_text = " ".join(
                [f"{verse['verse']}. {verse['text']}" for verse in matching_verses]
            )
            return {"reference": f"{book} {chapter}", "text": verses_text}

        max_verse = max(verse["verse"] for verse in matching_verses)
        if (
            verse_start < 1
            or verse_start > max_verse
            or (verse_end and verse_end > max_verse)
        ):
            return {
                "error": f"Verse range {verse_start}-{verse_end} out of bounds for {book} {chapter}."
            }

        selected_verses = [
            verse
            for verse in matching_verses
            if verse_start
            <= verse["verse"]
            <= (verse_end if verse_end else verse_start)
        ]

        selected_verses.sort(key=lambda v: v["verse"])

        verses_text = " ".join(
            [f"{verse['verse']}. {verse['text']}" for verse in selected_verses]
        )

        return {
            "reference": f"{book} {chapter}:{verse_start}"
            + (f"-{verse_end}" if verse_end and verse_end != verse_start else ""),
            "text": verses_text,
        }

    def _search_by_keywords(self, keywords: str) -> List[Dict]:
        """
        Search the Bible for passages containing the specified keywords.
        Returns a list of matching references with their text.
        """
        results = []
        keywords_lower = keywords.lower()

        for verse in self.bible_data["verses"]:
            if keywords_lower in verse["text"].lower():
                results.append(
                    {
                        "reference": f"{verse['book_name']} {verse['chapter']}:{verse['verse']}",
                        "text": f"{verse['verse']}. {verse['text']}",
                    }
                )

                if len(results) >= 10:
                    break

        return results

    def _run(self, query: str) -> str:
        """
        Run the Bible search tool with the given query.
        The query can be a Bible reference or search keywords.
        """
        if re.match(r"[\w\s]+\s+\d+(?::\d+(?:-\d+)?)?", query):
            ref_parts = self._parse_reference(query)
            if ref_parts:
                result = self._get_passage_by_reference(ref_parts)
                if "error" in result:
                    return result["error"]
                return f"{result['reference']}: {result['text']}"

        results = self._search_by_keywords(query)
        if not results:
            return f"No matches found for '{query}' in the Bible."

        formatted_results = "\n\n".join(
            [f"{r['reference']}: {r['text']}" for r in results]
        )
        return f"Found {len(results)} matches for '{query}':\n\n{formatted_results}"
