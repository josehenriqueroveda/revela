from datetime import date
from crew import RevelaCrew


def save_devotional(content):
    with open(f"devotional-{date.today()}.md", "w", encoding="utf-8") as file:
        file.write(content)
        return content


def main():
    theme = input("Enter the theme for the devotional/sermon: ").strip()
    crew = RevelaCrew(theme)
    result = crew.run()
    return result


if __name__ == "__main__":
    result = main()
    save_devotional(result)
