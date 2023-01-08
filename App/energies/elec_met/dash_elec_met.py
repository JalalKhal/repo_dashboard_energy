import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table
import os
import sys

# This line gets the absolute path of the current file
absolute_path = os.path.dirname(__file__)
# This line defines a relative path to another directory
relative_path="../../../"
# This line appends the relative path to the sys.path list, so that Python can find modules in that directory
sys.path.append(os.path.join(absolute_path, relative_path))
# This line imports a function from a module in the directory specified by the relative path
from App.energies.elec_met.ProcessSQLElecMet import ProcessSQLElecMet

# Define a list of French month names
months_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
# Define a list of French quarter names
quarters_fr = ["1er trimestre", "2ème trimestre", "3ème trimestre", "4ème trimestre"]
# Define a dictionary to map column names to display names
mapping_namcol = {"libelle_metropole":"Métropole","consommation":"Consommation (en MW)","date":"Date","heures":"Horaire"}

# Call the function to get SQL data from SQL Server
df = ProcessSQLElecMet().get_sqlserver()

# Initialize the Dash app
app = Dash(__name__)
# Define the layout of the app
app.layout = html.Div([
    # Add a title
    html.H1("Tableau de la Consommation d'électricité par métropole en France",style={"color":"#DC143C"}),
    # Add an interval component that updates every 120 seconds (2 minutes)
    dcc.Interval(
        id='interval-component',
        interval=120*1000, # in milliseconds
        n_intervals=0,
    ),
    # Add a data table inside a div element
    html.Div([
        dash_table.DataTable(
            id='table',
            # Define the columns of the table, using the display names from the mapping dictionary
            columns=[{"name": mapping_namcol[i], "id": i}
                     for i in df.columns],
            # Set the data of the table
            data=df.to_dict('records'),
            # Set the text alignment of the cells
            style_cell=dict(textAlign='left'),
            # Set the background color of the header cells
            style_header=dict(backgroundColor="paleturquoise"),
            # Set the background color of the data cells
            style_data=dict(backgroundColor="lavender"),
            # Set the number of rows per page
            page_size=21,
        ),
    ])
],
)
# Define a callback function that updates the table data when the interval component updates
@app.callback(
    Output("table","data"),
    Input("interval-component","n_intervals")
)
def update_table(n):
    # Call the function to get SQL data from SQL Server
    return ProcessSQLElecMet().get_sqlserver().to_dict(orient='records')

# Print a message to the console
print("Loading..")
# Pause the script for 5 seconds
os.system("sleep 5")
# Run the app
app.run_server(debug=True,port=8053)
