import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import requests
import json
# Define a list of French month names
months_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
# Define a list of French quarter names
quarters_fr = ["1er trimestre", "2ème trimestre", "3ème trimestre", "4ème trimestre"]

#Pre-processing
def g(i):
    if -1<i and i<10:
        return "0"+str(i)
    return str(i)

# Set the number of rows to retrieve from the API (limit:10000 rows)
rows=10000
# Make a request to the API and store the response in r
r=requests.get(f"https://odre.opendatasoft.com/api/records/1.0/search/?dataset=courbe-de-charge-eldgrd-regional-grtgaz-terega&q=&rows={rows}&sort=date&facet=date&facet=operateur&facet=region")
# Parse the response as a JSON object
data_json=json.loads(r.text)
# Extract the records from the JSON object
records=data_json["records"]
dict_rec=records[0]
features=list(dict_rec["fields"].keys())
# Construct a list of dictionaries, each containing the feature-value pairs for a record
records=[{feature:value for feature,value in \
          zip(features,list(dict_rec["fields"].values()))} for dict_rec in records]
records={i:dict_i for i,dict_i in enumerate(records)}
# Convert the list of dictionaries to a pandas DataFrame
df=pd.read_json(json.dumps(records),orient="index")
# Drop the mois column and select certain columns
df=df.drop("mois",axis=1)
columns=["date","code_insee_region","region","secteur_d_activite","operateur","conso_journaliere_mwh_pcs_0degc"]+ \
        ["00_00_00"]+["0"+str(i+1)+"_00" for i in range(4)]+["05_00_00","06_00_00"]+ ["0"+str(i+1)+"_00" for i in range(6,9)]+["10_00"]+ \
        ["11_00_00","12_00_00"]+[str(i+1)+"_00" for i in range(12,18)]+["19_00_00"]+[str(i+1)+"_00" for i in range(19,23)]
df=df[columns]
df.columns=[col[:5] for col in df.columns]
# Rename some of the columns
df=df.rename(columns={"regio":"region","opera":"operateur","code_":"code",})
# Define a mapping from regions to region groups
groups_region={"Île-de-France":0,"Grand Est":0,"Hauts-de-France":0,"Bourgogne-Franche-Comté":1,"Auvergne-Rhône-Alpes":1, \
               "Provence-Alpes-Côte d'Azur":1,"Occitanie":2,"Nouvelle-Aquitaine":2,"Centre-Val de Loire":2, \
               "Normandie":3,"Bretagne":3,"Pays de la Loire":3}
map_groups={0:"Nord-est",1:"Sud-est",2:"Sud-ouest",3:"Nord-ouest"}
# Add a column with the region group label
df["region_groups"]=[map_groups[groups_region[region]] for region in df["region"]]
df["02_00"]=df[["01_00","03_00"]].mean(axis=1) #inconsistent data for 2 am

# Add new columns with the month, day, quarter, and year
df["month"]=df["date"].dt.month
df["day"]=df["date"].dt.day
df["quarter"]=df["date"].dt.quarter
df["year"]=df["date"].dt.year
# Rearrange the columns
df=df[list(df.columns[:1])+["region_groups"]+list(df.columns[-1:-5:-1])+list(df.columns[1:30])]



#DataViz

# Initialize the Dash app
app = Dash(__name__)
# Define the layout of the app
app.layout = html.Div([
    html.H1("Consommation de Gaz en France",style={"color":"#DC143C"}),
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
        dcc.Dropdown(
            id='hours-axis_chart',
            options=["Toutes horaires"]+[g(i)+"h00" for i in range(24)],
            value="Toutes horaires",
            clearable=False,
            style={"width":"50%"},
        ),
        dcc.Dropdown(
            id='period-axis_chart',
            options=["Année","Trimestre","Mois"],
            value="Mois",
            clearable=False,
            style={"width":"50%"},
        ),
        dcc.Graph(id="graph_chart"),
    ],style={"display":"block"}
    ),
    html.Div(children=[
        dcc.Dropdown(
            id='hours-axis_hist',
            options=["Toutes horaires"]+[g(i)+"h00" for i in range(24)],
            value="Toutes horaires",
            clearable=False,
            style={"width":"50%"},
        ),
        dcc.Graph(id="graph_hist"),
    ],style={"display":"block"},
    ),
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
    df_agg = df.groupby(['date', 'region_groups'])[['conso']+[f"{g(i)}_00" for i in range(24)]].mean().reset_index()
    # Create the area plot
    fig = px.area(df_agg, x="date", y=feature, color="region_groups", line_group="region_groups",\
        color_discrete_map={0:"#9400D3",1:"#1E90FF",2:"#FFFFF0",3:"#FF4500"},\
        labels={feature:"Consommation à "+hour,"region_groups":"Groupe de régions"})\
    .update_layout(
        title="Graphique représentant la consommation de Gaz (MWh) moyenne par groupe de régions et par date", \
        xaxis_title="Date",yaxis_title="Consommation de Gaz (MWh) moyenne")
    return fig

# Define the callback function for the bar chart
@app.callback(
    Output("graph_chart", "figure"),
    Input("hours-axis_chart", "value"),
    Input("period-axis_chart", "value"),)
def display_graph_chart(hour,period):
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
    })\
    .update_layout(
    title="Diagramme à barres de la consommation de Gaz (MWh) moyenne par groupe de régions/par horaire/par fréquence temporelle",\
        xaxis_title=conv_period_dict[period_conv],yaxis_title="Consommation de Gaz (MWh) moyenne")
    if period != "Année":
        fig.update_xaxes(tickvals=conv_fr[period][0], ticktext=conv_fr[period][1])

    return fig

# Define the callback function for the histogram
@app.callback(
    Output("graph_hist", "figure"),
    Input("hours-axis_hist", "value"))
def display_graph_hist(hour):
    # If the "Toutes horaires" option was selected, set the feature to "conso"
    if hour=="Toutes horaires":
        feature="conso"
    else:
        # Otherwise, set the feature to the selected hour
        feature=hour[:2]+"_00"

    # Create the histogram
    fig = px.histogram(df,x=feature).update_layout(
    title="Histogramme de la consommation de Gaz (MWh) par horaire", xaxis_title="Consommation de Gaz (en MWh)",yaxis_title="Effectifs")
    return fig

# Run the app
app.run_server(debug=True)