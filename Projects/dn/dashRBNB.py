from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

app = Dash(__name__)
logo = "logo.jpg"
df = pd.read_csv(r'C:\Users\trist\Desktop\Coding\Portfolio\Projects\listings.csv.gz')

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns], style = {"border": "1px solid black"})
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col], style = {"border": "1px solid black"}) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ], style = {"border": "1px solid black"})

def visu1():
    acco = df.groupby(["accommodates"])["accommodates"].count().reset_index(name="listings")
    acco = acco.loc[(acco["accommodates"]<6) & (acco["accommodates"]>0)]

    fig = px.bar(acco, x="accommodates", y="listings")
    fig.update_traces(marker_color='#C6DCE4', marker_line_color='rgb(8,48,107)',
                    marker_line_width=1.5, opacity=0.8)
    
    visu = html.Div(children=[
        html.Label("Nombre de logement acceuillant X personnes"),
        dcc.Graph(
            id='acco',
            figure=fig
        )])
    return visu

app.layout = html.Div(
    id="app-container", 
    children=[
        visu1()
        ]
)

if __name__ == '__main__':
    app.run_server(debug=True)