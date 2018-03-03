# What it can do:

- reckoner
  - http:
    - update debts
      - /habitations/<int:habitant_id>/update_depts
      - trello data provider
      - habitant_id is not used
    - get bills
      - /habitations/<int:habitant_id>/bills
      - trello data provider
      - habitant_id is not used
    - get residents
      - /habitations/<int:habitant_id>/residents
      - trello data provider
      - habitant_id is not used
  - facebook
    - add bill
      - add bill to trello board
      - trello data provider use that data
    - get_residents
      - add resident to trello board
      - trello data provider use that data
- kozos kassza
  - facebook
    - add record
      - to trello board
    - add product
      - to trello board
    - get products
      - from trello board
    - get buyers
      - from trello board

# Main classes

- trello_kk
  - handle messages from facebook
  - add/get data from directly from trello board
- rent_provider_trello
  - data provider class that integrate trello
- reckoner
  - use data provider that can be switched easily
  - calculate debts
  - prepare data for the ui