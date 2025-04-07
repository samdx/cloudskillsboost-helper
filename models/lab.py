# Description: This file contains the Lab class which is a subclass of BaseEntity.
from services.md_helper import MDHelper
from .base_entity import BaseEntity

# Lab entity based on BaseEntity
class Lab(BaseEntity):
    def __init__(self,
                 id: str,
                 name: str = None,
                 description: str = None,
                 url: str = None,
                 steps: dict = None,
                 type: str = 'Lab'):
        super().__init__(id,
                         name,
                         type,
                         description,
                         url)
        self.steps = steps or {}

