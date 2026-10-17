import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

EARTH_RADIUS_KM = 6371.0088


def identify_clusters(df, eps_km=2.0, min_samples=10):
    df = df.copy()

    coordinates = np.radians(df[["Latitude", "Longitude"]].to_numpy())
    eps_radians = eps_km / EARTH_RADIUS_KM

    model = DBSCAN(
        eps=eps_radians,
        min_samples=min_samples,
        metric="haversine",
        algorithm="ball_tree",
    )

    df["Cluster"] = model.fit_predict(coordinates)

    cluster_counts = (
        df[df["Cluster"] != -1]
        .groupby("Cluster")
        .agg(
            Restaurant_Count=("Restaurant ID", "size"),
            Center_Latitude=("Latitude", "mean"),
            Center_Longitude=("Longitude", "mean"),
        )
        .reset_index()
        .sort_values("Restaurant_Count", ascending=False)
        .reset_index(drop=True)
    )

    cluster_sizes = df["Cluster"].value_counts()
    number_of_clusters = int((cluster_sizes.index != -1).sum())
    noise_count = int((df["Cluster"] == -1).sum())

    summary = {
        "number_of_clusters": number_of_clusters,
        "noise_count": noise_count,
        "clustered_restaurants": len(df) - noise_count,
        "eps_km": eps_km,
        "min_samples": min_samples,
    }

    return df, cluster_counts, summary
