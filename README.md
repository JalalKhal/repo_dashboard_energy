
## Projet UNIX 2023
# Consommation d'énergies en France

Ce projet a pour but de récupérer des données sur les différents types d'énergies en France à travers l'API open data. Les données récupérées sont ensuite stockées dans deux serveurs différents : MongoDB Server et SQL Server. Par la suite, des tableaux de bord illustrant la consommation énergétique des différentes énergies en France sont produits à l'aide de Dash (python) et une interface web est créée pour visualiser ces tableaux de bord.
## Installation

Installer les dépendances nécessaires au projet:
init.sh installe toutes les dépendances nécessaires pour le projet

```bash
  chmod +x init.sh
  sudo ./init.sh
```

## Deployment

Pour déployer le projet:
Une fois l'infrastructure des données (serveurs MongoDB/SQL Server) créés et initialisés:
```bash
  sudo ./run_app.sh
```
une fois run_app exécuté, l'interface web est créée un url pour visualiser les tableaux de bord


## Screenshots

![App Screenshot](documentation/img/dash_lineplt_ex.png)
![App Screenshot](documentation/img/dash_scatter_ex.png)
![App Screenshot](documentation/img/dash_tab_ex.png)


## Tech Stack
Coté serveur:
docker,MongoDB Server (container), SQL Server (container)

Dashboards:
Dash (avec python)

Librairies python:
pandas,plotly,pandas,pymongo,SQLAlchemy,validators,pyodbc,regex

