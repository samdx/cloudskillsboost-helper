from pathlib import Path as PathlibPath
from config.settings import *
from models.collection import Collection
class CloudSkillsBoost:
    def __init__(self):
        self.paths_collection, self.courses_collection, self.labs_collection = self.load_data()

    @staticmethod
    def load_data():
        col_paths = Collection(type='paths', name='Paths Collection')
        col_paths.load_json()

        col_courses = Collection(type='courses', name='Courses Collection')
        col_courses.load_json()

        col_labs = Collection(type='labs', name='Labs Collection')
        col_labs.load_json()

        return col_paths, col_courses, col_labs

if __name__ == "__main__":

    # Create the OUTPUT FOLDERS if they do not exist
    if not PathlibPath(OUTPUT_FOLDER_NAME).exists():
        PathlibPath(OUTPUT_FOLDER_NAME).mkdir(parents=True, exist_ok=True)
        PathlibPath(OUTPUT_FOLDER_NAME) / 'paths'.mkdir(parents=True, exist_ok=True)
        PathlibPath(OUTPUT_FOLDER_NAME) / 'courses'.mkdir(parents=True, exist_ok=True)
        PathlibPath(OUTPUT_FOLDER_NAME) / 'labs'.mkdir(parents=True, exist_ok=True)
    
    # Create the DATA FOLDERS if they do not exist
    if not PathlibPath(DATA_FOLDER_NAME).exists():
        PathlibPath(OUTPUT_FOLDER_NAME).mkdir(parents=True, exist_ok=True)
        PathlibPath(DATA_FOLDER_NAME) / 'paths'.mkdir(parents=True, exist_ok=True)
        PathlibPath(DATA_FOLDER_NAME) / 'courses'.mkdir(parents=True, exist_ok=True)
        PathlibPath(DATA_FOLDER_NAME) / 'labs'.mkdir(parents=True, exist_ok=True)

    # STARTING THE PROGRAM
    # https://talyian.github.io/ansicolors/
    # https://en.wikipedia.org/wiki/ANSI_escape_code
    print()
    print("\033[45m"
          "=================================================================="
          "\033[0m")
    print("                CloudSkillsBoost Automation Script                ")
    print("NOTE:"
          "\n\tDO NOT NEED TO LOGIN TO CLOUDSKILLSBOOST.GOOGLE"
          "\n\tHOWEVER, TO SAVE THE PROGRESS, PLEASE LOGIN.")
    print("\033[45m"
          "=================================================================="
          "\033[0m"
          "\n")

