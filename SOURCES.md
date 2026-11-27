# Data sources and quality flags (v4 datasets)

Every row in the v4 CSVs has a `data_quality` column:

| Flag | Meaning |
|------|---------|
| sourced | taken from a published figure (listed below) |
| estimated | interpolated or back-cast from sourced anchor points |
| illustrative | placeholder values, NOT real statistics |

The three original files (`city_data.csv`, `city_climate_data.csv`, `city_income_happiness.csv`)
are **illustrative / simulated**. Known weaknesses: population shows Hyderabad overtaking
Bangalore, which does not match reality; income vs happiness is almost a perfect line;
the monthly "₹" costs are far too low for real rupee amounts.

## city_environment_data.csv (annual mean PM2.5, µg/m³)
- 2023 (Hyderabad 38, Bengaluru 33) and the 40 µg/m³ annual standard: Lok Sabha Unstarred
  Question 20, answered 22 Jul 2024 (MoEFCC), Annexure I.
- 2019, 2021, 2024: Respirer Living Sciences, "Towards Clear Skies 2025" (CPCB data).
  Hyderabad 41.6 / 39.7 / 32.4; Bengaluru 35.9 (2019) and 33.0 (2024).
  Note: one Bengaluru paragraph in that report repeats Hyderabad's figures; the 35.9 to 33.0 values were used.
- All other years: estimated (2020 shows a lockdown dip; 2015-2018 back-cast; 2025 held near 2024).
- Replace with: CPCB Central Control Room (CCR) annual city averages.

## city_economy_data.csv (IT employment, lakh; year = fiscal year ending March)
- Hyderabad = **Telangana state** IT/ITeS figures (Hyderabad dominates, but this is a state proxy).
  - FY2013-14: 3,23,396; FY2022-23: 9,05,715 (+1,27,594, +16.29%): state IT dept annual report.
  - FY2023-24: 9.46 lakh (+40,000, +4.5%): Telangana government release.
  - FY2024-25: 9,39,054 (down 7,231): Telangana Socio Economic Outlook 2025.
  - FY2020-21: "more than 6.3 lakh"; FY2021-22: 7,78,121.
  - FY2015-FY2021 growth: estimated (constant growth rate between the 2014 and 2021 anchors).
- Bangalore = **modelled**, anchored to two published points: about 25 lakh IT professionals
  (Karnataka Deputy CM, Nov 2025, a political statement) and +1.46 lakh jobs in the year
  Nasscom measured (quoted by Telangana's IT minister, Jan 2023). Treat as indicative only.
- Replace with: Telangana ICT annual reports (yearly), Nasscom Strategic Review.

## city_snapshot_data.csv
- GCC units (Bengaluru 1,080; Hyderabad 515) and Global 2000 GCC units (320 vs 165): Nasscom-Zinnov GCC Landscape Report 2026.
  Other sources count GCCs differently (e.g. 870+ vs 550 in 2024), so compare only within one source.
- IT exports FY2024-25: Telangana ₹3.13 lakh crore (Socio Economic Outlook 2025); Karnataka ₹4.58 lakh crore
  (IT/BT minister, Assembly). State-level. MeitY/STPI figures use a narrower definition and differ.
- IT companies: Hyderabad "more than 1,500" (2023, Wikipedia). **No comparable Bengaluru count was found**,
  so none is included. "Total companies" is not charted for the same reason.

## city_education_data.csv: ALL ILLUSTRATIVE
School fee, engineering fee, food cost and the infrastructure index are placeholders with
plausible magnitudes. Nothing here was measured. Qualitative context only: NIRF 2025 ranks IISc
Bengaluru #1 among universities and IIT Hyderabad #7 in engineering.
- Replace with: NIRF city-wise institution counts for the infrastructure score; state fee-regulatory
  committee notifications for tuition; a cost-of-living survey for food.
