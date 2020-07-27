from .transaction import Transactions
import plotly.graph_objects as go

def waterfall_plot_transactions(transactions: Transactions):
	fig = go.Figure()
	fig.add_trace(
		go.Waterfall(
			x = [t.date for t in transactions],
			y = [t.ammount for t in transactions],
			text = [str(t.date) + '<br>Comment: ' + t.comment + '<br>Tags: ' + str(t.tags) for t in transactions],
			offset = 0, # See https://plot.ly/python/reference/#waterfall-offset
		)
	)
	return fig
