# Google Cloud Skills Boost Automation/Scraping Script

![Welcome Screen](docs/assets/welcome-screen.png)

A helper or a scraper.

This is a small tools for scraping contents from Google Cloud Skills Boost website to Markdown files, which helps to build your Personal Knowledge Base, Obsidian, for example.

## Samples

## PDF Files
- Course: [Conversational AI on Vertex AI and Dialogflow CX](docs/samples/output/courses/Conversational-AI-on-Vertex-AI-and-Dialogflow-CX.md)

### Output Markdown Files

- A Collection: [Paths Collection](docs/samples/paths.md)

```yaml
---
type: paths
name: 'Paths Collection'
url: https://www.cloudskillsboost.google
date: 2025-01-05
---

# [Paths Collection](https://www.cloudskillsboost.google)
```

- A Path: [Google Cloud Applied AI Summit Learning Path](docs/samples/output/paths/Google-Cloud-Applied-AI-Summit-Learning-Path.md)

```yaml
---
id: 280
name: 'Google Cloud Applied AI Summit Learning Path'
type: Path
url: https://www.cloudskillsboost.google/paths/280
date: 2025-01-05
datePublished: 2025-01-02
---

# [Google Cloud Applied AI Summit Learning Path](https://www.cloudskillsboost.google/paths/280)
```

- A Course: [Conversational AI on Vertex AI and Dialogflow CX](docs/samples/output/courses/Conversational-AI-on-Vertex-AI-and-Dialogflow-CX.md)

```yaml
---
id: 892
name: 'Conversational AI on Vertex AI and Dialogflow CX'
type: Course
url: https://www.cloudskillsboost.google/course_templates/892
date: 2025-01-06
datePublished: 2023-11-21
topics: []
---

# [Conversational AI on Vertex AI and Dialogflow CX](https://www.cloudskillsboost.google/course_templates/892)
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

## Features

- Gathers a list of Path.
- Offer selection to specify a course or list of courses.
- Extract the course(s)' content, including id, title, tag, videos' transcript, and quiz.
- Write path's or course's content to a well-structured Markdown file for each.
- Can also help to 'Mark Complete Video' as well.
- Generate prompt for LLM to re-formatting the videos' transcripts.

## TODO

- Command-line interface.
- Do not over-write the existing Markdown files, it's actually up to you, as a user.
- Call to Gemini/LLAMA or any other LLM for helping summarize/re-formatting the transcripts.
   + For time being, Gemini for me, is not so good so I don't use yet.
   + LM Studio is a good choice with LLAMA 3.1, 3.2 but my machine is not suitable for running this continously.

Check [CONTRIBUTION](CONTRIBUTION.md) for more.

## I. Installation - A Manual Approach

### 1. Clone the repo

```sh
git clone https://github.com/samdx/cloudskillsboost-helper.git
cd cloudskillsboost-helper
```

### 2. Create a Virtual Environment

You can create a virtual environment using `venv`:

```sh
python -m venv .venv
```

### 3. Activate the Virtual Environment

- **Windows**:

  ```sh
  .venv\Scripts\activate
  ```

- **macOS/Linux**:

  ```sh
  source .venv/bin/activate
  ```

### 4. Install Packages from `requirements.txt`

Once the virtual environment is activated, you can install the packages listed in `requirements.txt`:

```sh
pip install -r requirements.txt
```

## II. Installation - Automating the Process

There is a script to automate the entire process.

#### `setup_env.sh`

Linux/macOS:

```sh
#!/bin/sh

# Create virtual environment
python -m venv .venv

# Activate virtual environment
. .venv/Scripts/activate

# Install packages
pip install -r requirements.txt
```

Windows:

```sh
#!/bin/sh

# Create virtual environment
python -m venv .venv

# Activate virtual environment
. .venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Running the Script

Make the script executable and run it:

```sh
chmod +x setup_env.sh
./setup_env.sh
```

### III. Optional - Using `pipenv`

Alternatively, you can use `pipenv` to manage your virtual environment and dependencies in one step:

1. **Install `pipenv`**:
   ```sh
   pip install pipenv
   ```

2. **Create Virtual Environment and Install Packages**:
   ```sh
   pipenv install -r requirements.txt
   ```

3. **Activate the Virtual Environment**:
   ```sh
   pipenv shell
   ```

## IV. Usage

```bash
python main.py
```

### Specify The Task You Want To Go With

1. (`c`) Specify a certain course's ID to go with.
2. (`p`) Specify a certain path's ID to go with, from there you can select a(ll) or a certain course to continue.
3. (`l`) List out all the recorded Path and continue.

![Welcome Screen](docs/assets/welcome-example.png)

### Hidden Menu

- `99`: **To Fetch Courses List For Each Of The Paths on the first run.** Use this to download all Paths details prior to do anything else later on.
- `5`: Generate prompt for downloaded/fetched course. Output will be save to `data/courses/{course-id-number}-prompt.json`.

![Hidden Menu 99](docs/assets/hidden-menu-99.png)

## Database

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

## Output folder

- The same structure to the above *database* folder.
- All files are Markdown.
- Instead of `id`, the file name is the course/path/lab' names stripped out all the special characters and no more spaces.

```
[your output folder here]
|---courses
|---- A-Course-Name-Here.md
|---labs
|----- A-Lab-Name-Here.md
|---paths
|----- A-Path-Name-Here.md
```

## Example of Obsidian

File View.

![Obsidian File View](docs/assets/obsidian-files.png)

Graph View.

![Obsidian File View](docs/assets/obsidian-graph.png)

The script in action.

![The script in action](docs/assets/script-in-action.png)
