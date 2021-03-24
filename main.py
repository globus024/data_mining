# Azamat Khankhodjaev
# 25.09.2020

# Задача организовать сбор данных,
# необходимо иметь метод сохранения данных в .json файлы
#
# результат: Данные скачиваются с источника, при вызове метода/функции сохранения в файл скачанные данные сохраняются в Json вайлы, для каждой категории товаров должен быть создан отдельный файл и содержать товары исключительно соответсвующие данной категории.
#
# пример структуры данных для файла:
# нейминг ключей можно делать отличным от примера
#
# {
# "name": "имя категории",
# "code": "Код соответсвующий категории (используется в запросах)",
# "products": [{PRODUCT}, {PRODUCT}........] # список словарей товаров соответсвующих данной категории
# }

from pathlib import Path
from parse_5ka_category import Parse5kaCategory

file_path = Path(__file__).parent.joinpath("categories_products")

if not file_path.exists():
    file_path.mkdir()
parser = Parse5kaCategory("https://5ka.ru/api/v2/categories/", file_path)
parser.run()