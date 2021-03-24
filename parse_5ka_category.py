# Azamat Khankhodjaev
# 25.09.2020

from parse_5ka import Parse5ka
from parse_5ka_product import Parse5kaProduct

class Parse5kaCategory(Parse5ka):

    def run(self):
        prod_url = "https://5ka.ru/api/v2/special_offers/"
        pre_data = {}

        for category in self._parse(self.start_url):
            new_url = f'{self.start_url}{category["parent_group_code"]}'
            for category_item in self._parse(new_url):
                if category_item['group_code']:
                    product_parse = Parse5kaProduct(prod_url, self.result_path, category_item['group_code'])
                    product_data = product_parse.get_data()
                    if product_data:
                        pre_data['name'] = category_item['group_name']
                        pre_data['code'] = category_item['group_code']
                        pre_data['products'] = product_data
                        self._save(pre_data)

    def _parse(self, url):
        response = self._get_response(url, params=self.params)
        data = response.json()
        return data


