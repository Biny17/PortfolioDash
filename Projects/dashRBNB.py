from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv('listings.csv.gz')

acco = df.groupby(["accommodates"])["accommodates"].count().reset_index(name="nb")
acco = acco.loc[(acco["accommodates"]<6) & (acco["accommodates"]>0)]

fig = px.bar(acco, x="accommodates", y="nb")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)