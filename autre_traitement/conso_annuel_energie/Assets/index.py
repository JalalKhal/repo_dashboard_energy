import dash
from dash import html
from dash import dcc
import pandas as pd


def get_total_consumption(year):
    """
    Fonction qui calcule la consommation totale d'énergie pour chaque année
    :param year:
    :return:
    """
    return df[df['Année'] == year]['Consommation totale (MWh)'].sum()


# lecture des données et stockage sous forme de dataframe
df = pd.read_csv('../Data/conso-elec-gaz-annuelle-par-secteur-dactivite-agregee-region.csv', sep=';')

# récupération des modalités de la variable année (unique)
years = df['Année'].unique()

# Calculer la conso. pour chaque année
consumption_values = [get_total_consumption(year) for year in years]

# ####### CREATION DU DASHBOARD #########
app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Évolution de la consommation totale d\'énergie'),

    dcc.Graph(
        id='consumption-graph',
        figure={
            'data': [
                {'x': years, 'y': consumption_values, 'type': 'line', 'name': 'Consommation totale'},
            ],
            'layout': {
                'title': 'Consommation totale d\'énergie par année'
            }
        }
    )
])
# ####### fin DU DASHBOARD #########

if __name__ == '__main__':
    app.run_server(debug=True)
