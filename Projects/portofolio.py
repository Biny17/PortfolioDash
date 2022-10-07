from turtle import st
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
from pathlib import Path
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import pickle
import json
from area import area
import plotly.express as px
import plotly.io as pio

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])
app.title = 'Tristan Gallet'

HERE = Path(__file__).parent
LOGO = "https://i.ibb.co/k2Xhr9v/Sans-titre.png"

with open(HERE / "data.pickle", 'rb') as f:
    listing, calendar = pickle.load(f)
quartierGeo = json.load(open(file=HERE / "neighbourhoods.geojson", mode="r", encoding='utf-8'))

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

listing['bedrooms'] = listing['bedrooms'].fillna(0)
listing["price"] = listing["price"].apply(lambda x: int(float(x.replace("$", "").replace(",", ""))))
listing["Arrondissement"] = listing["neighbourhood_cleansed"].apply(lambda x: nomToNumero[x])

# Créer une page me contacter
mecontacter = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem(html.A("GitHub", href="#")),
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
            html.Img(id="logo", src=LOGO, height="40px"), 
            dbc.NavbarBrand("Tristan Gallet", className="ms-2"),
            html.Div(html.H3("Portfolio - données de AirBNB"), style={'color':'#FFFFFF', 'margin-left':'20px'}),
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
    color="primary",
    dark=True,
    className="mb-5",
)

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

def cartePrixAuMetreCarre():
    prix_m2_arr="""1er arrondissement : 13.445 €/m2
2eme arrondissement : 12.570 €/m2
3eme arrondissement : 12.982 €/m2
4eme arrondissement : 13.928 €/m2
5eme arrondissement : 13.186 €/m2
6eme arrondissement : 15.367 €/m2
7eme arrondissement : 14.827 €/m2
8eme arrondissement : 12.510 €/m2
9eme arrondissement : 11.872 €/m2
10eme arrondissement : 11.065 €/m2
11eme arrondissement : 11.305 €/m2
12eme arrondissement : 10.355 €/m2
13eme arrondissement : 9.916 €/m2
14eme arrondissement : 10.805 €/m2
15eme arrondissement : 10.976 €/m2
16eme arrondissement : 12.086 €/m2
17eme arrondissement : 11.767 €/m2
18eme arrondissement : 10.855 €/m2
19eme arrondissement : 9.475 €/m2
20eme arrondissement : 9.874 €/m2""".splitlines()
    keys = [{v: k for k, v in nomToNumero.items()}[a] for a in [a[0:a.find(" ")] for a in prix_m2_arr]]
    values = [int(a[a.find(":")+2:a.find("€")-1].replace(".","")) for a in prix_m2_arr]
    prix_m2_arr = pd.DataFrame({"neighbourhood" : keys, "PrixMcarré": values})
    fig = px.choropleth_mapbox(prix_m2_arr, geojson=quartierGeo, color='PrixMcarré',
                locations='neighbourhood', featureidkey="properties.neighbourhood",
                mapbox_style="carto-positron", center={"lat":48.86, "lon": 2.35}, zoom=10.4,
                opacity=0.6, hover_data=["neighbourhood", "PrixMcarré"], color_continuous_scale='purples')
    fig.update_layout(autosize=True)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def carteDensite():
    # Dictionnaire associant chaque quartier à son aire
    neighbourhoodArea = dict()
    for cartier in quartierGeo["features"]:
        neighbourhoodArea[cartier["properties"]["neighbourhood"]] = round(area(cartier["geometry"]))
    neighbourhoodArea["Reuilly"] += -9950000 #J'enlève la superficie du bois de Vincenne qui fait partie du 12eme
    #Nombre de logement par quartier:
    mapData = pd.DataFrame(listing.groupby(["neighbourhood_cleansed"])["neighbourhood_cleansed"].count().reset_index(name="#logements"))
    mapData["superficie"] = mapData["neighbourhood_cleansed"].apply(lambda x: neighbourhoodArea[x])
    #nombre de logement par hectares par quartier
    mapData["nb/hectares"] = round(mapData["#logements"]/(mapData["superficie"]/10000), 2)
    mapData = mapData.rename(columns={mapData.columns[0] : 'neighbourhood'})
    mapData["Arrondissement"] = mapData["neighbourhood"].apply(lambda x: nomToNumero[x])
    fig = px.choropleth_mapbox(mapData, geojson=quartierGeo, color='nb/hectares',
              locations='neighbourhood', featureidkey="properties.neighbourhood",
              mapbox_style="carto-positron", center={"lat":48.86, "lon": 2.35}, zoom=10.4,
              opacity=0.6, hover_data=["Arrondissement", "nb/hectares", "#logements"],color_continuous_scale='reds')
    fig.update_layout(autosize=True)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def cartePrix():
    mapData = listing.loc[listing["accommodates"]==2].groupby(["neighbourhood_cleansed"])["price"].mean().reset_index(name="prix Moyen")
    mapData["prix Moyen"] = round(mapData["prix Moyen"],2)
    mapData = mapData.rename(columns={"neighbourhood_cleansed":"quartier"})
    fig = px.choropleth_mapbox(mapData, geojson=quartierGeo, color='prix Moyen',
                locations='quartier', featureidkey="properties.neighbourhood",
                mapbox_style="carto-positron", center={"lat":48.86, "lon": 2.35}, zoom=10.4,
                opacity=0.6, color_continuous_scale='greens')
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(autosize=True)
    return fig

def carteScore():
    mapData = listing.groupby("neighbourhood_cleansed").mean("review_scores_rating")["review_scores_rating"].reset_index(name="Evalutation")
    fig = px.choropleth_mapbox(mapData, geojson=quartierGeo, color='Evalutation',
                locations='neighbourhood_cleansed', featureidkey="properties.neighbourhood",
                mapbox_style="carto-positron", center={"lat":48.86, "lon": 2.35}, zoom=10.4,
                opacity=0.6, color_continuous_scale='blues')
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(autosize=True)
    return fig

def carteValue():
    mapData = listing.groupby("neighbourhood_cleansed").mean("review_scores_value")["review_scores_value"].reset_index(name="Evalutation")
    fig = px.choropleth_mapbox(mapData, geojson=quartierGeo, color='Evalutation',
                locations='neighbourhood_cleansed', featureidkey="properties.neighbourhood",
                mapbox_style="carto-positron", center={"lat":48.86, "lon": 2.35}, zoom=10.4,
                opacity=0.6, color_continuous_scale='oranges')
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
            dcc.Graph(
                id="graph1",
                figure=cartePrix()
            )
        ]
    ),
    id="carte1",
    color='light'
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
            dcc.Graph(
                id="graph2",
                figure=carteDensite()
            )
        ]
    ),
    id="carte2",
    color='light'
)

cards1 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(carteA),
                dbc.Col(carteB)
            ],
            className="mb-6"
        )
    ]
)

@app.callback(
    Output('graph2', 'figure'),
    Input('DD graph2', 'value')
)
def update_graph2(choix):
    return eval(f"{choix}()")
    
@app.callback(
    Output('graph1', 'figure'),
    Input('DD graph1', 'value')
)
def update_graph1(choix):
    return eval(f"{choix}()")

app.layout = html.Div(
    [banniere, cards1]
)

if __name__ == "__main__":
    app.run_server(debug=True)