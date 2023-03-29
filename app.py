# sélection de la période à analyser
    # sélection d'année par plage
    # sélection d'un mois en particulier OU pas de sélection pour avoir toute l'année
    #==> sélection date par plage
# Dashboard
    # graphe des soldes mensuels
    # graphe des bénéfices mensuels moyens
    # Dataframe des dépenses/recettes trié dans l'ordre de montant avec sunburst
    # Ratio dépense/recette Clément ou Caro

# A AJOUTER
    # DROPDOWN POUR SELECT PERIOD (mois en cours, annee en cours, etc)




from dash import Dash, dcc, html, dash_table
from dash.dependencies import Output, State, Input
from datetime import date, datetime, timedelta
import pandas as pd
import time
import plotly.express as px
from functions import initialisation, trace_solde, trace_solde_moy, detail_depense, detail_revenu, calcul_equilibre, trace_evo_dep

app = Dash(__name__)






##### VALEUR D'INITIALISATION

### Couleur
colors = {
    'background': '#ced2cc',
    'text': '#000000'
}

### Date
global date_min_global
global date_max_global

date_min_global = date(date.today().year, 1, 1)
date_max_global = date.today()

global date_min_prec
global date_max_prec

date_min_prec = date_min_global
date_max_prec = date_max_global


### Import data
global df_global
global nom_dossier

nom_dossier = "G:\\Mon Drive\\Info fun\\Compta - pipenv\\Extract_for_python\\test_2019\\"
df_global = initialisation(nom_dossier)



### Graphe
df = px.data.iris()  # iris is a pandas DataFrame
global fig_init
fig_init = px.scatter(df, x="sepal_width", y="sepal_length")
fig_init.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    font_size=25,
    font_family='Calibri'
)



fig_solde_mensuel = fig_init
fig_solde_moy = fig_init
fig_sunburst = fig_init



app.layout = html.Div(
    id='whole_page',
    children=[
        html.Div(
            id="line_1",
            children = [
                html.Div(
                    id="date_min_1",
                    children=[
                        dcc.DatePickerSingle(
                            id="date_min_2",
                            month_format="DD/MM/YYYY",
                            placeholder="DD/MM/YYYY",
                            display_format="DD/MM/YYYY",
                            date=date_min_global
                        ),
                    ],
                    style={
                        'width':'10%',
                    }
                ),
                html.Div(
                    id="date_max_1",
                    children=[
                        dcc.DatePickerSingle(
                            id="date_max_2",
                            month_format="DD/MM/YYYY",
                            placeholder="DD/MM/YYYY",
                            display_format="DD/MM/YYYY",
                            date=date_max_global
                        )
                    ],
                    style={
                        'width':'10%',
                    }
                ),
                html.Div(
                    id="periode_1",
                    children=[
                        dcc.Dropdown(
                            id="periode_2",
                            options=["Mois en cours", "Mois précédent", "Mois flottant", "Année en cours", "Année précédente", "Année flottante"],
                            value=None,
                            clearable=True
                        )
                    ],
                    style={
                        'width':'20%',
                        'textAlign':'left'
                    }
                ),
                html.Div(
                    id="qui_1",
                    children=[
                        dcc.Dropdown(
                            id="qui_2",
                            options=["Tous", "Clément", "Carolane"],
                            value="Tous",
                            clearable=False
                        )
                    ],
                    style={
                        'width':'20%',
                        'textAlign':'left'
                    }
                ),
                html.Div(
                    id="nb_mois_1",
                    children=[
                        dcc.Slider(
                            id="nb_mois_2",
                            min=1,
                            max=12,
                            step=1,
                            value=3,
                            updatemode="drag"
                        )
                    ],
                    style={
                        'width':'30%'
                    }
                ),
                # html.Div(
                #     id="categorie_1",
                #     children=[
                #         dcc.RadioItems(
                #             id="categorie_2",
                #             options=["Dépense", "Recette"],
                #             value="Dépense",
                #             labelStyle={'display': 'block'}
                #         )
                #     ],
                #     style={
                #         'width':'10%',
                #         'textAlign':'left'
                #     }
                # )
            ],
            style={
                'display':'flex',
                'textAlign':'center',
                'height':'6.67%',
                'width':'98%',
                'padding-left':'2%',
                'padding-top':'1.33%'
            }
        ),
        html.Div(
            id='line_2',
            children=[
                dcc.Graph(
                    id='line_2_col_1',
                    # children='Soldes mensuels',
                    figure=fig_solde_mensuel,
                    style={
                        'display':'inline-block',
                        'height':'100%',
                        'width':'50%'
                    }
                ),
                dcc.Graph(
                    id='line_2_col_2',
                    # children='Bénéfices mensuels',
                    figure=fig_solde_moy,
                    style={
                        'display':'inline-block',
                        'height':'100%',
                        'width':'50%'
                    }
                )
            ],
            style={
                'height':'42%',
                'width':'100%'
            }
        ),
        html.Div(
            id='line_3',
            children=[
                dcc.Graph(
                    id='line_3_col_1',
                    figure=fig_sunburst,
                    # children='Sunburst Dépense',
                    style={
                        'height':'100%',
                        'width':'20%'
                    }
                ),
                dcc.Graph(
                    id='line_3_col_2',
                    # children='Sunburst Recette',
                    style={
                        'height':'100%',
                        'width':'20%'
                    }
                ),
                html.Div(
                    id='line_3_col_3_4',
                    children=[
                        dcc.Graph(
                            id='line_3_col_3_4_1',
                            # children='Sunburst Recette',
                            style={
                                'height':'100%', #80%
                                'width':'100%'
                            }
                        ),
                        # html.Div(
                        #     id='line_3_col_3_4_2',
                        #     children="A COMPLETER",
                        #     style={
                        #         'height':'20%',
                        #         'padding-top':'5%'
                        #     }
                        # ),
                    ],
                    style={
                        'height':'100%',
                        'width':'45%',
                        'font-size':'150%',
                        'text-align':'center'
                    }
                ),
                html.Div(
                    id='line_3_col_3',
                    children=[
                        html.Div(
                            id='line_3_col_3_1',
                            children="Equilibre",
                            style={
                                'height':'10%',
                                'padding-top':'25%'
                            }
                        )
                    ],
                    style={
                        'height':'100%',
                        'width':'15%',
                        'font-size':'200%',
                        'text-align':'center',
                        'padding-top':'5%'
                    }
                )
            ],
            style={
                'display':'flex',
                'height':'50%',
                'width':'100%'
            }
        )
    ],
    style={
        'height':'100vh',
        'width':'100vw'
    }
)



