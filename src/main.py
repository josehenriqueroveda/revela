from datetime import date
from crew import RevelaCrew


def save_devotional(content):
    with open(f"devotional-{date.today()}.md", "w", encoding="utf-8") as file:
        file.write(content)
        return content


if __name__ == "__main__":
    crew = RevelaCrew._create_crew()
    result = crew.kickoff()
    save_devotional(result)
