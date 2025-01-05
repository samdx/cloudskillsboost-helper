from config.settings import *
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

# TODO: Make Path() matches the json file structure from the website
