import sys
import pandas as pd
import requests
import json

base = 'https://agile-stream-12274.herokuapp.com/'
bills_url = base + 'habitations/1/bills'
resident_url = base + 'habitations/1/residents'
payments_url = base + 'habitations/1/payments'
update_debts_url = base + 'habitations/1/update_depts'

class Messenger(object):

    def handle_messages(self, ms):
            if 'yes' in ms.lower() or 'candy' in ms.lower():
                return ('I see.. Well, then see into the green bowl under the black hat..\n'
            +'add_bill:\n'
            +'add_resident\n'
            +'add_payments\n'
            +'get_bills\n'
            +'get_residents\n'
            +'add_payments\n'
            +'update_debts')
            ms = ms.split('\n')
            if len(ms) == 1:
                return self.handle_message(ms[0])
            else:
                for m in ms:
                    self.handle_message(m)
                return 'all_done'

    def handle_message(self, m):
        try:
            m = m.split(' ')
            if m[0] == 'add_bill':
                return str(self.add_bill(0, m[1], m[2], m[3], float(m[4]), m[5]))
            elif m[0] == 'add_resident':
                return str(self.add_resident(0, m[1], m[2], m[3]))
            elif m[0] == 'add_payments':
                return str(self.add_payment(0, m[1], m[2], m[3], m[4]))
            elif m[0] == 'get_bills':
                return str(self.get_bills(0))
            elif m[0] == 'get_residents':
                return str(self.get_residents(0))
            elif m[0] == 'get_payments':
                return str(self.get_payments(0))
            elif m[0] == 'update_debts':
                return str(self.update_debts(0))
            else:
                return 'What? Want some candy?'
        except:
            e = sys.exc_info()
            print(e)
            return 'Something terrible happend.'

    def get_residents(self, resident_id):
        residents = requests.get(resident_url).json()
        return '\n'.join(map(lambda r: r['name'] + '\'s debt is ' + str(r['dept']), residents))

    def get_payments(self, resident_id):
        payments = requests.get(payments_url).json()
        return '\n'.join(map(lambda r: r['receiver'] + '\'s paid ' + str(r['payer']) + ' ' + str(r['amount']), payments))
    
    def get_bills(self, resident_id):
        bills = requests.get(bills_url).json()
        return '\n'.join(map(lambda r: r['type'] + ' ' + str(r['start']) + ' ' + str(r['end']) + ' ' + str(r['amount']), bills))

    def add_resident(self, resident_id, start, end, name):
        resident = json.dumps({
            "start": str(start),
            "end": str(end),
            "name": name
        })
        return requests.post(resident_url, headers=self.headers(), data=resident).text

    def add_payment(self, resident_id, amount, payer, receiver, date):
        payment = json.dumps({
            "amount": str(amount),
            "payer": payer,
            "receiver": receiver,
            "date": str(date)
        })
        return requests.post(payments_url, headers=self.headers(), data=payment).text

    def add_bill(self, resident_id, start, end, type, amount, paid_by):
        bill = json.dumps({
            "start": str(start),
            "end": str(end),
            "type": type,
            "amount": amount,
            "paid_by": paid_by
        })
        return requests.post(bills_url, headers=self.headers(), data=bill).text
        
    def update_debts(self, habitant_id):
        return requests.get(update_debts_url).text

    def headers(self):
        return {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
