import pandas as pd
from trello import TrelloClient
from reckoner import RentReckoner
from rent_provider_trello import DataProvider

DATA_PATH = ""
DATA_PROVIDER = DataProvider(DATA_PATH)
RENT_RECKONER = RentReckoner(DATA_PROVIDER)

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
            error = 'Failed: sum of percents should be 100, but was: %d' % sum(subcripers.values())
            print(error)
            return error
        elif product_name in set(products['name']):
            error = 'Failed: product already added: %s' % product_name
            print(error)
            return error
        else:
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
        record = '%s %s %d' % (buyer, product_name, int(float(value)))
        board.open_lists()[2].add_card(record)
        return '%s added' % record

    def add_product_to_trello(self, product_name, m):
        subscribers = dict(map(lambda s: s.split('='), m))
        subscribers = dict(map(lambda k: [k, int(subscribers[k])], subscribers.keys()))
        if sum(subscribers.values()) != 100:
            error = 'Failed: sum of percents should be 100, but was: ' + str(sum(subscribers.values()))
            print(error)
            return error
        board = self.client.get_board('f0EDhQy7')
        product = product_name + ' ' + ' '.join(list(map(lambda k: '%s=%s'%(k, subscribers[k]), subscribers)))
        board.open_lists()[1].add_card(product)
        return product + ' added'

    def split_them(self, l):
        return list(map(lambda r: str(r).replace('<', '').replace('>', '').split(' '), l))

    def add_resident(self, name, dept, residents):
        residents.loc[-1] = [name, dept]
        residents.index = residents.index + 1
        return residents

    def get_products(self):
        board = self.client.get_board('f0EDhQy7')
        raw_products = board.open_lists()[1].list_cards()
        products_splitted = self.split_them(raw_products)
        products = pd.DataFrame(columns=['name', 'subscribers'])
        for m in products_splitted:
            subscribers = dict(map(lambda s: s.split('='), m[2:]))
            subscribers = dict(map(lambda k: [k, float(subscribers[k])], subscribers.keys()))
            products = self.add_product(m[1], subscribers, products)
        return products

    def get_residents(self):
        board = self.client.get_board('f0EDhQy7')
        products = self.get_products(board)
        raw_residents = board.open_lists()[0].list_cards()
        residents_splitted = self.split_them(raw_residents)
        residents_clean = list(map(lambda r: [r[1], 0], residents_splitted))
        residents = pd.DataFrame(residents_clean, columns=['name', 'dept'])
        records = board.open_lists()[2].list_cards()
        records_list = self.split_them(records)
        for r in records_list:
            residents = self.add_record(r[1], r[2], float(r[3]), residents, products)
        cards = board.get_cards()
        for i in range(len(residents)):
            cards[i].set_name(residents['name'][i] + ' ' + str(residents['dept'][i]))
        return '\n'.join(residents.apply(lambda r: r['name'] + '\'s debt is ' + str(r['dept']), axis=1))

    def add_bill(self, start, end, type, amount):
        DATA_PROVIDER.add_bill(start, end, type, amount)
        return 'bill added: start:%s, end:%s, type: %s, amount: %s' % (start, end, type, amount)
        
    def update_depts(self, habitant_id):
        residents = RENT_RECKONER.update_debts(habitant_id)
        return '\n'.join(list(map(lambda r: r['name'] + '\'s debt is ' + str(r['dept']), residents)))

    def handle_message(self, m):
        m = m.split(' ')
        if m[0] == 'add_record':
            return self.add_record_to_trello(m[1], m[2], float(m[3]))
        elif m[0] == 'add_product':
            return self.add_product_to_trello(m[1], m[2:])
        elif m[0] == 'get_products':
            products = self.get_products()
            return ' '.join(products.apply(lambda r: r['name'], axis=1))
        elif m[0] == 'get_buyers':
            return str(self.get_residents())
        elif m[0] == 'add_bill':
            return str(self.add_bill(m[1], m[2], m[3], float(m[4])))
        elif m[0] == 'get_residents':
            return str(self.update_depts(0))

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
            +'get_buyers\n'
            +'add_product tej P=40 G=30 E=30\n'
            +'add_record E tej 299\n'
            +'get_residents\n'
            +'add_bill 2017-07-12 2017-08-14 elec 5588')
            ms = ms.split('\n')
            if len(ms) == 1:
                return self.handle_message(ms[0])
            else:
                for m in ms:
                    self.handle_message(m)
                return 'all_done'
