# Azamat Khankhodjaev
# 25.03.2021
from magnit_parser import MagnitParse
from datetime import datetime
from urllib.parse import urljoin
import bs4


class MagnitParseFull(MagnitParse):

    def __init__(self, start_url, mongo_url):
        super().__init__(start_url, mongo_url)

    @property
    def template(self):
        data_template = {
            "url": lambda a: urljoin(self.start_url, a.attrs.get("href", "/")),
            "promo_name": lambda a: a.find("div", attrs={"class": "card-sale__header"}).text,
            "product_name": lambda a: a.find("div", attrs={"class": "card-sale__title"}).text,
            "image_url": lambda a: urljoin(
                self.start_url, a.find("picture").find("img").attrs.get("data-src", "/")
            ),
            "date_from": lambda a: self.get_datetime_by_str(
                a.find("div", attrs={"class": "card-sale__date"})
                    .find('p').text
            ),
            "date_to": lambda a: self.get_datetime_by_str(
                a.find("div", attrs={"class": "card-sale__date"})
                    .find('p')
                    .find_next_sibling("p").text
            ),
            "old_price": lambda a: self.get_price(
                a.find("div", attrs={"class": "label__price label__price_old"})
                    .find("span", attrs={"class": "label__price-integer"}),
                a.find("div", attrs={"class": "label__price label__price_old"})
                    .find("span", attrs={"class": "label__price-decimal"})),

            "new_price": lambda a: self.get_price(
                a.find("div", attrs={"class": "label__price label__price_new"})
                    .find("span", attrs={"class": "label__price-integer"}),
                a.find("div", attrs={"class": "label__price label__price_new"})
                    .find("span", attrs={"class": "label__price-decimal"})),
        }
        return data_template

    # def get_product_name(self, prod_name:bs4.BeautifulSoup):
    #     print(prod_name.text)
    #     if prod_name.text:
    #         return prod_name.text
    #     raise AttributeError('Product name empty')

    def _parse(self, soup):
        products_a = soup.find_all("a", attrs={"class": "card-sale"})
        for prod_tag in products_a:
            if prod_tag.find("div", attrs={"class": "card-sale__title"}):
                product_data = {}
                for key, func in self.template.items():
                    try:
                        product_data[key] = func(prod_tag)
                    except AttributeError:
                        pass
                yield product_data

    def get_price(self, price_int: bs4.BeautifulSoup, price_dec: bs4.BeautifulSoup):
        if price_int:
            price_int = price_int.text
        if price_dec:
            price_dec = price_dec.text
        if price_int.isnumeric() and price_dec.isnumeric():
            return float(f'{price_int}.{price_dec}')
        return None

    def get_datetime_by_str(self, date_str: str):
        if date_str == '':
            return None

        date_str = date_str.replace('с ', '')
        date_str = date_str.replace('до ', '')

        date_list = {
            'января': '01',
            'февраля': '02',
            'марта': '03',
            'апреля': '04',
            'мая': '05',
            'июня': '06',
            'июля': '07',
            'августа': '08',
            'сентября': '09',
            'октября': '10',
            'ноября': '11',
            'декабря': '12',
        }
        date_str_spl = date_str.split()

        if len(date_str_spl) > 1:
            day = date_str_spl[0]
            month_ru = date_str_spl[1]
            if month_ru in date_list and day != '':
                month = date_list[month_ru]
                today = datetime.today()
                current_year = today.year
                date_res = f'{current_year}-{month}-{day}'
                date_t = datetime.strptime(date_res, '%Y-%m-%d')
                return date_t
        return None


if __name__ == '__main__':
    url = "https://magnit.ru/promo/"
    mongo_url = "mongodb://localhost:27017"
    parser = MagnitParseFull(url, mongo_url)
    parser.run()
