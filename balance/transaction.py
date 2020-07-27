import datetime

class Transaction:
	def __init__(self, ammount, date, currency, comment = '', tags = []):
		self._ammount = ammount
		self._date = date
		self._comment = comment
		self._tags = tags
		self._currency = currency
	
	@property
	def ammount(self):
		return self._ammount
	
	@property
	def date(self):
		return self._date
	
	@property
	def comment(self):
		return self._comment
	
	@property
	def tags(self):
		return self._tags
	
	@property
	def currency(self):
		return self._currency
	
	def __str__(self):
		string = 'ammount: ' + str(self.ammount) + ', currency: ' + str(self.currency) + ', date = ' + str(self.date)
		if self.comment != '':
			string += ', comment: ' + self.comment
		if self.tags != []:
			string += ', tags: ' + str(self.tags)
		return string

class Transactions:
	def __init__(self, transactions: list = []):
		for transaction in transactions:
			if not isinstance(transaction, Transaction):
				raise TypeError('<transactions> must be a list of Transaction objects')
		self._transactions = transactions
		self.sort()
	
	def sort(self):
		self._transactions = sort_transactions_by_date(self._transactions)
		
	def get_by_date(self, From = None, To = None):
		return Transactions(filter_by_date(self._transactions, From = From, To = To))
	
	def From(self, From):
		return self.get_by_date(From = From)
		
	def To(self, To):
		return self.get_by_date(To = To)
	
	def tags(self, tags, criteria='have all'):
		if isinstance(tags, str):
			return Transactions(filter_by_tags(self._transactions, criteria, [tags]))
		else:
			return Transactions(filter_by_tags(self._transactions, criteria, tags))
	
	def list_tags(self):
		tags = []
		for transaction in self._transactions:
			for tag in transaction.tags:
				if tag not in tags:
					tags.append(tag)
		return tags
	
	def append(self, transaction: Transaction):
		if not isinstance(transaction, Transaction):
			raise TypeError('<transaction> must be an instance of Transaction')
		self._transactions.append(transaction)
	
	def __getitem__(self, key):
		return self._transactions[key]
	
	def __add__(self, other):
		return Transactions(self._transactions + other._transactions)
	
	def __iter__(self):
		for transaction in self._transactions:
			yield transaction
		
	def __len__(self):
		return len(self._transactions)

def sort_transactions_by_date(transactions: list):
	dates = [transaction.date for transaction in transactions]
	dates.sort()
	ordered_transactions = []
	for date in dates:
		for k,transaction in enumerate(transactions):
			if transaction.date == date:
				ordered_transactions.append(transaction)
				transactions.pop(k)
				continue
	return ordered_transactions

def separate_dates(transactions):
	for k,transaction in enumerate(transactions):
		if k == 0:
			prev_date = transaction.date
			prev_k = k
			continue
		if prev_date == transaction.date:
			transactions[k].date += datetime.timedelta(hours = k-prev_k+1)
			continue
		prev_date = transaction.date
		prev_k = k
	return transactions

def filter_by_tags(transactions, criteria, tags):
	valid_criteria = ['dont have any', 'have all', 'have at least one']
	if criteria not in valid_criteria:
		raise ValueError('The "criteria" argument must be one of ' + str(valid_criteria))
	filtered_transactions = []
	for transaction in transactions:
		if criteria == valid_criteria[0]: # Dont have any tag
			for idx, tag in enumerate(transaction.tags):
				if tag in tags:
					break
				if idx == len(transaction.tags) - 1:
					filtered_transactions.append(transaction)
		if criteria == valid_criteria[1]: # Have all tags
			for idx, tag in enumerate(tags):
				if tag not in transaction.tags:
					break
				if idx == len(tags) - 1:
					filtered_transactions.append(transaction)
		if criteria == valid_criteria[2]: # Have at least one tag
			for tag in transaction.tags:
				if tag in tags:
					filtered_transactions.append(transaction)
					break
	return filtered_transactions

def filter_by_date(transactions, From = None, To = None):
	filtered_transactions = []
	for transaction in transactions:
		if From != None and transaction.date < From:
			continue
		if To != None and transaction.date > To:
			continue
		filtered_transactions.append(transaction)
	return filtered_transactions

def ammounts_by_tags(transactions):
	ammounts = {}
	for transaction in transactions:
		for tag in transaction.tags:
			ammounts[tag] = transaction.ammount if ammounts.get(tag) is None else ammounts[tag] + transaction.ammount
	return ammounts
