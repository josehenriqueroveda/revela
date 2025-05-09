import os

from dotenv import load_dotenv
from crewai import Agent
from langchain_openai import ChatOpenAI

from tools.search import BibleSearchTool


def get_llm(temperature: float = 0.1):
    load_dotenv()

    MODEL_NAME = os.getenv("MODEL_NAME", "ollama/gemma3:1b")
    BASE_URL = os.getenv("BASE_URL", "http://localhost:11434/v1")

    print(f"🤗 Initializing local LLM via Ollama: {MODEL_NAME} available at {BASE_URL}")

    llm = ChatOpenAI(
        model=MODEL_NAME,
        base_url=BASE_URL,
        api_key="sk-ollama-placeholder",
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
                "You are a respected theologian and ordained pastor with a deep love for Jesus Christ and the Gospel."
                "Your mission is to help others understand God's Word with depth, clarity, and faithfulness, "
                "applying its truths to the modern Christian life, **based on the scripture passages provided to you.**"
            ),
            verbose=True,
            allow_delegation=False,
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
            allow_delegation=False,
            llm=self.llm,
        )
