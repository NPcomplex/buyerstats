'''
Created on May 27, 2018

@author: Natty
'''

import requests
import json
from connection.tcg_auth import TcgApiAuthenticator

class TcgApiQueryMachine:

    #This needs to be a class so that I can initialize this TODO
    access_dict = {}
    base_url = None
    
    def __init__(self):
        tcg_authenticator = TcgApiAuthenticator(r'C:\development\TCGPlayer_api\buyer_stats\tcg_auth.csv')        
        self.access_dict = tcg_authenticator.get_access_data()
        self.base_url = tcg_authenticator.base_url
    
    #returns: minimum price, the type (normal/foil) AND associated product ID 
    def find_min_price(self, cardname, price_type):
        min_price = None
        min_product_id = None
        min_type = None
        product_ids = self.get_product_ids(cardname)
        for product_id in product_ids:
            product_prices = self.get_product_prices(product_id, price_type)
            for price_entry in product_prices:
                #This is ugly, I can do better, but for some reason None < any number
                if (price_entry['price'] is not None) and ((min_price is None) or (price_entry['price'] < min_price)):
                    min_price = price_entry['price']
                    min_product_id = product_id
                    min_type = price_entry['subTypeName']
            
        #print str(min_product_id) + '\n' + min_type + '\n' + str(min_price)
        return (min_product_id, min_type, min_price)
       
    def get_product_ids(self, cardname):
        head= {"Accept":"application/json",
                "Content-type": "application/json",
                "Authorization": self.access_dict["token_type"] + " " + self.access_dict["access_token"]}
        
        #Hard coding the category and limit here, I should make it more flexible in the future TODO
        param_list = (('categoryId', '1'), ('productName', cardname), ('limit',100))
        ret = requests.get(self.base_url + 'catalog/products', headers = head, params=param_list)
        json_data = json.loads(ret.text)
        
        product_ids = []
        for entry in json_data['results']:
            product_ids.append(entry['productId'])
            
        return product_ids
    
    #I could query the entire list of product IDs here in a single api call TODO    
    def get_product_prices(self, product_id, price_type):
        head= {"Accept":"application/json",
                "Content-type": "application/json",
                "Authorization": self.access_dict["token_type"] + " " + self.access_dict["access_token"]}
        
        #Hard coding the category here, I should make it more flexible in the future TODO
        ret = requests.get(self.base_url + 'pricing/product/' + str(product_id), headers = head)
        json_data = json.loads(ret.text)
        
        prices = []
        for entry in json_data['results']:
            prices.append({'subTypeName':entry['subTypeName'], 'price':entry[price_type]})
            
        return prices
        
        
if __name__ == '__main__':
    api_query_machine = TcgApiQueryMachine()
    api_query_machine.find_min_price('arrest', 'midPrice')