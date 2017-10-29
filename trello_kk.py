import pandas as pd
from trello import TrelloClient

class KoKa(object):

    def __init__(self):
        self.client = TrelloClient(
            api_key='4c48eb6acff05f1a7105b93ed58e912b',
            api_secret='7196c21a9f0a7a8656bf802b9af2e1cbae447fc30d5ccd64868836cf4d14e74f',
            token='6bbb65aab16eada17f8137017b695dd0b61f463b5b77ce98ff7f25c8ecabd71f',
            token_secret='7196c21a9f0a7a8656bf802b9af2e1cbae447fc30d5ccd64868836cf4d14e74f'
        )

    def get_subcribers(self, name, products):
        if name not in set(products['name']):
            print('Failed: not existing product: ' + name)
            return list()
        else:
            return list(products.loc[products['name'] == name,'subscribers'])[0]

    def get_dept(self, name, residents):
        return residents.loc[residents['name'] == name,'dept']

    def add_to_dept(self, name, value, residents):
        residents.loc[residents['name'] == name,'dept'] = self.get_dept(name, residents) + value
        return residents

    def def_facto_add_product(self, product_name, subcripers, products):
        return products.append({'name': product_name, 'subscribers': subcripers}, ignore_index=True)
    
    def add_product(self, product_name, subcripers, products):
        if sum(subcripers.values()) != 100:
            print('Failed: sum of percents should be 100, but was: ' + str(sum(subcripers.values())))
            return 'Failed: sum of percents should be 100, but was: ' + str(sum(subcripers.values()))
        elif product_name in set(products['name']):
            print('Failed: product already added ' + product_name)
            return 'Failed: product already added ' + product_name
        else:
            print('Product added: ' + product_name + ', subscribers: ' + str(subcripers))
            subcripers = {k: v/100 for k, v in subcripers.items()}
            return self.def_facto_add_product(product_name, subcripers, products)

    def add_record(self, buyer, product_name, value, residents, products):
        subcribers = self.get_subcribers(product_name, products)
        print(buyer + ' paid for ' + product_name + ' in value of ' + str(value))
        print(product_name + ' will be consumed by:')
        for name, percent in subcribers.items():
            print(name + ' in value of ' + str(value * percent))
            residents = self.add_to_dept(name, value * percent, residents)
        residents = self.add_to_dept(buyer, -value, residents)
        return residents

    def add_record_to_trello(self, buyer, product_name, value):
        board = self.client.get_board('f0EDhQy7')
        board.open_lists()[2].add_card(buyer + ' ' + product_name + ' ' + str(value))
        return buyer + ' paid for ' + product_name + ' in value of ' + str(value)

    def add_product_to_trello(self, product_name, p=0, g=0, e=0, a=0):
        board = self.client.get_board('f0EDhQy7')
        board.open_lists()[1].add_card(product_name + ' ' + str(p) + ' ' + str(g) + ' ' + str(e) + ' ' + str(a))
        return product_name + ': P:' + str(p) + '%, G:' + str(g) + '%, E:' + str(e) + '%, A:' + str(a) + '% added'

    def split_them(self, l):
        return list(map(lambda r: str(r).replace('<', '').replace('>', '').split(' '), l))

    def add_resident(self, name, dept, residents):
        residents.loc[-1] = [name, dept]
        residents.index = residents.index + 1
        return residents

    def get_products(self, board):
        products_list = board.open_lists()[1].list_cards()
        products_list = self.split_them(products_list)
        products = pd.DataFrame(columns=['name', 'subscribers'])
        for m in products_list:
            products = self.add_product(m[1], {'P':float(m[2]), 'G':float(m[3]), 'E':float(m[4]), 'A':float(m[5])}, products)
        return products

    def get_residents(self):
        board = self.client.get_board('f0EDhQy7')
        products = self.get_products(board)
        residents = pd.DataFrame(
            [{'name': 'P', 'dept': 0},
            {'name': 'G', 'dept': 0},
            {'name': 'E', 'dept': 0},
            {'name': 'A', 'dept': 0}])
        records = board.open_lists()[2].list_cards()
        records_list = self.split_them(records)
        for r in records_list:
            residents = self.add_record(r[1], r[2], float(r[3]), residents, products)
        cards = board.get_cards()
        for i in range(len(residents)):
            cards[i].set_name(residents['name'][i] + ' ' + str(residents['dept'][i]))
        return residents
        
    def handle_message(self, m):
        m = m.split(' ')
        if m[0] == 'add_record':
            return self.add_record_to_trello(m[1], m[2], float(m[3]))
        elif m[0] == 'add_product':
            return self.add_product_to_trello(m[1], m[2], m[3], m[4], m[5])
        elif m[0] == 'get_products':
            board = self.client.get_board('f0EDhQy7')
            return str(self.get_products(board))
        elif m[0] == 'get_residents':
            return str(self.get_residents())
        elif m[0] == 'get_products_json':
            board = self.client.get_board('f0EDhQy7')
            return str(self.get_products(board).to_json())
        elif m[0] == 'get_residents_json':
            return str(self.get_residents().to_json())
        else:
            return 'What? Want some candy?'

    def handle_messages(self, ms):
            if 'yes' in ms.lower() or 'candy' in ms.lower():
                return ('I see.. Well, then see into the green bowl under the black hat..\n'
            +'Usage:\n'
            +'get_products\n'
            +'get_residents\n'
            +'add_product name p% g% e% a%\n'
            +'add_record buyer_name product_name value')
            ms = ms.split('\n')
            if len(ms) == 1:
                return self.handle_message(ms[0])
            else:
                for m in ms:
                    self.handle_message(m)
                return 'all_done'


KK = KoKa()
print(KK.handle_messages('get_residents'))