from pydantic import BaseModel, root_validator

class Item(BaseModel):
    id: int
    name: str
    salePriceU: float
    brand: str
    sale: int
    rating: float
    volume: int
    supplierId: int
    brandId: int

    #@root_validator(pre=True)
    #def convert_sale_price(cls,values:dict):
        #sale_price = values.get('salePriceU')
        ### return values

class Items(BaseModel):
    products: list[Item]