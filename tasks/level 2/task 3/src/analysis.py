def analyze_geography(df):
    city_counts = (
        df.groupby("City")
        .size()
        .reset_index(name="Restaurant Count")
        .sort_values("Restaurant Count", ascending=False)
        .reset_index(drop=True)
    )

    locality_counts = (
        df.groupby(["City", "Locality"])
        .size()
        .reset_index(name="Restaurant Count")
        .sort_values("Restaurant Count", ascending=False)
        .reset_index(drop=True)
    )

    summary = {
        "total_restaurants": len(df),
        "unique_cities": df["City"].nunique(),
        "top_city": city_counts.iloc[0]["City"],
        "top_city_count": int(city_counts.iloc[0]["Restaurant Count"]),
        "top_locality": locality_counts.iloc[0]["Locality"],
        "top_locality_city": locality_counts.iloc[0]["City"],
        "top_locality_count": int(locality_counts.iloc[0]["Restaurant Count"]),
    }

    return {
        "city_counts": city_counts,
        "locality_counts": locality_counts,
        "summary": summary,
    }
