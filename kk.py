import pandas as pd

class KoKa(object):

    def __init__(self):
        self.products = pd.read_json('products.json')
        self.residents = pd.read_json('residents.json')

    def get_subcribers(self, name):
        self.products = pd.read_json('products.json')
        if name not in set(self.products['name']):
            print('Failed: not existing product: ' + name)
            return list() # TODO not been tested!
        else:
            return list(self.products.loc[self.products['name'] == name,'subcribers'])[0]
    def get_dept(self, name):
        self.residents = pd.read_json('residents.json')
        return self.residents.loc[self.residents['name'] == name,'dept']
    def add_to_dept(self, name, value):
        self.residents = pd.read_json('residents.json')
        self.residents.loc[self.residents['name'] == name,'dept'] = self.get_dept(name) + value
        self.residents.to_json('residents.json')
    def def_facto_add_product(self, product_name, subcripers):
        self.products = self.products.append({'name': product_name, 'subcribers': subcripers}, ignore_index=True)
        self.products.to_json('products.json')
    
    def add_product(self, product_name, subcripers):
        """ product_name is the new product name
            subcripers is a dictionaries of elements like {'resident_name':usage_percent} """
        if sum(subcripers.values()) != 100:
            print('Failed: sum of percents should be 100, but was: ' + str(sum(subcripers.values())))
            return 'Failed: sum of percents should be 100, but was: ' + str(sum(subcripers.values()))
        elif product_name in set(self.products['name']):
            print('Failed: product already added ' + product_name)
            return 'Failed: product already added ' + product_name
        else:
            print('Product added: ' + product_name + ', subscriber: ' + str(subcripers))
            # normailze percentages ({'E': 50, 'P': 50} -> {'E': 0.5, 'P': 0.5})
            subcripers = {k: v/100 for k, v in subcripers.items()}
            self.def_facto_add_product(product_name, subcripers)
            return 'Product added: ' + product_name + ', subscriber: ' + str(subcripers)

    def add_record(self, buyer, product_name, value):
        subcribers = self.get_subcribers(product_name)
        print()
        print(buyer + ' paid for ' + product_name + ' in value of ' + str(value))
        print(product_name + ' will be consumed by:')
        for name, percent in subcribers.items():
            print(name + ' in value of ' + str(value * percent))
            self.add_to_dept(name, value * percent)
        self.add_to_dept(buyer, -value)
        return buyer + ' paid for ' + product_name + ' in value of ' + str(value)

    def handle_message(self, m):
        m = m.split(' ')
        if m[0] == 'add_record':
            return self.add_record(m[1], m[2], float(m[3]))
        elif m[0] == 'add_product':
            return self.add_product(m[1], {'P':float(m[2]), 'G':float(m[3]), 'E':float(m[4]), 'A':float(m[5])})
        elif m[0] == 'get_products':
            self.products = pd.read_json('products.json')
            return str(self.products)
        elif m[0] == 'get_residents':
            self.residents = pd.read_json('residents.json')
            return str(self.residents)
        elif m[0] == 'reset_products':
            self.products = pd.DataFrame(columns=['name', 'subcribers'])
            self.products.to_json('products.json')
            return "reset done"
        elif m[0] == 'reset_residents':
            self.residents = pd.DataFrame(
                [{'name': 'P', 'dept': 0},
                {'name': 'G', 'dept': 0},
                {'name': 'E', 'dept': 0},
                {'name': 'A', 'dept': 0}])
            self.residents.to_json('residents.json')
            return "reset done"
        elif m[0] == 'get_products_json':
            self.products = pd.read_json('products.json')
            return str(self.products.to_json())
        elif m[0] == 'get_residents_json':
            self.residents = pd.read_json('residents.json')
            return str(self.residents.to_json())
        else:
            return 'What? Want some candy?'

    def handle_messages(self, ms):
        try:
            ms = ms.split('\n')
            if len(ms) == 1:
                return self.handle_message(ms[0])
            else:
                for m in ms:
                    self.handle_message(m)
                return 'all_done'
        except Exception as e:
            print(e)
            return 'Something terrible happend.'
"""
residents = pd.DataFrame(
    [{'name': 'P', 'dept': 0},
    {'name': 'G', 'dept': 0},
    {'name': 'E', 'dept': 0},
    {'name': 'A', 'dept': 0}])
products = pd.DataFrame(columns=['name', 'subcribers'])

residents.to_json('residents.json')
products.to_json('products.json')
"""
"""
KK = KoKa()
print(KK.handle_messages('add_product elmex 50 0 50 0'))
print(KK.handle_messages('add_record P elmex 800'))
print(KK.handle_messages('get_products'))
print(KK.handle_messages('get_residents'))
"""

"""
self.residents = pd.DataFrame(
    [{'name': 'P', 'dept': 0},
     {'name': 'G', 'dept': 0},
     {'name': 'E', 'dept': 0},
     {'name': 'A', 'dept': 0}])
self.products = pd.DataFrame(columns=['name', 'subcribers'])

handle_message('add_product elmex 50 0 50 0')
handle_message('add_product mez 30 30 30 10')
handle_message('add_product tej 40 30 30 0')
handle_message('add_product tejfol 34 33 33 0')
handle_message('add_product tea 40 20 20 20')
"""

"""
handle_message('add_product elmex 50 0 50 0')
handle_message('add_record P elmex 800')
handle_message('add_product tej 40 30 30 0')
print(handle_message('get_self.products'))
print(handle_message('get_self.residents'))
"""

"""
print(handle_message('add_product elmex 50 0 50 0'))
print(handle_message('add_record P elmex 800'))
print(handle_message('get_self.products'))
print(handle_message('get_self.residents'))
"""

"""
self.residents = pd.DataFrame(
    [{'name': 'P', 'dept': 0},
     {'name': 'G', 'dept': 0},
     {'name': 'E', 'dept': 0},
     {'name': 'A', 'dept': 0}])
self.products = pd.DataFrame(columns=['name', 'subcribers'])

add_product('elmex',  {'P':50,         'E':50}        )
add_product('mez',    {'P':30, 'G':30, 'E':30, 'A':10})
add_product('tej',    {'P':40, 'G':30, 'E':30}        )
add_product('tejfol', {'P':34, 'G':33, 'E':33}        )
add_product('tea',    {'P':40, 'G':20, 'E':20, 'A':20})

add_record('P', 'elmex',  800)
add_record('P', 'mez',    1500)
add_record('P', 'tej',    200)
add_record('P', 'tejfol', 110)
add_record('P', 'tea',    600)
add_record('G', 'tej',    289)
add_record('G', 'mez',    800)
"""