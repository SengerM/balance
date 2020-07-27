from .transaction import Transaction, Transactions

class Account:
	def __init__(self, account_name, currency, transactions = Transactions()):
		self._account_name = account_name
		self._balance = []
		self._currency = currency
		self._transactions = Transactions()
		self.add(transactions)
		self._update_balance()
	
	@property
	def account_name(self):
		return self._account_name
	
	@property
	def currency(self):
		return self._currency
	
	@property
	def transactions(self):
		return self._transactions
	
	def add(self, transaction_or_transactions):
		if isinstance(transaction_or_transactions, Transaction):
			if transaction_or_transactions.currency != self.currency:
				raise ValueError('<transaction_or_transactions> currency is ' + str(transaction_or_transactions.currency) + ' but this account currency is ' + str(self.currency))
			self._transactions.append(transaction_or_transactions)
		elif isinstance(transaction_or_transactions, Transactions):
			for transaction in transaction_or_transactions:
				self.add(transaction)
		self._update_balance()
	
	def __add__(self, other):
		if self.currency != other.currency:
			raise TypeError('Cannot add two accounts with different currencies')
		return Account(
			account_name = self.account_name + '+' + other.account_name, 
			currency = self.currency,
			transactions = self._transactions + other._transactions
		)
	
	def __str__(self):
		string = 'Account name: ' + self.account_name + '\n'
		string += 'Currency: ' + self.currency + '\n'
		string += 'This account has ' + str(len(self._transactions)) + ' transactions\n'
		string += 'Opening balance: ' + str(self._balance[0]) + ', closing balance: ' + str(self._balance[-1])
		return string
	
	def _update_balance(self):
		self._transactions.sort()
		self._balance = []
		for idx, transaction in enumerate(self._transactions):
			self._balance.append(self._balance[idx-1] + transaction.ammount if idx>0 else transaction.ammount)
	
	# ~ def plot_waterfall(self, From = None, To = None):
		# ~ transactions_to_plot = self._transactions.get_by_date(From,To)
		# ~ if From != None:
			# ~ transactions_to_integrate = self.transactions.filter_by_date(To = From-datetime.timedelta(days=1))
			# ~ integrated_transaction = Transaction(
				# ~ ammount = sum([t.ammount for t in transactions_to_integrate]), 
				# ~ date = From-datetime.timedelta(days=1), 
				# ~ currency = account.currency, 
				# ~ comment = 'SUM OF TRANSACTIONS PREVIOUS TO ' + str(From)
			# ~ )
			# ~ transactions_to_plot.insert(0,integrated_transaction)
		# ~ fig = go.Figure()
		# ~ waterfall_plot_transactions(transactions_to_plot, fig)
		# ~ fig.update_layout(
			# ~ title = self.account_name,
			# ~ yaxis_title = self.currency
		# ~ )
		# ~ return fig
		
