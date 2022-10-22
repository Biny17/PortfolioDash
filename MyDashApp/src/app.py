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

listing = pd.read_csv("http://data.insideairbnb.com/france/ile-de-france/paris/2022-06-06/data/listings.csv.gz")
calendar = pd.read_csv("http://data.insideairbnb.com/france/ile-de-france/paris/2022-06-06/data/calendar.csv.gz")
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

numeroToNom = {v: k for k, v in nomToNumero.items()}

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
    keys = [{v: k for k, v in nomToNumero.items()}[a] for a in [a[0:a.find(" ")] for a in prix_m2_arr]]
    values = [int(a[a.find(":")+2:a.find("€")-1].replace(".","")) for a in prix_m2_arr]
    mapData = pd.DataFrame({"neighbourhood" : keys, "PrixMcarré": values})
    mapData["Arrondissement"] = mapData["neighbourhood"].apply(lambda x: nomToNumero[x])
    fig = px.choropleth_mapbox(mapData, geojson=quartierGeo, color='PrixMcarré',
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
    mapData = mapData.rename(columns={"neighbourhood_cleansed" : 'neighbourhood'})
    mapData["Arrondissement"] = mapData["neighbourhood"].apply(lambda x: nomToNumero[x])
    fig = px.choropleth_mapbox(mapData, geojson=quartierGeo, color='nb/hectares',
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
    mapData = listing.loc[listing["accommodates"]==2].groupby(["neighbourhood_cleansed"])["price"].mean().reset_index(name="Prix moyen")
    mapData["Prix moyen"] = round(mapData["Prix moyen"],2)
    mapData = mapData.rename(columns={"neighbourhood_cleansed":"neighbourhood"})
    mapData["Arrondissement"] = mapData["neighbourhood"].apply(lambda x: nomToNumero[x])
    fig = px.choropleth_mapbox(mapData, geojson=quartierGeo, color='Prix moyen',
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
    mapData = listing.groupby("neighbourhood_cleansed").mean("review_scores_rating")["review_scores_rating"].reset_index(name="Evaluation")
    mapData["Arrondissement"] = mapData["neighbourhood_cleansed"].apply(lambda x: nomToNumero[x])
    mapData["Evaluation"] = round(mapData["Evaluation"],2)
    fig = px.choropleth_mapbox(mapData, geojson=quartierGeo, color='Evaluation',
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
    mapData = listing.groupby("neighbourhood_cleansed").mean("review_scores_value")["review_scores_value"].reset_index(name="Evaluation")
    mapData["Arrondissement"] = mapData["neighbourhood_cleansed"].apply(lambda x: nomToNumero[x])
    mapData["Evaluation"] = round(mapData["Evaluation"],2)
    fig = px.choropleth_mapbox(mapData, geojson=quartierGeo, color='Evaluation',
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
    listing.loc[listing["bedrooms"]==0, "bedrooms"] = 0.999
    listing["prixParChambre"] = listing["price"]/listing["bedrooms"]
    listing.loc[listing["bedrooms"]==0.999, "bedrooms"] = 0
    pPC = listing.groupby("bedrooms")["prixParChambre"].mean().reset_index(name="prixParChambre").rename(columns={"bedrooms":"chambres"})
    pPC["prixParChambre"] = pPC["prixParChambre"].apply(lambda x : round(x, 2))
    pPC["chambres"] = pPC["chambres"].apply(lambda x : round(x))
    pPC["Prix/chambre"] = pPC['prixParChambre'].apply(lambda x: f"{round(x)}€")
    pPC = pPC.loc[pPC["chambres"] <= 4]
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
    Logements = listing.groupby(["room_type"])["room_type"].count()\
                .reset_index(name="#logements")\
                .sort_values(by=['#logements'],ascending=False)
    Logements["room_type"] = ["Logement entier", "Chambre perso", "Chambre d'hotel","Dortoir"]
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
    prix = listing[['price', 'neighbourhood_cleansed', 'bedrooms']]
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