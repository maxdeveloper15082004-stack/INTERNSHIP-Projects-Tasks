from pathlib import Path

from src.analysis import analyze_geography
from src.clustering import identify_clusters
from src.data_loader import load_data
from src.preprocessing import clean_geographic_data
from src.visualization import (
    create_city_chart,
    create_cluster_chart,
    create_restaurant_map,
)

PROJECT_ROOT = Path(__file__).resolve().parent
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"


def save_reports(city_counts, locality_counts, cluster_counts, summary, cluster_summary):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    city_path = REPORTS_DIR / "city_restaurant_counts.csv"
    locality_path = REPORTS_DIR / "locality_restaurant_counts.csv"
    cluster_path = REPORTS_DIR / "geographic_clusters.csv"
    report_path = REPORTS_DIR / "geographic_analysis_report.txt"

    city_counts.to_csv(city_path, index=False)
    locality_counts.to_csv(locality_path, index=False)
    cluster_counts.to_csv(cluster_path, index=False)

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("GEOGRAPHIC RESTAURANT ANALYSIS REPORT\n")
        file.write("=" * 50 + "\n\n")
        file.write(f"Restaurants analyzed: {summary['total_restaurants']}\n")
        file.write(f"Unique cities: {summary['unique_cities']}\n\n")

        file.write("TOP 10 CITIES\n")
        file.write("-" * 50 + "\n")
        file.write(city_counts.head(10).to_string(index=False))

        file.write("\n\nTOP 10 LOCALITIES\n")
        file.write("-" * 50 + "\n")
        file.write(locality_counts.head(10).to_string(index=False))

        file.write("\n\nDBSCAN CLUSTERING SUMMARY\n")
        file.write("-" * 50 + "\n")
        file.write(f"Number of clusters: {cluster_summary['number_of_clusters']}\n")
        file.write(f"Restaurants assigned to clusters: {cluster_summary['clustered_restaurants']}\n")
        file.write(f"Restaurants classified as noise: {cluster_summary['noise_count']}\n")
        file.write(f"Neighborhood distance: {cluster_summary['eps_km']} km\n")
        file.write(f"Minimum samples: {cluster_summary['min_samples']}\n\n")

        file.write("TOP 10 LARGEST GEOGRAPHIC CLUSTERS\n")
        file.write("-" * 50 + "\n")
        if not cluster_counts.empty:
            file.write(cluster_counts.head(10).to_string(index=False))
        else:
            file.write("No geographic clusters were identified.")

        file.write("\n\nKEY FINDINGS\n")
        file.write("-" * 50 + "\n")
        file.write(f"City with the most restaurants: {summary['top_city']}\n")
        file.write(f"Restaurant count: {summary['top_city_count']}\n")
        file.write(
            f"Most represented locality: {summary['top_locality']}, {summary['top_locality_city']}\n"
        )
        file.write(f"Restaurant count: {summary['top_locality_count']}\n")

    print(f"\nCity report saved: {city_path}")
    print(f"Locality report saved: {locality_path}")
    print(f"Cluster report saved: {cluster_path}")
    print(f"Analysis report saved: {report_path}")


def main():
    print("=" * 60)
    print("GEOGRAPHIC RESTAURANT ANALYSIS")
    print("=" * 60)

    df = load_data()
    df = clean_geographic_data(df)

    geographic_results = analyze_geography(df)
    city_counts = geographic_results["city_counts"]
    locality_counts = geographic_results["locality_counts"]
    summary = geographic_results["summary"]

    clustered_df, cluster_counts, cluster_summary = identify_clusters(
        df,
        eps_km=2.0,
        min_samples=10,
    )

    print("\n1. GEOGRAPHIC SUMMARY")
    print("-" * 50)
    print(f"Restaurants analyzed: {summary['total_restaurants']}")
    print(f"Unique cities: {summary['unique_cities']}")

    print("\n2. TOP 10 CITIES")
    print("-" * 50)
    print(city_counts.head(10).to_string(index=False))

    print("\n3. TOP 10 LOCALITIES")
    print("-" * 50)
    print(locality_counts.head(10).to_string(index=False))

    print("\n4. DBSCAN CLUSTERING RESULTS")
    print("-" * 50)
    print(f"Number of clusters: {cluster_summary['number_of_clusters']}")
    print(f"Restaurants assigned to clusters: {cluster_summary['clustered_restaurants']}")
    print(f"Restaurants classified as noise: {cluster_summary['noise_count']}")

    print("\n5. LARGEST GEOGRAPHIC CLUSTERS")
    print("-" * 50)
    if not cluster_counts.empty:
        print(cluster_counts.head(10).to_string(index=False))
    else:
        print("No geographic clusters were identified.")

    create_restaurant_map(clustered_df)
    create_city_chart(city_counts)
    create_cluster_chart(clustered_df)

    save_reports(city_counts, locality_counts, cluster_counts, summary, cluster_summary)

    print("\nGeographic analysis completed successfully!")


if __name__ == "__main__":
    main()
