# Multiplot Urban Analytics Dashboard V3

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-013243?logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange)
![Version](https://img.shields.io/badge/Release-V3.0-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

> **From Data to Urban Intelligence — Understanding Cities Beyond Numbers.**

## Project Overview

A Python-based urban analytics and data visualization dashboard comparing **Hyderabad and Bengaluru (Bangalore)** across demographic, economic, environmental, educational and technological indicators.

The project combines seven CSV datasets, exploratory data analysis (EDA), numerical computing and multi-page visualization to make complex urban comparisons easier to understand. It expands the original four-chart dashboard into nine analytical categories, with individual chart summaries and an executive comparison report.

[View the complete 11-page PDF report](urban_report_v4.pdf) · [Data sources and limitations](SOURCES.md)

## What's New in V3

| Feature | Previous dashboard | V3 release |
|---|---|---|
| Visualization categories | 4 | 9 |
| CSV datasets | 3 | 7 |
| Dashboard layout | Single page | 11-page interactive report |
| Data coverage | Simulated datasets | Published, estimated and simulated data |
| Analytical summaries | Basic charts | Individual chart summaries and executive table |
| Export | PNG | PDF and optional page-by-page PNG |

### Changelog — V3.0.0

- Expanded comparison of two real-world metropolitan cities: Hyderabad and Bengaluru.
- Added published urban statistics where available, with explicit data-quality flags.
- Added five new visualization categories covering pollution, IT employment, education and food costs, technology ecosystems and institutional infrastructure.
- Introduced interactive keyboard-based page navigation.
- Added chart-specific analytical summaries and an executive comparison table.
- Introduced automated PDF report generation and optional PNG exports.
- Extended CSV loading and validation, and documented data sources and limitations.
- Retained the original dashboard implementation for reference.

## Features and Visualizations

| No. | Visualization | Description |
|---|---|---|
| 1 | Population growth | Compares yearly population trends. |
| 2 | Cost of living | Compares housing, food, transport, utilities and health costs. |
| 3 | Climate variability | Compares daily temperature distributions and average temperatures. |
| 4 | Income vs happiness | Displays household income and happiness scores with linear trend lines. |
| 5 | Air quality | Compares annual PM2.5 levels and the applicable annual standard. |
| 6 | IT employment | Examines employment trends and growth using reported and modelled figures. |
| 7 | Education and food costs | Compares illustrative school fees, engineering fees and food expenses. |
| 8 | Technology ecosystem | Compares Global Capability Centres (GCCs) and related technology indicators. |
| 9 | Institutional infrastructure | Compares illustrative institutional infrastructure indicators. |

## Report Structure

| Pages | Content |
|---|---|
| 1 | Overview of all nine visualization categories |
| 2–10 | Individual chart pages with analytical summaries |
| 11 | Executive comparison table with data-quality information |

## Technologies Used

- **Python** — application logic
- **pandas** — CSV loading, validation and data manipulation
- **NumPy** — numerical calculations and trend analysis
- **Matplotlib** — charts, interactive viewer and PDF export
- **CSV** — structured dataset storage

## Project Files

```text
urban-analytics-dashboard/
├── Multiplotdashboardv4.py       # Expanded dashboard entry point
├── Multiplotdashboardv3.py       # Original four-chart implementation
├── data_loader.py               # Dataset loading and validation
├── city_data.csv
├── city_climate_data.csv
├── city_income_happiness.csv
├── city_environment_data.csv
├── city_economy_data.csv
├── city_education_data.csv
├── city_snapshot_data.csv
├── urban_report_v4.pdf           # Generated report
├── requirements.txt
├── SOURCES.md                    # Data sources and quality notes
└── README.md
```

## Requirements

- Python 3.9 or newer (a currently supported Python version is recommended)
- pip
- Internet access for initial dependency installation
- A graphical desktop session for the interactive viewer

A virtual environment is optional. The following instructions use your regular Python installation.

## Run on Windows

1. Install Python from [python.org](https://www.python.org/downloads/) and enable **Add Python to PATH**.
2. Download or clone this repository.
3. Open the project folder in File Explorer, type `cmd` in the address bar and press Enter.
4. Install dependencies:

   ```bat
   py -m pip install -r requirements.txt
   ```

5. Run the expanded dashboard:

   ```bat
   py Multiplotdashboardv4.py
   ```

If `py` is unavailable, use:

```bat
python -m pip install -r requirements.txt
python Multiplotdashboardv4.py
```

## Run on macOS

Install Python 3 from [python.org](https://www.python.org/downloads/) if needed, then open Terminal in the project folder:

```bash
python3 -m pip install -r requirements.txt
python3 Multiplotdashboardv4.py
```

## Run on Linux

Open a terminal in the project folder:

```bash
python3 -m pip install -r requirements.txt
python3 Multiplotdashboardv4.py
```

If macOS or Linux reports an externally managed Python environment, use a virtual environment instead of forcing a system-wide installation:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python Multiplotdashboardv4.py
```

## Dashboard Controls

| Key | Action |
|---|---|
| Left arrow | Previous page |
| Right arrow | Next page |
| Home | First page |
| End | Last page |

## Output and Report Export

The default command generates `urban_report_v4.pdf` in the project directory and opens the interactive Matplotlib viewer.

Generate only the PDF (without opening the viewer):

```bat
py Multiplotdashboardv4.py --no-show
```

Export all report pages as PNG images in `report_pages/` as well as the PDF:

```bat
py Multiplotdashboardv4.py --png --no-show
```

On macOS and Linux, replace `py` with `python3`.

The original four-chart dashboard can still be run using `py Multiplotdashboardv3.py` on Windows. It exports `urban_dashboard_v3.png`.

## Dataset Documentation

| Dataset | Main fields and purpose |
|---|---|
| `city_data.csv` | Year, city, population, housing, food, transport, utilities and health costs, average income and happiness. |
| `city_climate_data.csv` | Day, city and temperature in Celsius. |
| `city_income_happiness.csv` | Household ID, city, annual income and happiness score. |
| `city_environment_data.csv` | Year, city, PM2.5, CPCB category and data quality. |
| `city_economy_data.csv` | Year, city, IT employment, jobs added, job growth and data quality. |
| `city_education_data.csv` | Year, city, school and engineering fees, food costs, infrastructure index and data quality. |
| `city_snapshot_data.csv` | Metric, city, value, unit, period, data quality and source. |

Keep all seven CSV files beside the Python scripts. The loader locates datasets relative to the script directory rather than a personal computer path.

## Data Sources and Transparency

The project compares real cities, but not every value is a verified real-world statistic.

| Quality flag | Meaning |
|---|---|
| `sourced` | Taken from a published figure documented in SOURCES.md. |
| `estimated` | Modelled, interpolated or back-cast from available figures. |
| `illustrative` | Simulated or placeholder data, not measured statistics. |

The original population, cost-of-living, climate and household income/happiness datasets are illustrative. Education costs and the institutional infrastructure index are also illustrative. IT employment includes state-level proxies and modelled values; some IT export figures are state-level rather than city-level. These limitations matter when interpreting comparisons.

See [SOURCES.md](SOURCES.md) for the documented references, quality classifications and known limitations. The project is an educational analytics demonstration, not an independently verified city ranking.

## Troubleshooting

### Python or py is not recognized

Install Python, enable **Add Python to PATH** on Windows and reopen the terminal.

### No module named pandas, numpy or matplotlib

Install dependencies using the same interpreter that runs the dashboard:

```bat
py -m pip install -r requirements.txt
```

### A CSV file cannot be found

Ensure all seven CSV files are present beside the Python scripts and have their original filenames.

### The chart window does not appear

Use a desktop session with graphical display support, or run with `--no-show` to generate the PDF without opening the viewer.

### PDF cannot be overwritten

Close the existing PDF in your document viewer and try again.

## Future Scope

- Integrate live public data APIs and regularly updated official datasets.
- Replace illustrative datasets with validated measurements.
- Expand comparisons to more Indian metropolitan cities.
- Introduce interactive web-based visualizations and filters.
- Explore forecasting and additional urban sustainability indicators.

## Technical Notes

- Linear trend lines describe the supplied sample and do not establish causation between income and happiness.
- Comparisons should account for differences in geographical coverage, reporting periods and measurement methods.
- Public release name: **V3.0**. The expanded implementation retains the filename `Multiplotdashboardv4.py` to preserve compatibility with the existing project files.

## License

No license has been specified. Add a `LICENSE` file before distributing the project under a particular open-source license.

---

**Multiplot Urban Analytics Dashboard V3** — An exploratory approach to understanding urban differences through data science and visualization.
