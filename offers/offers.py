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

# Populacja miast w tysiącach mieszkańców (dane przybliżone)
populacja_miast = {
    'Warszawa': 1862,
    'Kraków': 808,
    'Wrocław': 674,
    'Poznań': 537,
    'Gdańsk': 488,
    'Katowice': 286,
    'Łódź': 649,
    'Lublin': 329,
    'Szczecin': 388,
    'Bydgoszcz': 325,
    'Białystok': 291,
    'Rzeszów': 197,
    'Toruń': 195
}

def show_all_offers(all, location_colors, title="Liczba ofert per miasto od września 2023 do czerwca 2024", updateXaxes=True):
    filtered_df = all[all["location"] != "Remote"]

    location_counts = filtered_df["location"].value_counts().reset_index()
    location_counts.columns = ["location", "count"]

    fig = px.bar(location_counts, y="location", x="count",
                 title=title,
                 labels={"location": "Miasto", "count": "Liczba ofert"},
                 width=800,
                 color="location",
                 color_discrete_map=location_colors,
                 orientation='h'
                 )

    fig.update_xaxes(categoryorder="total descending")
    fig.update_layout(showlegend=False)
    if updateXaxes:
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500],
                ticktext=['0', '0,5k', '1k', '1,5k', '2k', '2,5k', '3k', '3,5k', '4k', '4,5k']
            )
        )

    # fig.write_html("offers/all_offers.html")
    return fig


def show_latest_offers(latest, location_colors):
    fig = show_all_offers(latest, location_colors, title="Liczba ofert per miasto w dniu 1 czerwca 2024", updateXaxes=False)
    # fig.write_html("offers/latest_offers.html")
    return fig

def show_all_offers_per_1000(all, location_colors, title="Liczba ofert na 1000 mieszkańców od września 2023 do czerwca 2024"):
    filtered_df = all[all["location"] != "Remote"]

    location_counts = filtered_df["location"].value_counts().reset_index()
    location_counts.columns = ["location", "count"]

    location_counts["populacja"] = location_counts["location"].map(lambda x: populacja_miast.get(x, 0))
    location_counts = location_counts[location_counts["populacja"] > 0]
    location_counts["oferty_na_1000"] = location_counts["count"] / location_counts["populacja"]

    fig = px.bar(location_counts, y="location", x="oferty_na_1000",
                 title=title,
                 labels={"location": "Miasto", "oferty_na_1000": "Liczba ofert na 1000 mieszkańców"},
                 width=800,
                 color="location",
                 color_discrete_map=location_colors,
                 orientation='h',
                 )

    fig.update_yaxes(categoryorder="total ascending")
    fig.update_layout(showlegend=False)

    # fig.write_html("offers/all_offers.html")
    return fig


def show_latest_offers_per_1000(latest, location_colors):
    fig = show_all_offers_per_1000(latest, location_colors, title="Liczba ofert na 1000 mieszkańców w dniu 1 czerwca 2024")
    # fig.write_html("offers/latest_offers.html")
    return fig


def show_cities_for_all_offers(all,
                               title="Liczba ofert pracy dla programistów na 1000 mieszkańców od września 2023 do czerwca 2024"):
    miasta_all = all[all['location'] != 'Remote']['location'].value_counts().reset_index()
    miasta_all.columns = ['miasto', 'liczba_ofert']

    # Dodaj dane o populacji i oblicz liczbę ofert na 1000 mieszkańców
    miasta_all['populacja'] = miasta_all['miasto'].map(lambda x: populacja_miast.get(x, 0))
    miasta_all = miasta_all[miasta_all['populacja'] > 0]
    miasta_all['oferty_na_1000'] = miasta_all['liczba_ofert'] / miasta_all['populacja'] * 1000

    miasta_all['lat'] = miasta_all['miasto'].map(lambda x: wspolrzedne_miast[x][0] if x in wspolrzedne_miast else None)
    miasta_all['lon'] = miasta_all['miasto'].map(lambda x: wspolrzedne_miast[x][1] if x in wspolrzedne_miast else None)
    miasta = miasta_all.dropna(subset=['lat', 'lon'])

    fig = px.scatter_mapbox(
        miasta,
        lat='lat',
        lon='lon',
        size='oferty_na_1000',
        hover_name='miasto',
        hover_data={
            'oferty_na_1000': ':.2f',
            'liczba_ofert': True,
            'populacja': True,
            'lat': False,
            'lon': False
        },
        color='oferty_na_1000',
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
        coloraxis_colorbar=dict(title="Oferty na 1000 mieszkańców")
    )
    # fig.write_html("offers/cities_for_all_offers.html")
    return fig


def show_cities_for_latest_offers(latest):
    fig = show_cities_for_all_offers(latest,
                                     title="Liczba ofert pracy dla programistów na 1000 mieszkańców w dniu 1 czerwca 2024")
    # fig.write_html("offers/cities_for_latest_offers.html")
    return fig
