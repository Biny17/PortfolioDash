from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

app = Dash(__name__)
app.title = "Paris Airbnb - Tristan Gallet"

df = pd.read_csv(r'C:\Users\trist\Desktop\Coding\Portfolio\Projects\listings.csv.gz')

colors = {
    "cell": "#FFFFFF",
    "background": "#f5f2f5",
    "text": "#000000"
}

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

acco = df.groupby(["accommodates"])["accommodates"].count().reset_index(name="listings")
acco = acco.loc[(acco["accommodates"]<6) & (acco["accommodates"]>0)]

fig = px.bar(acco, x="accommodates", y="listings")
fig.update_traces(marker_color='#F67280', marker_line_color='#661720',
                  marker_line_width=1.5, opacity=0.8)
'''fig.update_layout(
    plot_bgcolor=colors['cell'],
    paper_bgcolor=colors['cell'],
    font_color=colors['text']
)'''

beds_table = html.Div([
    html.Div(children=[
        html.H3(
            children="Nombre de logement possédant X chambres", 
            style={'textAlign': 'center', 'color': colors['text']}),
        dcc.Graph(
        id='acco',
        figure=fig
    )
    ], style={'padding': 10, 'flex': 2}),

    html.Div(children=[
        generate_table(acco)
    ], style={'padding': 10, 'flex': 1})
], style={'display': 'flex', 'flex-direction': 'row', 'backgroundColor': colors['background']})

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    beds_table
])

if __name__ == '__main__':
    app.run_server(debug=True)
