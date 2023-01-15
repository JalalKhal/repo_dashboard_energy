import os
import sys
absolute_path = os.path.dirname(__file__)
relative_path="../../"
sys.path.append(os.path.join(absolute_path, relative_path))

import pandas as pd
from dash import Dash, dcc, html, Input, Output,dash_table
import plotly.express as px
from App.energies.gaz.ProcessSQLGaz import ProcessSQLGaz
from App.energies.gaz_elec.ProcessSQLGazElec import ProcessSQLGazElec
from App.energies.gaz_industriel.ProcessSQLGazIndustriel import ProcessSQLGazIndustriel
from App.energies.elec_day.ProcessSQLElecDay import ProcessSQLElecDay
from App.energies.elec_met.ProcessSQLElecMet import ProcessSQLElecMet

absolute_path = os.path.dirname(__file__)
relative_path="../../"
sys.path.append(os.path.join(absolute_path, relative_path))
# Define a list of French month names
months_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
# Define a list of French quarter names
quarters_fr = ["1er trimestre", "2ème trimestre", "3ème trimestre", "4ème trimestre"]
mapping_namcol_elec_met={"libelle_metropole":"Métropole","consommation":"Consommation (en MW)","date":"Date","heures":"Horaire"}

def g(i):
    if -1<i and i<10:
        return "0"+str(i)
    return str(i)

df_gaz=ProcessSQLGaz().get_sqlserver() #get SQL data from SQL Server
df_gaz_elec=ProcessSQLGazElec().get_sqlserver() #get SQL data from SQL Server
df_gaz_industrial=ProcessSQLGazIndustriel().get_sqlserver() #get SQL data from SQL Server
df_elec_day=ProcessSQLElecDay().get_sqlserver() #get SQL data from SQL Server
df_elec_met=ProcessSQLElecMet().get_sqlserver() #get SQL data from SQL Server



#DataViz
# Initialize the Dash app
app = Dash(__name__)
# Define the layout of the app

app.layout =html.Div([
    html.Div([
        html.H1("Consommation de Gaz des ménages en France",style={"color":"#DC143C"}),
        html.Div(
            dash_table.DataTable(id="table_gaz",data=df_gaz.to_dict('records'),columns=[{"name": i, "id": i} for i in df_gaz.columns]),
            style={"display":"none"},
        ),
        dcc.Interval(
            id='interval-component_gaz',
            interval=600*1000, # in milliseconds
            n_intervals=0,
        ),
        html.Div(children=[
            html.P("Selectionnez l'horaire de consommation:"),
            dcc.Dropdown(
                id='hours-axis_line_gaz',
                options=["Toutes horaires"]+[g(i)+"h00" for i in range(24)],
                value="Toutes horaires",
                clearable=False,
                style={"width":"50%"},
            ),
            dcc.Graph(id="graph_line_gaz"),
        ],style={"display":"block"},
        ),
        html.Div(children=[
            dcc.Dropdown(
                id='hours-axis_chart_gaz',
                options=["Toutes horaires"]+[g(i)+"h00" for i in range(24)],
                value="Toutes horaires",
                clearable=False,
                style={"width":"50%"},
            ),
            dcc.Dropdown(
                id='period-axis_chart_gaz',
                options=["Année","Trimestre","Mois"],
                value="Mois",
                clearable=False,
                style={"width":"50%"},
            ),
            dcc.Graph(id="graph_chart_gaz"),
        ],style={"display":"block"}
        ),
        html.Div(children=[
            dcc.Dropdown(
                id='hours-axis_hist_gaz',
                options=["Toutes horaires"]+[g(i)+"h00" for i in range(24)],
                value="Toutes horaires",
                clearable=False,
                style={"width":"50%"},
            ),
            dcc.Graph(id="graph_hist_gaz"),
        ],style={"display":"block"},
        ),

    ],
    ),
    #fin Gaz---------------------------------------------------------------------------------------------------------#

    html.Div([
        html.H1("Consommation de Gaz en France pour les clients industriels",style={"color":"#DC143C"}),
        # Add a hidden div to store the data
        html.Div(
            dash_table.DataTable(id="table_gaz_industrial",data=df_gaz_industrial.to_dict('records'),columns=[{"name": i, "id": i} for i in df_gaz_industrial.columns]),
            style={"display":"none"},
        ),
        dcc.Interval(
            id='interval-component_gaz_industrial',
            interval=60*1000, # in milliseconds
            n_intervals=0,
        ),
        html.Div(children=[
            html.P("Selectionnez l'horaire de consommation:"),
            dcc.Dropdown(
                id='hours-axis_line_gaz_industrial',
                options=["Toutes horaires"]+[g(i)+"h00" for i in range(24)],
                value="Toutes horaires",
                clearable=False,
                style={"width":"50%"},
            ),
            dcc.Graph(id="graph_line_gaz_industrial"),
        ],style={"display":"block"},
        ),
        html.Div(children=[
            dcc.Dropdown(
                id='hours-axis_chart_gaz_industrial',
                options=["Toutes horaires"]+[g(i)+"h00" for i in range(24)],
                value="Toutes horaires",
                clearable=False,
                style={"width":"50%"},
            ),
            dcc.Dropdown(
                id='period-axis_chart_gaz_industrial',
                options=["Année","Trimestre","Mois"],
                value="Mois",
                clearable=False,
                style={"width":"50%"},
            ),
            dcc.Graph(id="graph_chart_gaz_industrial"),
        ],style={"display":"block"}
        ),
    ],
    ),
    #fin GazIndustrial---------------------------------------------------------------------------------------------------------#

    html.Div(children=[
        html.H1(children='Évolution de la consommation totale d\'énergie (Gaz et Électricité)',style={"color":"#DC143C"}),
        html.Div(
            dash_table.DataTable(id="table_gaz_elec",data=df_gaz_elec.to_dict('records'),columns=[{"name": i, "id": i} for i in df_gaz_elec.columns]),
            style={"display":"none"},
        ),
        dcc.Interval(
            id='interval-component_gaz_elec',
            interval=60*1000, # in milliseconds
            n_intervals=0,
        ),
        dcc.Graph(id='graph_line_chart_gaz_elec'),

    ]),
    #fin Gaz_Elec---------------------------------------------------------------------------------------------------------#
    html.Div([
        html.H1("Consommation de Gaz pour différents types de clients en France",style={"color":"#DC143C"}),
        html.Div(
            dash_table.DataTable(id="table_elec_day",data=df_elec_day.to_dict('records'),columns=[{"name": i, "id": i} for i in df_elec_day.columns]),
            style={"display":"none"},
        ),
        dcc.Interval(
            id='interval-component_elec_day',
            interval=600*1000, # in milliseconds
            n_intervals=0,
        ),
        html.Div(children=[
            dcc.Dropdown(
                id='period-axis_chart_elec_day',
                options=["Année","Trimestre","Mois"],
                value="Mois",
                clearable=False,
                style={"width":"50%"},
            ),
            dcc.Graph(id="graph_chart_elec_day"),
        ],style={"display":"block"}
        ),
    ],
    ),
    #fin Elec_Day---------------------------------------------------------------------------------------------------------#
    html.Div([
        html.H1("Tableau de la Consommation d'électricité par métropole en France",style={"color":"#DC143C"}),
        dcc.Interval(
            id='interval-component_elec_met',
            interval=120*1000, # in milliseconds
            n_intervals=0,
        ),
        html.Div([
            dash_table.DataTable(
                id='table_elec_met',
                columns=[{"name": mapping_namcol_elec_met[i], "id": i}
                         for i in df_elec_met.columns],
                data=df_elec_met.to_dict('records'),
                style_cell=dict(textAlign='left'),
                style_header=dict(backgroundColor="paleturquoise"),
                style_data=dict(backgroundColor="lavender"),
                page_size=21,
            ),
        ])
    ],
    ),
    #fin Elec_Met---------------------------------------------------------------------------------------------------------#
],
)



