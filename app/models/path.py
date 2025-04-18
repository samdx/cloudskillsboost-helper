import json
from bs4 import BeautifulSoup
import requests
from config.settings import *
from services.md_helper import MDHelper
from .base_entity import BaseEntity

# Constants for the extraction of the course data
LD_JSON = "script[type='application/ld+json']"

# Path entity
class Path(BaseEntity):
    def __init__(self,
                 id: str,
                 name: str = None,
                 description: str = None,
                 datePublished: str = None,
                 courses: dict = None):
        super().__init__(id,
                         name,
                         description)
        self.datePublished = datePublished
        self.courses = courses or {}

    # Fetch the Path data from the website
    def fetch_data(self):
        """
        Fetch Path data from the website and save it to a JSON file.
        """

        try:
            # Navigate to the path URL
            response = requests.get(self.url, timeout=20)
            response.raise_for_status()

            path_html = BeautifulSoup(response.text, "html.parser")

            # Locate the <script> tag containing the JSON data
            script_element = path_html.select_one(LD_JSON)
            json_content = script_element.string

            # Parse JSON content
            path_data = json.loads(json_content)

        except Exception as error:
            print(f"fetch_data(): Unable to find LD+JSON element - {error}")
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
                "url": course["url"].strip()
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

# TODO: Make Path() matches the json file structure from the website
