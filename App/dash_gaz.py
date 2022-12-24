import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

def g(i):
    if -1<i and i<10:
        return "0"+str(i)
    return str(i)

df=pd.read_csv("./data_gaz.csv")
df=df.rename(columns={"regio":"region","opera":"operateur","code_":"code",})
df.head(50)
groups_region={"Île-de-France":0,"Grand Est":0,"Hauts-de-France":0,"Bourgogne-Franche-Comté":1,"Auvergne-Rhône-Alpes":1, \
               "Provence-Alpes-Côte d'Azur":1,"Occitanie":2,"Nouvelle-Aquitaine":2,"Centre-Val de Loire":2, \
               "Normandie":3,"Bretagne":3,"Pays de la Loire":3}
map_groups={0:"Nord-est",1:"Sud-est",2:"Sud-ouest",3:"Nord-ouest"}
df["region_groups"]=[map_groups[groups_region[region]] for region in df["region"]]
df["02_00"]=df[["01_00","03_00"]].mean(axis=1) #données incohérentes à 2 heure du matin



app = Dash(__name__)

app.layout = html.Div([
    html.H1("Consommation de Gaz en France",style={"color":"#DC143C"}),
    html.P("Selectionnez l'horaire de consommation:"),
    dcc.Dropdown(
        id='period-axis',
        options=["Toutes horaires"]+[g(i)+"h00" for i in range(24)],
        value="Toutes horaires"
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"),
    Input("period-axis", "value"))
def display_area(hour):
    if hour=="Toutes horaires":
        feature="conso"
    else:
        feature=hour[:2]+"_00"
    fig = px.area(df, x="date", y=feature, color="region_groups", line_group="region_groups",\
                  color_discrete_map={0:"#9400D3",1:"#1E90FF",2:"#FFFFF0",3:"#FF4500"},labels={feature:"Consommation à "+hour})
    return fig


app.run_server(debug=True)