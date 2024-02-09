from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from myby import by
import json


class RoundcudeAPI:

    def __init__(self, config_file: str = "config.json", headless: bool = True) -> None:
        with open(config_file) as f:
            config: dict = json.load(f)
        
        self.username = config.get("username")
        self.password = config.get("password")

        options = Options()
        if headless:
            options.add_argument("headless")
        else:
            options.add_argument("start-maximized")
        self.driver = webdriver.Edge(options)
        self.webdriverwait = WebDriverWait(self.driver, 30)

    def wait(self, whatby, path):
        self.webdriverwait.until(EC.visibility_of_element_located((whatby, path)))

    def find(self, whatby, path):
        self.wait(whatby, path)
        return self.driver.find_element(whatby, path)

    def click(self, whatby, path):
        self.find(whatby, path).click()
    
    def send_keys(self, whatby, path, content):
        self.find(whatby, path).send_keys(content)

    def login(self):
        self.driver.get("https://portail.lyc-leverger.ac-reunion.fr:8443/login?service=https%3A%2F%2Fportail.lyc-leverger.ac-reunion.fr%2Froundcube%2F%3F_task%3Dmail%26_action%3Dlogin")
        self.send_keys(by.id, 'username', self.username)
        self.send_keys(by.id, 'password', self.password)
        self.click(by.id, 'valider')
    
    