import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show_technology_distribution(all_offers):
    """
    Creates a bar chart showing the distribution of technologies in job offers
    """
    # Explode the technology column to get one row per technology
    tech_data = all_offers.explode('technology')

    # Count occurrences of each technology
    tech_counts = tech_data['technology'].value_counts().reset_index()
    tech_counts.columns = ['technology', 'count']

    # Filter for top technologies
    top_techs = tech_counts.head(15)

    fig = px.bar(
        top_techs,
        x='technology',
        y='count',
        title='Najpopularniejsze technologie w ofertach pracy',
        labels={'technology': 'Technologia', 'count': 'Liczba ofert'},
        text='count',
        color='technology',
        color_discrete_sequence=px.colors.qualitative.Dark2
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(width=1200, height=600, showlegend=False)
    fig.update_xaxes(categoryorder='total descending')

    fig.write_html("technologies/technology_distribution.html")
    return fig

def show_contract_type_by_technology(all_offers):
    """
    Creates a stacked bar chart showing the distribution of contract types by technology
    """
    # Explode the technology column to get one row per technology
    tech_data = all_offers.explode('technology')

    # Get top technologies
    top_techs = tech_data['technology'].value_counts().head(10).index.tolist()

    # Filter for top technologies
    tech_contract = tech_data[tech_data['technology'].isin(top_techs)]

    # Group by technology and contract type
    tech_contract_counts = tech_contract.groupby(['technology', 'contract type']).size().reset_index(name='count')

    fig = px.bar(
        tech_contract_counts,
        x='technology',
        y='count',
        color='contract type',
        title='Rozkład typów kontraktów według technologii',
        labels={'technology': 'Technologia', 'count': 'Liczba ofert', 'contract type': 'Typ kontraktu'},
        color_discrete_sequence=px.colors.qualitative.Dark2
    )

    fig.update_layout(width=1200, height=600)
    fig.update_xaxes(categoryorder='total descending')

    fig.write_html("technologies/contract_type_by_technology.html")
    return fig

def show_technology_trends_over_time(all_offers):
    """
    Creates a line plot showing trends in job offers for top technologies over time
    """
    # Explode the technology column to get one row per technology
    tech_data = all_offers.explode('technology')

    # Get top technologies
    top_techs = tech_data['technology'].value_counts().head(6).index.tolist()

    # Filter for top technologies
    filtered_data = tech_data[tech_data['technology'].isin(top_techs)]

    # Group by month and technology
    tech_trends = filtered_data.groupby([
        pd.Grouper(key='report date', freq='ME'),
        'technology'
    ]).size().reset_index(name='count')

    # Create line plot
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
        color_discrete_sequence=px.colors.qualitative.Dark2
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
    fig.write_html("technologies/technologies_trends_over_time.html")
    return fig

def show_remote_contract_types(all_offers):
    """
    Creates a pie chart showing the distribution of contract types for remote work
    """
    # Filter for remote jobs
    remote_jobs = all_offers[all_offers['location'] == 'Remote']

    # Count occurrences of each contract type
    contract_counts = remote_jobs['contract type'].value_counts()

    # Map contract types to more readable labels
    label_map = {
        'b2b': 'Tylko B2B',
        'both': 'B2B i UoP',
        'employment': 'Tylko UoP'
    }

    # Create a dataframe for the pie chart
    contract_df = contract_counts.reset_index()
    contract_df.columns = ['contract type', 'count']
    contract_df['contract type'] = contract_df['contract type'].map(label_map)

    # Create pie chart
    fig = px.pie(
        contract_df,
        names='contract type',
        values='count',
        title='Rozkład typów kontraktów dla pracy zdalnej',
        color='contract type',
        color_discrete_sequence=px.colors.qualitative.Dark2,
        width=750
    )

    fig.write_html("technologies/remote_contract_types.html")
    return fig

def show_popular_technologies_treemap_all_offers(all_offers, title="Najpopularniejsze technologie programistyczne dla miast i pracy zdalnej od września 2023 do czerwca 2024"):
    """
    Creates a treemap showing the most popular technologies by location
    """
    # Group by location and technology, count occurrences
    tech_by_location = all_offers.groupby(['location', 'technology']).size().reset_index(name="count")

    # Create treemap
    fig = px.treemap(
        tech_by_location,
        path=['location', 'technology'],
        values='count',
        color='count',
        color_continuous_scale=px.colors.sequential.matter,
        title=title,
        width=1200
    )

    fig.update_layout(
        margin=dict(t=50, l=25, r=25, b=25), 
        coloraxis_colorbar=dict(title="Liczba ofert")
    )

    fig.write_html("technologies/popular_technologies_treemap.html")
    return fig

def show_popular_technologies_treemap_latest(latest_offers):
    return show_popular_technologies_treemap_all_offers(latest_offers, title="Najpopularniejsze technologie programistyczne dla miast i pracy zdalnej w dniu 1 czerwca 2024")

def show_contract_types_by_city(all_offers):
    """
    Creates a horizontal bar chart showing the proportions of contract types by city
    """
    # Filter out remote jobs and group by location and contract type
    contract_dist = all_offers[all_offers['location'] != 'Remote'].groupby(['location', 'contract type']).size().unstack().fillna(0)

    # Calculate percentages
    contract_dist = contract_dist.div(contract_dist.sum(axis=1), axis=0) * 100

    # Reset index and rename columns
    contract_dist = contract_dist.reset_index().rename(columns={'location': 'Miasto'})

    # Map contract types to more readable labels
    contract_type_mapping = {
        'b2b': 'Tylko B2B',
        'both': 'B2B i UoP',
        'employment': 'Tylko UoP'
    }
    contract_dist = contract_dist.rename(columns=contract_type_mapping)

    # Melt the dataframe for plotting
    contract_dist_melted = contract_dist.melt(id_vars='Miasto', var_name='Typ kontraktu', value_name='Procent ofert')

    # Create horizontal bar chart
    fig = px.bar(
        contract_dist_melted,
        y='Miasto',
        x='Procent ofert',
        color='Typ kontraktu',
        orientation='h',
        title='Proporcje typów kontraktów na tle miast',
        color_discrete_sequence=['#1E8449', '#77B43F', '#5D6D7E'],
        width=800,
        height=400
    )

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(title='Typ kontraktu', y=1, yanchor='top', x=1, xanchor='left'),
        margin=dict(l=50, r=0, t=50, b=50)
    )

    fig.write_html("technologies/contract_types_by_city.html")
    return fig
