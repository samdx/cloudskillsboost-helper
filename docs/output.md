## Output

### The output folder

- Define in `config/settings.py`:

```python
# Output folder name
OUTPUT_FOLDER_NAME: str = '../cloudskillsboost_md'
```

Attributes:

- The same structure to the `data` folder.
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

### Output Markdown Files

- A Collection: [Paths Collection](samples/paths.md)

```yaml
---
type: paths
name: 'Paths Collection'
url: https://www.cloudskillsboost.google
date: 2025-01-05
---

# [Paths Collection](https://www.cloudskillsboost.google)
```

- A Path: [Google Cloud Applied AI Summit Learning Path](samples/output/paths/Google-Cloud-Applied-AI-Summit-Learning-Path.md)

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

- A Course: [Conversational AI on Vertex AI and Dialogflow CX](samples/output/courses/Conversational-AI-on-Vertex-AI-and-Dialogflow-CX.md)

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

### PDF Files

May or may come with table of content, it's up to user.

- Path: [Google Cloud Applied AI Summit Learning Path](samples/output/paths/Google-Cloud-Applied-AI-Summit-Learning-Path.pdf)
- Course: [Conversational AI on Vertex AI and Dialogflow CX](samples/output/courses/Conversational-AI-on-Vertex-AI-and-Dialogflow-CX.pdf)
