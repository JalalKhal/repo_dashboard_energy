import os
import sys
# This line gets the absolute path of the current file
absolute_path = os.path.dirname(__file__)
# This line defines a relative path to another directory
relative_path="../../../"
# This line appends the relative path to the sys.path list, so that Python can find modules in that directory
sys.path.append(os.path.join(absolute_path, relative_path))

# Import necessary libraries and classes
from dash import Dash, html, dcc, dash_table, Output, Input
from App.energies.gaz_elec.ProcessSQLGazElec import ProcessSQLGazElec
import pandas as pd
import plotly.express as px

# Retrieve data from SQL Server
df = ProcessSQLGazElec().get_sqlserver()

# Initialize Dash app
app = Dash()

# Set app layout
app.layout = html.Div(children=[
    # Title
    html.H1(children='Évolution de la consommation totale d\'énergie (Gaz et Électricité)',
            style={"color":"#DC143C"}),
    # Data table (hidden)
    html.Div(
        dash_table.DataTable(id="table", data=df.to_dict('records'),
                             columns=[{"name": i, "id": i} for i in df.columns]),
        style={"display":"none"},
    ),
    # Interval component to trigger updates every 10 minutes
    dcc.Interval(
        id='interval-component',
        interval=600*1000, # in milliseconds
        n_intervals=0,
    ),
    # Graph component for line chart
    dcc.Graph(id='graph_line_chart'),
])

@app.callback(
    # Output component for data table
    Output("table","data"),
    # Input component for interval component
    Input("interval-component","n_intervals")
)
def update_table(n):
    # Retrieve data from SQL Server and convert to dictionary
    return ProcessSQLGazElec().get_sqlserver().to_dict(orient='records')

@app.callback(
    # Output component for line chart
    Output("graph_line_chart", "figure"),
    # Input component for data table
    Input("table","data"),
)
def display_line_chart(df_json):
    # Convert data from JSON to pandas DataFrame and group by year
    df = pd.DataFrame.from_dict(df_json).sort_values(by="annee")
    consumption_values = df.groupby("annee")["consototale"].sum()

    # Create line chart using plotly express and update layout
    try:
        fig = px.line(df, x=df["annee"].unique(), y=consumption_values, markers=True,
                      title='Consommation totale d\'énergie (Gaz et Électricité) par année') \
            .update_layout(
            xaxis_title="Année",
            yaxis_title="Consommation totale (somme) de Gaz et Électricité (en MWh)") \
            .update_traces(line=dict(color="#72A0C1"))
    except:
        # Catch any errors and create line chart again
        fig = px.line(df, x=df["annee"].unique(), y=consumption_values, markers=True,
                      title='Consommation totale d\'énergie (Gaz et Électricité) par année') \
            .update_layout(
            xaxis_title="Année",
            yaxis_title="Consommation totale (somme) de Gaz et Électricité (en MWh)") \
            .update_traces(line=dict(color="#72A0C1"))
    return fig

# Run the app
print("Loading..")
os.system("sleep 5")
app.run_server(debug=True,port=8053)
