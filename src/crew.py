from crewai import Crew, Process
from agents import RevelaAgents
from tasks import RevelaTasks


class RevelaCrew:
    def __init__(self, theme: str):
        self.theme = theme
        self.agents = RevelaAgents()
        self.tasks = RevelaTasks(theme)
        self.crew = self._create_crew()

    def _create_crew(self):
        return Crew(
            agents=[
                self.agents.bible_researcher(),
                self.agents.theological_analyst(),
                self.agents.sermon_writer(),
            ],
            tasks=[
                self.tasks.bible_research_task(),
                self.tasks.theological_analysis_task(),
                self.tasks.sermon_writing_task(),
            ],
            verbose=1,
            process=Process.sequential,
        )

    def run(self):
        return self.crew.kickoff()
