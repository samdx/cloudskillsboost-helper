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


# END OF COURSE CLASS
# END OF FILE
