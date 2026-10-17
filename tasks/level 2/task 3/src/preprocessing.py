import pandas as pd


def clean_geographic_data(df):
    df = df.copy()

    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Aggregate rating"] = pd.to_numeric(df["Aggregate rating"], errors="coerce")

    original_count = len(df)

    df = df.dropna(subset=["Longitude", "Latitude"]).copy()
    df = df[df["Longitude"].between(-180, 180) & df["Latitude"].between(-90, 90)].copy()

    zero_coordinates = (df["Longitude"] == 0) & (df["Latitude"] == 0)
    zero_count = int(zero_coordinates.sum())
    df = df[~zero_coordinates].copy()

    for column in ["Restaurant Name", "City", "Locality"]:
        df[column] = df[column].fillna("Unknown").astype(str).str.strip()

    df["Aggregate rating"] = df["Aggregate rating"].where(
        df["Aggregate rating"].between(0, 5)
    )

    print("\nDATA CLEANING SUMMARY")
    print("-" * 40)
    print(f"Original records: {original_count}")
    print(f"Records at (0, 0): {zero_count}")
    print(f"Valid geographic records: {len(df)}")

    return df
