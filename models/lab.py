# Description: This file contains the Lab class which is a subclass of BaseEntity.
from services.md_helper import MDHelper
from .base_entity import BaseEntity

# Lab entity based on BaseEntity
class Lab(BaseEntity):
    def __init__(self,
                 id: str,
                 name: str,
                 description: str,
                 url: str,
                 steps: dict,
                 type: str = 'Lab'):
        super().__init__(id,
                         name,
                         type,
                         description,
                         url)
        self.steps = steps or {}

    # Save the Lab data to a Markdown file
    def save_markdown(self):
        """
        Write the {self.to_dict()} into a Markdown files for each path.
        """
        # Until we extract the lab content, for time being,
        # can use the same helper for Path
        md_helper = MDHelper()
        # Generate the markdown content
        path_md = md_helper.md_helper_lab(self.to_dict())

        # Write the markdown content to a file, overwrite if exists
        with open(self._md_path, "w", encoding="utf-8", newline='\n') as md_file:
            md_file.write(path_md)
