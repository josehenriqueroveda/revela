from crewai import Crew, Process
from agents import RevelaAgents
from tasks import RevelaTasks


class RevelaCrew:
    def __init__(self):
        self.crew = self._create_crew()

    def _create_crew():
        return Crew(
            agents=[
                RevelaAgents.bible_researcher,
                RevelaAgents.theological_analyst,
                RevelaAgents.sermon_writer,
            ],
            tasks=[
                RevelaTasks.bible_reserch_task,
                RevelaTasks.theological_analysis_task,
                RevelaTasks.sermon_writing_task,
            ],
            verbose=1,
            process=Process.sequential,
        )
