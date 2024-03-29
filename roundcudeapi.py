from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from myby import by
import json
import time
import os


class RoundcudeAPI:

    def __init__(self, config_file: str = "config.json", headless: bool = True) -> None:
        with open(config_file) as f:
            config: dict = json.load(f)
        
        self.username = config.get("username")
        self.password = config.get("password")
        self.portail = config.get("portail")

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
        self.driver.get(f"https://{self.portail}:8443/login?service=https%3A%2F%2F{self.portail}%2Froundcube%2F%3F_task%3Dmail%26_action%3Dlogin")
        self.send_keys(by.id, 'username', self.username)
        self.send_keys(by.id, 'password', self.password)
        self.click(by.id, 'valider')

    def _go_home(self):
        self.click(by.xpath, '//*[@id="rcmbtn101"]')
    
    def send_msg(self, name, object, content):
        self.click(by.xpath, '//*[@id="rcmbtn100"]')
        input_dest = self.find(by.xpath, '//*[@id="compose_to"]/div/div/ul/li/input')
        input_dest.send_keys(name)
        time.sleep(3)
        input_dest.send_keys(Keys.TAB)
        self.send_keys(by.xpath, '//*[@id="compose-subject"]', object)
        self.driver.execute_script('''
            var iframe = document.getElementById('composebody_ifr');

            if (iframe) {
                var iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
                
                if (iframeDocument) {
                    var paragraph = iframeDocument.querySelector('p');
                    
                    if (paragraph) {
                        paragraph.textContent = "x280"
                        console.log(paragraph.innerText);
                    }
                }
            }
        '''.replace("x280", content))
        self.click(by.xpath, '//*[@id="rcmbtn111"]')
        time.sleep(.1)

    def get_latest_msg(self):
        data = {}
        msg_object = self.find(by.class_name, "message")
        msg_object.click()
        author_element = msg_object.find_element(by.class_name, 'rcmContactAddress')
        object_element = msg_object.find_element(by.class_name, 'subject')
        date_element = msg_object.find_element(by.class_name, 'date')

        piece_jointe_element = msg_object.find_element(by.class_name, 'attachment')
        innerHtml = self.driver.execute_script("return arguments[0].innerHTML", piece_jointe_element)
        if innerHtml == '&nbsp;':
            piece_jointe = {}
        else:
            time.sleep(2)
            someone = self.driver.execute_script('''
                var iframe = document.getElementById('messagecontframe');

                if (iframe) {
                    var iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
                    
                    if (iframeDocument) {
                        var name = iframeDocument.querySelector('span.attachment-name').textContent;
                        var size = iframeDocument.querySelector('span.attachment-size').textContent;
                        var path = iframeDocument.querySelector('a.filename').getAttribute("href")
                        return [name, size, path]
                    }
                }
            ''')
            piece_jointe = {
                "name": someone[0],
                "size": someone[1].removeprefix("(").removeprefix('~').removesuffix(")"),
                "path": self.driver.current_url.split("?")[0] + someone[2].removeprefix("./")
            }
        
        data["author"] = author_element.text
        data["object"] = object_element.text.split("\n")[-1]
        data["date"] = date_element.text
        data["piece jointe"] = piece_jointe

        return data

