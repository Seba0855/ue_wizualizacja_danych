import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from offers import offers
from salary import salary
from seniority import seniority
from technologies import technologies

csv_files = {
    '2023-09-01': pd.read_csv('./dataset/202309_soft_eng_jobs_pol.csv'),
    '2023-10-01': pd.read_csv('./dataset/202310_soft_eng_jobs_pol.csv'),
    '2023-11-01': pd.read_csv('./dataset/202311_soft_eng_jobs_pol.csv'),
    '2023-12-01': pd.read_csv('./dataset/202312_soft_eng_jobs_pol.csv'),
    '2024-01-01': pd.read_csv('./dataset/202401_soft_eng_jobs_pol.csv'),
    '2024-02-01': pd.read_csv('./dataset/202402_soft_eng_jobs_pol.csv'),
    '2024-03-01': pd.read_csv('./dataset/202403_soft_eng_jobs_pol.csv'),
    '2024-04-01': pd.read_csv('./dataset/202404_soft_eng_jobs_pol.csv'),
    '2024-05-01': pd.read_csv('./dataset/202405_soft_eng_jobs_pol.csv'),
    '2024-06-01': pd.read_csv('./dataset/202406_soft_eng_jobs_pol.csv')
}

dfs = []
for report_date in csv_files:
    df = csv_files[report_date]
    df['report date'] = report_date
    df['report date'] = pd.to_datetime(df['report date'])
    dfs.append(df)

all_offers = pd.concat(dfs)

columns = all_offers.columns.to_list()
all_offers['salary employment mean'] = round(
    all_offers['salary employment min'] * 0.5 + all_offers['salary employment max'] * 0.5)
all_offers['salary b2b mean'] = round(all_offers['salary b2b min'] * 0.5 + all_offers['salary b2b max'] * 0.5)
all_offers['contract type'] = all_offers.apply(lambda x: 'both' if (
        (np.isnan(x['salary employment mean']) == False) & (np.isnan(x['salary b2b mean']) == False)) else False,
                                               axis=1)
all_offers['contract type'] = all_offers.apply(
    lambda x: 'b2b' if ((x['contract type'] == False) & (np.isnan(x['salary employment mean']) == True)) else x[
        'contract type'], axis=1)
all_offers['contract type'] = all_offers.apply(
    lambda x: 'employment' if ((x['contract type'] == False) & (np.isnan(x['salary b2b mean']) == True)) else x[
        'contract type'], axis=1)
all_offers['contract type'] = all_offers.apply(
    lambda x: 'none' if (x['contract type'] == False) else x['contract type'], axis=1)
all_offers['company size'] = all_offers['company size'].transform(lambda x: None if np.isnan(x) else min(10000, x))
all_offers['company size'] = all_offers['company size'].transform(
    lambda x: None if np.isnan(x) else str(round(x)) + "+")
all_offers['is remote'] = all_offers['location'].transform(lambda x: 'Non Remote' if x != 'Remote' else x)
latest = all_offers[all_offers['report date'] == all_offers['report date'].unique().max()]


def layout_home():
    return html.Div(
        [
            html.H1("Analiza ofert pracy programistów w Polsce", style={"margin-top": "2rem"}),
            html.P(
                "Celem naszego projektu było przygotowanie zestawienia przedstawiającego informacje na temat zarobków i ilości ofert pracy w największych miastach Polski. Przygotowane przez nas wizualizacje mogą być pomocne dla osób, które chcą zorientować się w aktualnej sytuacji rynkowej w sektorze IT.",
                style={"margin-top": "1rem"}),
            html.Div(
                [
                    html.Div(
                        [
                            html.H4("Liczba analizowanych ofert"),
                            html.H2("18 209", style={"color": "#4e79a7"}),
                        ],
                        className="card p-3 m-2",
                        style={"background": "#f9f9f9", "display": "inline-block", "width": "350px"}
                    ),
                    html.Div(
                        [
                            html.H4("Zakres dat"),
                            html.H2("09.2023 - 06.2024", style={"color": "#f28e2b"}),
                        ],
                        className="card p-3 m-2",
                        style={"background": "#f9f9f9", "display": "inline-block", "width": "350px"}
                    )
                ],
                style={"display": "flex", "flex-wrap": "wrap"}
            ),
            html.Div([
                html.P("Wykorzystany przez nas dataset:", style={"margin-top": "1rem", "font-weight": "bold"}),
                html.A(
                    "https://www.kaggle.com/code/krzysztofjamroz/software-engineers-jobs-in-poland-analysis",
                    href="https://www.kaggle.com/code/krzysztofjamroz/software-engineers-jobs-in-poland-analysis",
                    target="_blank",
                    style={
                        "color": "#4e79a7",
                        "textDecoration": "none",
                        "fontStyle": "italic",
                        "marginLeft": "20px",
                        "borderBottom": "1px dashed #4e79a7"
                    }
                )
            ], style={"margin": "10px 0", "display": "flex", "alignItems": "center"}),
        ],
        style={"margin-left": "20rem", "margin-right": "2rem", "padding": "2rem 1rem"},
    )


