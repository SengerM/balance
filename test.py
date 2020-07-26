import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import utils

accounts = utils.read_accounts_sheet('/home/alf/Senger Efectos/La administracion/new_balance.xlsx')
dollar_cash = accounts[3]
abri_cu = accounts[4]
pesos_bna = accounts[0]
dollar_bna = accounts[1]
pesos_cash = accounts[2]

total_dollars = None
total_pesos = None
total_CHF = None
for account in accounts:
	if account.currency == 'U$D':
		total_dollars = account if total_dollars is None else total_dollars + account
	if account.currency == 'AR$':
		total_pesos = account if total_pesos is None else total_pesos + account
	if account.currency == 'CHF':
		total_CHF = account if total_CHF is None else total_CHF + account

From = datetime.datetime(year=2020,month=7,day=5)
To = datetime.datetime(year=2021,month=5,day=1)

utils.waterfall_plot_account(total_CHF).show()

# ~ utils.plot_tags_monthly(
	# ~ account = total_CHF,
	# ~ From = From,
	# ~ To = To,
# ~ ).show()
