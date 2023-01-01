from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import sys
sys.path.insert(0, "../../../../") #insert repo_dashboards_ecom to PYTHONPATH
from App.energy_Jelel.gaz_industriel.ProcessSQLGazIndustriel import ProcessSQLGazIndustriel
# Define a list of French month names
months_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
# Define a list of French quarter names
quarters_fr = ["1er trimestre", "2ème trimestre", "3ème trimestre", "4ème trimestre"]

def g(i):
    if -1<i and i<10:
        return "0"+str(i)
    return str(i)

df=ProcessSQLGazIndustriel().get_sqlserver() #get SQL data from SQL Server

#DataViz
# Initialize the Dash app
app = Dash(__name__)
# Define the layout of the app
app.layout = html.Div([
    html.H1("Consommation de Gaz en France pour les clients industriels",style={"color":"#DC143C"}),
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
    )
],
)
# Define the callback function for the area plot
@app.callback(
    Output("graph_line", "figure"),
    Input("hours-axis_line", "value"))
def display_graph_line(hour):
    # If the "Toutes horaires" option was selected, set the feature to "conso"
    if hour=="Toutes horaires":
        feature="conso"
    else:
        # Otherwise, set the feature to the selected hour
        feature=hour[:2]+"_00"
    # Aggregate the data by date and regions group
    df_agg = df.groupby(["date","operateur"])[['conso']+[f"{g(i)}_00" for i in range(24)]].mean().reset_index()
    # Create the area plot
    fig = px.area(df_agg, x="date", y=feature, color="operateur", line_group="operateur",\
        labels={feature:"Consommation à "+hour,"operateur":"Opérateurs"})\
    .update_layout(
        title="Graphique représentant la consommation de Gaz pour les clients industriels (MWh) moyenne par date et par opérateur", \
        xaxis_title="Date",yaxis_title="Consommation de Gaz (MWh) moyenne")
    return fig

# Run the app
app.run_server(debug=True,port=8051)