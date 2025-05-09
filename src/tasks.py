from crewai import Task

from agents import RevelaAgents


class RevelaTasks:
    """Class to manage the tasks"""

    def __init__(self, theme: str):
        self.theme = theme
        self.agents = RevelaAgents()

    def bible_research_task(self):
        return Task(
            description=(
                f"Search the Bible for passages that relate to the theme: '{self.theme}'. "
                f"Return 3 to 5 relevant verses with full references and content. "
                f"Include a brief explanation (1-2 sentences) of why each verse is relevant to the theme."
            ),
            expected_output=(
                "A list of 3–5 Bible passages (with book, chapter, and verse), including the verse text "
                "and a short explanation for each."
            ),
            agent=self.agents.bible_researcher(),
        )

    def theological_analysis_task(self):
        return Task(
            description=(
                "Analyze the selected Bible passages in depth. For each passage, provide:\n"
                "- Historical and cultural context\n"
                "- Literary style and structure\n"
                "- Theological significance\n"
                "- Application to modern life"
            ),
            expected_output=(
                "A detailed theological analysis (1-2 paragraphs per verse) explaining its meaning, background, "
                "and relevance today."
            ),
            agent=self.agents.theological_analyst(),
            context=[self.bible_research_task()],
        )

    def sermon_writing_task(self):
        return Task(
            description=(
                f"Using the theological analysis, write a short sermon or devotional (500–800 words) "
                f"based on the theme '{self.theme}'. Structure it with:\n"
                "- An engaging introduction\n"
                "- Scriptural exposition (using the analyzed passages)\n"
                "- A spiritual or practical application\n"
                "- A closing encouragement or prayer"
            ),
            expected_output="A complete, well-structured sermon or devotional message.",
            agent=self.agents.sermon_writer(),
            context=[self.theological_analysis_task()],
        )
