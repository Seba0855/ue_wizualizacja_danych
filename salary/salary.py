import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show_salary_distribution_by_contract_type(all_offers):
    """
    Creates a histogram showing the salary distribution for B2B vs UoP contracts
    """
    b2b_salaries = all_offers[all_offers['contract type'] == 'b2b']['salary b2b mean'].dropna()
    uop_salaries = all_offers[all_offers['contract type'] == 'employment']['salary employment mean'].dropna()

    colors = px.colors.qualitative.Dark2[:3]

    fig = go.Figure()

    fig.add_trace(go.Histogram(x=b2b_salaries, name='B2B', opacity=0.7, marker_color=colors[0]))
    fig.add_trace(go.Histogram(x=uop_salaries, name='UoP', opacity=0.7, marker_color=colors[2]))

    fig.update_layout(
        title='Rozkład wynagrodzeń dla B2B vs UoP',
        xaxis_title='Wynagrodzenie',
        yaxis_title='Liczba ofert',
        barmode='overlay',
        width=1200
    )

    fig.write_html("salary/salary_distribution_by_contract_type.html")
    return fig

def show_salary_by_company_size_b2b(all_offers):
    """
    Creates a box plot showing the salary distribution by company size for B2B contracts
    """
    b2b_data = all_offers[all_offers['contract type'] == 'b2b'].dropna(subset=['salary b2b mean'])

    fig = px.box(b2b_data,
                 x='company size',
                 y='salary b2b mean',
                 title='Rozkład wynagrodzeń B2B według wielkości firmy',
                 labels={'salary b2b mean': 'Wynagrodzenie B2B', 'company size': 'Wielkość firmy'},
                 color='company size',
                 color_discrete_sequence=px.colors.qualitative.Dark2)

    fig.update_layout(width=1000, height=600, showlegend=False)
    fig.update_xaxes(categoryorder="category ascending")

    fig.write_html("salary/salary_by_company_size_b2b.html")
    return fig

def show_salary_by_company_size_uop(all_offers):
    """
    Creates a box plot showing the salary distribution by company size for UoP contracts
    """
    uop_data = all_offers[all_offers['contract type'] == 'employment'].dropna(subset=['salary employment mean'])

    fig = px.box(uop_data,
                 x='company size',
                 y='salary employment mean',
                 title='Rozkład wynagrodzeń UoP według wielkości firmy',
                 labels={'salary employment mean': 'Wynagrodzenie UoP', 'company size': 'Wielkość firmy'},
                 color='company size',
                 color_discrete_sequence=px.colors.qualitative.Dark2)

    fig.update_layout(width=1000, height=600, showlegend=False)
    fig.update_xaxes(categoryorder="category ascending")

    fig.write_html("salary/salary_by_company_size_uop.html")
    return fig

def wykres_zarobkow_dla_segmentu(all_offers, latest_offers, nazwa_segmentu, tekst_segmentu, kolejność=None):
    """
    Creates a grid of histograms showing salary distributions for different experience levels
    across different segments (technology, location, etc.)
    """
    latest_offers_clean = latest_offers.copy()

    # Create 'offer' column as mean of salary ranges
    latest_offers_clean['offer'] = np.nan

    # For B2B contracts
    b2b_mask = latest_offers_clean['contract type'] == 'b2b'
    latest_offers_clean.loc[b2b_mask, 'offer'] = latest_offers_clean.loc[b2b_mask, 'salary b2b mean']

    # For employment contracts
    emp_mask = latest_offers_clean['contract type'] == 'employment'
    latest_offers_clean.loc[emp_mask, 'offer'] = latest_offers_clean.loc[emp_mask, 'salary employment mean']

    # For both contract types, take the average
    both_mask = latest_offers_clean['contract type'] == 'both'
    latest_offers_clean.loc[both_mask, 'offer'] = (
        latest_offers_clean.loc[both_mask, 'salary b2b mean'].fillna(0) + 
        latest_offers_clean.loc[both_mask, 'salary employment mean'].fillna(0)
    ) / 2

    latest_offers_clean['offer'] = pd.to_numeric(latest_offers_clean['offer'], errors='coerce')
    latest_offers_clean = latest_offers_clean[np.isfinite(latest_offers_clean['offer'])]

    experience = ['Junior', 'Mid', 'Senior', 'Expert']

    if kolejność:
        segmenty = kolejność
    else:
        # Group by segment and count offers with salary data
        latest_salaries = latest_offers_clean[np.isfinite(latest_offers_clean['offer'])]
        segmenty = latest_salaries.groupby([nazwa_segmentu])['offer'].count().reset_index()
        segmenty = segmenty[segmenty['offer'] > 100][nazwa_segmentu].to_list()

    # Kolory i układ
    kolory = ['indianred', 'lightseagreen', 'coral', 'darkcyan']

    # Generowanie tytułów
    subplot_titles = []
    for _ in segmenty:
        for poziom in experience:
            subplot_titles.append(f"{poziom}")

    fig = make_subplots(
        rows=len(segmenty),
        cols=4,
        subplot_titles=subplot_titles,
        vertical_spacing=0.1,
        horizontal_spacing=0.05
    )

    for j, segment in enumerate(segmenty):
        for i, poziom in enumerate(experience):
            idx = j * 4 + i

            # Filtracja i czyszczenie danych
            dane = latest_offers_clean.loc[
                (latest_offers_clean['seniority'] == poziom.lower()) &
                (latest_offers_clean[nazwa_segmentu] == segment)
            ]

            if not dane.empty:
                mediana = round(dane['offer'].median())
                counts, bins = np.histogram(dane['offer'], bins=50)
                max_count = counts.max() if counts.size > 0 else 0
            else:
                mediana = 0
                max_count = 0

            if not dane.empty and mediana > 0:
                # Histogram
                fig.add_trace(
                    go.Histogram(
                        x=dane['offer'],
                        marker_color=kolory[i],
                        showlegend=False,
                        opacity=0.7,
                        nbinsx=50
                    ),
                    row=j+1,
                    col=i+1
                )

                # Linia mediany
                fig.add_shape(
                    type="line",
                    x0=mediana,
                    x1=mediana,
                    y0=0,
                    y1=max_count * 1.1,
                    line=dict(color="black", width=3),
                    xref=f"x{idx+1}",
                    yref=f"y{idx+1}"
                )

                # Adnotacje
                fig.add_annotation(
                    x=mediana + 5000,
                    y=max_count * 0.8,
                    text=f"{segment}<br>Mediana: {mediana} zł",
                    showarrow=False,
                    bgcolor="white",
                    bordercolor="black",
                    borderwidth=1,
                    xref=f"x{idx+1}",
                    yref=f"y{idx+1}"
                )

                # Tytuł z medianą
                fig.layout.annotations[idx].update(text=f"{poziom}<br>Mediana: {mediana} zł")
            else:
                # Ukryj pusty wykres
                fig.update_xaxes(visible=False, row=j+1, col=i+1)
                fig.update_yaxes(visible=False, row=j+1, col=i+1)
                fig.add_annotation(
                    text="<b>Brak danych</b>",
                    xref=f"x{idx+1}",
                    yref=f"y{idx+1}",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=14, color="red")
                )

    fig.update_layout(
        title_text=f"<b>Rozkład zarobków według {tekst_segmentu}</b>",
        height=250*len(segmenty),
        width=1400,
        margin=dict(t=120),
        title_x=0.5,
        title_font=dict(size=20)
    )

    for i in range(1,5):
        fig.update_xaxes(
            title_text="Wynagrodzenie (PLN)",
            row=len(segmenty),
            col=i,
            title_font=dict(size=12)
        )

    return fig