@app.callback(
    Output("table_gaz","data"),
    Input("interval-component_gaz","n_intervals")
)
def update_table(n):
    return ProcessSQLGaz().get_sqlserver().to_dict(orient='records')#get SQL data from SQL Server
# Define the callback function for the area plot
@app.callback(
    Output("graph_line_gaz", "figure"),
    Input("hours-axis_line_gaz", "value"),
    Input("table_gaz","data"),
)
def display_graph_line(hour,df_json):
    df=pd.DataFrame.from_dict(df_json)
    # If the "Toutes horaires" option was selected, set the feature to "conso"
    if hour=="Toutes horaires":
        feature="conso"
    else:
        # Otherwise, set the feature to the selected hour
        feature=hour[:2]+"_00"
    # Aggregate the data by date and regions group
    df_agg = df.groupby(['date', 'region_groups'])[['conso']+[f"{g(i)}_00" for i in range(24)]].mean().reset_index()
    # Create the area plot
    fig = px.scatter(df_agg, x="date", y=feature, color="region_groups", \
                     color_discrete_map={0:"#9400D3",1:"#1E90FF",2:"#FFFFF0",3:"#FF4500"}, \
                     labels={feature:"Consommation à "+hour,"region_groups":"Groupe de régions"}) \
        .update_layout(
        title="Graphique représentant la consommation de Gaz (MWh) moyenne par groupe de régions et par date", \
        xaxis_title="Date",yaxis_title="Consommation de Gaz (MWh) moyenne")
    return fig

# Define the callback function for the bar chart
@app.callback(
    Output("graph_chart_gaz", "figure"),
    Input("hours-axis_chart_gaz", "value"),
    Input("period-axis_chart_gaz", "value"),
    Input("table_gaz","data"),
)
def display_graph_chart(hour,period,df_json):
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
    df_agg = df.groupby([period_conv, 'region_groups'])[['conso']+[f"{g(i)}_00" for i in range(24)]].mean().reset_index()
    # Create the bar chart
    fig = px.bar(df_agg, x=period_conv, y=feature, color="region_groups",barmode="group",
                 labels={
                     "region_groups":"Groupe de régions",
                 }) \
        .update_layout(
        title="Diagramme à barres de la consommation de Gaz (MWh) moyenne par groupe de régions/par horaire/par fréquence temporelle", \
        xaxis_title=conv_period_dict[period_conv],yaxis_title="Consommation de Gaz (MWh) moyenne")
    if period != "Année":
        fig.update_xaxes(tickvals=conv_fr[period][0], ticktext=conv_fr[period][1])

    return fig

