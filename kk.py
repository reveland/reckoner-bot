import pandas as pd

def get_subcribers(name):
    if name not in set(products['name']):
        print('Failed: not existing product: ' + name)
        return list() # TODO not been tested!
    else:
        return list(products.loc[products['name'] == name,'subcribers'])[0]
def get_dept(name):
    return residents.loc[residents['name'] == name,'dept']
def add_to_dept(name, value):
    residents.loc[residents['name'] == name,'dept'] = get_dept(name) + value
def def_facto_add_product(product_name, subcripers):
    global products
    products =  products.append({'name': product_name, 'subcribers': subcripers}, ignore_index=True)
    
def add_product(product_name, subcripers):
    """ product_name is the new product name
        subcripers is a dictionaries of elements like {'resident_name':usage_percent} """
    if sum(subcripers.values()) != 100:
        print('Failed: sum of percents should be 100, but was: ' + str(sum(subcripers.values())))
        return 'Failed: sum of percents should be 100, but was: ' + str(sum(subcripers.values()))
    elif product_name in set(products['name']):
        print('Failed: product already added ' + product_name)
        return 'Failed: product already added ' + product_name
    else:
        print('Product added: ' + product_name + ', subscriber: ' + str(subcripers))
        # normailze percentages ({'E': 50, 'P': 50} -> {'E': 0.5, 'P': 0.5})
        subcripers = {k: v/100 for k, v in subcripers.items()}
        def_facto_add_product(product_name, subcripers)
        return 'Product added: ' + product_name + ', subscriber: ' + str(subcripers)

def add_record(buyer, product_name, value):
    subcribers = get_subcribers(product_name)
    print()
    print(buyer + ' paid for ' + product_name + ' in value of ' + str(value))
    print(product_name + ' will be consumed by:')
    for name, percent in subcribers.items():
        print(name + ' in value of ' + str(value * percent))
        add_to_dept(name, value * percent)
    add_to_dept(buyer, -value)
    return buyer + ' paid for ' + product_name + ' in value of ' + str(value)

def handle_message(p):
    p = p.split(' ')
    try:
        if p[0] == 'add_record':
            return add_record(p[1], p[2], float(p[3]))
        elif p[0] == 'add_product':
            return add_product(p[1], {'P':float(p[2]), 'G':float(p[3]), 'E':float(p[4]), 'A':float(p[5])})
        elif p[0] == 'get_products':
            return str(products)
        elif p[0] == 'get_residents':
            return str(residents)
        else:
            return 'What? Want some candy?'
    except Exception as e:
        print(e)
        return 'Something terrible happend.'

residents = pd.DataFrame(
    [{'name': 'P', 'dept': 0},
     {'name': 'G', 'dept': 0},
     {'name': 'E', 'dept': 0},
     {'name': 'A', 'dept': 0}])
products = pd.DataFrame(columns=['name', 'subcribers'])

"""
handle_message('add_product elmex 50 0 50 0')
handle_message('add_record P elmex 800')
handle_message('add_product tej 40 30 30 0')
print(handle_message('get_products'))
print(handle_message('get_residents'))
"""


print(handle_message('add_product elmex 50 0 50 0'))
print(handle_message('add_record P elmex 800'))
print(handle_message('get_products'))
print(handle_message('get_residents'))

"""
residents = pd.DataFrame(
    [{'name': 'P', 'dept': 0},
     {'name': 'G', 'dept': 0},
     {'name': 'E', 'dept': 0},
     {'name': 'A', 'dept': 0}])
products = pd.DataFrame(columns=['name', 'subcribers'])

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