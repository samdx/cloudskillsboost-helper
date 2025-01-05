from random import random
import re
import sys
import time
import html2text
from pathlib import Path as PathlibPath
from models.collection import Collection
from models.lab import Lab
from services.md_helper import MDHelper
from .base_entity import BaseEntity
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.webdriver.edge.webdriver import WebDriver
import json
import html
import requests
from bs4 import BeautifulSoup
from config.settings import BASE_URL_COURSES, BASE_URL, BASE_URL_LAB
from utils.utils import util_replace_quote_marks, util_strip_html_tags
from services.launch_browser import launch_browser


# Course entity based on BaseEntity
class Course(BaseEntity):
    def __init__(self,
                 id: str = None,
                 name: str = None,
                 type: str = 'Course',
                 description: str = None,
                 url: str = None,
                 datePublished: str = None,
                 objectives: list = None,
                 topics: list = None,
                 modules: list = None):
        super().__init__(id,
                         name,
                         type,
                         url,
                         description)
        self.datePublished = datePublished or ""
        self.objectives = objectives or []
        self.topics = topics or []
        self.modules = modules or []

    # Fetch the Course data from the website including the course outline, modules, and activities
    def extract_transcript(self) -> None:
        f"""
        Gather transcript of a course. Return its id and name.\
        - Write down the course MD file.
        """

        # TODO: Implement logic for handling a lab, for example:
        # A Tour of Google Cloud Hands-on Labs (1281)

        # Print out the course name if provided
        # if self.name:
        #     print(f"(extract_transcript) \033[45m====| {self.name.upper()} |====\033[0m")

        # Create an instance of the HTML2Text class
        html2md = html2text.HTML2Text()
        html2md.body_width = 0  # Disable word wrapping to minimize newlines
        # h.ignore_links = True  # Ignore links if you don't want them in the output

        # The course URL
        course_url = f"{BASE_URL_COURSES}/{self.id}"

        print("\nTranscript Extracting is starting...\n")

        # Browse the course url
        try:
            response = requests.get(course_url)
            response.raise_for_status()
        except requests.RequestException as get_course_url_error:
            print(f"(extract_transcript) Error: Unable to load the course page. {get_course_url_error}")
            return

        # Parse the HTML content
        course_html = BeautifulSoup(response.text, "html.parser")
        # Get the course properties from the ld+json element including the course objectives, description, etc.
        try:
            course_ld_json_element = course_html.select_one("script[type='application/ld+json']")
            # Locate the <meta> element by its name attribute
            meta_element = course_html.select_one("meta[name='description']")
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
            self.id = course_objectives_json.get('@id').split('/')[-1]
            self.url = course_objectives_json.get('@id')
            self.type = course_objectives_json.get('@type')
            self.name = course_objectives_json.get('name').strip()
            self.description = course_description
            self.datePublished = course_objectives_json.get('datePublished')
            self.topics = course_objectives_json.get('about')
            self.objectives = course_objectives_json.get('teaches')

        except NoSuchElementException as _:
            print(
                f"(extract_transcript) Error: Failed to process the course: {self.id}{': ' + self.name if self.name else ''}.\n")
            return  # Exit the function early

        # Get the course outline
        try:
            course_outline_element = course_html.select_one("ql-course-outline")
            if not course_outline_element:
                raise NoSuchElementException("(extract_transcript) ql-course-outline is not found.")

            # Set the course modules, this is important
            self.modules = json.loads(course_outline_element["modules"])
        except NoSuchElementException as _:
            print(
                f"(extract_transcript) Error: Failed to detect outline for: {self.id}{': ' + self.name if self.name else ''}.")
            return

        # Go through the course modules and extract the transcript for each video
        for module in self.modules:
            module_title = module["title"].strip()
            print(f"(extract_transcript) \033[34m• MODULE: {module_title}\033[0m")

            # Strip out unwanted html tags and special chars (weird quota marks)
            # TODO: Strip any HTML element here, the most common are p, br
            if module.get("description"):
                module_description = util_strip_html_tags(html.unescape(module.get("description")))
                module_description = util_replace_quote_marks(module_description)
            else:
                module_description = ''

            # Set it back to the module
            module['description'] = module_description

            # Go through the steps in the module
            for step in module['steps']:
                activities = step['activities']
                for activity in activities:
                    activity_type = activity['type']
                    activity_id = activity['id']
                    activity_title = activity['title'].strip()
                    activity_full_url = f"{BASE_URL}{activity['href']}"

                    # Proceed logic for video
                    if activity_type == "video":
                        print(f"(extract_transcript) •-> "
                              f"Vid: {activity_id:>6} - {activity_title}")

                        try:

                            response = requests.get(activity_full_url)
                            response.raise_for_status()
                            video_html = BeautifulSoup(response.text, "html.parser")

                            video_element = video_html.select_one("ql-youtube-video")
                            transcript_data = video_element["transcript"]
                            # Please take note: the original value is videoId not videoid
                            # This is because of BeautifulSoup will converts attribute names to lowercase for all
                            video_id = video_element["videoid"]

                            activity['videoId'] = video_id

                            # TODO: Transcript formating with Gemini or LLama
                            # TODO: The auto-generated transcript is sometime very poor quality
                            if transcript_data:
                                transcript_json = json.loads(transcript_data)
                                video_transcript = " ".join([f"{item['text']}" for item in transcript_json])
                                video_transcript = util_replace_quote_marks(video_transcript)
                                activity['transcript'] = video_transcript
                            else:
                                activity['transcript'] = '(No video transcript.)'

                            print(f"(extract_transcript) •-• [+]")

                        except NoSuchElementException as get_video_activity_error:
                            print(f"(extract_transcript) Error: Unable to extract transcript. {get_video_activity_error}")

                    # Proceed logic for lab
                    # TODO: Extract Lab Content
                    elif activity_type == "lab":
                        print(f"(extract_transcript) •-> "
                              f"Lab: {activity_id:>6} - {activity_title}")
                        lab_title = activity_title
                        lab_description = f"{activity['description']}"

                        # Get the lab title, description, and permalink
                        try:
                            response = requests.get(activity_full_url)
                            response.raise_for_status()

                            lab_page_html = BeautifulSoup(response.text, "html.parser")
                            lab_review_lab_id_element = lab_page_html.select_one("#lab_review_lab_id")
                            lab_content_outline_element = lab_page_html.select_one('ul.lab-content__outline')

                            # Getting the lab id, then compile a permalink for the lab
                            lab_id = lab_review_lab_id_element["value"].strip()
                            lab_permalink = f"{BASE_URL_LAB}/{lab_id}"

                            # Extract outline or steps from the lab
                            lab_steps = {}
                            if lab_content_outline_element:
                                for a_tag in lab_content_outline_element.find_all('a'):
                                    step = a_tag['href'][-1]
                                    text = a_tag.text
                                    lab_steps[step] = text

                        except NoSuchElementException as _error:
                            print(f"(extract_transcript) {activity_title}:\n"
                                  f"Unable to locate the id lab_review_lab_id\n")
                            raise NoSuchElementException

                        # Create a Lab instance
                        lab = Lab(
                            id=lab_id,
                            name=lab_title,
                            url=lab_permalink,
                            description=lab_description,
                            steps=lab_steps
                        )

                        # Save the lab data to a JSON file and a Markdown file
                        lab.save_json()
                        lab.save_markdown()

                        # Add the lab to the lab collection
                        labs_collection = Collection(type='labs', name='Labs Collection')
                        labs_collection.load_json()
                        labs_collection.add_item(lab_id, lab_title)
                        labs_collection.save_json()

                        print(f"(extract_transcript) •-• [+]")

                    # Proceed logic for quiz
                    elif activity_type == 'quiz':
                        print(f"(extract_transcript) •-> "
                              f"Qui: {activity_id:>6} - {activity_title}")
                        try:
                            response = requests.get(activity_full_url)
                            response.raise_for_status()
                            quiz_page_html = BeautifulSoup(response.text, "html.parser")

                            # The webpages dynamic and are rendered by JS at client/browser
                            quiz_element = quiz_page_html.select_one("ql-quiz")

                            # Some quiz comes with a Start button and time limited
                            # For that we need help from WebDriver, requests simply can't handle dynamic web pages.
                            if quiz_element is None:
                                # Create a browser instance
                                a_webdriver = launch_browser(None, True)
                                a_webdriver.get(activity_full_url)

                                # Get the Start button and click it
                                start_button = a_webdriver.find_element(By.XPATH,
                                                                        "//a[@class='start-button button button--positive']")
                                start_button.click()

                                # Find the ql-quiz element again
                                quiz_element = a_webdriver.find_element(By.XPATH, "//ql-quiz")
                                quiz_question_data = quiz_element.get_attribute("quizVersion")
                            else:
                                # Again, if it's requests with BeautifulSoup, attrs will be lower():
                                # quizversion vs quizVersion
                                quiz_question_data = quiz_element["quizversion"]

                            # Parse the JSON data
                            quiz_question_json = json.loads(quiz_question_data)
                            # Add the quiz items to the activity
                            activity['quizItems'] = quiz_question_json.get('quizItems')

                            print(f"(extract_transcript) •-• [+]")

                        except NoSuchElementException as quiz_element_error:
                            print(f"(extract_transcript) Error: Failed to get Quiz's text. {quiz_element_error}")

        # Save the course data to a JSON file and a Markdown file
        self.save_json()
        self.save_markdown()

        # Inform the user that the course transcript extraction is completed
        print(f"(extract_transcript) \033[34m•-• COMPLETED: {self.id} - {self.name.upper()}\033[0m\n")

    # Complete the videos in the course
    def complete_videos(self):
        f"""
        Mark the videos to be completed in the course.\n
        PLEASE USE THIS AFTER YOU LOGGED IN TO CLOUDSKILLSBOOST.GOOGLE.COM\n
        Turn off the headless mode to use a graphic browser and login to your account.
        """

        # TODO: Check for the course's json file, if it doesn't exist, no need to fetch the course, just complete the videos.

        # We need a browser to complete the videos
        a_webdriver = launch_browser(None, True)

        # Browse the course url
        try:
            a_webdriver.get(self.url)
        except Exception as get_course_url_error:
            print(f"(complete_videos) Error: Unable to load the course page. {get_course_url_error}")
            input("Press Enter to exit the script.")
            sys.exit(1)

        # Get the course outline
        try:
            course_title = a_webdriver.find_element(By.CSS_SELECTOR,
                                                    ".course-info > .ql-title-medium").text.strip()
            course_outline_element = a_webdriver.find_element(By.XPATH,
                                                              f"//ql-course-outline")

            # The modules list
            course_modules_list = json.loads(course_outline_element.get_attribute("modules"))
        except NoSuchElementException as course_outline_element_error:
            print(f"(complete_videos) Unable to find course outline. {course_outline_element_error}")
            sys.exit(1)

        print(f"(complete_videos) \033[45m====| {course_title.upper()} |====\033[0m")

        # Check Completion status of each video activity.
        for course_module in course_modules_list:
            # Go through the modules
            module_title: str = course_module["title"].strip()
            print(
                f"(complete_videos) \033[34m• {module_title}\033[0m")

            steps: list[dict] = course_module['steps']

            # Go through the steps
            for step in steps:
                activity: dict = step['activities'][0]
                activity_type: str = activity['type']
                activity_id: str = activity['id']
                activity_href: str = activity['href']
                activity_title: str = activity['title'].strip()
                activity_is_complete: bool = activity['isComplete']

                # If the video is not completed yet, let complete it
                if activity_type == "video" and activity_is_complete is False:
                    print(f"(complete_videos) •-> "
                          f"Video: {activity_id:>6} - {activity_title}")

                    # Browse the video page
                    a_webdriver.get(f"{BASE_URL}{activity_href}")

                    # play_video(my_driver)
                    time.sleep(random() * 6 + 6)  # Hold for 10 seconds (or any desired duration)

                    # Mark the video as completed
                    self.mark_completed_button(a_webdriver,
                                               activity_id)
                    print(
                        f"(complete_videos) •-• [+]"
                    )

                    # Hold for a while before moving to the next video
                    time.sleep(random() * 6 + 6)  # Hold for 10 seconds (or any desired duration)

                # If the video is already completed, just print it out
                elif activity_type == "video" and activity_is_complete is True:
                    print(f"(complete_videos) •-• COMPLETED •-"
                          f"Video: {activity_id:>6} - {activity_title}")

    # Find and click the 'Mark as Completed' button for the current activity
    def mark_completed_button(self, mywebdriver: WebDriver, activity_id: str) -> None:
        """
        Find and click the 'Mark as Completed' button for the current activity.
        :param mywebdriver: WebDriver instance
        :param activity_id: ID of the activity
        """

        button_href = f"/course_templates/{self.id}/video/{activity_id}/complete_button"

        try:
            button = mywebdriver.find_element(By.XPATH,
                                              f"//ql-button[@href='{button_href}']")

            # Click on the button
            button.click()
        except NoSuchElementException as mark_completed_button_error:
            print(f"(mark_completed_button) {mark_completed_button_error}")
            # Some video page doesn't have a Mark as Completed button, just move on
            pass


    # Generate the course data to a Markdown file
    def save_markdown(self):
        """
        Write the {self.to_dict()} into a Markdown files for each path.
        """

        # Create an instance of the MDHelper class
        md_helper = MDHelper()

        # Generate the markdown content
        path_md = md_helper.md_helper_course(self.to_dict())

        # Write the markdown content to a file, overwrite if exists
        with open(self._md_path, "w", encoding="utf-8", newline='\n') as md_file:
            md_file.write(path_md)



# END OF COURSE CLASS
# END OF FILE
