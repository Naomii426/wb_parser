import requests
import re
import csv

from models import Items


class ParseWB:
    def __init__(self, url: str):
        self.seller_id = self.__get_seller_id(url)
        self.brand_id = self.__get_brand_id(url)

    @staticmethod
    def __get_item_id(url: str):
        regex = "(?<=catalog/).+(?=/detail)"
        item_id = re.search(regex, url)[0]
        return item_id

    def __get_seller_id(self, url):
        response = requests.get(url=f"https://card.wb.ru/cards/v1/detail?nm={self.__get_item_id(url=url)}")
        seller_id = Items.model_validate(response.json()["data"])
        return seller_id.products[0].supplierId

    def __get_brand_id(self, url):
        response = requests.get(url=f"https://card.wb.ru/cards/v1/detail?nm={self.__get_item_id(url=url)}")
        brand_id = Items.model_validate(response.json()["data"])
        return brand_id.products[0].brandId

    def parse(self):
        _page = 1
        self.__create_csv()
        while True:
            response = requests.get(
                f'https://catalog.wb.ru/brands/t/catalog?appType=1&brand={self.brand_id}&dest=-1257786&supplier={self.seller_id}&page={_page}')
            _page += 1
            items_info = Items.model_validate(response.json()["data"])
            if not items_info.products:
                break
            self.__get_images(items_info)
            self.__save_csv(items_info)

    def __create_csv(self):
        with open("wb_data7.csv", mode="w", newline="", encoding="UTF-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                ['id', 'название', 'цена', 'бренд', 'скидка', 'рейтинг', 'в наличии', 'id продавца', 'id бренда',
                 'Изображения'])

    def __save_csv(self, items):
        with open("wb_data7.csv", mode="a", newline="", encoding="UTF-8") as file:
            writer = csv.writer(file)
            for product in items.products:
                writer.writerow([product.id,
                                 product.name,
                                 product.salePriceU,
                                 product.brand,
                                 product.sale,
                                 product.rating,
                                 product.volume,
                                 product.supplierId,
                                 product.brandId,
                                 product.image_links])

    def __get_images(self, item_model: Items):
        for product in item_model.products:
            _short_id = product.id // 100000
            if 0 <= _short_id <= 143:
                basket = '01'
            elif 144 <= _short_id <= 287:
                basket = '02'
            elif 288 <= _short_id <= 431:
                basket = '03'
            elif 432 <= _short_id <= 719:
                basket = '04'
            elif 720 <= _short_id <= 1007:
                basket = '05'
            elif 1008 <= _short_id <= 1061:
                basket = '06'
            elif 1062 <= _short_id <= 1115:
                basket = '07'
            elif 1116 <= _short_id <= 1169:
                basket = '08'
            elif 1170 <= _short_id <= 1313:
                basket = '09'
            elif 1314 <= _short_id <= 1601:
                basket = '10'
            elif 1602 <= _short_id <= 1655:
                basket = '11'
            elif 1656 <= _short_id <= 1919:
                basket = '12'
            elif 1920 <= _short_id <= 2045:
                basket = '13'
            elif 2046 <= _short_id <= 2189:
                basket = '14'
            else:
                basket = '15'

            url = f"https://basket-{basket}.wbbasket.ru/vol{_short_id}/part{product.id // 1000}/{product.id}/images/big/1.webp"
            res = requests.get(url=url)
            if res.status_code == 200:
                link_str = "".join([
                                       f"https://basket-{basket}.wbbasket.ru/vol{_short_id}/part{product.id // 1000}/{product.id}/images/big/{i}.webp;"
                                       for i in range(1, product.pics)])
                product.image_links = link_str
                link_str = ''


if __name__ == '__main__':
    ParseWB('https://www.wildberries.ru/catalog/14797929/detail.aspx').parse()
