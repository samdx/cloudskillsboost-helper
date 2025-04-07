
import json
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from config.settings import BASE_URL_PATHS

# Constants for the extraction of the course data
LD_JSON = "script[type='application/ld+json']"

class DataManagement():
    
    def fetch_path_data(path_id):
        
        """
        Fetch path data based on the provided path_id.
        """
        # Path URL
        a_path = Path(id=path_id)

        try:
            # Navigate to the path URL
            response = requests.get(a_path.url, timeout=20)
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
                "url": course["url"]
            }

        # Core Path details
        a_path.name = path_data['name'].strip()
        a_path.description = path_data['description'].strip()
        a_path.datePublished = path_data['datePublished'].strip()

        # Courses list of the Path
        a_path.courses = courses_list

        a_path.save_json()
        a_path.save_markdown()

    def fetch_course_data(course_id):

        """
        Fetch course data from the website and save it to a JSON file.
        """

        pass

    def fetch_lab_data(lab_id):
        """
        Fetch lab data based on the provided lab_id.
        """

        pass
