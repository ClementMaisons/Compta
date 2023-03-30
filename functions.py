from typing import Type
import pandas as pd
from datetime import datetime, timedelta
import datetime as dt
import plotly.graph_objects as go
import os
import plotly.express as px



##### VALEUR INITIALISATION
# Solde_initial_total = 8048.07
# Solde_initial_Clement = 7829.53
# Solde_initial_Caro = 218.54

SOLDE_INITIAL = {
    "Tous":8048.07,
    "Clement":7829.53,
    "Carolane":218.54
}

# Annee_dep = 2019
# dossier = "G:\\Mon Drive\\Info fun\\Projet\\Compta\\Extract_for_python\\"





##### FONCTIONS
### Import des dataframe
def initialisation(nom_dossier):
    
    for filename in os.scandir(nom_dossier):
        if filename.is_file():
            date_extract, personne_temp = filename.name.split('_')
            personne = personne_temp.split(".")[0]

            df_temp = pd.read_excel(
                nom_dossier + filename.name,
                header=2
            )
            df_temp.dropna(inplace=True, subset=["Date"])

            if personne == 'Carolane':
                df_temp["Qui"] = "Carolane"
            elif personne == 'Clement':
                df_temp["Qui"] = "Clement"
            else: #gère les fichiers mal renommés
                return f'Les fichiers doivent être renommés "année_Personne.xlsx" pas {filename.name}'

            try:
                df_total = pd.concat([df_total, df_temp], ignore_index=True)
            except UnboundLocalError: #si le dataframe global n'existe pas on le crée
                df_total = df_temp

    df_temp = df_total["Catégorie"].str.split(pat=" > ", expand=True)

    df_total["Catégorie_ppal"] = df_temp[0]
    df_total["Catégorie_sec"] = df_temp.loc[:,1:len(df_temp.columns)]
    df_total["Crédit"] = pd.to_numeric(df_total["Crédit"])

    return df_total

# df_global = initialisation(dossier)
# print(df_global)





### filtre le dataframe selon critères
def filtre_df(df, date_from, date_to, liste_qui, compte_virement):    
    df_temp = df[
        (df["Qui"].isin(liste_qui))
    ]

    if not compte_virement:
        df_temp = df_temp[
            (df_temp["Mode de paiement"]!="Virement interne")
        ]


    df_temp = df_temp[
        (df_temp["Date"] <= date_to) &
        (df_temp["Date"] >= date_from)
    ]


    
    # print(df_temp)
    

    return df_temp





##### DASHBOARD #####
def trace_solde(df_total, date_from, date_to, liste_qui, compte_virement): # compte_virement = True si une seule personne
    
    df_temp = df_total[
        (df_total["Qui"].isin(liste_qui))
    ]

    if not compte_virement:
        df_temp = df_temp[
            (df_temp["Mode de paiement"]!="Virement interne")
        ]

    df_tot_month = df_temp.groupby(pd.Grouper(key="Date",freq="1M")).sum().reset_index()

    df_tot_month["Solde"] = df_tot_month["Crédit"] - df_tot_month["Débit"]

    if "Clement" in liste_qui and "Carolane" in liste_qui:
        df_tot_month["Solde_tot"] = df_tot_month["Solde"].cumsum() + SOLDE_INITIAL["Tous"]
    elif "Clement" in liste_qui and "Carolane" not in liste_qui:
        df_tot_month["Solde_tot"] = df_tot_month["Solde"].cumsum() + SOLDE_INITIAL["Clement"]
    elif "Clement" not in liste_qui and "Carolane" in liste_qui:
        df_tot_month["Solde_tot"] = df_tot_month["Solde"].cumsum() + SOLDE_INITIAL["Carolane"]


    
    df_tot_month["Date"] = df_tot_month["Date"].apply(lambda x: x - timedelta(days=x.day - 1))

    df_tot_month = df_tot_month[
        (df_tot_month["Date"] >= date_from) &
        (df_tot_month["Date"] <= date_to)
    ]


    fig = go.Figure(data=[
        go.Bar(
            name='Débit',
            x=df_tot_month["Date"],
            y=df_tot_month["Débit"],
            marker_color='red'
        ),
        go.Bar(
            name='Crédit',
            x=df_tot_month["Date"],
            y=df_tot_month["Crédit"],
            marker_color='green'
        ),
        go.Bar(
            name='Solde',
            x=df_tot_month["Date"],
            y=df_tot_month["Solde"],
            marker_color='orange'
        ),
        go.Scatter(
            name='Solde comptes',
            x=df_tot_month["Date"],
            y=df_tot_month["Solde_tot"],
            marker_color='blue'
        )
    ])


    fig.update_layout(
        title=f"Soldes Mensuels du {date_from.date()} au {date_to.date()}",
        xaxis_title=None,
        yaxis_title="Montant",
        legend_title="Types de soldes",
        barmode='group'
    )



    # fig.show()
    return fig