def layout_offers():
    return html.Div([
        html.H2("Porównanie ofert względem miasta - praca stacjonarna"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=offers.show_all_offers(all_offers)), width=6),
            dbc.Col(dcc.Graph(figure=offers.show_latest_offers(latest)), width=6),
        ]),
        dbc.Row([dcc.Graph(figure=offers.show_cities_for_all_offers(all_offers))], style={"margin-top": "2rem"}),
    ], style={"margin-left": "20rem", "padding": "2rem 1rem"})


def layout_salaries():
    return html.Div([
        html.H2("Porównanie wynagrodzeń"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=salary.show_salary_distribution_by_contract_type(all_offers)), width=12),
        ]),
        dbc.Row([dcc.Graph(figure=salary.show_salary_by_company_size_b2b(all_offers))], style={"margin-top": "2rem"}),
        dbc.Row([dcc.Graph(figure=salary.show_salary_by_company_size_uop(all_offers))], style={"margin-top": "2rem"}),
        dbc.Row([dcc.Graph(figure=salary.show_salary_by_technology(all_offers, latest))], style={"margin-top": "2rem"}),
        dbc.Row([dcc.Graph(figure=salary.show_salary_by_city(all_offers, latest))], style={"margin-top": "2rem"}),
    ], style={"margin-left": "20rem", "padding": "2rem 1rem"})


def layout_seniority():
    return html.Div([
        html.H2("Porównanie poziomu doświadczenia"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=seniority.show_seniority_distribution(all_offers)), width=12),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=seniority.show_seniority_trends_over_time(all_offers)), width=12),
        ], style={"margin-top": "2rem"}),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=seniority.show_seniority_by_city(all_offers)), width=12),
        ], style={"margin-top": "2rem"}),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=seniority.show_technology_by_seniority(latest)), width=12),
        ], style={"margin-top": "2rem"}),
    ], style={"margin-left": "20rem", "padding": "2rem 1rem"})


def layout_technologies():
    return html.Div([
        html.H2("Porównanie technologii i typów kontraktów"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=technologies.show_technology_distribution(all_offers)), width=12),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=technologies.show_popular_technologies_treemap_all_offers(all_offers)), width=12),
        ], style={"margin-top": "2rem"}),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=technologies.show_popular_technologies_treemap_latest(latest)), width=12),
        ], style={"margin-top": "2rem"}),
        # dbc.Row([
        #     dbc.Col(dcc.Graph(figure=technologies.show_remote_contract_types(all_offers)), width=12),
        # ], style={"margin-top": "2rem"}),
        # dbc.Row([
        #     dbc.Col(dcc.Graph(figure=technologies.show_technology_trends_over_time(all_offers)), width=12),
        # ], style={"margin-top": "2rem"}),
        # dbc.Row([
        #     dbc.Col(dcc.Graph(figure=technologies.show_technology_by_city(all_offers)), width=12),
        # ], style={"margin-top": "2rem"}),
    ], style={"margin-left": "20rem", "padding": "2rem 1rem"})

def layout_contracts():
    return html.Div([
        html.H2("Preferowane typy kontraktów"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=technologies.show_contract_types_by_city(all_offers)), width=12),
        ], style={"margin-top": "2rem"}),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=technologies.show_remote_contract_types(all_offers)), width=12),
        ], style={"margin-top": "2rem"}),
    ], style={"margin-left": "20rem", "padding": "2rem 1rem"})


# Aplikacja Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

sidebar = html.Div(
    [
        html.P("Nawigacja", className="lead", style={"color": "white"}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Wprowadzenie", href="/", active="exact"),
                dbc.NavLink("Oferty per miasto", href="/offers", active="exact"),
                dbc.NavLink("Stosowane technologie", href="/tech_stack", active="exact"),
                dbc.NavLink("Preferowane typy kontraktów", href="/contracts", active="exact"),
                dbc.NavLink("Porównanie wynagrodzeń", href="/salaries", active="exact"),
                dbc.NavLink("Porównanie poziomu doświadczenia", href="/seniority", active="exact"),
            ],
            vertical=True,
            pills=True
        ),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "18rem",
        "padding": "2rem 1rem",
        "background-color": "#22223b",
        "color": "white",
    },
)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    html.Div(id="page-content")
])


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/offers":
        return layout_offers()
    elif pathname == "/tech_stack":
        return layout_technologies()
    elif pathname == "/salaries":
        return layout_salaries()
    elif pathname == "/seniority":
        return layout_seniority()
    elif pathname == "/contracts":
        return layout_contracts()
    else:
        return layout_home()


if __name__ == "__main__":
    app.run(debug=True)
