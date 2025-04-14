## Data

### `data` Folder

- No database for this actually, it's JSON-based database.
- All Path, Course, Lab details and content will be saved to the `data` folder and subfolders.

### `id.json` and JSON Files

- `courses.json`: a `dict [str, str]` of all the known courses, downloaded or not.
- `labs.json`: a `dict [str, str]` of all the known labs, downloaded only.
- `paths.json`: a `dict [str, str]` of all the known paths, downloaded or not.
- `{number}.json`: a `dict [str, str | dict [str, Any]]` of either a Path, or Course or Lab within respetive folder.

```
data
|--- courses.json
|--- labs.json
|--- paths.json
|--- courses
|----- 20.json
|--- labs
|----- 100.json
|--- paths
|----- 12.json
```

### Data JSON Files

- A Collection: [Paths Collection](docs/samples/data/paths.json)

```json
{
  "type": "paths",
  "name": "Paths Collection",
  "url": "https://www.cloudskillsboost.google",
  "date": "2025-01-05",
  "collection": {
    "21": "API Developer Learning Path",
    "183": "Advanced: Generative AI for Developers Learning Path",
   ...
  }
}
```

- A Path: [Google Cloud Applied AI Summit Learning Path](docs/samples/data/paths/280.json)

```json
{
  "id": "280",
  "name": "Google Cloud Applied AI Summit Learning Path",
  "type": "Path",
  "url": "https://www.cloudskillsboost.google/paths/280",
  "description": "This learning path contains courses and labs on Vertex AI and Duet AI in Google Cloud, for technical practitioners looking to upskill with the latest Google Cloud AI technology.",
  "date": "2025-01-05",
  "datePublished": "2025-01-02",
  "courses": {
    "6395": {
      "id": "6395",
      "type": "Course",
      "name": "Generative AI with Vertex AI: Prompt Design",
      "url": "https://www.cloudskillsboost.google/course_templates/6395"
    },
   ...
  }
}
```

- A Course: [Conversational AI on Vertex AI and Dialogflow CX](docs/samples/data/courses/892.json)

```yaml
{
  "id": "892",
  "name": "Conversational AI on Vertex AI and Dialogflow CX",
  "type": "Course",
  "url": "https://www.cloudskillsboost.google/course_templates/892",
  "description": "In this course you will learn how to use the new generative AI features in Dialogflow CX to create virtual agents that can have more natural and engaging conversations with customers. Discover how to deploy generative fallback responses to gracefully handle errors and omissions in customer conversations, deploy generators to increase intent coverage, and structure, ingest, and manage data in a data store. And explore how to deploy and maintain generative AI agents using your data, and deploy and maintain hybrid agents in combination with existing intent-based design paradigms.",
  "date": "2025-01-06",
  "datePublished": "2023-11-21",
  "objectives": [
    "Articulate and explain the functionality of the new generative AI features in Dialogflow CX.",
    "Implement generators to increase intent coverage in customer conversations.",
    "Enable generative fallback responses to gracefully handle errors and omissions in customer conversations.",
    "Deploy and maintain Generative AI agents that use your data."
  ],
  "topics": [],
  "modules": [
    {
      "id": "63784",
      "title": "Course Introduction",
      "description": "Discover what is covered in the Conversational AI on Vertex AI and Dialogflow CX course, including the target audience, prerequisites and the agenda, before refreshing your understanding of Dialogflow CX key concepts and terminology.",
      "steps": [
        {
         ...
        }
    }
}
```
