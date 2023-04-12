import re
import time
import json
from typing import Union, List
from selenium import webdriver
from pathlib import Path


class DomainChecker:

    def __init__(self, url: str, output_dir: Union[str, Path] = None) -> None:
        self.url = url
        if output_dir is None:
            # Use the directory where the calling script is located
            self.output_dir = Path().resolve() / 'output'
        else:
            self.output_dir = Path(output_dir).resolve()
        self.output_file = self.output_dir / f'output{self._get_output_index()}.json'
        self.driver = webdriver.Chrome()
        self.free_list = []
        self.taken_list = []

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

    def login(self):
        """This method should be overridden if website asks for some sort of authentication"""
        pass

    @staticmethod
    def get_input_domains(filename: Union[str, Path]) -> List[str]:
        """Get domains to check from file (each domain should be on separate line)"""
        with open(filename, 'r') as file:
            domains = file.read().splitlines()
        return domains

    def dump_output(self):
        """Saves dictionaries with processed domains as into output file in output dir"""
        self.output_dir.mkdir(exist_ok=True, parents=True)

        with open(self.output_file, 'w') as output_json:
            json.dump({'Free': self.free_list, 'Taken': self.taken_list}, output_json, indent=4)

    def check_if_free(self, check_field, domain: str, free_text: str = None, taken_text: str = None) -> bool:
        check_field.send_keys(domain)

        time.sleep(1)
        return True
