# Annalyse et visualisation avec Python et Dash, création d'un site internet

### L'[application](https://airport-craw-harvester-0sh2.herokuapp.com/) sur un serveur Heroku : https://airport-craw-harvester-0sh2.herokuapp.com/

Analyse et visualisation des données [de AirBNB Paris](http://insideairbnb.com/get-the-data)
Avec Dash, Plotly, Numpy et Pandas

J'ai fait l'exploration, le nettoyage et les premières visualisation dans le notebook [airbnbParis.ipynb](airbnbParis.ipynb)
Les différents composant Dash du site internet ont été conçu dans [dash_parts.ipynb](dash_parts.ipynb)

Ensuite tout ce qui concerne l'application sur le serveur est situé dans MyDashApp, les données ont été réduits au nécessaire dans un fichier data.pickle.
Le code du site en Python est dans [MyDashApp/src](MyDashApp/src/app.py)

[neighbourhoods.geojson](neighbourhoods.geojson) contient les coordonnées des différents arrondissements de Paris pour la visualisation