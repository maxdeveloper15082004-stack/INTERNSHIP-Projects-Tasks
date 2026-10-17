import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from config import (
    CHARTS_DIR,
    ONLINE_REPORT_PATH,
    TABLE_REPORT_PATH,
    COMPARISON_REPORT_PATH,
)


def calculate_service_percentages(df, service_column):
    result = (
        df.groupby("Price range")[service_column]
        .value_counts(normalize=True)
        .mul(100)
        .rename("Percentage")
        .reset_index()
    )

    result = result[result[service_column] == "Yes"].copy()
    result = result.rename(columns={service_column: "Availability"})
    result = result[["Price range", "Percentage"]]
    result["Percentage"] = result["Percentage"].round(2)

    return result


def analyze_price_range(df):
    print("\n========== PRICE RANGE ANALYSIS ==========")

    price_counts = df.groupby("Price range").size().reset_index(name="Restaurant Count")
    print("\nRestaurant count by price range:")
    print(price_counts.to_string(index=False))

    online_analysis = calculate_service_percentages(df, "Has Online delivery")
    table_analysis = calculate_service_percentages(df, "Has Table booking")

    online_analysis.to_csv(ONLINE_REPORT_PATH, index=False)
    table_analysis.to_csv(TABLE_REPORT_PATH, index=False)

    print("\nOnline delivery availability by price range:")
    print(online_analysis.to_string(index=False))

    print("\nTable booking availability by price range:")
    print(table_analysis.to_string(index=False))

    comparison = (
        df.groupby("Price range")
        .agg(
            Restaurant_Count=("Restaurant Name", "size"),
            Online_Delivery_Percentage=(
                "Has Online delivery",
                lambda values: values.eq("Yes").mean() * 100,
            ),
            Table_Booking_Percentage=(
                "Has Table booking",
                lambda values: values.eq("Yes").mean() * 100,
            ),
        )
        .reset_index()
    )

    percentage_columns = ["Online_Delivery_Percentage", "Table_Booking_Percentage"]
    comparison[percentage_columns] = comparison[percentage_columns].round(2)

    comparison.to_csv(COMPARISON_REPORT_PATH, index=False)

    print("\n========== SERVICE COMPARISON ==========")
    print(comparison.to_string(index=False))

    plot_online_delivery(comparison)
    plot_table_booking(comparison)
    plot_service_comparison(comparison)
    plot_heatmap(comparison)

    return comparison


def plot_online_delivery(comparison):
    plt.figure(figsize=(9, 6))
    sns.barplot(data=comparison, x="Price range", y="Online_Delivery_Percentage")
    plt.title("Online Delivery Availability by Price Range")
    plt.xlabel("Price Range")
    plt.ylabel("Restaurants Offering Online Delivery (%)")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "online_delivery_by_price.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_table_booking(comparison):
    plt.figure(figsize=(9, 6))
    sns.barplot(data=comparison, x="Price range", y="Table_Booking_Percentage")
    plt.title("Table Booking Availability by Price Range")
    plt.xlabel("Price Range")
    plt.ylabel("Restaurants Offering Table Booking (%)")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "table_booking_by_price.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_service_comparison(comparison):
    plot_data = comparison.melt(
        id_vars=["Price range"],
        value_vars=["Online_Delivery_Percentage", "Table_Booking_Percentage"],
        var_name="Service",
        value_name="Percentage",
    )

    plot_data["Service"] = plot_data["Service"].map(
        {
            "Online_Delivery_Percentage": "Online Delivery",
            "Table_Booking_Percentage": "Table Booking",
        }
    )

    plt.figure(figsize=(10, 6))
    sns.barplot(data=plot_data, x="Price range", y="Percentage", hue="Service")
    plt.title("Service Availability Across Price Ranges")
    plt.xlabel("Price Range")
    plt.ylabel("Restaurants Offering Service (%)")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "service_comparison_by_price.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_heatmap(comparison):
    heatmap_data = comparison.set_index("Price range")[[
        "Online_Delivery_Percentage",
        "Table_Booking_Percentage",
    ]]
    heatmap_data.columns = ["Online Delivery (%)", "Table Booking (%)"]

    plt.figure(figsize=(8, 5))
    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt=".2f",
        cmap="YlGnBu",
        vmin=0,
        vmax=100,
    )
    plt.title("Service Availability by Price Range")
    plt.xlabel("Service")
    plt.ylabel("Price Range")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "service_availability_heatmap.png", dpi=300, bbox_inches="tight")
    plt.close()
