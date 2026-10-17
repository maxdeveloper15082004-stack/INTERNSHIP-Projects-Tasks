import pandas as pd


def analyze_restaurant_chains(df):
    chain_analysis = (
        df.groupby("Restaurant Name")
        .agg(
            outlet_count=("Restaurant Name", "size"),
            average_rating=("Aggregate rating", "mean"),
            total_votes=("Votes", "sum"),
            average_votes=("Votes", "mean"),
            cities=("City", "nunique"),
            rated_outlets=("Aggregate rating", "count")
        )
        .reset_index()
    )

    chains = chain_analysis[
        chain_analysis["outlet_count"] > 1
    ].copy()

    chains = chains.sort_values(
        by="outlet_count",
        ascending=False
    )

    highest_rated = chains[
        chains["rated_outlets"] >= 3
    ].sort_values(
        by=["average_rating", "rated_outlets"],
        ascending=[False, False]
    )

    most_popular = chains.sort_values(
        by="total_votes",
        ascending=False
    )

    top_chains = chains.head(10)

    print("\n========== RESTAURANT CHAIN ANALYSIS ==========")

    print(f"\nTotal unique restaurant names: {df['Restaurant Name'].nunique()}")

    print(f"Potential restaurant chains found: {len(chains)}")

    print("\nTop 10 Chains by Number of Outlets:")
    print(
        top_chains[
            [
                "Restaurant Name",
                "outlet_count",
                "average_rating",
                "total_votes"
            ]
        ].to_string(index=False)
    )

    print("\nTop 10 Chains by Average Rating:")
    print(
        highest_rated[
            [
                "Restaurant Name",
                "outlet_count",
                "average_rating",
                "total_votes"
            ]
        ].head(10).to_string(index=False)
    )

    print("\nTop 10 Chains by Total Votes:")
    print(
        most_popular[
            [
                "Restaurant Name",
                "outlet_count",
                "average_rating",
                "total_votes"
            ]
        ].head(10).to_string(index=False)
    )

    return chains, top_chains, highest_rated, most_popular
