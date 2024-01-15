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

    def __get_brand_id(self,url):
        response = requests.get(url=f"https://card.wb.ru/cards/v1/detail?nm={self.__get_item_id(url=url)}")
        brand_id = Items.model_validate(response.json()["data"])
        return brand_id.products[0].brandId
    def parse(self):
        _page = 1
        self.__create_csv()
        while True:
            response = requests.get(f'https://catalog.wb.ru/brands/t/catalog?appType=1&brand={self.brand_id}&dest=-1257786&supplier={self.seller_id}&page={_page}')
            _page += 1
            items_info = Items.model_validate(response.json()["data"])
            if not items_info.products:
                break
            self.__save_csv(items_info)




    def __create_csv(self):
        with open("wb_data1.csv", mode="w", newline="",encoding="UTF-8") as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'название', 'цена', 'бренд', 'скидка', 'рейтинг', 'в наличии', 'id продавца', 'id бренда'])


    def __save_csv(self, items):
        with open("wb_data1.csv", mode="a", newline="",encoding="UTF-8") as file:
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
                                 product.brandId])


if __name__ == '__main__':
    ParseWB('https://www.wildberries.ru/catalog/138892916/detail.aspx').parse()
