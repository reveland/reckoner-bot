import pandas as pd

class KK(object):

    def __init__(self):
        self.residents = pd.DataFrame(
            [{'name': 'P', 'dept': 0},
            {'name': 'G', 'dept': 0},
            {'name': 'E', 'dept': 0},
            {'name': 'A', 'dept': 0}])
        self.products = pd.DataFrame(columns=['name', 'subcribers'])

    def get_subcribers(self, name):
        if name not in set(self.products['name']):
            print('Failed: not existing product: ' + name)
            return list() # TODO not been tested!
        else:
            return list(self.products.loc[self.products['name'] == name,'subcribers'])[0]
    def get_dept(self, name):
        return self.residents.loc[self.residents['name'] == name,'dept']
    def add_to_dept(self, name, value):
        self.residents.loc[self.residents['name'] == name,'dept'] = self.get_dept(name) + value
    def def_facto_add_product(self, product_name, subcripers):
        self.products =  self.products.append({'name': product_name, 'subcribers': subcripers}, ignore_index=True)
    
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

    def handle_message(self, p):
        p = p.split(' ')
        try:
            if p[0] == 'add_record':
                return self.add_record(p[1], p[2], float(p[3]))
            elif p[0] == 'add_product':
                return self.add_product(p[1], {'P':float(p[2]), 'G':float(p[3]), 'E':float(p[4]), 'A':float(p[5])})
            elif p[0] == 'get_self.products':
                return str(self.products)
            elif p[0] == 'get_self.residents':
                return str(self.residents)
            elif p[0] == 'reset_self.products':
                self.products = pd.DataFrame(columns=['name', 'subcribers'])
                return "reset done"
            elif p[0] == 'reset_self.residents':
                self.residents = pd.DataFrame(
                    [{'name': 'P', 'dept': 0},
                    {'name': 'G', 'dept': 0},
                    {'name': 'E', 'dept': 0},
                    {'name': 'A', 'dept': 0}])
                return "reset done"
            else:
                return 'What? Want some candy?'
        except Exception as e:
            print(e)
            return 'Something terrible happend.'

KK = KK()
print(KK.handle_message('add_product elmex 50 0 50 0'))
print(KK.handle_message('add_record P elmex 800'))
print(KK.handle_message('get_self.products'))
print(KK.handle_message('get_self.residents'))

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