# Define the callback function for the histogram
@app.callback(
    Output("graph_hist_gaz", "figure"),
    Input("hours-axis_hist_gaz", "value"),
    Input("table_gaz","data"),
)
def display_graph_hist(hour,df_json):
    df=pd.DataFrame.from_dict(df_json)
    # If the "Toutes horaires" option was selected, set the feature to "conso"
    if hour=="Toutes horaires":
        feature="conso"
    else:
        # Otherwise, set the feature to the selected hour
        feature=hour[:2]+"_00"
    # Create the histogram
    try:
        fig = px.histogram(df,x=feature).update_layout(
            title="Histogramme de la consommation de Gaz (MWh) par horaire", xaxis_title="Consommation de Gaz (en MWh)",yaxis_title="Effectifs")
    except ValueError:
        fig = px.histogram(df,x=feature).update_layout(
            title="Histogramme de la consommation de Gaz (MWh) par horaire", xaxis_title="Consommation de Gaz (en MWh)",yaxis_title="Effectifs")
    return fig
#fin Gaz---------------------------------------------------------------------------------------------------------#


@app.callback(
    Output("table_gaz_elec","data"),
    Input("interval-component_gaz_elec","n_intervals")
)
def update_table(n):
    return ProcessSQLGazElec().get_sqlserver().to_dict(orient='records')#get SQL data from SQL Server

@app.callback(
    Output("graph_line_chart_gaz_elec", "figure"),
    Input("table_gaz_elec","data"),
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

#fin GazElec---------------------------------------------------------------------------------------------------------#

@app.callback(
    Output("table_gaz_industrial","data"),
    Input("interval-component_gaz_industrial","n_intervals")
)
def update_table(n):
    return ProcessSQLGazIndustriel().get_sqlserver().to_dict(orient='records')#get SQL data from SQL Server
# Define the callback function for the area plot
@app.callback(
    Output("graph_line_gaz_industrial", "figure"),
    Input("hours-axis_line_gaz_industrial", "value"),
    Input("table_gaz_industrial","data")
)
def display_graph_line(hour,df_json):
    # If the "Toutes horaires" option was selected, set the feature to "conso"
    df=pd.DataFrame.from_dict(df_json)
    if hour=="Toutes horaires":
        feature="conso"
    else:
        # Otherwise, set the feature to the selected hour
        feature=hour[:2]+"_00"
    # Aggregate the data by date and regions group
    df_agg = df.groupby(["date","operateur"])[['conso']+[f"{g(i)}_00" for i in range(24)]].mean().reset_index()
    # Create the area plot
    fig = px.scatter(df_agg, x="date", y=feature, color="operateur", \
                     labels={feature:"Consommation à "+hour,"operateur":"Opérateurs"}) \
        .update_layout(
        title="Graphique représentant la consommation de Gaz pour les clients industriels (MWh) moyenne par date et par opérateur", \
        xaxis_title="Date",yaxis_title="Consommation de Gaz (MWh) moyenne")
    return fig

# Define the callback function for the bar chart
@app.callback(
    Output("graph_chart_gaz_industrial", "figure"),
    Input("hours-axis_chart_gaz_industrial", "value"),
    Input("period-axis_chart_gaz_industrial", "value"),
    Input("table_gaz_industrial","data"),
)
def display_graph_chart(hour,period,df_json):
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
    if period != "Année":
        fig.update_xaxes(tickvals=conv_fr[period][0], ticktext=conv_fr[period][1])
    return fig
#fin GazIndustrial---------------------------------------------------------------------------------------------------------#

@app.callback(
    Output("graph_chart_elec_day", "figure"),
    Input("period-axis_chart_elec_day", "value"),
    Input("table_elec_day","data"),
)
def display_graph_chart(period,df_json):
    df=pd.DataFrame.from_dict(df_json)
    # Convert the period to the corresponding column and labels in French
    conv_fr={"Trimestre":(list(range(1,5)),quarters_fr),"Mois":(list(range(1,13)),months_fr)}
    period_conv={"Année":"year","Trimestre":"quarter","Mois":"month"}[period]
    conv_period_dict={value:key for key,value in {"Année":"year","Trimestre":"quarter","Mois":"month"}.items()}
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
    if period != "Année":
        fig.update_xaxes(tickvals=conv_fr[period][0], ticktext=conv_fr[period][1])
    return fig

#fin Elec_Day---------------------------------------------------------------------------------------------------------#
@app.callback(
    Output("table_elec_met","data"),
    Input("interval-component_elec_met","n_intervals")
)

def update_table(n):
    return ProcessSQLElecMet().get_sqlserver().to_dict(orient='records')#get SQL data from SQL Server

#fin Elec_Met---------------------------------------------------------------------------------------------------------#

app.run_server(debug=False,host="0.0.0.0",port=8051)

