import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, Dash
from pathlib import Path
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import pickle
import json
from area import area
import plotly.express as px

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = 'Tristan Gallet'
server = app.server

HERE = Path(__file__).parent
LOGO = "logo.png"

with open(HERE/"data.pickle", 'rb') as f:
    pxmc,densite,prix,score,value,pPC,Logements,repartition = pickle.load(f)
    
quartierGeo = json.load(open(file=HERE/"assets"/"neighbourhoods.geojson", mode="r", encoding='utf-8'))

nomToNumero = {
    "Louvre":"1er",
    "Bourse":"2eme",
    "Temple":"3eme",
    "Hôtel-de-Ville":"4eme",
    "Panthéon":"5eme",
    "Luxembourg":"6eme",
    "Palais-Bourbon":"7eme",
    "Élysée":"8eme",
    "Opéra":"9eme",
    "Entrepôt":"10eme",
    "Popincourt":"11eme",
    "Reuilly":"12eme",
    "Gobelins":"13eme",
    "Observatoire":"14eme",
    "Vaugirard":"15eme",
    "Passy":"16eme",
    "Batignolles-Monceau":"17eme",
    "Buttes-Montmartre":"18eme",
    "Buttes-Chaumont":"19eme",
    "Ménilmontant":"20eme"
}

numeroToNom = {v: k for k, v in nomToNumero.items()}


# Créer une page me contacter
mecontacter = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem(html.A("GitHub", href="https://github.com/Biny17/PortfolioDash")),
        dbc.DropdownMenuItem(html.A("Linkedin", href="https://www.linkedin.com/in/tristan-gallet-0ab174206/")),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem(html.A("Mes réseaux", href="https://linktr.ee/tristanbiny")),
    ],
    nav=True,
    in_navbar=True,
    label="Me contacter",
)

