import os
import sys

absolute_path = os.path.dirname(__file__)
relative_path="../../"
sys.path.append(os.path.join(absolute_path, relative_path))

from dash import Dash, html, dcc, dash_table, Output, Input
from App.energies.gaz_elec.ProcessSQLGazElec import ProcessSQLGazElec
import pandas as pd
import plotly.express as px

df=ProcessSQLGazElec().get_sqlserver() #get SQL data from SQL Server
app =Dash()
app.layout = html.Div(children=[
    html.H1(children='Évolution de la consommation totale d\'énergie (Gaz et Électricité)',style={"color":"#DC143C"}),
    html.Div(
        dash_table.DataTable(id="table",data=df.to_dict('records'),columns=[{"name": i, "id": i} for i in df.columns]),
        style={"display":"none"},
    ),
    dcc.Interval(
        id='interval-component',
        interval=600*1000, # in milliseconds
        n_intervals=0,
    ),
    dcc.Graph(id='graph_line_chart'),

])

@app.callback(
    Output("table","data"),
    Input("interval-component","n_intervals")
)
def update_table(n):
    return ProcessSQLGazElec().get_sqlserver().to_dict(orient='records')#get SQL data from SQL Server

@app.callback(
    Output("graph_line_chart", "figure"),
    Input("table","data"),
)
def display_line_chart(df_json):
    df=pd.DataFrame.from_dict(df_json).sort_values(by="annee")
    consumption_values=df.groupby("annee")["consototale"].sum()
    try:
        fig=px.line(df,x=df["annee"].unique(),y=consumption_values,markers=True, \
                    title='Consommation totale d\'énergie (Gaz et Électricité) par année') \
            .update_layout(
            xaxis_title="Année",yaxis_title="Consommation totale (somme) de Gaz et Électricité (en MWh)") \
            .update_traces(line=dict(color="#72A0C1"))
    except:
        fig=px.line(df,x=df["annee"].unique(),y=consumption_values,markers=True, \
                    title='Consommation totale d\'énergie (Gaz et Électricité) par année') \
            .update_layout(
            xaxis_title="Année",yaxis_title="Consommation totale (somme) de Gaz et Électricité (en MWh)") \
            .update_traces(line=dict(color="#72A0C1"))
    return fig


# Run the app
app.run_server(debug=True,port=8055)

