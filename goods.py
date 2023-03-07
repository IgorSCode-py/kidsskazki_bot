#This module is for reating list of selling goods (price list)
#Now it`s hardcoding because there are only 3 goods

class Goods:
    def __init__(self, title, description, payload, price, photo_url, telegram_channel_id):
        self.title = title
        self.description = description
        self.payload = payload
        self.price = price
        self.photo_url = photo_url
        self.telegram_channel_id = telegram_channel_id

#hardcoding 3 goods
#if you have more goods, use database for storing goods and creating class Good
def get_goods():
    pricelist = {}

    #1-st
    pricelist['Custom-Payload-1'] = Goods(title="Кот Огонëк короткие сказки",
                            description="Сказки для быстрого засыпания",
                            payload="Custom-Payload-1",
                            price=100,
                            photo_url='https://thumb.tildacdn.com/tild6631-3166-4163-a162-323036373962/-/format/webp/____1024.jpg',
                            telegram_channel_id=-1001669090613
                          )
    #2-nd
    pricelist['Custom-Payload-2'] = Goods(title="Кот Огонëк 45 минут",
                            description='Длинная сказка для быстрого засыпания',
                            payload="Custom-Payload-2",
                            price=150,
                            photo_url='https://thumb.tildacdn.com/tild6139-3164-4664-a135-323136313164/-/format/webp/1675765768559.jpg',
                            telegram_channel_id=-1001862709465
                          )
    #3-rd
    pricelist['Custom-Payload-3'] = Goods(title="28 сказок про буквы",
                            description='28 сказок про буквы русского алфавита',
                            payload="Custom-Payload-3",
                            price=200,
                            photo_url='https://thumb.tildacdn.com/tild3239-3537-4262-a366-373739623239/-/format/webp/___2400_5.jpg',
                            telegram_channel_id=-1001625228766
                          )


    return pricelist



if __name__ == "__main__":
    get_goods()