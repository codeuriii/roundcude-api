from selenium import webdriver
from selenium.webdriver.edge.options import Options
from myby import by
import json


class RoundcudeAPI:

    def __init__(self, config_file: str = "config.json") -> None:
        with open(config_file) as f:
            config: dict = json.load(f)
        
        self.username = config.get("username")
        self.password = config.get("password")