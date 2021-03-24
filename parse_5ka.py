# Azamat Khankhodjaev
# 25.09.2020

import time
import json
from pathlib import Path
import requests
from abc import ABC,abstractmethod


class Parse5ka(ABC):
    params = {
        "records_per_page": 20,
    }

    def __init__(self, start_url: str, result_path: Path):
        self.start_url = start_url
        self.result_path = result_path

    def _get_response(self, url, *args, **kwargs) -> requests.Response:
        while True:
            response = requests.get(url, *args, **kwargs)
            if response.status_code == 200:
                return response
            time.sleep(1)

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def _parse(self, url):
        pass

    def _save(self, data):
        file_path = self.result_path.joinpath(f'{data["code"]}.json')
        file_path.write_text(json.dumps(data))