# trace_solde(df_global, datetime(2022,1,1), datetime(2022,12,31), ['Clement'], True)





### Solde moyen mensuel avec moyenne
def trace_solde_moy(df_total, date_from, date_to, liste_qui, compte_virement, nb_mois):  # compte_virement = True si une seule personne
    df_temp = filtre_df(df_total, date_from, date_to, liste_qui, compte_virement)

    df_tot_month = df_temp.groupby(pd.Grouper(key="Date", freq="1M")).sum().reset_index()
    df_tot_month["Solde"] = df_tot_month["Crédit"] - df_tot_month["Débit"]
    
    if "Clement" in liste_qui and "Carolane" in liste_qui:
        df_tot_month["Solde_tot"] = df_tot_month["Solde"].cumsum() + SOLDE_INITIAL["Tous"]
    elif "Clement" in liste_qui and "Carolane" not in liste_qui:
        df_tot_month["Solde_tot"] = df_tot_month["Solde"].cumsum() + SOLDE_INITIAL["Clement"]
    elif "Clement" not in liste_qui and "Carolane" in liste_qui:
        df_tot_month["Solde_tot"] = df_tot_month["Solde"].cumsum() + SOLDE_INITIAL["Carolane"]

    df_tot_month['Solde moyen'] = df_tot_month['Solde'].rolling(nb_mois).mean()

    df_tot_month["Date"] = df_tot_month["Date"].apply(lambda x: x - timedelta(days=x.day - 1))


    fig = go.Figure(data=[
        go.Bar(
            name='Solde',
            x=df_tot_month["Date"],
            y=df_tot_month["Solde"],
            marker_color='orange'
        ),
        go.Scatter(
            name=f'Solde moyen {nb_mois} mois',
            x=df_tot_month["Date"],
            y=df_tot_month["Solde moyen"],
            marker_color='blue'
        ),
        go.Scatter(
            name='Solde moyen',
            x=df_tot_month["Date"],
            y=[df_tot_month["Solde"].mean()]*len(df_tot_month["Date"]),
            mode='lines',
            line=dict(
                color='black',
                dash='dash',
                width=1
            )
        )
    ])

    fig.update_layout(
        title=f"Solde Mensuel du {date_from.date()} au {date_to.date()}",
        xaxis_title=None,
        yaxis_title="Montant",
        legend_title="Types de soldes",
        barmode='group'
    )

    # fig.show()
    return fig

# trace_solde_moy(df_global, datetime(2021,1,1), datetime(2022,12,31), ['Clement', 'Carolane'], False, 3)





### Tracer proportion des depenses
def detail_depense(df_total, date_from, date_to, liste_qui, compte_virement): # compte_virement toujours False
    df_temp = filtre_df(df_total, date_from, date_to, liste_qui, compte_virement)

    df_depense_cat = df_temp[
        ~(df_temp["Débit"].isna())
    ]

    df_depense_cat["Catégorie_ppal"] = df_depense_cat["Catégorie_ppal"].str.split(" - ").str[1]
    df_depense_cat["Catégorie_sec"] = df_depense_cat["Catégorie_sec"].str.split(" - ").str[1]

    fig = px.sunburst(
        df_depense_cat,
        path=['Catégorie_ppal', 'Catégorie_sec'],
        values='Débit'
    )

    fig.update_traces(textinfo="label+percent parent")

    # fig.show()

    # On crée le dataframe à afficher
    df_temp = df_depense_cat.groupby(
        by=["Catégorie_ppal"]
    ).sum().sort_values(
        by=["Débit"],
        ascending=False
    )

    df_temp = df_temp[["Débit"]]
    df_temp["Percent"] = round(
        df_temp["Débit"]/df_temp["Débit"].sum() * 100, 1
    )

    return fig, df_temp

# detail_depense(df_global, datetime(2022,1,1), datetime(2022,11,5), ['Clement', 'Carolane'], False)





### Tracer proportion des revenus
def detail_revenu(df_total, date_from, date_to, liste_qui, compte_virement): # compte_virement toujours False
    df_temp = filtre_df(df_total, date_from, date_to, liste_qui, compte_virement)

    df_revenu_cat = df_temp[
        ~(df_temp["Crédit"].isna())
    ]

    df_revenu_cat["Catégorie_ppal"] = df_revenu_cat["Catégorie_ppal"].str.split(" - ").str[1]
    df_revenu_cat["Catégorie_sec"] = df_revenu_cat["Catégorie_sec"].str.split(" - ").str[1]

    fig = px.sunburst(
        df_revenu_cat,
        path=['Catégorie_ppal', 'Catégorie_sec'],
        values='Crédit'
    )

    fig.update_traces(textinfo="label+percent parent")

    # fig.show()

    # On crée le dataframe à afficher
    df_temp = df_revenu_cat.groupby(
        by=["Catégorie_ppal"]
    ).sum().sort_values(
        by=["Crédit"],
        ascending=False
    )

    df_temp = df_temp[["Crédit"]]
    df_temp["Percent"] = round(
        df_temp["Crédit"]/df_temp["Crédit"].sum() * 100, 1
    )

    return fig, df_temp