banniere = dbc.Navbar(
    dbc.Container(
        [
            html.Img(id="logo", src=app.get_asset_url(LOGO), height="40px"), 
            dbc.NavbarBrand("Tristan Gallet", className="ms-2"),
            html.Div(html.H3("Portfolio - AirBNB"), style={'color':'#FFFFFF', 'margin-left':'20px'}),
            dbc.Collapse(
                dbc.Nav(
                    [mecontacter],
                    className="ms-auto",
                    navbar=True,
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ],
    ),
    color="#040200",
    dark=True,
    className="mb-2",
)

def cartePrixAuMetreCarre():
    fig = px.choropleth_mapbox(pxmc, geojson=quartierGeo, color='PrixMcarré',
                locations='neighbourhood', featureidkey="properties.neighbourhood",
                mapbox_style="carto-positron", center={"lat":48.86, "lon": 2.35}, zoom=11,
                opacity=0.7, color_continuous_scale='purples', 
                hover_data={
                    "neighbourhood":False,
                    "Arrondissement":True
                    },
                labels={
                    "PrixMcarré":"Prix du m²"
                })
    fig.update_layout(autosize=True)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def carteDensite():
    fig = px.choropleth_mapbox(densite, geojson=quartierGeo, color='nb/hectares',
              locations='neighbourhood', featureidkey="properties.neighbourhood",
              mapbox_style="carto-positron", center={"lat":48.86, "lon": 2.35}, zoom=11,
              opacity=0.8, color_continuous_scale='reds',
              labels={
                  "#logements":"Nombre de logements",
                  "nb/hectares":"Densité"
                  },
              hover_data={
                  "neighbourhood":False,
                  "Arrondissement":True,
                  "nb/hectares":True,
                  "#logements":True
              })
    fig.update_layout(autosize=True)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def cartePrix():
    fig = px.choropleth_mapbox(prix, geojson=quartierGeo, color='Prix moyen',
                locations='neighbourhood', featureidkey="properties.neighbourhood",
                mapbox_style="carto-positron", center={"lat":48.86, "lon": 2.35}, zoom=11,
                opacity=0.6, color_continuous_scale='greens',
                hover_data={
                    "neighbourhood":False,
                    "Arrondissement":True,
                })
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(autosize=True)
    return fig

def carteScore():
    fig = px.choropleth_mapbox(score, geojson=quartierGeo, color='Evaluation',
                locations='neighbourhood_cleansed', featureidkey="properties.neighbourhood",
                mapbox_style="carto-positron", center={"lat":48.86, "lon": 2.35}, zoom=11,
                opacity=0.6, color_continuous_scale='blues',
                hover_data={
                    "neighbourhood_cleansed":False,
                    "Arrondissement":True,
                })
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(autosize=True)
    return fig

def carteValue():
    fig = px.choropleth_mapbox(value, geojson=quartierGeo, color='Evaluation',
                locations='neighbourhood_cleansed', featureidkey="properties.neighbourhood",
                mapbox_style="carto-positron", center={"lat":48.86, "lon": 2.35}, zoom=11,
                opacity=0.6, color_continuous_scale='oranges',
                hover_data={
                    "neighbourhood_cleansed":False,
                    "Arrondissement":True,
                })
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(autosize=True)
    return fig

carteA = dbc.Card(
    dbc.CardBody(
        [
            dbc.Label("Sélection de la carte A"),
            html.Div(dcc.Dropdown(
                options=[
                    {'label':'Prix moyen', 'value':'cartePrix'},
                    {'label':'Densité de logements', 'value':'carteDensite'},
                    {'label':'Prix du mètre carré', 'value':'cartePrixAuMetreCarre'},
                    {'label':'Note générale', 'value':'carteScore'},
                    {'label':'Note qualité-prix', 'value':'carteValue'}
                ],
                value = 'cartePrix',
                id="DD graph1",
                clearable=False
            ), style={'margin-bottom':'1rem'}),
            html.H4("Nom du graphique 1", id = "Titre1"),
            dcc.Graph(
                id="graph1",
                figure=cartePrix()
            )
        ]
    ),
    id="carte1",
    color='#FFFFFF',
)

carteB = dbc.Card(
    dbc.CardBody(
        [
            dbc.Label("Sélection de la carte B:"),
            html.Div(
            dcc.Dropdown(
                options=[
                    {'label':'Prix moyen', 'value':'cartePrix'},
                    {'label':'Densité de logements', 'value':'carteDensite'},
                    {'label':'Prix du mètre carré', 'value':'cartePrixAuMetreCarre'},
                    {'label':'Note générale', 'value':'carteScore'},
                    {'label':'Note qualité-prix', 'value':'carteValue'}
                ],
                value = 'carteDensite',
                id="DD graph2",
                clearable=False
            ), style={'margin-bottom':'1rem'}),
            html.H4(id='Titre2'),
            dcc.Graph(
                id="graph2",
                figure=carteDensite()
            )
        ]
    ),
    id="carte2",
    color='#FFFFFF',
)

cards1 = html.Div(
    [
        dbc.Alert(
            children=[
                "Données pour la ville de Paris de ", 
                html.A("Inside AirBNB", href="http://insideairbnb.com/get-the-data/")
                ],
            #style={"padding":"15px 20px 15px 60px"}
        color="success"),
        dbc.Card([
            html.H4("Comparaison de différentes métriques par arrondissements de Paris:", 
                    style={"margin":"15px 20px 15px 35px"},
                    className="card-title"),
            dbc.Row(
                [
                    dbc.Col(carteA, width=6),
                    dbc.Col(carteB, width=6)
                ],
                className="g-0",
            )
        ], style={"background-color":"#FFFFFF"})
    ],style={"margin":"10px"}
)


@app.callback(
    Output('graph2', 'figure'),
    Input('DD graph2', 'value')
)
def update_graph2(choix):
    return eval(f"{choix}()")
    
@app.callback(
    Output('Titre1', 'children'),
    Input('DD graph1', 'value')
)
def update_graph_title1(choix):
    if choix == 'cartePrix': return "Prix moyen pour 2 personnes"
    if choix == 'carteDensite': return "Nombre de logements par hectare"
    if choix == 'cartePrixAuMetreCarre': return "Prix du m²"
    if choix == 'carteScore': return "Note générale du logement sur 5"
    if choix == 'carteValue': return "Note rapport qualité-prix sur 5"

@app.callback(
    Output('graph1', 'figure'),
    Input('DD graph1', 'value')
)
def update_graph1(choix):
    return eval(f"{choix}()")

@app.callback(
    Output('Titre2', 'children'),
    Input('DD graph2', 'value')
)
def update_graph_title2(choix):
    if choix == 'cartePrix': return "Prix moyen pour 2 personnes"
    if choix == 'carteDensite': return "Nombre de logements par hectare"
    if choix == 'cartePrixAuMetreCarre': return "Prix du m²"
    if choix == 'carteScore': return "Note générale du logement sur 5"
    if choix == 'carteValue': return "Note rapport qualité-prix sur 5"

def prixParChambre():
    colors = ["#89CFF0"]*5
    colors[2]="#DC143C"
    fig = px.bar(pPC, x='chambres', y='prixParChambre', text='Prix/chambre',
                 hover_data={'prixParChambre':False},
                 labels={"prixParChambre":"Prix/Chambre"},
                 template="plotly_white")
    fig.update_traces(marker_color=colors, marker_line_color='rgb(0,0,0)',
                    marker_line_width=2, opacity=1)
    fig.update_layout(title={
        "text":"Prendre un AirBNB à plusieurs est-il rentable ?",
        "x":0.5,
        "font":{
            "size":20
        }
    })
    fig
    return fig

def typeLogement():
    fig = px.pie(Logements, values="#logements", names="room_type", 
                 color_discrete_sequence=px.colors.qualitative.Safe,
                 template="plotly_white")
    fig.update_layout(title={
        "text":"Type de logements:",
        "x":0.5,
        "font":{
            "size":20
        }
    })
    return fig


histoPrix = dbc.Card(children=[dcc.Graph(id="graph3",figure=prixParChambre())])
pieType = dbc.Card(children=[dcc.Graph(id="graph4", figure=typeLogement())])

cards2 = dbc.Card([
    #titlerow,
    dbc.Row([
        dbc.Col(histoPrix, width=6),
        dbc.Col(pieType, width=6)
    ],
    align="center", className="g-0")
],
body=True,
style={"margin":"10px"})

prixPlotCallback = dbc.Card(
    children=[
        html.Label("Choisir l'arrondissement:"),
        dcc.Dropdown(['Tout']+list(nomToNumero.values()),
                     value='Tout',
                     id='dropdown_graph5',
                     clearable=False),
        html.Br(),
        html.Label('Nombre de chambres:'),
        dcc.RadioItems(["Tout","1","2","3"], value='Tout', id='radio_graph5')
], body=True)

cards3 = dbc.Card(children=[
    dbc.Row([
        dbc.Col([dbc.Card(children=[dcc.Graph(id="graph5")])], 
            width=9),
        dbc.Col(prixPlotCallback, width=3)
        ],
    align="start", class_name='g-0')
    ], style={"margin":"10px"})

@app.callback(
    Output('graph5', 'figure'),
    Input('radio_graph5', 'value'),
    Input('dropdown_graph5', 'value'))
def prixPlot(chambres, arrond):
    prix = repartition[['price', 'neighbourhood_cleansed', 'bedrooms']]
    if chambres != 'Tout':
        prix = prix.loc[(prix['bedrooms'] == int(chambres))]
    if arrond != 'Tout':
        prix = prix.loc[(prix['neighbourhood_cleansed'] == numeroToNom[arrond])]
    #considérons que 93% des valeurs sinon distribution trop grande, graphique moche
    low, high = np.percentile(prix['price'], 0), np.percentile(prix['price'], 93) 
    prix = prix.loc[(prix['price'] < high) & (prix['price'] >= low)]['price']
    prix = prix.rename("Prix en € pour une nuit")
    fig = px.histogram(prix, x="Prix en € pour une nuit", 
                       nbins=35, 
                       color_discrete_sequence=['#800020'],
                       template="plotly_white"
                       )
    fig.update_layout(title={
        "text":"Type de logements:",
        "x":0.5,
        "font":{
            "size":20
        }
    })
    return fig

app.layout = dbc.Container(
    [banniere,
     cards1,
     cards2,
     cards3],
    fluid = True,
    className="dbc",
    style={"padding":"0px"}
)

if __name__ == "__main__":
    app.run_server(debug=False)