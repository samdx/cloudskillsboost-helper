# Description: Configuration file for the project

# Output folder name
OUTPUT_FOLDER_NAME: str = '../cloudskillsboost_md'
DATA_FOLDER_NAME: str = "data"

# Base URL for the Cloud Skills Boost website
BASE_URL: str = "https://www.cloudskillsboost.google"
BASE_URL_PATHS: str = f"{BASE_URL}/paths"
BASE_URL_LAB: str = f"{BASE_URL}/catalog_lab"
BASE_URL_COURSES: str = f"{BASE_URL}/course_templates"
BASE_URL_PARTNERS: str = "https://partner.cloudskillsboost.google"

# Webdriver configuration
WEBDRIVER_PROFILE_FOLDER_NAME: str = '.webdriver_profiles'
WEBDRIVER_OPTIONS_HEADLESS: bool = True

# Constants for the extraction of the course data
PATH_CARDS = "ql-activity-card"
LD_JSON = "script[type='application/ld+json']"
META_DESCRIPTION = "meta[name='description']"
COURSE_OUTLINE = "ql-course-outline"
QL_YOUTUBE_VIDEO = "ql-youtube-video"
QL_IFRAME = "ql-iframe"
LAB_REVIEW_LAB_ID = "#lab_review_lab_id"
LAB_CONTENT_OUTLINE = "ul.lab-content__outline"
LAB_TITLE = "ql-title-medium"
QL_QUIZ = "ql-quiz"
XPATH_START_BUTTON = "//a[@class='start-button button button--positive']"
XPATH_QUIZ = "//ql-quiz"
QUIZ_VERSION = "quizVersion"
QUIZ_ITEMS = "quizItems"
LINK_URL_A_TAG = "ql-card.document-link a"
