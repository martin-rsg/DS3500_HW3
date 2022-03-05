
import pprint as pp
import copy

class Orderbook:

    def __init__(self):
        self.orderBook = {}
        self.order_number = 1

    def add_order(self, priority, order_quantity, product_code):

        self.orderBook[copy.deepcopy(self.order_number)] = {'priority': priority,
                                                           'order_quantity': order_quantity,
                                                           'product_code': product_code}
        self.order_number += 1

    def add_orders_from_json(self, json):
        pass



    def remove_order(self, order_number):

        self.orderBook.remove(order_number)


