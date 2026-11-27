from pathlib import Path

import pandas as pd


# Keep the CSV files beside this Python file so the project works from any
# terminal working directory.
DATA_DIR = Path(__file__).resolve().parent


def load_csv(filename, label):
    """Load one CSV file from the project folder."""
    filepath = DATA_DIR / filename

    if not filepath.is_file():
        print(f"ERROR: Could not find {filename} in {DATA_DIR}")
        return None

    try:
        df = pd.read_csv(filepath)
        print(f"Loaded {label}: {len(df)} rows ({filename})")
        return df
    except (OSError, pd.errors.ParserError, UnicodeDecodeError) as error:
        print(f"ERROR: Could not read {filename}: {error}")
        return None


def validate_columns(df, required_columns, label):
    """Check that a DataFrame exists and contains the required columns."""
    if df is None:
        return False

    missing = [column for column in required_columns if column not in df.columns]
    if missing:
        print(f"ERROR: {label} is missing required columns: {', '.join(missing)}")
        return False

    if df[required_columns].isnull().any().any():
        print(f"ERROR: {label} contains missing values in required columns.")
        return False

    print(f"Validated {label}.")
    return True


def load_yearly_data(filename="city_data.csv"):
    """Load yearly population, cost, income, and happiness data."""
    return load_csv(filename, "yearly city data")


def validate_yearly_data(df):
    required = [
        "year", "city", "population", "housing_cost", "food_cost",
        "transport_cost", "utilities_cost", "health_cost", "avg_income",
        "avg_happiness",
    ]
    numeric = [
        "year", "population", "housing_cost", "food_cost", "transport_cost",
        "utilities_cost", "health_cost", "avg_income", "avg_happiness",
    ]
    if not validate_columns(df, required, "yearly city data"):
        return False
    for column in numeric:
        if not pd.api.types.is_numeric_dtype(df[column]):
            print(f"ERROR: Column '{column}' in yearly data must be numeric.")
            return False
    return True


def load_climate_data(filename="city_climate_data.csv"):
    """Load daily temperature data."""
    return load_csv(filename, "climate data")


def validate_climate_data(df):
    required = ["day", "city", "temperature_celsius"]
    if not validate_columns(df, required, "climate data"):
        return False
    if not pd.api.types.is_numeric_dtype(df["temperature_celsius"]):
        print("ERROR: 'temperature_celsius' must be numeric.")
        return False
    return True


def load_income_happiness_data(filename="city_income_happiness.csv"):
    """Load household income and happiness data."""
    return load_csv(filename, "income-happiness data")


def validate_income_happiness_data(df):
    required = ["household_id", "city", "annual_income", "happiness_score"]
    if not validate_columns(df, required, "income-happiness data"):
        return False
    for column in ["household_id", "annual_income", "happiness_score"]:
        if not pd.api.types.is_numeric_dtype(df[column]):
            print(f"ERROR: Column '{column}' must be numeric.")
            return False
    return True


def load_all_data():
    """Load all datasets and return them only when all are valid."""
    print("\nLoading project datasets...\n")

    yearly_df = load_yearly_data()
    climate_df = load_climate_data()
    income_df = load_income_happiness_data()

    checks = [
        validate_yearly_data(yearly_df),
        validate_climate_data(climate_df),
        validate_income_happiness_data(income_df),
    ]

    if not all(checks):
        print("\nOne or more datasets are missing or invalid.")
        print("Check that all three CSV files are in the project folder.")
        return None, None, None

    print("\nAll datasets loaded and validated successfully.\n")
    return yearly_df, climate_df, income_df


# ---------------------------------------------------------------------------
# v4 additions: environment, economy, education and snapshot datasets
# ---------------------------------------------------------------------------
def _check_numeric(df, columns, label):
    for column in columns:
        if not pd.api.types.is_numeric_dtype(df[column]):
            print(f"ERROR: Column '{column}' in {label} must be numeric.")
            return False
    return True


def load_environment_data(filename="city_environment_data.csv"):
    """Load yearly air-quality (PM2.5) data."""
    return load_csv(filename, "environment data")


def validate_environment_data(df):
    required = ["year", "city", "pm25_ugm3", "cpcb_category", "data_quality"]
    return (validate_columns(df, required, "environment data")
            and _check_numeric(df, ["year", "pm25_ugm3"], "environment data"))


def load_economy_data(filename="city_economy_data.csv"):
    """Load yearly IT employment and job-growth data."""
    return load_csv(filename, "economy data")


def validate_economy_data(df):
    required = ["year", "city", "it_employment_lakh", "jobs_added_lakh",
                "job_growth_pct", "data_quality"]
    return (validate_columns(df, required, "economy data")
            and _check_numeric(df, required[2:5], "economy data"))


def load_education_data(filename="city_education_data.csv"):
    """Load yearly education-cost, food-cost and institution-infrastructure data."""
    return load_csv(filename, "education data")


def validate_education_data(df):
    required = ["year", "city", "school_fee_annual_inr", "engineering_fee_annual_inr",
                "food_cost_monthly_inr", "institution_infra_index", "data_quality"]
    return (validate_columns(df, required, "education data")
            and _check_numeric(df, required[2:6], "education data"))


def load_snapshot_data(filename="city_snapshot_data.csv"):
    """Load single-year snapshot metrics (GCC units, IT exports, ...)."""
    return load_csv(filename, "snapshot data")


def validate_snapshot_data(df):
    required = ["metric", "city", "value", "unit", "period", "data_quality", "source"]
    return (validate_columns(df, required, "snapshot data")
            and _check_numeric(df, ["value"], "snapshot data"))


def load_extended_data():
    """Load all seven datasets. Returns a dict, or None if any is invalid."""
    yearly, climate, income = load_all_data()
    if any(df is None for df in (yearly, climate, income)):
        return None

    env = load_environment_data()
    econ = load_economy_data()
    edu = load_education_data()
    snap = load_snapshot_data()

    checks = [validate_environment_data(env), validate_economy_data(econ),
              validate_education_data(edu), validate_snapshot_data(snap)]
    if not all(checks):
        print("\nOne or more v4 datasets are missing or invalid.")
        return None

    print("All v4 datasets loaded and validated successfully.\n")
    return {"yearly": yearly, "climate": climate, "income": income,
            "env": env, "econ": econ, "edu": edu, "snap": snap}


if __name__ == "__main__":
    yearly, climate, income = load_all_data()
    for label, dataframe in [
        ("Yearly city data", yearly),
        ("Climate data", climate),
        ("Income-happiness data", income),
    ]:
        if dataframe is not None:
            print(f"\n{label} — first 3 rows:")
            print(dataframe.head(3).to_string(index=False))
