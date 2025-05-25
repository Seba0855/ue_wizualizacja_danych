from math import pi

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

color_map = {
    'junior': '#56B4E9',
    'mid': '#009E73',
    'senior': '#E69F00',
    'expert': '#CC79A7'
}


def show_seniority_trends_over_time(all_offers):
    seniority_trends = all_offers.groupby([
        pd.Grouper(key='report date', freq='ME'),
        'seniority'
    ]).size().reset_index(name='count')

    fig = px.line(
        seniority_trends,
        x='report date',
        y='count',
        color='seniority',
        markers=True,
        title='Zmiany w liczbie ofert w czasie wg poziomu doświadczenia',
        labels={
            'report date': 'Data wystawienia oferty',
            'count': 'Liczba ofert',
            'seniority': 'Doświadczenie'
        },
        color_discrete_map=color_map
    )

    fig.update_layout(
        width=1200,
        height=600,
        legend=dict(
            title="Doświadczenie",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # fig.write_html("seniority/seniority_trends_over_time.html")
    return fig


def show_technology_by_seniority(latest_offers):
    new_order = ['junior', 'mid', 'senior', 'expert']
    tech_senior = latest_offers.explode('technology').groupby(['technology', 'seniority']).size().unstack()
    tech_senior = tech_senior.div(tech_senior.sum(axis=1), axis=0)
    tech_senior = tech_senior.fillna(0)
    tech_senior = tech_senior[new_order]
    top_techs = latest_offers.explode('technology')['technology'].value_counts().head(10).index.tolist()
    tech_senior = tech_senior.loc[tech_senior.index.isin(top_techs)]
    print(tech_senior)

    categories = tech_senior.index.tolist()
    N = len(categories)

    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # Close the loop

    fig = go.Figure()

    colors = ['#56B4E9', '#009E73', '#E69F00', '#CC79A7']

    for i, seniority in enumerate(tech_senior.columns):
        values = tech_senior[seniority].tolist()
        values += values[:1]

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            name=seniority,
            line=dict(color=colors[i], width=2),
            fill='toself',
            fillcolor=colors[i],
            opacity=0.5
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickvals=[0.25, 0.5, 0.75, 1],
                ticktext=["25%", "50%", "75%", "100%"]
            )
        ),
        title="Porównanie ofert o określonym poziomie doświadczenia a technologia",
        width=800,
        height=800,
        legend=dict(
            title="Doświadczenie",
            orientation="v",
            yanchor="bottom",
            y=0.8,
            xanchor="right",
            x=1.2
        )
    )

    # fig.write_html("seniority/technology_by_seniority.html")
    return fig


def show_seniority_distribution(all_offers):
    seniority_counts = all_offers['seniority'].value_counts().reset_index()
    seniority_counts.columns = ['seniority', 'count']

    seniority_order = ['junior', 'mid', 'senior', 'expert']

    seniority_counts['seniority_order'] = seniority_counts['seniority'].map(
        {level: i for i, level in enumerate(seniority_order)}
    )

    seniority_counts = seniority_counts.sort_values('seniority_order')

    fig = px.bar(
        seniority_counts,
        x='seniority',
        y='count',
        title='Rozkład poziomów doświadczenia w ofertach pracy',
        labels={'seniority': 'Poziom doświadczenia', 'count': 'Liczba ofert'},
        text='count',
        color='seniority',
        color_discrete_map=color_map
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(width=1000, height=600, showlegend=False)

    # fig.write_html("seniority/seniority_distribution.html")
    return fig


def show_seniority_by_city(all_offers):
    non_remote = all_offers[all_offers['location'] != 'Remote']
    top_cities = non_remote['location'].value_counts().head(10).index.tolist()

    city_data = non_remote[non_remote['location'].isin(top_cities)]

    city_seniority = city_data.groupby(['location', 'seniority']).size().reset_index(name='count')

    fig = px.bar(
        city_seniority,
        x='location',
        y='count',
        color='seniority',
        title='Rozkład poziomów doświadczenia w ofertach pracy według miast',
        labels={'location': 'Miasto', 'count': 'Liczba ofert', 'seniority': 'Poziom doświadczenia'},
        color_discrete_map=color_map
    )

    fig.update_layout(width=1200, height=600)
    fig.update_xaxes(categoryorder='total descending')

    # fig.write_html("seniority/seniority_by_city.html")
    return fig
