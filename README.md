# Wallet transaction system

## Installation and running

- Requires `Python 3.8` or above installed
- Install dependencies `pip install -r requirements.txt`
- Create database `python manage.py migrate`
- Create test user `python manage.py createsuperuser`
- Run server `python manage.py runserver`

## Structure

### API structure

- `/<user_id>/wallet/` root node to access all functionalities for the wallet associated with user of id _user_id_
	- `create/` __(POST)__ creates new wallet
	- `balance/` __(GET)__ gets current balance
	- `debit/` __(POST)__ debits _amount_
	- `credit/` __(POST)__ credits _amount_

### Response structure

Responses are returned in JSON format. Each response has a _success_ field which indicates whether the given action was successfully performed or not. In case of failure, there is an _error_ field which indicates the type of error which occurred.

### Sample curl requests
- `curl --request POST --url http://localhost:8000/1/wallet/create/` create a new wallet for user 1
- `curl --request GET --url http://localhost:8000/1/wallet/balance/` get balance for wallet of user 1. returns _{"success": true, "balance": 100}_
- `curl --request POST --url http://localhost:8000/1/wallet/debit/ -H "Content-Type: application/json" -d '{"amount": 20}'` debit 20 amount from wallet of user 1
- `curl --request POST --url http://localhost:8000/1/wallet/credit/ -H "Content-Type: application/json" -d '{"amount": 20}'` credit 20 amount to wallet of user 1

__Note:__ all transactions create a log entry in the log file for the respective wallet. log files can be found in _logs/_ directory with format _wallet\<wallet_id\>.log_

__Note:__ debit transactions fail if balance is less than minimum balance (currently set to 100. can be adjusted in _server/config.py_)

__Note:__ this API does not handle user creation and authentication

__Note:__ only 1 create or credit or debit transaction is performed at a time for a user
