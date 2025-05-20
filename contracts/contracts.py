import plotly.express as px


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

    return fig

