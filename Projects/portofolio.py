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

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
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
listing["Arrondissement"] = listing["neighbourhood_cleansed"].apply(lambda x: x+" - "+nomToNumero[x])

# Créer une page me contacter
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("tristangallet17@gmail.com"),
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
                    [dropdown],
                    className="ms-auto",
                    navbar=True,
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ],
    ),
    color="dark",
    dark=True,
    className="mb-5",
)

def carteDensite():
    # Dictionnaire associant chaque quartier à son aire
    neighbourhoodArea = dict()
    for cartier in quartierGeo["features"]:
        neighbourhoodArea[cartier["properties"]["neighbourhood"]] = round(area(cartier["geometry"]))
    neighbourhoodArea["Reuilly"] += -9950000 #J'enlève la superficie du bois de Vincenne qui fait partie du 12eme
    #Nombre de logement par quartier:
    mapData = pd.DataFrame(listing.loc[listing["accommodates"]==2].groupby(["neighbourhood_cleansed"])["neighbourhood_cleansed"].count().reset_index(name="#logements"))
    mapData["superficie"] = mapData["neighbourhood_cleansed"].apply(lambda x: neighbourhoodArea[x])
    #nombre moyen de logement en moyenne par quartier
    mapData["#logements/hectares"] = round(mapData["#logements"]/(mapData["superficie"]/10000), 2)
    mapData = mapData.rename(columns={mapData.columns[0] : 'neighbourhood'})
    mapData["Arrondissement"] = mapData["neighbourhood"].apply(lambda x: nomToNumero[x])
    fig = px.choropleth_mapbox(mapData, geojson=quartierGeo, color='#logements/hectares',
              locations='neighbourhood', featureidkey="properties.neighbourhood",
              mapbox_style="carto-positron", center={"lat":48.86, "lon": 2.35}, zoom=10.5,
              opacity=0.5, hover_data=["Arrondissement", "#logements/hectares", "#logements"])
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    carte = dcc.Graph(
        id="Densité par quartier",
        figure=fig
    )
    return carte
    
def cartePrix():
    mapData = pd.DataFrame(listing.groupby(["neighbourhood_cleansed"])["neighbourhood_cleansed"].count().reset_index(name="#logements"))
    mapPrix = listing.groupby(["neighbourhood_cleansed"])["price"].mean().reset_index(name="prix_moyen")
    mapPrix = mapPrix.rename(columns={"neighbourhood_cleansed":"quartier"})
    fig = px.choropleth_mapbox(mapPrix, geojson=quartierGeo, color='prix_moyen',
                locations='quartier', featureidkey="properties.neighbourhood",
                mapbox_style="carto-positron", center={"lat":48.86, "lon": 2.35}, zoom=10.5,
                opacity=0.5)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    carte = dcc.Graph(
        id="Prix moyen par quartier",
        figure=fig
    )
    return carte
    
partie1 = html.Div(children=[
    html.Div([
        html.Div([html.H6("BLABLABLABLA")]),
        carteDensite()
    ])
])


app.layout = html.Div(
    [banniere, carteDensite(), cartePrix()]
)

if __name__ == "__main__":
    app.run_server(debug=True)