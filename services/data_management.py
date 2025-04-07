
import html
import json
from pathlib import Path
import re
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
import requests
from config.settings import LD_JSON, COURSE_META_DESCRIPTION, COURSE_OUTLINE
from models.course import Course
from utils.utils import util_replace_quote_marks, util_strip_html_tags

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

        # The course URL
        a_course = Course(id=course_id)

        # Browse the course url
        try:
            response = requests.get(a_course.url, timeout=20)
            response.raise_for_status()
        except requests.RequestException as get_course_url_error:
            print(f"(extract_transcript) Error: Unable to load the course page. {get_course_url_error}")
            return

        # Parse the HTML content
        course_html = BeautifulSoup(response.text, "html.parser")

        # Get the course properties from the ld+json element including the course objectives, description, etc.
        try:
            course_ld_json_element = course_html.select_one(LD_JSON)
            # Locate the <meta> element by its name attribute
            meta_element = course_html.select_one(COURSE_META_DESCRIPTION)
            # meta_element = course_html.find("meta", {"name": "description"})

            if not course_ld_json_element or not meta_element:
                raise NoSuchElementException("(write_script) meta_element not found.")

            course_ld_json_text = course_ld_json_element.string

            # Extract the content attribute
            course_description = html.unescape(meta_element['content'])
            course_description = util_strip_html_tags(course_description)
            # Strip out extra \n caused by multiple <p> or <br/>
            # The code is not clean, I know, but it works. Damn the text.
            course_description = re.sub(r'\s{2,}', '\n\n', course_description)
            course_description = util_replace_quote_marks(course_description)

            course_objectives_json = json.loads(course_ld_json_text)

            # Set the course properties
            a_course.id = course_objectives_json.get('@id').split('/')[-1]
            a_course.url = course_objectives_json.get('@id')
            a_course.type = course_objectives_json.get('@type')
            a_course.name = course_objectives_json.get('name').strip()
            a_course.description = course_description
            a_course.datePublished = course_objectives_json.get('datePublished')
            a_course.topics = course_objectives_json.get('about')
            a_course.objectives = course_objectives_json.get('teaches')

        except NoSuchElementException as _:
            print(
                f"(fetch_data) Error: Failed to process the course: {a_course.id}{': ' + a_course.name if a_course.name else ''}.\n")
            return  # Exit the function early

        # Get the course outline
        try:
            course_outline_element = course_html.select_one(COURSE_OUTLINE)
            if not course_outline_element:
                raise NoSuchElementException("(fetch_data) ql-course-outline is not found.")

            # Set the course modules, this is important
            a_course.modules = json.loads(course_outline_element["modules"])
        except NoSuchElementException as _:
            print(
                f"(fetch_data) Error: Failed to detect outline for: {a_course.id}{': ' + a_course.name if a_course.name else ''}.")
            return

        # Save the course data to a JSON file and a Markdown file
        a_course.save_json()
        a_course.save_markdown()

    def fetch_lab_data(lab_id):
        """
        Fetch lab data based on the provided lab_id.
        """

        pass
