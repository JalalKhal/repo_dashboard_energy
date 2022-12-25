import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import requests
import json

#Pre-processing
def g(i):
    if -1<i and i<10:
        return "0"+str(i)
    return str(i)
rows=10000
r=requests.get(f"https://odre.opendatasoft.com/api/records/1.0/search/?dataset=courbe-de-charge-eldgrd-regional-grtgaz-terega&q=&rows={rows}&sort=date&facet=date&facet=operateur&facet=region")
data_json=json.loads(r.text)
records=data_json["records"]
dict_rec=records[0]
features=list(dict_rec["fields"].keys())
records=[{feature:value for feature,value in \
          zip(features,list(dict_rec["fields"].values()))} for dict_rec in records]
records={i:dict_i for i,dict_i in enumerate(records)}
df=pd.read_json(json.dumps(records),orient="index")
df=df.drop("mois",axis=1)
columns=["date","code_insee_region","region","secteur_d_activite","operateur","conso_journaliere_mwh_pcs_0degc"]+ \
        ["00_00_00"]+["0"+str(i+1)+"_00" for i in range(4)]+["05_00_00","06_00_00"]+ ["0"+str(i+1)+"_00" for i in range(6,9)]+["10_00"]+ \
        ["11_00_00","12_00_00"]+[str(i+1)+"_00" for i in range(12,18)]+["19_00_00"]+[str(i+1)+"_00" for i in range(19,23)]
df=df[columns]
df.columns=[col[:5] for col in df.columns]
df=df.rename(columns={"regio":"region","opera":"operateur","code_":"code",})
groups_region={"Île-de-France":0,"Grand Est":0,"Hauts-de-France":0,"Bourgogne-Franche-Comté":1,"Auvergne-Rhône-Alpes":1, \
               "Provence-Alpes-Côte d'Azur":1,"Occitanie":2,"Nouvelle-Aquitaine":2,"Centre-Val de Loire":2, \
               "Normandie":3,"Bretagne":3,"Pays de la Loire":3}
map_groups={0:"Nord-est",1:"Sud-est",2:"Sud-ouest",3:"Nord-ouest"}
df["region_groups"]=[map_groups[groups_region[region]] for region in df["region"]]
df["02_00"]=df[["01_00","03_00"]].mean(axis=1) #données incohérentes à 2 heure du matin
df["month"]=df["date"].dt.month_name()
df["day"]=df["date"].dt.day_name()
df["quarter"]=df["date"].dt.quarter
df["year"]=df["date"].dt.year
df=df[list(df.columns[:1])+["region_groups"]+list(df.columns[-1:-5:-1])+list(df.columns[1:30])]



#DataViz
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Consommation de Gaz en France",style={"color":"#DC143C"}),
    html.P("Selectionnez l'horaire de consommation:"),
    html.Div(children=[
    dcc.Dropdown(
        id='hours-axis_line',
        options=["Toutes horaires"]+[g(i)+"h00" for i in range(24)],
        value="Toutes horaires",
        clearable=False,
    ),
    dcc.Graph(id="graph_line"),
    ],style={"width":"100%"},
    ),
    html.Div(children=[
        dcc.Dropdown(
            id='hours-axis_chart',
            options=["Toutes horaires"]+[g(i)+"h00" for i in range(24)],
            value="Toutes horaires",
            clearable=False,
        ),
        dcc.Dropdown(
            id='period-axis_chart',
            options=["Année","Trimestre","Mois"],
            value="Mois",
            clearable=False,
        ),
        dcc.Graph(id="graph_chart"),
    ],style={"width":"50%"},
    ),


])

@app.callback(
    Output("graph_line", "figure"),
    Input("hours-axis_line", "value"))
def display_graph_line(hour):
    if hour=="Toutes horaires":
        feature="conso"
    else:
        feature=hour[:2]+"_00"
    df_agg = df.groupby(['date', 'region_groups'])[['conso']+[f"{g(i)}_00" for i in range(24)]].mean().reset_index()
    fig = px.area(df_agg, x="date", y=feature, color="region_groups", line_group="region_groups",\
                  color_discrete_map={0:"#9400D3",1:"#1E90FF",2:"#FFFFF0",3:"#FF4500"},labels={feature:"Consommation à "+hour})
    return fig

@app.callback(
    Output("graph_chart", "figure"),
    Input("hours-axis_chart", "value"),
    Input("period-axis_chart", "value"),)
def display_graph_chart(hour,period):
    period_conv={"Année":"year","Trimestre":"quarter","Mois":"month"}[period]
    if hour=="Toutes horaires":
        feature="conso"
    else:
        feature=hour[:2]+"_00"
    df_agg = df.groupby([period_conv, 'region_groups'])[['conso']+[f"{g(i)}_00" for i in range(24)]].mean().reset_index()
    fig = px.bar(df_agg, x=period_conv, y=feature, color="region_groups",barmode="group")
    return fig


app.run_server(debug=True)