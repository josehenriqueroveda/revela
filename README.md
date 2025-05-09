# Revela
Revela is an AI-powered Bible study tool that uses CrewAI to provide deep, contextual analysis of Biblical passages. Given a chapter or verse from the Bible, Revela combines an expert search agent with a theological analyst agent to deliver comprehensive insights into the chosen passage.


# Bible Data
The application uses a JSON file (bible.json) that contains the complete text of the Bible in a specific format. The expected structure is:
```json{
  "metadata": {
    "name": "Authorized King James Version",
    "shortname": "KJV"
  },
  "verses": [
    {
      "book_name": "Genesis",
      "book": 1,
      "chapter": 1,
      "verse": 1,
      "text": "In the beginning God created the heaven and the earth."
    },
    ...
  ]
}
```
Make sure this file is placed in the `src/data` directory.