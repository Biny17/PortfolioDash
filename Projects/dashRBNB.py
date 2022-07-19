from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = Dash(__name__)

df = pd.read_csv(r'C:\Users\trist\Desktop\Coding\Portfolio\Portfolio\Projects\listings.csv.gz')

colors = {
    'background':'#FFFFFF',
    'text':'#111111'
}

acco = df.groupby(["accommodates"])["accommodates"].count().reset_index(name="number of listings")
acco = acco.loc[(acco["accommodates"]<6) & (acco["accommodates"]>0)]

fig = px.bar(acco, x="accommodates", y="number of listings")
fig.update_traces(marker_color='#C6DCE4', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='AirBNB analysis - Tristan Gallet',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for your data.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure=fig
    ),
    generate_table(acco)
])
if __name__ == '__main__':
    app.run_server(debug=True)