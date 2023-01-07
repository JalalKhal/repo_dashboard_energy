import pandas as pd
from dash import Dash, dcc, html, Input, Output,dash_table
import os
import sys
absolute_path = os.path.dirname(__file__)
relative_path="../../../"
sys.path.append(os.path.join(absolute_path, relative_path))
from App.energies.elec_met.ProcessSQLElecMet import ProcessSQLElecMet

# Define a list of French month names
months_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
# Define a list of French quarter names
quarters_fr = ["1er trimestre", "2ème trimestre", "3ème trimestre", "4ème trimestre"]
mapping_namcol={"libelle_metropole":"Métropole","consommation":"Consommation (en MW)","date":"Date","heures":"Horaire"}


df=ProcessSQLElecMet().get_sqlserver() #get SQL data from SQL Server

#DataViz
# Initialize the Dash app
app = Dash(__name__)
# Define the layout of the app
app.layout = html.Div([
    html.H1("Tableau de la Consommation d'électricité par métropole en France",style={"color":"#DC143C"}),
    dcc.Interval(
        id='interval-component',
        interval=120*1000, # in milliseconds
        n_intervals=0,
    ),
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": mapping_namcol[i], "id": i}
                     for i in df.columns],
            data=df.to_dict('records'),
            style_cell=dict(textAlign='left'),
            style_header=dict(backgroundColor="paleturquoise"),
            style_data=dict(backgroundColor="lavender"),
            page_size=21,
        ),
    ])
],
)

@app.callback(
    Output("table","data"),
    Input("interval-component","n_intervals")
)
def update_table(n):
    return ProcessSQLElecMet().get_sqlserver().to_dict(orient='records')#get SQL data from SQL Server



# Run the app
print("Loading..")
os.system("sleep 5")
app.run_server(debug=True,port=8053)





