# Azamat Khankhodjaev
# 25.09.2020

from pathlib import Path
from parse_5ka import Parse5ka


class Parse5kaProduct(Parse5ka):
    params = {
        "records_per_page": 20,
    }
    _data = []

    def __init__(self, start_url: str, result_path: Path, category_id: int):
        super(Parse5kaProduct, self).__init__(start_url, result_path)
        self.start_url = start_url
        self.result_path = result_path
        self.params['categories'] = category_id
        self.run()

    def run(self):
        for product in self._parse(self.start_url):
            self._data.append(product)

    def _parse(self, url):
        while url:
            response = self._get_response(url, params=self.params)
            data = response.json()
            url = data.get("next")
            for product in data.get("results", []):
                yield product

    def get_data(self):
        return self._data

