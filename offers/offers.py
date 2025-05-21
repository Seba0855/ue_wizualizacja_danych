import plotly.express as px

wspolrzedne_miast = {
    'Warszawa': (52.2297, 21.0122),
    'Kraków': (50.0647, 19.9450),
    'Wrocław': (51.1079, 17.0385),
    'Poznań': (52.4064, 16.9252),
    'Gdańsk': (54.3520, 18.6466),
    'Katowice': (50.2649, 19.0238),
    'Łódź': (51.7592, 19.4560),
    'Lublin': (51.2465, 22.5684),
    'Szczecin': (53.4285, 14.5528),
    'Bydgoszcz': (53.1235, 18.0084),
    'Białystok': (53.1325, 23.1688),
    'Rzeszów': (50.0412, 21.9991),
    'Toruń': (53.0138, 18.5984)
}


def show_all_offers(all, location_colors, title="Liczba ofert per miasto od września 2023 do czerwca 2024"):
    filtered_df = all[all["location"] != "Remote"]

    location_counts = filtered_df["location"].value_counts().reset_index()
    location_counts.columns = ["location", "count"]

    fig = px.bar(location_counts, x="location", y="count",
                 title=title,
                 labels={"location": "Miasto", "count": "Liczba ofert"},
                 text="count",
                 width=800,
                 color="location",
                 color_discrete_map=location_colors,
                 )

    fig.update_traces(textposition="outside")
    fig.update_xaxes(categoryorder="total descending")
    fig.update_layout(showlegend=False)

    fig.write_html("offers/all_offers.html")
    return fig


def show_latest_offers(latest, location_colors):
    fig = show_all_offers(latest, location_colors, title="Liczba ofert per miasto w dniu 1 czerwca 2024")
    fig.write_html("offers/latest_offers.html")
    return fig


def show_cities_for_all_offers(all,
                               title="Liczba ofert pracy dla programistów w polskich miastach od września 2023 do czerwca 2024"):
    miasta_all = all[all['location'] != 'Remote']['location'].value_counts().reset_index()
    miasta_all.columns = ['miasto', 'liczba_ofert']

    miasta_all['lat'] = miasta_all['miasto'].map(lambda x: wspolrzedne_miast[x][0] if x in wspolrzedne_miast else None)
    miasta_all['lon'] = miasta_all['miasto'].map(lambda x: wspolrzedne_miast[x][1] if x in wspolrzedne_miast else None)
    miasta = miasta_all.dropna(subset=['lat', 'lon'])

    fig = px.scatter_mapbox(
        miasta,
        lat='lat',
        lon='lon',
        size='liczba_ofert',
        hover_name='miasto',
        hover_data={'liczba_ofert': True, 'lat': False, 'lon': False},
        color='liczba_ofert',
        color_continuous_scale=px.colors.sequential.matter,
        size_max=40,
        zoom=5,
        center={"lat": 52.1, "lon": 19.4},
        title=title,
        width=1200
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        coloraxis_colorbar=dict(title="Liczba ofert")
    )
    # fig.write_html("offers/cities_for_all_offers.html")
    return fig


def show_cities_for_latest_offers(latest):
    fig = show_cities_for_all_offers(latest,
                                     title="Liczba ofert pracy dla programistów w polskich miastach w dniu 1 czerwca 2024")
    # fig.write_html("offers/cities_for_latest_offers.html")
    return fig
