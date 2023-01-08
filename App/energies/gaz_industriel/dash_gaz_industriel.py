import os
import sys

# Find the absolute path of the script
absolute_path = os.path.dirname(__file__)
# Define the relative path of the modules
relative_path="../../../"
# Add the relative path to the system path so that the modules can be imported
sys.path.append(os.path.join(absolute_path, relative_path))

# Import required Dash and Pandas libraries
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd
# Import the ProcessSQLGazIndustriel module from the App.energies.gaz_industriel package
from App.energies.gaz_industriel.ProcessSQLGazIndustriel import ProcessSQLGazIndustriel

# Define a list of French month names
months_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
# Define a list of French quarter names
quarters_fr = ["1er trimestre", "2ème trimestre", "3ème trimestre", "4ème trimestre"]

# Define a function to pad single-digit integers with a leading zero
def g(i):
    if -1<i and i<10:
        return "0"+str(i)
    return str(i)

# Get the data from the SQL server using the ProcessSQLGazIndustriel module
df=ProcessSQLGazIndustriel().get_sqlserver()

# Initialize the Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    # Add a heading
    html.H1("Consommation de Gaz en France pour les clients industriels",style={"color":"#DC143C"}),
    # Add a hidden div to store the data
    html.Div(
        # Use the dash_table library to create a DataTable from the Pandas dataframe
        dash_table.DataTable(id="table",data=df.to_dict('records'),columns=[{"name": i, "id": i} for i in df.columns]),
        style={"display":"none"},
    ),
    # Add an interval component to update the data and charts every 10 minutes
    dcc.Interval(
        id='interval-component',
        interval=600*1000, # in milliseconds
        n_intervals=0,
    ),
    html.Div(children=[
    html.P("Selectionnez l'horaire de consommation:"),
    dcc.Dropdown(
        id='hours-axis_line',
        options=["Toutes horaires"]+[g(i)+"h00" for i in range(24)],
        value="Toutes horaires",
        clearable=False,
        style={"width":"50%"},
    ),
    dcc.Graph(id="graph_line"),
    ],style={"display":"block"},
    ),
    html.Div(children=[
        # Add a dropdown to select the hour
        dcc.Dropdown(
            id='hours-axis_chart',
            # Options for the dropdown are "Toutes horaires" and the hours from 00h00 to 23h00
            options=["Toutes horaires"]+[g(i)+"h00" for i in range(24)],
            value="Toutes horaires",
            clearable=False,
            style={"width":"50%"},
        ),
        # Add a dropdown to select the period (year, quarter, or month)
        dcc.Dropdown(
            id='period-axis_chart',
            options=["Année","Trimestre","Mois"],
            value="Mois",
            clearable=False,
            style={"width":"50%"},
        ),
        # Add a graph component to display the chart
        dcc.Graph(id="graph_chart"),
    ],style={"display":"block"}
    ),
],
)

@app.callback(
    # Output the data of the table
    Output("table","data"),
    # Input the number of intervals passed
    Input("interval-component","n_intervals")
)
# Define the update_table function
def update_table(n):
    # Get the data from the SQL server using the ProcessSQLGazIndustriel module and return it in 'records' format
    return ProcessSQLGazIndustriel().get_sqlserver().to_dict(orient='records')

# Define the callback function for the line chart
@app.callback(
    # Output the figure of the graph
    Output("graph_line", "figure"),
    # Input the selected hour and the data of the table
    Input("hours-axis_line", "value"),
    Input("table","data")
)
# Define the display_graph_line function
def display_graph_line(hour,df_json):
    # Convert the data from json format to a Pandas dataframe
    df=pd.DataFrame.from_dict(df_json)
    # If the "Toutes horaires" option was selected, set the feature to "conso"
    if hour=="Toutes horaires":
        feature="conso"
    else:
        # Otherwise, set the feature to the selected hour
        feature=hour[:2]+"_00"
    # Aggregate the data by date and regions group
    df_agg = df.groupby(["date","operateur"])[['conso']+[f"{g(i)}_00" for i in range(24)]].mean().reset_index()
    # Create the line chart
    fig = px.scatter(df_agg, x="date", y=feature, color="operateur", \
                     labels={feature:"Consommation à "+hour,"operateur":"Opérateurs"}) \
        .update_layout(
        title="Graphique représentant la consommation de Gaz pour les clients industriels (MWh) moyenne par date et par opérateur", \
        xaxis_title="Date",yaxis_title="Consommation de Gaz (MWh) moyenne")
    return fig

# Define the callback function for the bar chart
@app.callback(
    # Output the figure of the graph
    Output("graph_chart", "figure"),
    # Input the selected hour, period, and data of the table
    Input("hours-axis_chart", "value"),
    Input("period-axis_chart", "value"),
    Input("table","data"),
)
# Define the display_graph_chart function
def display_graph_chart(hour,period,df_json):
    # Convert the data from json format to a Pandas dataframe
    df=pd.DataFrame.from_dict(df_json)
    # Convert the period to the corresponding column and labels in French
    conv_fr={"Trimestre":(list(range(1,5)),quarters_fr),"Mois":(list(range(1,13)),months_fr)}
    period_conv={"Année":"year","Trimestre":"quarter","Mois":"month"}[period]
    conv_period_dict={value:key for key,value in {"Année":"year","Trimestre":"quarter","Mois":"month"}.items()}
    # If the "Toutes horaires" option was selected, set the feature to "conso"
    if hour=="Toutes horaires":
        feature="conso"
    else:
        # Otherwise, set the feature to the selected hour
        feature=hour[:2]+"_00"
    # Aggregate the data by the selected period and region group
    df_agg = df.groupby([period_conv, 'operateur'])[['conso']+[f"{g(i)}_00" for i in range(24)]].mean().reset_index()
    # Create the bar chart
    fig = px.bar(df_agg, x=period_conv, y=feature, color="operateur",barmode="group",
                 labels={
                     "operateur":"Opérateurs",
                 }) \
        .update_layout(
        title="Diagramme à barres de la consommation de Gaz (MWh) moyenne par opérateur/par horaire/par fréquence temporelle", \
        xaxis_title=conv_period_dict[period_conv],yaxis_title="Consommation de Gaz (MWh) moyenne")
    # If the period is not "Année", update the x-axis tick values and text with the corresponding French labels
    if period != "Année":
        fig.update_xaxes(tickvals=conv_fr[period][0], ticktext=conv_fr[period][1])
    return fig

# Run the app
print("Loading..")
# Pause for 5 seconds before running the app
os.system("sleep 5")
# Run the app in debug mode on port 8053
app.run_server(debug=True,port=8053)
