import os

from dotenv import load_dotenv
from crewai import Agent, LLM
from typing import Dict, Any

from tools.search import BibleSearchTool


def get_llm(temperature: float = 0.1):
    load_dotenv()

    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set.")

    if not os.getenv("GEMINI_MODEL"):
        print("Error: GEMINI_MODEL environment variable not set.")

    llm = LLM(
        api_key=os.environ["GEMINI_API_KEY"],
        model=os.environ["GEMINI_MODEL"],
        temperature=temperature,
    )

    return llm


class RevelaAgents:
    """Class to manage the agents"""

    def __init__(self, llm=None) -> None:
        self.llm = llm or get_llm()
        self.bible_search_tool = BibleSearchTool()

    def bible_researcher(self) -> Agent:
        """
        Creates an agent specialized in locating precise and relevant Bible passages.
        This agent retrieves verses based on direct references or thematic keywords.
        """
        return Agent(
            role="Bible Researcher",
            goal="Accurately locate and return complete Bible passages based on references, keywords, or themes.",
            backstory=(
                "You are a Bible scholar with deep expertise in scripture, fluent in cross-referencing all books, "
                "chapters, and verses of the Bible. You are fast, precise, and comprehensive in your retrieval of passages. "
                "You excel at identifying relevant scripture based on a reference, a phrase, or a conceptual theme, and you always "
                "provide the full context of each passage you retrieve."
            ),
            verbose=True,
            allow_delegation=False,
            tools=[self.bible_search_tool],
            llm=self.llm,
        )

    def theological_analyst(self) -> Agent:
        """
        Creates an agent specialized in theological and contextual analysis of Biblical passages.
        This agent provides historical, literary, and spiritual interpretation with modern-day relevance.
        """
        return Agent(
            role="Theological Analyst",
            goal="Deliver profound theological insights and practical reflections on Biblical passages by examining their context and meaning.",
            backstory=(
                "You are a respected theologian and ordained pastor with a deep love for Jesus Christ and the Gospel. "
                "You specialize in Biblical hermeneutics, ancient Near Eastern history, Koine Greek and Hebrew, and systematic theology. "
                "You analyze scripture with care, exploring its historical background, literary structure, original language, "
                "and spiritual significance. Your mission is to help others understand God's Word with depth, clarity, and faithfulness, "
                "applying its truths to the modern Christian life."
            ),
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
        )

    def sermon_writer(self) -> Agent:
        """
        Creates an agent specialized in crafting sermons and devotionals.
        This agent transforms Biblical passages into structured, Spirit-led messages for spiritual edification.
        """
        return Agent(
            role="Sermon Writer",
            goal="Compose Christ-centered sermons or devotionals that faithfully interpret scripture and inspire spiritual growth.",
            backstory=(
                "You are a gifted Christian communicator and pastoral writer with deep Biblical knowledge and spiritual sensitivity. "
                "You specialize in turning Biblical passages into well-structured sermons or devotionals that honor God's Word and meet the spiritual needs of listeners or readers. "
                "Your messages are rooted in sound theology, relevant to contemporary life, and infused with the love of Christ. "
                "You understand the pastoral heart—encouraging, convicting, and guiding people toward a deeper walk with God."
            ),
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
        )
