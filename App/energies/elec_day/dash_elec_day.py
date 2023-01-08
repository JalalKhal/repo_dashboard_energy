import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import os
import sys

# This line gets the absolute path of the current file
absolute_path = os.path.dirname(__file__)
# This line defines a relative path to another directory
relative_path="../../../"
# This line appends the relative path to the sys.path list, so that Python can find modules in that directory
sys.path.append(os.path.join(absolute_path, relative_path))
# This line imports a function from a module in the directory specified by the relative path
from App.energies.elec_day.ProcessSQLElecDay import ProcessSQLElecDay

# Define a list of French month names
months_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
# Define a list of French quarter names
quarters_fr = ["1er trimestre", "2ème trimestre", "3ème trimestre", "4ème trimestre"]

# Call the function to get SQL data from SQL Server
df = ProcessSQLElecDay().get_sqlserver()

# Initialize the Dash app
app = Dash(__name__)
# Define the layout of the app
app.layout = html.Div([
    # Add a title
    html.H1("Consommation de Gaz pour différents types de clients en France",style={"color":"#DC143C"}),
    # Add a data table that is not displayed
    html.Div(
        dash_table.DataTable(id="table",data=df.to_dict('records'),columns=[{"name": i, "id": i} for i in df.columns]),
        style={"display":"none"},
    ),
    # Add an interval component that updates every 600 seconds (10 minutes)
    dcc.Interval(
        id='interval-component',
        interval=600*1000, # in milliseconds
        n_intervals=0,
    ),
    # Add a dropdown menu and a graph inside a div element
    html.Div(children=[
        dcc.Dropdown(
            id='period-axis_chart',
            # Define the options of the dropdown menu
            options=["Année","Trimestre","Mois"],
            # Set the default value of the dropdown menu
            value="Mois",
            # Make the dropdown menu non-clearable
            clearable=False,
            # Set the width of the dropdown menu
            style={"width":"50%"},
        ),
        dcc.Graph(id="graph_chart"),
    ],style={"display":"block"}
    ),
],
)

# Define a callback function that updates the graph based on the selected period and the data in the table
@app.callback(
    Output("graph_chart", "figure"),
    Input("period-axis_chart", "value"),
    Input("table","data"),
)
def display_graph_chart(period, df_json):
    # Convert the data in the table to a Pandas DataFrame
    df = pd.DataFrame.from_dict(df_json)
    # Convert the period to the corresponding column and labels in French
    conv_fr = {"Trimestre":(list(range(1,5)),quarters_fr),"Mois":(list(range(1,13)),months_fr)}
    period_conv = {"Année":"year","Trimestre":"quarter","Mois":"month"}[period]
    conv_period_dict = {value:key for key,value in {"Année":"year","Trimestre":"quarter","Mois":"month"}.items()}
    # Aggregate the data by the selected period and region group
    df_agg = df.groupby([period_conv, "categorie"])["value"].mean().reset_index()
    # Create the bar chart
    fig = px.bar(df_agg, x=period_conv, y="value", color="categorie",barmode="group",
                 labels={
                     "categorie":"Catégorie de client",
                 }) \
        .update_layout(
        title="Diagramme à barres de la consommation journalière d'électricité (en W) moyenne par catégorie client.", \
        xaxis_title=conv_period_dict[period_conv],yaxis_title="Consommation d'électricité moyenne (en W)")
    # If the selected period is not "Année", update the x-axis tick values and tick labels
    if period != "Année":
        fig.update_xaxes(tickvals=conv_fr[period][0], ticktext=conv_fr[period][1])
    # Return the figure
    return fig

# Print a message to the console
print("Loading..")
# Pause the script for 5 seconds
os.system("sleep 5")
# Run the app
app.run_server(debug=True,port=8053)
