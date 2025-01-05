# Description: This file contains the Lab class which is a subclass of BaseEntity.
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

