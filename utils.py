import xlrd
import datetime
import account as acnt
import transaction as trcn
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

HEADER_LINES = 3

def parse_account(book, account_col_number):
	accounts_sheet = book.sheet_by_index(0)
	account = acnt.account(account_name = accounts_sheet.col_values(account_col_number)[0], currency = accounts_sheet.col_values(account_col_number)[2])
	for idx, raw_transaction in enumerate(accounts_sheet.col_values(account_col_number)[HEADER_LINES:]):
		if raw_transaction == '':
			continue
		date_cell = accounts_sheet.col_values(0)[idx+HEADER_LINES]
		tags = accounts_sheet.col_values(2)[idx+HEADER_LINES].split(', ')
		if tags == ['']: tags = []
		account.transactions.append(
			trcn.transaction(
				ammount = raw_transaction,
				currency = account.currency,
				date = datetime.datetime(*xlrd.xldate_as_tuple(date_cell, book.datemode)) if date_cell != '' else None,
				comment = accounts_sheet.col_values(1)[idx+HEADER_LINES],
				tags = tags,
				)
			)
	account.transactions = trcn.sort_transactions_by_date(account.transactions)
	account.update_balance()
	return account

def read_accounts_sheet(file):
	book = xlrd.open_workbook(file)
	accounts_sheet = book.sheet_by_index(0) 
	account_names = accounts_sheet.row_values(0)[HEADER_LINES:]
	accounts = [None]*len(account_names)
	for k in range(len(account_names)):
		accounts[k] = parse_account(book, k+HEADER_LINES)
	return accounts

def plot_tags_monthly(account, From, To):
	total_months = lambda dt: dt.month + 12 * dt.year
	months_list = []
	for tot_m in range(total_months(From)-1, total_months(To)):
		y, m = divmod(tot_m, 12)
		months_list.append(datetime.datetime(y, m+1, 1))
	
	y_axis_data = {}
	for month_idx, month in enumerate(months_list):
		this_month_transactions = []
		for transaction in account.transactions:
			if transaction.date.year == month.year and transaction.date.month == month.month:
				this_month_transactions.append(transaction)
		this_month_data = trcn.ammounts_by_tags(this_month_transactions)
		for tag in this_month_data:
			if tag not in y_axis_data:
				y_axis_data[tag] = [0]*len(months_list)
			y_axis_data[tag][month_idx] = this_month_data[tag]
	
	data = []
	for tag in y_axis_data:
		data.append(
			go.Bar(
				name = tag,
				x = months_list,
				y = y_axis_data[tag],
			)
		)
	fig = go.Figure(data)
	fig.update_layout(barmode = 'stack')
	fig.update_layout(
		yaxis_title = account.currency,
		title = account.account_name
	)
	return fig

def plot_monthly_by_tags(account, criteria, tags, From, To):
	transactions = account.transactions
	transactions = trcn.filter_by_date(transactions, From, To)
	transactions = trcn.filter_by_tags(transactions, criteria, tags)
	
	total_months = lambda dt: dt.month + 12 * dt.year
	months_list = []
	for tot_m in range(total_months(From)-1, total_months(To)):
		y, m = divmod(tot_m, 12)
		months_list.append(datetime.datetime(y, m+1, 1))
	
	data = {
		'date':[], 
		'ammount': [],
		'comment': [],
	}
	for transaction in transactions:
		data['date'].append(transaction.date.replace(day = 1))
		data['ammount'].append(transaction.ammount)
		data['comment'].append(transaction.comment)
	
	fig = px.bar(
			pd.DataFrame.from_dict(data), 
			x = 'date', 
			y = 'ammount',
			text = 'comment'
		  )
	return fig

def waterfall_plot_transactions(transactions, fig):
	return fig.add_trace(
		go.Waterfall(
			x = [t.date for t in transactions],
			y = [t.ammount for t in transactions],
			text = ['Comment: ' + t.comment + '<br>Tags: ' + str(t.tags) for t in transactions],
			offset = 0, # See https://plot.ly/python/reference/#waterfall-offset
		)
	)

def waterfall_plot_account(account, From=None, To=None):
	transactions_to_plot = trcn.filter_by_date(account.transactions,From,To)
	transactions_to_plot = trcn.separate_dates(transactions_to_plot)
	if From != None:
		transactions_to_integrate = trcn.filter_by_date(account.transactions, To = From-datetime.timedelta(days=1))
		integrated_transaction = trcn.transaction(
			ammount = sum([t.ammount for t in transactions_to_integrate]), 
			date = From-datetime.timedelta(days=1), 
			currency = account.currency, 
			comment = 'SUM OF TRANSACTIONS PREVIOUS TO ' + str(From)
		)
		transactions_to_plot.insert(0,integrated_transaction)
	fig = go.Figure()
	waterfall_plot_transactions(transactions_to_plot, fig)
	fig.update_layout(
		title = account.account_name,
		yaxis_title = account.currency
	)
	return fig