##### Callback
@app.callback(
    [
        Output("line_2_col_1", "figure"),
        Output("line_2_col_2", "figure"),
        Output("line_3_col_1", "figure"),
        Output("line_3_col_2", "figure"),
        Output("line_3_col_3_1", "children"),
        Output("line_3_col_3_4_1", "figure"),
    ],
    [
        Input("date_min_2", "date"),
        Input("date_max_2", "date"),
        Input("qui_2", "value"),
        Input("nb_mois_2", "value"),
        Input("periode_2", "value")
    ]
)
def update_graph(date_min, date_max, qui, nb_mois, periode):
    
    global df_global
    df_global = initialisation(nom_dossier)


    global date_min_prec
    global date_max_prec

    try:
        date_min = datetime.strptime(date_min, "%Y-%m-%d")
        date_max = datetime.strptime(date_max, "%Y-%m-%d")

        date_min_prec = date_min
        date_max_prec = date_max

    except:
        date_min = date_min_prec
        date_max = date_max_prec


    if periode != None:
        if periode == "Mois en cours":
            annee = date.today().year
            mois = date.today().month
            
            date_min = datetime(annee, mois, 1)

            next_month = date_min.replace(day=28) + timedelta(days=4)

            date_max = next_month - timedelta(next_month.day)
            date_max = datetime.combine(date_max, datetime.min.time())

        elif periode == "Mois précédent":
            annee = date.today().year
            mois = date.today().month - 1

            if mois == 0:
                annee -= 1
                mois =12

            date_min = datetime(annee, mois, 1)

            next_month = date_min.replace(day=28) + timedelta(days=4)

            date_max = next_month - timedelta(next_month.day)
            date_max = datetime.combine(date_max, datetime.min.time())

        elif periode == "Mois flottant":
            date_max = datetime.today()
            date_min = date_max - timedelta(days = 30)

        elif periode == "Année en cours":
            annee = date.today().year

            date_min = datetime(annee, 1, 1)
            date_max = datetime(annee, 12, 31)

        elif periode == "Année précédente":
            annee = date.today().year

            date_min = datetime(annee-1, 1, 1)
            date_max = datetime(annee-1, 12, 31)

        elif periode == "Année flottante":
            date_max = datetime.today()
            date_min = date_max - timedelta(days = 365)

    if qui == "Tous":
        liste_qui = ["Clement", "Carolane"]
        compte_virement = False
    elif qui == "Clément":
        liste_qui = ["Clement"]
        compte_virement = True
    elif qui == "Carolane":
        liste_qui = ["Carolane"]
        compte_virement = True


    
    result_temp = detail_depense(df_global, date_min, date_max, liste_qui, False)
    fig_sunburst_dep = result_temp[0]
    
    result_temp = detail_revenu(df_global, date_min, date_max, liste_qui, False)
    fig_sunburst_rec = result_temp[0]

    fig_solde = trace_solde(df_global, date_min, date_max, liste_qui, compte_virement)

    fig_solde_moy = trace_solde_moy(df_global, date_min, date_max, liste_qui, compte_virement, nb_mois)

    fig_evo_dep = trace_evo_dep(df_global, date_min, date_max, liste_qui, False)


    fig_solde.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        font_size=25,
        font_family='Calibri'
    )
    fig_solde_moy.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        font_size=25,
        font_family='Calibri'
    )
    fig_sunburst_dep.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        font_size=25,
        font_family='Calibri'
    )
    fig_sunburst_rec.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        font_size=25,
        font_family='Calibri'
    )
    fig_evo_dep.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        font_size=25,
        font_family='Calibri'
    )



    valeur = round(calcul_equilibre(df_global, date_min, date_max, 'Clement', 'Carolane'), 2)

    if valeur > 0:
        string_to_print_1 = f"Clément doit {valeur}€ à Carolane du {date_min.date()} au {date_max.date()}."
    elif valeur < 0:
        string_to_print_1 = f"Carolane doit {-valeur}€ à Clément du {date_min.date()} au {date_max.date()}."
    elif valeur == 0:
        string_to_print_1 = f"Equilibre du {date_min.date()} au {date_max.date()}."
    else:
        string_to_print_1 = f"Error"

    return [
        fig_solde,
        fig_solde_moy,
        fig_sunburst_dep,
        fig_sunburst_rec,
        string_to_print_1,
        fig_evo_dep
    ]












##### LANCE LE SERVEUR
if __name__ == '__main__':
    app.run_server(
        debug=True,
        port=4050)

### http://127.0.0.1:4050/