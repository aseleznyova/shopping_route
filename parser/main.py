import json
import requests
from google.protobuf.json_format import MessageToJson
import str_pb2
import pandas as pd
import sentence_transformers
import re


def cur_store(cur, store, price):
    if store == cur:
        return price
    else:
        return None

class Parser:
    def __init__(self):
        self.offers = pd.DataFrame(columns=[ "name", "weight", "5ka", "magnit-univer", "dixy",
                                            "7shagoff", "tdreal.spb", "lenta-giper", "lenta-super",
                                            "verno", "auchan", "perekrestok"])
        self.model = sentence_transformers.SentenceTransformer('inkoziev/sbert_synonymy')

    def similarity(self, sentence1, sentence2):
        embeddings = self.model.encode([sentence1, sentence2])
        return sentence_transformers.util.cos_sim(a=embeddings[0], b=embeddings[1]).item()

    def parse_page(self, city, store, page_num=1):
        """
        :param city: location of the shop
        :param store: store name
        :param page_num: parsed page number
        :return: None
        """
        url = f"https://squark.edadeal.ru/web/search/offers?count=5&locality={city}&page={page_num}&retailer={store}"
        data = requests.get(url, allow_redirects=True)  # data.content is a protobuf message

        offers = str_pb2.Offers()  # protobuf structure
        offers.ParseFromString(data.content)  # parse binary data
        products: str = MessageToJson(offers)  # convert protobuf message to json
        products = json.loads(products)
        return products

    def parse_store(self, store):
        city = 'kudrovo'
        products = []
        page = 1
        print(store)
        while True:
            print(page)
            offers = self.parse_page(city, store, page)
            if 'offer' not in offers:
                break
            page += 1
            for offer in offers['offer']:
                if 'amount' not in offer:
                    continue
                weight = self.get_weight(offer['name'])
                if not weight:
                    continue
                if (self.offers['weight'] == weight).any():
                    flag = True
                    for index, row in self.offers[self.offers['weight'] == weight].iterrows():
                        if self.similarity(row['name'].lower(), offer['name'].lower()) > 0.90:
                            print(row['name'], offer['name'])
                            row[store] = offer['priceAfter']
                            flag = False
                    if flag:
                        self.offers.loc[len(self.offers.index)] = [offer['name'], weight,
                                                                   cur_store(store, "5ka", offer['priceAfter']),
                                                                   cur_store(store, "magnit-univer",
                                                                             offer['priceAfter']),
                                                                   cur_store(store, "dixy", offer['priceAfter']),
                                                                   cur_store(store, "7shagoff", offer['priceAfter']),
                                                                   cur_store(store, "tdreal.spb", offer['priceAfter']),
                                                                   cur_store(store, "lenta-giper", offer['priceAfter']),
                                                                   cur_store(store, "lenta-super", offer['priceAfter']),
                                                                   cur_store(store, "verno", offer['priceAfter']),
                                                                   cur_store(store, "auchan", offer['priceAfter']),
                                                                   cur_store(store, "perekrestok", offer['priceAfter'])
                                                                   ]
                else:
                    self.offers.loc[len(self.offers.index)] = [ offer['name'], weight,
                                                               cur_store(store, "5ka", offer['priceAfter']),
                                                               cur_store(store, "magnit-univer", offer['priceAfter']),
                                                               cur_store(store, "dixy", offer['priceAfter']),
                                                               cur_store(store, "7shagoff", offer['priceAfter']),
                                                               cur_store(store, "tdreal.spb", offer['priceAfter']),
                                                               cur_store(store, "lenta-giper", offer['priceAfter']),
                                                               cur_store(store, "lenta-super", offer['priceAfter']),
                                                               cur_store(store, "verno", offer['priceAfter']),
                                                               cur_store(store, "auchan", offer['priceAfter']),
                                                               cur_store(store, "perekrestok", offer['priceAfter'])
                                                               ]

    def parse_stores(self):
        with open("conf.json", 'r') as file:
            stores = json.loads(file.read())
        if "stores" not in stores:
            return
        for store in stores["stores"]:
            self.parse_store(store)
        self.offers.to_csv('offers.csv', encoding='utf-8')

    def get_weight(self, str):
        weight = re.search(r'( ?((\d+[*,.\-/]\d+)|(\d+)) ?(Г|г|кг|мл|л|L|шт|пак[\.]?|х|Х)+ ?(х|Х|[*])?){1,2}', str)
        if not weight:
            return None
        num = 0
        value = re.search(r'(Г|г|кг|мл|л|L)', weight.group())
        count = re.search(r'(шт|пак)', weight.group())
        if not value:
            return None
        if count:
            if value.start() < count.start():
                num = re.search(r'((\d+[,.]\d+)|(\d+))', weight.group()[:value.start()]).group()
                count = re.search(r'((\d+[,.]\d+)|(\d+))', weight.group()[value.start():count.start()]).group().replace(',', '.')
            else:
                num = re.search(r'((\d+[,.]\d+)|(\d+))', weight.group()[:count.start()]).group()
                count = re.search(r'((\d+[,.]\d+)|(\d+))', weight.group()[count.start():value.start()]).group().replace(',', '.')
        else:
            count = 1
            num = re.search(r'((\d+[,.]\d+)|(\d+))', weight.group()).group()
        k = 1
        if 'кг' in value.group():
            k = 1000
        if ('л' in value.group() or 'L' in value.group()) and 'мл' not in value.group():
            k = 1000
        return float(num.replace(',', '.')) * k * float(count)


if __name__ == "__main__":
    parser = Parser()
    parser.parse_stores()