from crewai import Task
from agents import RevelaAgents


class RevelaTasks:
    """Class to manage the tasks"""

    def __init__(self, theme: str):
        self.theme = theme
        self.agents_handler = RevelaAgents()

    def bible_research_task(self):
        return Task(
            description=(
                f"You must search the Bible for passages related to the central theme: '{self.theme}'. "
                f"To do this, you will use the 'BibleSearchTool'. "
                f"The 'query' argument for this tool MUST be the theme string itself, which is EXACTLY: '{self.theme}'. "
                f"Provide only this exact string as the value for the 'query' argument. Do not wrap it in a dictionary or any other structure."
            ),
            expected_output=(
                "A list of 3–5 Bible passages (with book, chapter, and verse), including the verse text "
                "and a short explanation for each, relevant to the theme."
            ),
            agent=self.agents_handler.bible_researcher(),
            tools=[self.agents_handler.bible_search_tool],
        )

    def theological_analysis_task(self):
        research_task_output_placeholder = "{context_from_bible_research_task}"
        return Task(
            description=(
                "You have received a list of Bible passages from the Bible Researcher. "
                f"Your task is to analyze these specific passages: \n'{research_task_output_placeholder}'\n\n"
                "For each passage in the provided list, you must provide:\n"
                "- Historical and cultural context\n"
                "- Literary style and structure\n"
                "- Theological significance\n"
                "- Application to modern life\n\n"
                "Focus solely on the passages given to you. Do not attempt to search for other passages or delegate this search."
            ),
            expected_output=(
                "A detailed theological analysis (1-2 paragraphs per verse) for each of the provided Bible passages, "
                "explaining its meaning, background, and relevance today."
            ),
            agent=self.agents_handler.theological_analyst(),
            context=[self.bible_research_task()],
        )

    def sermon_writing_task(self):
        analysis_task_output_placeholder = "{context_from_theological_analysis_task}"
        return Task(
            description=(
                "You have received an theological insights from the Theological Analyst. "
                f"Your task is to write a short sermon or devotional (100–300 words) using these insights: \n'{analysis_task_output_placeholder}'\n\n"
                f"Your sermon shoud be base on the theme '{self.theme}' plus the insights received. Structure it with:\n"
                "- An engaging introduction\n"
                "- Scriptural exposition (using the analyzed passages)\n"
                "- A spiritual or practical application\n"
                "- A closing encouragement or prayer"
                "Focus solely on the insights given to you. Do not attempt to search for other insights or delegate this search."
            ),
            expected_output="A complete, well-structured sermon or devotional message.",
            agent=self.agents_handler.sermon_writer(),
            context=[self.theological_analysis_task()],
        )
