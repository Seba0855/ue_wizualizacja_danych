import plotly.express as px


def show_contract_types_by_city(all_offers):
    contract_dist = all_offers[all_offers['location'] != 'Remote'].groupby(
        ['location', 'contract type']).size().unstack().fillna(0)
    contract_dist = contract_dist.div(contract_dist.sum(axis=1), axis=0) * 100
    contract_dist = contract_dist.reset_index().rename(columns={'location': 'Miasto'})

    contract_type_mapping = {
        'b2b': 'Tylko B2B',
        'both': 'B2B i UoP',
        'employment': 'Tylko UoP'
    }
    contract_dist = contract_dist.rename(columns=contract_type_mapping)

    contract_dist_melted = contract_dist.melt(id_vars='Miasto', var_name='Typ kontraktu', value_name='Procent ofert')

    fig = px.bar(
        contract_dist_melted,
        y='Miasto',
        x='Procent ofert',
        color='Typ kontraktu',
        orientation='h',
        title='Proporcje typów kontraktów na tle miast',
        color_discrete_sequence=['#1E8449', '#77B43F', '#5D6D7E'],
        width=800,
        height=400,
    )

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(title='Typ kontraktu', y=1, yanchor='top', x=1, xanchor='left'),
        margin=dict(l=50, r=0, t=50, b=50)
    )
    fig.update_xaxes(showticklabels=False)

    # fig.write_html("technologies/contract_types_by_city.html")
    return fig


def show_remote_contract_types(all_offers):
    remote_jobs = all_offers[all_offers['location'] == 'Remote']

    contract_counts = remote_jobs['contract type'].value_counts()

    label_map = {
        'b2b': 'Tylko B2B',
        'both': 'B2B i UoP',
        'employment': 'Tylko UoP'
    }

    contract_df = contract_counts.reset_index()
    contract_df.columns = ['contract type', 'count']
    contract_df['contract type'] = contract_df['contract type'].map(label_map)

    fig = px.pie(
        contract_df,
        names='contract type',
        values='count',
        title='Rozkład typów kontraktów dla pracy zdalnej',
        color='contract type',
        color_discrete_sequence=['#1E8449', '#77B43F', '#5D6D7E'],
        width=400,
    )
    fig.update_traces(textinfo="none")

    return fig
