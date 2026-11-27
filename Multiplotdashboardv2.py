import sys

import matplotlib.pyplot as plt
import numpy as np

from data_loader import load_all_data


COLOR_HYD = "#1f77b4"
COLOR_BLR = "#ff7f0e"


def get_population_data(yearly_df):
    """Return year and population arrays for Hyderabad and Bangalore."""
    hyd = yearly_df[yearly_df["city"] == "Hyderabad"].sort_values("year")
    blr = yearly_df[yearly_df["city"] == "Bangalore"].sort_values("year")
    if hyd.empty or blr.empty:
        raise ValueError("Yearly data must include both Hyderabad and Bangalore.")
    return (
        hyd["year"].to_numpy(),
        hyd["population"].to_numpy(),
        blr["year"].to_numpy(),
        blr["population"].to_numpy(),
    )


def get_cost_of_living_data(yearly_df):
    """Return latest-year monthly costs for both cities."""
    latest_year = yearly_df["year"].max()
    latest = yearly_df[yearly_df["year"] == latest_year]
    hyd = latest[latest["city"] == "Hyderabad"]
    blr = latest[latest["city"] == "Bangalore"]
    if hyd.empty or blr.empty:
        raise ValueError(f"Year {latest_year} must contain both cities.")
    categories = ["Housing", "Food", "Transport", "Utilities", "Health"]
    columns = ["housing_cost", "food_cost", "transport_cost",
               "utilities_cost", "health_cost"]
    return categories, hyd.iloc[0][columns].to_numpy(), blr.iloc[0][columns].to_numpy(), latest_year


def get_climate_data(climate_df):
    """Return daily temperature arrays for both cities."""
    hyd = climate_df.loc[climate_df["city"] == "Hyderabad", "temperature_celsius"].to_numpy()
    blr = climate_df.loc[climate_df["city"] == "Bangalore", "temperature_celsius"].to_numpy()
    if len(hyd) == 0 or len(blr) == 0:
        raise ValueError("Climate data must include both Hyderabad and Bangalore.")
    return hyd, blr


def get_income_happiness_data(income_df):
    """Return income and happiness arrays for both cities."""
    hyd = income_df[income_df["city"] == "Hyderabad"]
    blr = income_df[income_df["city"] == "Bangalore"]
    if hyd.empty or blr.empty:
        raise ValueError("Income-happiness data must include both cities.")
    return (
        (hyd["annual_income"].to_numpy(), hyd["happiness_score"].to_numpy()),
        (blr["annual_income"].to_numpy(), blr["happiness_score"].to_numpy()),
    )


def plot_population(ax, yearly_df):
    hyd_years, hyd_pop, blr_years, blr_pop = get_population_data(yearly_df)
    ax.plot(hyd_years, hyd_pop, marker="o", color=COLOR_HYD, label="Hyderabad", linewidth=2)
    ax.plot(blr_years, blr_pop, marker="s", color=COLOR_BLR, label="Bangalore", linewidth=2)
    ax.set_title("Population Growth")
    ax.set_xlabel("Year")
    ax.set_ylabel("Population")
    ax.legend()
    ax.grid(alpha=0.3)
    ax.ticklabel_format(axis="y", style="plain")
    ax.annotate(f"{hyd_pop[-1] / 1e6:.1f}M", (hyd_years[-1], hyd_pop[-1]), fontsize=9)
    ax.annotate(f"{blr_pop[-1] / 1e6:.1f}M", (blr_years[-1], blr_pop[-1]), fontsize=9)


def plot_cost_of_living(ax, yearly_df):
    categories, hyd_costs, blr_costs, latest_year = get_cost_of_living_data(yearly_df)
    x = np.arange(len(categories))
    width = 0.35
    ax.bar(x - width / 2, hyd_costs, width, color=COLOR_HYD, label="Hyderabad")
    ax.bar(x + width / 2, blr_costs, width, color=COLOR_BLR, label="Bangalore")
    ax.set_title(f"Cost of Living Comparison ({latest_year})")
    ax.set_xlabel("Category")
    ax.set_ylabel("Monthly Cost (₹)")
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=20)
    ax.legend()
    ax.grid(alpha=0.3, axis="y")


def plot_climate(ax, climate_df):
    hyd_temps, blr_temps = get_climate_data(climate_df)
    ax.hist(hyd_temps, bins=25, alpha=0.6, color=COLOR_HYD, label="Hyderabad")
    ax.hist(blr_temps, bins=25, alpha=0.6, color=COLOR_BLR, label="Bangalore")
    hyd_mean, blr_mean = np.mean(hyd_temps), np.mean(blr_temps)
    ax.axvline(hyd_mean, color=COLOR_HYD, linestyle="--", linewidth=2,
               label=f"Hyderabad mean: {hyd_mean:.1f}°C")
    ax.axvline(blr_mean, color=COLOR_BLR, linestyle="--", linewidth=2,
               label=f"Bangalore mean: {blr_mean:.1f}°C")
    ax.set_title("Climate Variability")
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Frequency (days)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)


def add_trend_line(ax, incomes, happiness, color):
    """Add a linear trend only when there are enough distinct income values."""
    if len(incomes) >= 2 and len(np.unique(incomes)) >= 2:
        order = np.argsort(incomes)
        coefficients = np.polyfit(incomes, happiness, 1)
        ax.plot(incomes[order], np.polyval(coefficients, incomes[order]),
                color=color, linestyle="--", linewidth=2, alpha=0.8)


def plot_income_happiness(ax, income_df):
    (hyd_income, hyd_happiness), (blr_income, blr_happiness) = get_income_happiness_data(income_df)
    ax.scatter(hyd_income, hyd_happiness, color=COLOR_HYD, alpha=0.7, s=35, label="Hyderabad")
    ax.scatter(blr_income, blr_happiness, color=COLOR_BLR, alpha=0.7, s=35, label="Bangalore")
    add_trend_line(ax, hyd_income, hyd_happiness, COLOR_HYD)
    add_trend_line(ax, blr_income, blr_happiness, COLOR_BLR)
    ax.set_title("Income vs Happiness")
    ax.set_xlabel("Annual Income (₹)")
    ax.set_ylabel("Happiness Score (1–10)")
    ax.legend()
    ax.grid(alpha=0.3)


def build_dashboard(yearly_df, climate_df, income_df):
    """Build the four-chart urban analytics dashboard."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Urban Analytics Dashboard: Hyderabad vs Bangalore",
                 fontsize=16, fontweight="bold")
    plot_population(axes[0, 0], yearly_df)
    plot_cost_of_living(axes[0, 1], yearly_df)
    plot_climate(axes[1, 0], climate_df)
    plot_income_happiness(axes[1, 1], income_df)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    return fig


def main():
    yearly_df, climate_df, income_df = load_all_data()
    if any(df is None for df in (yearly_df, climate_df, income_df)):
        return 1

    try:
        figure = build_dashboard(yearly_df, climate_df, income_df)
    except (ValueError, KeyError) as error:
        print(f"Could not build dashboard: {error}")
        return 1

    output_file = "urban_dashboard_v3.png"
    figure.savefig(output_file, dpi=150, bbox_inches="tight")
    print(f"Dashboard saved to: {output_file}")
    plt.show()
    return 0


if __name__ == "__main__":
    sys.exit(main())
