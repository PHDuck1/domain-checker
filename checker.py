import re
import time
import json
from typing import Union, List
from pathlib import Path

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class TextToCheckIfFreeIsNotProvidedException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DomainChecker:
    """
    A class for checking the availability of domains on a website.

    Attributes:
    - url (str): The URL of the website to check.
    - output_dir (str or Path): The directory in which to save the output file. If not specified,
      the directory where the calling script is located will be used.
    - timing (float or int): The number of seconds to wait for the webpage to load before
      checking whether a domain is free or taken.

    Methods:
    - __init__(self, url, output_dir=None, timing=1.5): Initializes a new DomainChecker instance.
    - run(self, filename='text.txt', by=By.TAG_NAME, value='input', free_text='', taken_text=''):
      Runs the process of checking each domain.
    - dump_output(self): Saves the list of free and taken domains as a JSON file.
    - login(self): Logs in to the website, if required.
    - get_input_domains(filename): Retrieves the list of domains to check from a text file.
    - check_if_free(self, check_field, domain, free_text=None, taken_text=None): Inputs a domain into
      the specified field on the webpage and checks if it is free or taken.

    Note: The `login` method should be overridden if the website asks for some sort of authentication.
    """
    def __init__(self, url: str, output_dir: Union[str, Path] = None, timing: Union[float, int] = 1.5) -> None:
        self.url = url
        if output_dir is None:
            # Use the directory where the calling script is located
            self.output_dir = Path().resolve() / 'output'
        else:
            self.output_dir = Path(output_dir).resolve()
        self.output_file = self.output_dir / f'output{self._get_output_index()}.json'
        self.driver = webdriver.Chrome()
        self.timing = timing
        self.free_list = []
        self.taken_list = []
        self.login()

    def _get_output_index(self) -> int:
        """Checks output dir: if output{n}.json file is present finds the next free n"""
        output_index = 0
        pattern = re.compile(r"(output)(\d+)\.json")
        for file in self.output_dir.glob(".json"):
            match = pattern.match(file.name)
            if match:
                n = int(match.group(2))
                output_index = max(output_index, n)

        return output_index

    def login(self) -> None:
        """This method should be overridden if website asks for some sort of authentication"""
        self.driver.get(self.url)

    @staticmethod
    def get_input_domains(filename: Union[str, Path]) -> List[str]:
        """Get domains to check from file (each domain should be on separate line)"""
        with open(filename, 'r') as file:
            domains = file.read().splitlines()
        return domains

    def dump_output(self) -> None:
        """Saves dictionaries with processed domains as into output file in output dir"""
        self.output_dir.mkdir(exist_ok=True, parents=True)

        with open(self.output_file, 'w') as output_json:
            json.dump({'Free': self.free_list, 'Taken': self.taken_list}, output_json, indent=4)

    def check_if_free(self, check_field, domain: str, free_text: str = None, taken_text: str = None) -> bool:
        """Input domain into field and wait if taken or free tag appeared on the page"""
        check_field.send_keys(domain)
        time.sleep(1)

        if free_text:
            try:
                WebDriverWait(self.driver, self.timing).until(
                    expected_conditions.text_to_be_present_in_element(
                        (By.XPATH, f"//*[contains(text(), '{free_text}')]"), free_text))
                return True
            except TimeoutException:
                return False

        elif taken_text:
            try:
                WebDriverWait(self.driver, self.timing).until(
                    expected_conditions.text_to_be_present_in_element(
                        (By.XPATH, f"//*[contains(text(), '{taken_text}')]"), taken_text))
                return False
            except TimeoutException:
                return True

        else:
            raise TextToCheckIfFreeIsNotProvidedException("Either free text or taken text must be provided")

    def run(self, filename='text.txt', by=By.TAG_NAME, value='input', free_text: str = '', taken_text: str = ''):
        """Run process of checking each domain"""
        try:
            check_field = self.driver.find_element(by, value)
            for domain in self.get_input_domains(filename):
                free = self.check_if_free(check_field, domain, free_text=free_text, taken_text=taken_text)
                if free:
                    self.free_list.append(domain)
                else:
                    self.taken_list.append(domain)
                check_field.clear()
        except Exception as e:
            self.dump_output()
            print('Output saved')
            raise e
        except KeyboardInterrupt:
            self.dump_output()
            print('Output saved')
