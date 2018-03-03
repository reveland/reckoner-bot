import calendar
from dateutil.parser import parse
from trello import TrelloClient

class DataProvider(object):

    def __init__(self, path):
        client = TrelloClient(
            api_key='4c48eb6acff05f1a7105b93ed58e912b',
            api_secret='7196c21a9f0a7a8656bf802b9af2e1cbae447fc30d5ccd64868836cf4d14e74f',
            token='6bbb65aab16eada17f8137017b695dd0b61f463b5b77ce98ff7f25c8ecabd71f',
            token_secret='7196c21a9f0a7a8656bf802b9af2e1cbae447fc30d5ccd64868836cf4d14e74f'
        )
        self.board = client.get_board('f0EDhQy7')

    def get_bills(self, habitant_id):
        bills_cards = self.board.open_lists()[4].list_cards()
        bills_splitted = self.__split_them(bills_cards)
        bills = self.__dict_them(bills_splitted, ['start', 'end', 'type', 'amount'])
        for item in bills:
            item["amount"] = float(item["amount"])
        return bills

    def get_residents(self, habitant_id):
        residents_cards = self.board.open_lists()[3].list_cards()
        residents_splitted = self.__split_them(residents_cards)
        residents = self.__dict_them(residents_splitted, ['start', 'end', 'name', 'dept', 'paid'])
        for item in residents:
            item["dept"] = float(item["dept"])
            item["paid"] = float(item["paid"])
        return residents

    def save_residents(self, habitant_id, residents):
        cards = self.board.open_lists()[3].list_cards()
        for i in range(len(residents)):
            row = residents[i]
            cards[i].set_name(' '.join([row['start'][:10], row['end'][:10], row['name'], str(row['dept']), str(int(float(row['paid'])))]))
    
    def save_bills(self, habitant_id, bills):
        for i in range(len(bills)):
            row = bills[i]
            self.board.open_lists()[4].add_card(' '.join([row['start'][:10], row['end'][:10], row['type'], str(row['amount']), row['paid_by']]))

    def add_bill(self, start, end, type, amount):
        self.board.open_lists()[4].add_card(start[:10] + ' ' + end[:10] + ' ' + type + ' ' + str(amount))

    def __transform_date_to_int(self, items):
        for item in items:
            item["end"] = calendar.timegm(parse(item["end"]).timetuple())
            item["start"] = calendar.timegm(parse(item["start"]).timetuple())
        return items

    def __increment_end_date_with_one_day(self, items):
        for item in items:
            item["end"] = item["end"] + 86400
        return items

    def __dict_them(self, l, keys):
        return list(map(lambda r: dict(zip(keys, r)), l))

    def __split_them(self, l):
        return list(map(lambda r: str(r).replace('<', '').replace('>', '').split(' ')[1:], l))

DP = DataProvider('nope')
# print(DP.get_residents(0))
# print(DP.get_bills(0))

