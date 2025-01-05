import json
from bs4 import BeautifulSoup
import requests
from config.settings import *
from services.md_helper import MDHelper
from .base_entity import BaseEntity


# Path entity
class Path(BaseEntity):
    def __init__(self,
                 id: str = None,
                 name: str = None,
                 type: str = 'Path',
                 description: str = None,
                 url: str = None,
                 datePublished: str = None,
                 courses: dict = None):
        super().__init__(id,
                         name,
                         type,
                         url,
                         description)
        self.datePublished = datePublished
        self.courses = courses or {}

    # Fetch the Path data from the website
    def fetch_data(self):

        # Path URL
        self.url = f'{BASE_URL_PATHS}/{self.id}'

        try:
            # Navigate to the path URL
            response = requests.get(self.url, timeout=20)
            response.raise_for_status()

            path_html = BeautifulSoup(response.text, "html.parser")

            # Locate the <script> tag containing the JSON data
            script_element = path_html.select_one("script[type='application/ld+json']")
            json_content = script_element.string

            # Parse JSON content
            path_data = json.loads(json_content)

        except Exception as error:
            print(f"fetch_course(): Unable to find LD+JSON element - {error}")
            return {}

        # Process Path and Courses data
        # Extract course details, collect id and name only
        courses_list: dict[str, dict] = {}

        # A Path JSON element should and must have 'hasPart' key
        for course in path_data['hasPart']:
            course_id = course['url'].split('/')[-1]
            courses_list[course_id] = {
                "id": course_id,
                "type": course["@type"],
                "name": course["name"].strip(),
                "url": course["url"]
            }

        # Core Path details    
        self.name = path_data['name'].strip()
        self.description = path_data['description'].strip()
        self.datePublished = path_data['datePublished'].strip()

        # Courses list of the Path
        self.courses = courses_list

    # Print out the courses list of a certain Path
    def courses_list(self):
        """
        Print out the courses list of a certain Path.
        """
        # Show the Path Title
        heading = f"{self.id} - {self.name.upper()}"
        print(f"\n\033[45m[{heading:^85}]\033[0m\n")

        # Print out each course in the Path
        for course in self.courses.values():
            course_id = course['id']
            course_name = course['name']
            print(f"+|-• \033[35m[{course_id:>5} - {course_name:<72}]\033[0m")

    # Generate a Markdown file for the Path
    def save_markdown(self):
        """
        Write the {self.to_dict()} into a Markdown files for each path.
        """

        # Create a new instance of MDHelper
        md_helper = MDHelper()
        # Generate the markdown content
        path_md = md_helper.md_helper_path(self.to_dict())

        # Create the folder if it doesn't exist
        md_path_folder = self._md_path.parent
        if not md_path_folder.exists():
            md_path_folder.mkdir(parents=True, exist_ok=True)

        # Write the markdown content to a file, overwrite if exists
        with open(self._md_path, "w", encoding="utf-8", newline='\n') as md_file:
            md_file.write(path_md)

# TODO: Make Path() matches the json file structure from the website
