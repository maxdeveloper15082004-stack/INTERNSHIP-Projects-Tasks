from pathlib import Path

import folium
import matplotlib.pyplot as plt
from folium.plugins import MarkerCluster

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MAPS_DIR = PROJECT_ROOT / "outputs" / "maps"
CHARTS_DIR = PROJECT_ROOT / "outputs" / "charts"


def create_restaurant_map(df):
    MAPS_DIR.mkdir(parents=True, exist_ok=True)

    center_lat = df["Latitude"].median()
    center_lon = df["Longitude"].median()

    restaurant_map = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=5,
        tiles="OpenStreetMap",
    )

    marker_cluster = MarkerCluster().add_to(restaurant_map)

    for _, row in df.iterrows():
        rating = row["Aggregate rating"]

        if rating == rating:
            rating_text = f"{rating:.1f}"
        else:
            rating_text = "Not available"

        popup_text = (
            f"<b>{row['Restaurant Name']}</b><br>"
            f"City: {row['City']}<br>"
            f"Locality: {row['Locality']}<br>"
            f"Rating: {rating_text}<br>"
            f"Latitude: {row['Latitude']:.6f}<br>"
            f"Longitude: {row['Longitude']:.6f}"
        )

        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=4,
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=row["Restaurant Name"],
            fill=True,
        ).add_to(marker_cluster)

    output_path = MAPS_DIR / "restaurant_locations_map.html"
    restaurant_map.save(str(output_path))
    print(f"Interactive map saved: {output_path}")


def create_city_chart(city_counts):
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    top_cities = city_counts.head(10).sort_values("Restaurant Count")

    plt.figure(figsize=(12, 7))
    plt.barh(top_cities["City"], top_cities["Restaurant Count"])
    plt.title("Top 10 Cities by Number of Restaurants")
    plt.xlabel("Number of Restaurants")
    plt.ylabel("City")
    plt.tight_layout()

    output_path = CHARTS_DIR / "top_cities.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"City chart saved: {output_path}")


def create_cluster_chart(clustered_df):
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 8))
    plt.scatter(
        clustered_df["Longitude"],
        clustered_df["Latitude"],
        c=clustered_df["Cluster"],
        s=8,
        alpha=0.6,
    )
    plt.title("Geographic Distribution of Restaurant Clusters")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.tight_layout()

    output_path = CHARTS_DIR / "geographic_clusters.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Cluster chart saved: {output_path}")
