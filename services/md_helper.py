from typing import Dict
from utils.utils import util_replace_special_chars  # Correct import

class MDHelper:

    @staticmethod
    def md_helper_path(data: Dict) -> str:
        markdown = []

        # Add front matter
        front_matter_lines = ["---"]
        for key, value in data.items():
            if key == "description" or key == "courses" or key == 'steps':
                continue

            if key == "topics" and data['topics']:
                front_matter_lines.append(f"{key}:")
                for topic in value:
                    front_matter_lines.append(f"- {topic}")
                continue

            if key == "name":
                front_matter_lines.append(f"{key}: '{value}'")
                continue

            front_matter_lines.append(f"{key}: {value}")
        front_matter_lines.append("---")
        markdown.append("\n".join(front_matter_lines))

        # The # main heading
        markdown.append(f"# [{data['name']}]({data['url']})")

        # Add description
        if "description" in data:
            markdown.append(f"{data['description']}")

        # Add courses belong to a Path
        if data["type"] == 'Path' and "courses" in data:
            markdown.append("## Courses & Progress")
            course_list = []
            for course_id, course in data["courses"].items():
                course_md_name = f"{util_replace_special_chars(course['name'])}.md"
                course_list.append(f"- [ ] [{course['name']} ({course_id})](../courses/{course_md_name})")
            markdown.append("\n".join(course_list))
        
        if data['type'] == 'Lab' and 'steps' in data:
            for step_number, step_text in data['steps'].items():
                markdown.append(f"## Step {step_number}: {step_text}")

        return "\n\n".join(markdown) + "\n"

    @staticmethod
    def md_helper_lab(data: Dict) -> str:
        markdown = []

        # Add front matter
        front_matter_lines = ["---"]
        for key, value in data.items():
            if key == "description" or key == 'steps':
                continue

            if key == "name":
                front_matter_lines.append(f"{key}: '{value}'")
                continue

            front_matter_lines.append(f"{key}: {value}")
        front_matter_lines.append("---")
        markdown.append("\n".join(front_matter_lines))

        # The # main heading
        markdown.append(f"# [{data['name']}]({data['url']})")

        # Add description
        if "description" in data:
            markdown.append(f"{data['description']}")
        
        # Add steps belong to a Lab, each step is a sub-heading at level 2
        if data['type'] == 'Lab' and 'steps' in data:
            for step_number, step_text in data['steps'].items():
                markdown.append(f"## Step {step_number}: {step_text}")

        return "\n\n".join(markdown) + "\n"
