import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from math import pi

def show_seniority_trends_over_time(all_offers):
    """
    Creates a line plot showing trends in job offers by seniority level over time
    """
    # Group data by month and seniority level
    seniority_trends = all_offers.groupby([
        pd.Grouper(key='report date', freq='ME'),
        'seniority'
    ]).size().reset_index(name='count')
    
    # Create line plot
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
        color_discrete_sequence=px.colors.qualitative.Dark2
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
    
    return fig

def show_technology_by_seniority(latest_offers):
    """
    Creates a radar chart comparing technologies by seniority level
    """
    # Explode the technology column and group by technology and seniority
    tech_senior = latest_offers.explode('technology').groupby(['technology', 'seniority']).size().unstack()
    
    # Calculate the proportion of each seniority level within each technology
    tech_senior = tech_senior.div(tech_senior.sum(axis=1), axis=0)
    
    # Fill NaN values with 0
    tech_senior = tech_senior.fillna(0)
    
    # Get the top technologies by total count
    top_techs = latest_offers.explode('technology')['technology'].value_counts().head(10).index.tolist()
    
    # Filter for top technologies
    tech_senior = tech_senior.loc[tech_senior.index.isin(top_techs)]
    
    # Create radar chart
    categories = tech_senior.index.tolist()
    N = len(categories)
    
    # Calculate angles for radar chart
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Create figure
    fig = go.Figure()
    
    # Add traces for each seniority level
    colors = px.colors.qualitative.Dark2
    
    for i, seniority in enumerate(tech_senior.columns):
        values = tech_senior[seniority].tolist()
        values += values[:1]  # Close the loop
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],  # Close the loop
            name=seniority,
            line=dict(color=colors[i], width=2),
            fill='toself',
            fillcolor=colors[i],
            opacity=0.25
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
            orientation="h",
            yanchor="bottom",
            y=1.1,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def show_seniority_distribution(all_offers):
    """
    Creates a bar chart showing the distribution of seniority levels
    """
    seniority_counts = all_offers['seniority'].value_counts().reset_index()
    seniority_counts.columns = ['seniority', 'count']
    
    # Define the correct order of seniority levels
    seniority_order = ['junior', 'mid', 'senior', 'expert']
    
    # Create a custom order for the seniority levels
    seniority_counts['seniority_order'] = seniority_counts['seniority'].map(
        {level: i for i, level in enumerate(seniority_order)}
    )
    
    # Sort by the custom order
    seniority_counts = seniority_counts.sort_values('seniority_order')
    
    fig = px.bar(
        seniority_counts,
        x='seniority',
        y='count',
        title='Rozkład poziomów doświadczenia w ofertach pracy',
        labels={'seniority': 'Poziom doświadczenia', 'count': 'Liczba ofert'},
        text='count',
        color='seniority',
        color_discrete_sequence=px.colors.qualitative.Dark2
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(width=1000, height=600, showlegend=False)
    
    return fig

def show_seniority_by_city(all_offers):
    """
    Creates a stacked bar chart showing the distribution of seniority levels by city
    """
    # Filter out remote jobs and get top cities
    non_remote = all_offers[all_offers['location'] != 'Remote']
    top_cities = non_remote['location'].value_counts().head(10).index.tolist()
    
    # Filter for top cities
    city_data = non_remote[non_remote['location'].isin(top_cities)]
    
    # Group by city and seniority
    city_seniority = city_data.groupby(['location', 'seniority']).size().reset_index(name='count')
    
    fig = px.bar(
        city_seniority,
        x='location',
        y='count',
        color='seniority',
        title='Rozkład poziomów doświadczenia w ofertach pracy według miast',
        labels={'location': 'Miasto', 'count': 'Liczba ofert', 'seniority': 'Poziom doświadczenia'},
        color_discrete_sequence=px.colors.qualitative.Dark2
    )
    
    fig.update_layout(width=1200, height=600)
    fig.update_xaxes(categoryorder='total descending')
    
    return fig