bills = [
{
    'end': '2016-09-17',
    'type': 'Heat/gas',
    'start': '2016-07-19',
    'amount': 580.0,
    'paid_by': ''
},
{
    'end': '2016-09-12',
    'type': 'Electronics',
    'start': '2016-08-12',
    'amount': 5859.0,
    'paid_by': ''
},
{
    'end': '2016-09-30',
    'type': 'Rent',
    'start': '2016-09-01',
    'amount': 80000.0,
    'paid_by': ''
},
{
    'end': '2016-09-30',
    'type': 'Services',
    'start': '2016-09-01',
    'amount': 13270.0,
    'paid_by': ''
},
{
    'end': '2016-11-10',
    'type': 'Water',
    'start': '2016-09-11',
    'amount': 6940.0,
    'paid_by': ''
},
{
    'end': '2016-10-11',
    'type': 'Electronics',
    'start': '2016-09-13',
    'amount': 11251.0,
    'paid_by': ''
},
{
    'end': '2016-10-15',
    'type': 'Heat/gas',
    'start': '2016-09-18',
    'amount': 3175.0,
    'paid_by': ''
},
{
    'end': '2016-10-31',
    'type': 'Rent',
    'start': '2016-10-01',
    'amount': 80000.0,
    'paid_by': ''
},
{
    'end': '2016-10-31',
    'type': 'Services',
    'start': '2016-10-01',
    'amount': 13270.0,
    'paid_by': ''
},
{
    'end': '2016-10-31',
    'type': 'TV/Phone/Internet',
    'start': '2016-10-04',
    'amount': 4065.0,
    'paid_by': ''
},
{
    'end': '2016-11-11',
    'type': 'Electronics',
    'start': '2016-10-12',
    'amount': 9056.0,
    'paid_by': ''
},
{
    'end': '2016-11-16',
    'type': 'Heat/gas',
    'start': '2016-10-16',
    'amount': 4000.0,
    'paid_by': ''
},
{
    'end': '2016-11-30',
    'type': 'Rent',
    'start': '2016-11-01',
    'amount': 80000.0,
    'paid_by': ''
},
{
    'end': '2016-11-30',
    'type': 'Services',
    'start': '2016-11-01',
    'amount': 13270.0,
    'paid_by': ''
},
{
    'end': '2016-11-30',
    'type': 'TV/Phone/Internet',
    'start': '2016-11-01',
    'amount': 4500.0,
    'paid_by': ''
},
{
    'end': '2017-01-10',
    'type': 'Water',
    'start': '2016-11-11',
    'amount': 4539.0,
    'paid_by': ''
},
{
    'end': '2016-12-08',
    'type': 'Electronics',
    'start': '2016-11-12',
    'amount': 6861.0,
    'paid_by': ''
},
{
    'end': '2016-12-17',
    'type': 'Heat/gas',
    'start': '2016-11-17',
    'amount': 4570.0,
    'paid_by': ''
},
{
    'end': '2016-12-31',
    'type': 'Rent',
    'start': '2016-12-01',
    'amount': 80000.0,
    'paid_by': ''
},
{
    'end': '2016-12-31',
    'type': 'Services',
    'start': '2016-12-01',
    'amount': 13270.0,
    'paid_by': ''
},
{
    'end': '2016-12-31',
    'type': 'TV/Phone/Internet',
    'start': '2016-12-01',
    'amount': 4500.0,
    'paid_by': ''
},
{
    'end': '2017-01-10',
    'type': 'Electronics',
    'start': '2016-12-09',
    'amount': 8710.0,
    'paid_by': ''
},
{
    'end': '2017-01-16',
    'type': 'Heat/gas',
    'start': '2016-12-18',
    'amount': 14163.0,
    'paid_by': ''
},
{
    'end': '2017-01-31',
    'type': 'Rent',
    'start': '2017-01-01',
    'amount': 80000.0,
    'paid_by': ''
},
{
    'end': '2017-01-31',
    'type': 'Services',
    'start': '2017-01-01',
    'amount': 13270.0,
    'paid_by': ''
},
{
    'end': '2017-01-31',
    'type': 'TV/Phone/Internet',
    'start': '2017-01-01',
    'amount': 4100.0,
    'paid_by': ''
},
{
    'end': '2017-02-09',
    'type': 'Electronics',
    'start': '2017-01-11',
    'amount': 7744.0,
    'paid_by': ''
},
{
    'end': '2017-03-10',
    'type': 'Water',
    'start': '2017-01-11',
    'amount': 5141.0,
    'paid_by': ''
},
{
    'end': '2017-02-15',
    'type': 'Heat/gas',
    'start': '2017-01-17',
    'amount': 8451.0,
    'paid_by': ''
},
{
    'end': '2017-02-28',
    'type': 'Rent',
    'start': '2017-02-01',
    'amount': 80000.0,
    'paid_by': ''
},
{
    'end': '2017-02-28',
    'type': 'Services',
    'start': '2017-02-01',
    'amount': 13270.0,
    'paid_by': ''
},
{
    'end': '2017-02-28',
    'type': 'TV/Phone/Internet',
    'start': '2017-02-01',
    'amount': 4100.0,
    'paid_by': ''
},
{
    'end': '2017-03-11',
    'type': 'Electronics',
    'start': '2017-02-10',
    'amount': 7821.0,
    'paid_by': ''
},
{
    'end': '2017-03-17',
    'type': 'Heat/gas',
    'start': '2017-02-16',
    'amount': 5944.0,
    'paid_by': ''
},
{
    'end': '2017-03-31',
    'type': 'Rent',
    'start': '2017-03-01',
    'amount': 80000.0,
    'paid_by': ''
},
{
    'end': '2017-03-31',
    'type': 'Services',
    'start': '2017-03-01',
    'amount': 13270.0,
    'paid_by': ''
},
{
    'end': '2017-03-31',
    'type': 'TV/Phone/Internet',
    'start': '2017-03-01',
    'amount': 4100.0,
    'paid_by': ''
},
{
    'end': '2017-04-15',
    'type': 'Electronics',
    'start': '2017-03-12',
    'amount': 8998.0,
    'paid_by': ''
},
{
    'end': '2017-04-15',
    'type': 'Heat/gas',
    'start': '2017-03-18',
    'amount': 3056.0,
    'paid_by': ''
},
{
    'end': '2017-04-30',
    'type': 'TV/Phone/Internet',
    'start': '2017-04-01',
    'amount': 4100.0,
    'paid_by': ''
},
{
    'end': '2017-04-30',
    'type': 'Rent',
    'start': '2017-04-01',
    'amount': 80000.0,
    'paid_by': ''
},
{
    'end': '2017-04-30',
    'type': 'Services',
    'start': '2017-04-01',
    'amount': 13270.0,
    'paid_by': ''
},
{
    'end': '2017-05-31',
    'type': 'TV/Phone/Internet',
    'start': '2017-05-01',
    'amount': 4100.0,
    'paid_by': ''
},
{
    'end': '2017-05-31',
    'type': 'Rent',
    'start': '2017-05-01',
    'amount': 80000.0,
    'paid_by': ''
},
{
    'end': '2017-05-31',
    'type': 'Services',
    'start': '2017-05-01',
    'amount': 13270.0,
    'paid_by': ''
},
{
    'end': '2017-06-30',
    'type': 'Rent',
    'start': '2017-06-01',
    'amount': 80000.0,
    'paid_by': ''
},
{
    'end': '2017-06-30',
    'type': 'Services',
    'start': '2017-06-01',
    'amount': 13270.0,
    'paid_by': ''
},
{
    'end': '2017-05-10',
    'type': 'Electronics',
    'start': '2017-04-16',
    'amount': 5141.0,
    'paid_by': ''
},
{
    'end': '2017-06-30',
    'type': 'TV/Phone/Internet',
    'start': '2017-06-01',
    'amount': 4100.0,
    'paid_by': ''
},
{
    'end': '2017-06-15',
    'type': 'Electronics',
    'start': '2017-05-11',
    'amount': 8283.0,
    'paid_by': ''
},
{
    'end': '2017-05-10',
    'type': 'Water',
    'start': '2017-03-11',
    'amount': 4538.0,
    'paid_by': ''
},
{
    'end': '2017-07-31',
    'type': 'TV/Phone/Internet',
    'start': '2017-07-01',
    'amount': 4100.0,
    'paid_by': ''
},
{
    'end': '2017-07-31',
    'type': 'Rent',
    'start': '2017-07-01',
    'amount': 80000.0,
    'paid_by': ''
},
{
    'end': '2017-07-31',
    'type': 'Services',
    'start': '2017-07-01',
    'amount': 13270.0,
    'paid_by': ''
},
{
    'end': '2017-09-01',
    'type': 'Other',
    'start': '2017-07-01',
    'amount': 7115.0,
    'paid_by': ''
},
{
    'end': '2017-07-11',
    'type': 'Electronics',
    'start': '2017-06-16',
    'amount': 3029.0,
    'paid_by': ''
},
{
    'end': '2017-08-31',
    'type': 'TV/Phone/Internet',
    'start': '2017-08-01',
    'amount': 4100.0,
    'paid_by': ''
},
{
    'end': '2017-08-14',
    'type': 'Electronics',
    'start': '2017-07-12',
    'amount': 5588.0,
    'paid_by': ''
},
{
    'end': '2017-09-30',
    'type': 'TV/Phone/Internet',
    'start': '2017-09-01',
    'amount': 4100.0,
    'paid_by': ''
},
{
    'end': '2017-07-12',
    'type': 'Water',
    'start': '2017-05-10',
    'amount': 4538.0,
    'paid_by': ''
},
{
    'end': '2017-08-31',
    'type': 'Rent',
    'start': '2017-08-01',
    'amount': 80000.0,
    'paid_by': ''
},
{
    'end': '2017-10-31',
    'type': 'TV/Phone/Internet',
    'start': '2017-10-01',
    'amount': 4100.0,
    'paid_by': ''
},
{
    'end': '2017-09-14',
    'type': 'Electronics',
    'start': '2017-08-15',
    'amount': 4963.0,
    'paid_by': ''
},
{
    'end': '2017-08-31',
    'type': 'Services',
    'start': '2017-08-01',
    'amount': 13270.0,
    'paid_by': ''
},
{
    'end': '2017-09-30',
    'type': 'Rent',
    'start': '2017-09-01',
    'amount': 80000.0,
    'paid_by': ''
},
{
    'end': '2017-09-30',
    'type': 'Services',
    'start': '2017-09-01',
    'amount': 13270.0,
    'paid_by': ''
},
{
    'end': '2017-10-31',
    'type': 'Rent',
    'start': '2017-10-01',
    'amount': 80000.0,
    'paid_by': ''
},
{
    'end': '2017-10-31',
    'type': 'Services',
    'start': '2017-10-01',
    'amount': 13270.0,
    'paid_by': ''
},
{
    'end': '2017-09-17',
    'type': 'Water',
    'start': '2017-07-12',
    'amount': 3939.0,
    'paid_by': ''
},
{
    'end': '2017-10-13',
    'type': 'Other',
    'start': '2017-10-01',
    'amount': 1500.0,
    'paid_by': ''
},
{
    'end': '2017-11-30',
    'type': 'Rent',
    'start': '2017-11-01',
    'amount': 80000.0,
    'paid_by': ''
},
{
    'end': '2017-11-30',
    'type': 'TV/Phone/Internet',
    'start': '2017-11-01',
    'amount': 4100.0,
    'paid_by': ''
},
{
    'end': '2017-11-15',
    'type': 'Heat/gas',
    'start': '2017-09-15',
    'amount': 7728.0,
    'paid_by': ''
},
{
    'end': '2017-10-13',
    'type': 'Electronics',
    'start': '2017-09-15',
    'amount': 8352.0,
    'paid_by': ''
},
{
    'end': '2017-11-30',
    'type': 'Services',
    'start': '2017-11-01',
    'amount': 13270.0,
    'paid_by': ''
}]


DP.save_bills(0, bills)
