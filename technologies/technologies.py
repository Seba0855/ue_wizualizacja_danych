import pandas as pd
import plotly.express as px


def show_technology_distribution(all_offers, technology_colors):
    tech_data = all_offers.explode('technology')
    tech_counts = tech_data['technology'].value_counts().reset_index()
    tech_counts.columns = ['technology', 'count']

    top_techs = tech_counts.head(15)

    fig = px.bar(
        top_techs,
        x='technology',
        y='count',
        title='Najpopularniejsze technologie w ofertach pracy',
        labels={'technology': 'Technologia', 'count': 'Liczba ofert'},
        text='count',
        color='technology',
        color_discrete_map=technology_colors
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(width=1200, height=600, showlegend=False)
    fig.update_xaxes(categoryorder='total descending')

    # fig.write_html("technologies/technology_distribution.html")
    return fig


def show_technology_trends_over_time(all_offers, technology_colors):
    tech_data = all_offers.explode('technology')
    top_techs = tech_data['technology'].value_counts().head(6).index.tolist()
    filtered_data = tech_data[tech_data['technology'].isin(top_techs)]

    tech_trends = filtered_data.groupby([
        pd.Grouper(key='report date', freq='ME'),
        'technology'
    ]).size().reset_index(name='count')

    fig = px.line(
        tech_trends,
        x='report date',
        y='count',
        color='technology',
        markers=True,
        title='Zmiany w liczbie ofert dla najpopularniejszych technologii w czasie',
        labels={
            'report date': 'Data wystawienia oferty',
            'count': 'Liczba ofert',
            'technology': 'Technologia'
        },
        color_discrete_map=technology_colors
    )

    fig.update_layout(
        width=1200,
        height=600,
        legend=dict(
            title="Technologia",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    # fig.write_html("technologies/technologies_trends_over_time.html")
    return fig


def show_popular_technologies_treemap_all_offers(all_offers,
                                                 title="Najpopularniejsze technologie programistyczne dla miast i pracy zdalnej od września 2023 do czerwca 2024"):
    tech_by_location = all_offers.groupby(['location', 'technology']).size().reset_index(name="count")

    fig = px.treemap(
        tech_by_location,
        path=['location', 'technology'],
        values='count',
        color='count',
        color_continuous_scale=px.colors.sequential.speed,
        title=title,
        width=1200
    )

    fig.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        coloraxis_colorbar=dict(title="Liczba ofert")
    )

    # fig.write_html("technologies/popular_technologies_treemap.html")
    return fig


def show_popular_technologies_treemap_latest(latest_offers):
    return show_popular_technologies_treemap_all_offers(latest_offers,
                                                        title="Najpopularniejsze technologie programistyczne dla miast i pracy zdalnej w dniu 1 czerwca 2024")
