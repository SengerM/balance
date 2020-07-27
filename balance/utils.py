import xlrd
import datetime
from .account import Account
from .transaction import Transaction, Transactions

HEADER_LINES = 3

def parse_account(book, account_col_number):
	accounts_sheet = book.sheet_by_index(0)
	account = Account(account_name = accounts_sheet.col_values(account_col_number)[0], currency = accounts_sheet.col_values(account_col_number)[2])
	transactions = Transactions()
	prev_date = None
	for idx, raw_transaction in enumerate(accounts_sheet.col_values(account_col_number)[HEADER_LINES:]):
		if raw_transaction == '':
			continue
		date_cell = accounts_sheet.col_values(0)[idx+HEADER_LINES]
		tags = accounts_sheet.col_values(2)[idx+HEADER_LINES].split(', ')
		if tags == ['']: 
			tags = []
			
		date = datetime.datetime(*xlrd.xldate_as_tuple(date_cell, book.datemode)) if date_cell != '' else None
		if prev_date == date:
			k_dates_equal += 1
			date += datetime.timedelta(hours = k_dates_equal)
		else:
			prev_date = date
			k_dates_equal = 0
		transactions.append(
			Transaction(
				ammount = raw_transaction,
				currency = account.currency,
				date = date,
				comment = accounts_sheet.col_values(1)[idx+HEADER_LINES],
				tags = tags,
				)
			)
	account.add(transactions)
	return account

def read_accounts_sheet(file: str):
	book = xlrd.open_workbook(file)
	accounts_sheet = book.sheet_by_index(0) 
	account_names = accounts_sheet.row_values(0)[HEADER_LINES:]
	accounts = [None]*len(account_names)
	for k in range(len(account_names)):
		accounts[k] = parse_account(book, k+HEADER_LINES)
	return accounts



