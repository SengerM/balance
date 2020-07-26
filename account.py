import transaction as trcn


class account:
	
	def __init__(self, account_name, currency):
		self.account_name = account_name
		self.transactions = []
		self.balance = []
		self.currency = currency
	
	def __add__(self, other):
		if self.currency != other.currency:
			raise TypeError('Cannot add two accounts with different currencies')
		added_accounts = account(account_name = self.account_name + '+' + other.account_name, currency = self.currency)
		for transaction in self.transactions:
			added_accounts.transactions.append(transaction)
		for transaction in other.transactions:
			added_accounts.transactions.append(transaction)
		added_accounts.transactions = trcn.sort_transactions_by_date(added_accounts.transactions)
		added_accounts.update_balance()
		return added_accounts
	
	def __str__(self):
		string = 'Account name: ' + self.account_name + '\n'
		string += 'Currency: ' + self.currency + '\n'
		string += 'Transactions:\n'
		for transaction in self.transactions:
			string += str(transaction) + '\n'
		string = string[:-1]
		return string
	
	def update_balance(self):
		for idx, transaction in enumerate(self.transactions):
			self.balance.append(self.balance[idx-1] + transaction.ammount if idx>0 else transaction.ammount)
	
	def ammounts_by_tags(self, From = None, To = None):
		return trcn.ammounts_by_tags(trcn.filter_by_date(self.transactions, From, To))