def show_salary_by_technology(all_offers, latest_offers):
    """
    Creates a grid of histograms showing salary distributions by technology
    """
    fig = wykres_zarobkow_dla_segmentu(
        all_offers, 
        latest_offers, 
        'technology', 
        "technologii", 
        ['Java', 'Python', 'C#', 'C/C++', 'JavaScript', 'PHP', "Kotlin"]
    )
    fig.write_html("salary/salary_by_technology.html")
    return fig

def show_salary_by_city(all_offers, latest_offers):
    """
    Creates a grid of histograms showing salary distributions by city
    """
    fig = wykres_zarobkow_dla_segmentu(
        all_offers, 
        latest_offers, 
        'location', 
        "miasta", 
        ['Warszawa', 'Katowice', 'Wrocław', 'Gdańsk']
    )
    fig.write_html("salary/salary_by_city.html")
    return fig

def show_salary_by_seniority(all_offers):
    """
    Creates a histogram showing salary distribution by seniority level
    """
    offers = all_offers.copy()

    # Create 'offer' column as mean of salary ranges
    offers['offer'] = offers.apply(lambda x: get_offers(x['salary employment min'], x['salary employment max']), axis=1)
    offers = offers.drop(columns=['salary employment min', 'salary employment max', 'salary employment mean'])
    offers = offers.set_index(offers.columns[:-1].to_list())
    offers = offers.apply(lambda x: x.str.split('|').explode()).reset_index()
    offers['offer'] = offers['offer'].astype('float')
    latest_offers = offers[offers['report date'] == offers['report date'].unique().max()]

    seniority_levels = ['junior', 'mid', 'senior', 'expert']
    colors = ['indianred', 'lightseagreen', 'coral', 'darkcyan']

    fig = go.Figure()

    for i, seniority in enumerate(seniority_levels):
        subset = latest_offers[latest_offers['seniority'] == seniority]
        subset = subset[subset['offer'].notna()]
        median_salary = round(subset['offer'].median() / 100) * 100

        fig.add_trace(go.Histogram(
            x=subset['offer'],
            name=seniority,
            marker_color=colors[i],
            opacity=0.75,
        ))

        # linia mediany
        fig.add_shape(
            type="line",
            x0=median_salary,
            y0=0,
            x1=median_salary,
            y1=3500,
            line=dict(color="black", width=2, dash="dash"),
            xref='x',
            yref='y'
        )
        fig.add_annotation(
            x=median_salary,
            y=3500,
            text=f"{median_salary} zł",
            showarrow=False,
            yanchor='bottom',
            font=dict(color='black', size=12)
        )

    fig.update_layout(
        title='Porównanie zarobków na tle doświadczenia',
        xaxis_title='Wynagrodzenie w tysiącach (PLN)',
        yaxis_title='Ilość ofert',
        barmode='overlay',
        bargap=0.1,
        legend_title="Doświadczenie",
        width=1200,
    )

    fig.write_html("salary/salary_by_seniority.html")
    return fig

def get_offers(min_val, max_val):
    """
    Generates a distribution of salary offers based on min and max values
    """
    mean = (max_val + min_val)/2
    range_val = max(mean*0.1, (max_val - min_val)/2)
    salary = np.random.normal(mean, range_val/3, size=1000).round()
    return '|'.join(salary.astype('str').tolist())