# detail_revenu(df_global, datetime(2020,1,1), datetime(2022,12,31), ['Clement', 'Carolane'], False)





### Calcul ratio bénéfice/gain réel pour chacun
def calcul_ratio_simple(df_total, date_from, date_to, qui): # qui est ici une seule et unique personne
    df_temp_avec_virement = filtre_df(df_total, date_from, date_to, [qui], True)
    df_temp_sans_virement = filtre_df(df_total, date_from, date_to, [qui], False)

    participation_min = 700 #moitié des charges mensuels

    debit_avec_virement = df_temp_avec_virement["Débit"].sum()

    df_temp = df_temp_avec_virement.groupby(pd.Grouper(key="Date", freq="1M")).sum()
    if len(df_temp) >= 3:
        value_start = df_temp.iloc[0]
        value_end = df_temp.iloc[-1]
        df_temp = df_temp.iloc[1:-1]

        df_temp["Crédit"] = df_temp["Crédit"].apply(lambda x: max(participation_min, x))
    
        credit_avec_virement = df_temp["Crédit"].sum() + value_start["Crédit"].sum() + value_end["Crédit"].sum()
    else:
        credit_avec_virement = df_temp["Crédit"].sum()

    # debit_sans_virement = df_temp_sans_virement["Débit"].sum()
    
    df_temp = df_temp_sans_virement.groupby(pd.Grouper(key="Date", freq="1M")).sum()
    if len(df_temp) >= 3:
        value_start = df_temp.iloc[0]
        value_end = df_temp.iloc[-1]
        df_temp = df_temp.iloc[1:-1]

        df_temp["Crédit"] = df_temp["Crédit"].apply(lambda x: max(participation_min, x))
    
        credit_sans_virement = df_temp["Crédit"].sum() + value_start["Crédit"].sum() + value_end["Crédit"].sum()
    else:
        credit_sans_virement = df_temp["Crédit"].sum()



    ratio = (credit_avec_virement-debit_avec_virement) / credit_sans_virement #epargne/gain net

    return ratio, debit_avec_virement, credit_avec_virement, credit_sans_virement



def calcul_equilibre(df_total, date_from, date_to, qui_1, qui_2): #combien doit qui_1 à qui_2
    result_qui_1 = calcul_ratio_simple(df_total, date_from, date_to, qui_1)
    result_qui_2 = calcul_ratio_simple(df_total, date_from, date_to, qui_2)
    
    D_A_1 = result_qui_1[1]
    C_A_1 = result_qui_1[2]
    C_S_1 = result_qui_1[3]

    D_A_2 = result_qui_2[1]
    C_A_2 = result_qui_2[2]
    C_S_2 = result_qui_2[3]
    
    equilibre = (C_S_2*(C_A_1 - D_A_1) + C_S_1*(D_A_2 - C_A_2)) / (C_S_1 + C_S_2)
    
    return equilibre

# print(calcul_equilibre(df_global, datetime(2019,1,1), datetime(2022,12,31), 'Clement', 'Carolane'))





### Historique dépense mensuelles
def trace_evo_dep(df_total, date_from, date_to, liste_qui, compte_virement):

    df_temp = df_total[
        (df_total["Qui"].isin(liste_qui))
    ]

    if not compte_virement:
        df_temp = df_temp[
            (df_temp["Mode de paiement"]!="Virement interne")
        ]

    df_temp["Catégorie_ppal"] = df_temp["Catégorie_ppal"].str.split(" - ").str[1]

    df_temp = df_temp[df_temp["Débit"]>0]
    df_temp = df_temp[
        (df_temp["Date"]>=date_from) &
        (df_temp["Date"]<=date_to)]
    df_temp = df_temp.groupby(["Catégorie_ppal", pd.Grouper(key="Date",freq="1M")]).sum().reset_index()
    df_temp["Date"] = df_temp["Date"].apply(lambda x: x - timedelta(days=x.day - 1))

    fig = px.bar(
        df_temp,
        x="Date",
        y="Débit",
        color="Catégorie_ppal")

    fig.update_layout(
        title=f"Evolution dépenses du {date_from.date()} au {date_to.date()}",
        xaxis_title=None,
        yaxis_title="Montant",
        legend_title="Catégories",
    )

    # fig.show()
    return fig

# trace_evo_dep(df_global, datetime(2022,1,1), datetime(2022,12,31), ['Clement', 'Carolane'], False)