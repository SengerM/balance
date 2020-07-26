import datetime

class transaction:
	
	def __init__(self, ammount, date, currency, comment = '', tags = []):
		self.ammount = ammount
		self.date = date
		self.comment = comment
		self.tags = tags
		self.currency = currency
	
	def __str__(self):
		string = 'ammount: ' + str(self.ammount) + ', currency: ' + str(self.currency) + ', date = ' + str(self.date)
		if self.comment != '':
			string += ', comment: ' + self.comment
		if self.tags != []:
			string += ', tags: ' + str(self.tags)
		return string

def sort_transactions_by_date(transactions):
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
