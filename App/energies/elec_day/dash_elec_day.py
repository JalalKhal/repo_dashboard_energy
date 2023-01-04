import pandas as pd
from dash import Dash, dcc, html, Input, Output,dash_table
import plotly.express as px
import os
import sys
absolute_path = os.path.dirname(__file__)
relative_path="../../../"
sys.path.append(os.path.join(absolute_path, relative_path))
from App.energies.elec_day.ProcessSQLElecDay import ProcessSQLElecDay

df=ProcessSQLElecDay().get_sqlserver() #get SQL data from SQL Server

#DataViz
# Initialize the Dash app
app = Dash(__name__)
# Define the layout of the app
app.layout = html.Div([
    html.H1("Consommation de Gaz des ménages en France",style={"color":"#DC143C"}),
    html.Div(
        dash_table.DataTable(id="table",data=df.to_dict('records'),columns=[{"name": i, "id": i} for i in df.columns]),
        style={"display":"none"},
    ),
    dcc.Interval(
        id='interval-component',
        interval=600*1000, # in milliseconds
        n_intervals=0,
    ),
    html.Div(children=[
        dcc.Graph(id="graph_chart"),
    ],style={"display":"block"}
    ),
],
)



@app.callback(
    Output("graph_chart", "figure"),
    Input("table","data"),
)
def display_graph_chart(df_json):
    df=pd.DataFrame.from_dict(df_json)
    fig = px.bar(df, x="categorie", y="value")\
        .update_layout(
        title="Consommation journalière par catégorie client (en W)", \
        xaxis_title="Catégorie",yaxis_title="Consommation (W)")
    return fig




# Run the app
app.run_server(debug=True,port=8053)
