from datetime import datetime
import json
from config.settings import BASE_URL_COURSES, BASE_URL_LAB, BASE_URL_PATHS, DATA_FOLDER_NAME, OUTPUT_FOLDER_NAME
from pathlib import Path as PathlibPath

from utils.utils import util_replace_special_chars
from .serialize import Serialize


# Base class for all entities including Path, Course, and Lab
class BaseEntity(Serialize):
    def __init__(self,
                 id: str,
                 name: str,
                 type: str,
                 description: str,
                 url: str,
                 date: str = None):
        self.id = id
        self.name = name
        self.type = type
        self.url = url
        self.description = description
        self.date = date or str(datetime.today().date())

    @property
    def type(self):
        """
        Dynamically determine the type based on the class name.
        """
        return self.__class__.__name__

    @property
    def url(self):
        """
        Dynamically generate the URL based on the type.
        """
        base_url = {
            "Path": BASE_URL_PATHS,
            "Course": BASE_URL_COURSES,
            "Lab": BASE_URL_LAB
        }.get(self.type, None)

        if not base_url:
            raise ValueError(f"Invalid entity type: {self.type}")

        return f"{base_url}/{self.id}"

    # Properties to get the JSON and Markdown file names and paths
    @property
    def _json_name(self):
        return f'{self.id}.json'
    
    # Properties to get the JSON and Markdown file names and paths
    @property
    def _md_name(self):
        return f'{util_replace_special_chars(self.name)}.md'

    # Properties to get the JSON and Markdown file names and paths
    @property
    def _json_path(self):
        if self.type == 'Path':
            return PathlibPath(DATA_FOLDER_NAME) / 'paths' / self._json_name
        if self.type == 'Course':
            return PathlibPath(DATA_FOLDER_NAME) / 'courses' / self._json_name
        if self.type == 'Lab':
            return PathlibPath(DATA_FOLDER_NAME) / 'labs' / self._json_name

    # Properties to get the JSON and Markdown file names and paths
    @property
    def _md_path(self):
        if self.type == 'Path':
            return PathlibPath(OUTPUT_FOLDER_NAME) / 'paths' / self._md_name
        if self.type == 'Course':
            return PathlibPath(OUTPUT_FOLDER_NAME) / 'courses' / self._md_name
        if self.type == 'Lab':
            return PathlibPath(OUTPUT_FOLDER_NAME) / 'labs' / self._md_name

    # Convert the entity's data to a dictionary without private attributes
    def to_dict(self):
        """
        Convert the entity's data to a dictionary.
        """

        the_dict = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        the_dict['type'] = self.type
        the_dict['url'] = self.url
        return the_dict

    # Load the entity data from a JSON file
    def load_json(self):
        """
        Load the entity data from a JSON file.
        """

        # If the JSON file doesn't exist, create an empty one with a JSON format
        if not self._json_path.exists():
            with open(self._json_path, 'w', encoding='utf-8', newline='\n') as json_file:
                json_file.write('{}')
        
        # Load the JSON file even if it's empty, and update the entity's data
        try:
            with open(self._json_path, 'r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
                self.__dict__.update(data)
        except FileNotFoundError:
            print(f"\033[33m(BaseEntity.load_json) The BaseEntity's data is not cached. Fetching... from website.\033[0m\n")
        except json.JSONDecodeError:
            print(f"(BaseEntity.load_json) Error decoding JSON from file: {self._json_path}")

    # Save the entity data to a JSON file
    def save_json(self):
        """
        Save the entity data to a JSON file.
        """

        # Convert the entity data to a dictionary, consider to sort the values
        data = self.to_dict()

        json_paths_folder = self._json_path.parent

        # Create the folder if it doesn't exist
        if not json_paths_folder.exists():
            json_paths_folder.mkdir(parents=True, exist_ok=True)

        # Save the data to a JSON file with UTF-8 encoding and Unix line endings
        with open(self._json_path, 'w', encoding='utf-8', newline='\n') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=2)
