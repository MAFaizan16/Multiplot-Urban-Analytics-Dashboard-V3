"""
Urban Analytics Report v4: Hyderabad vs Bangalore

Pages
  1      Overview (all 9 charts on one page)
  2-10   One FULL PAGE per chart: big chart on the left, a data-driven
         summary panel on the right
  11     Executive summary table

Run:
    python3 Multiplotdashboardv4.py            # saves PDF, opens page viewer
    python3 Multiplotdashboardv4.py --no-show  # only saves the PDF
    python3 Multiplotdashboardv4.py --png      # also saves every page as PNG

Viewer keys:  Right / Left = next / previous page,  Home / End = first / last,  Q = quit
"""

import sys
import textwrap
from pathlib import Path

import matplotlib

if "--no-show" in sys.argv:          # headless run: no window needed
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Patch

import Multiplotdashboardv3 as v3          # re-use the four original charts
from data_loader import load_extended_data

HYD, BLR = "Hyderabad", "Bangalore"
C_HYD, C_BLR = v3.COLOR_HYD, v3.COLOR_BLR
PM25_STANDARD = 40          # CPCB annual PM2.5 standard, ug/m3
OUT_DIR = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
def city_rows(df, city):
    return df[df["city"] == city].sort_values("year")


def pct_change(start, end):
    return (end - start) / start * 100


def snap_value(snap, metric, city):
    row = snap[(snap["metric"] == metric) & (snap["city"] == city)]
    return float(row["value"].iloc[0]) if not row.empty else None


def quality_line(ax, df, column):
    """Line chart where filled markers = sourced, hollow markers = not sourced."""
    for city, color, marker in ((HYD, C_HYD, "o"), (BLR, C_BLR, "s")):
        c = city_rows(df, city)
        x, y = c["year"].to_numpy(), c[column].to_numpy()
        solid = (c["data_quality"] == "sourced").to_numpy()
        ax.plot(x, y, color=color, linewidth=2, label=city)
        ax.scatter(x[solid], y[solid], color=color, marker=marker, s=55, zorder=3)
        ax.scatter(x[~solid], y[~solid], facecolors="white", edgecolors=color,
                   marker=marker, s=55, linewidths=1.6, zorder=3)
    handles, _ = ax.get_legend_handles_labels()
    handles += [
        Line2D([], [], marker="o", linestyle="", color="grey", label="sourced"),
        Line2D([], [], marker="o", linestyle="", markerfacecolor="white",
               markeredgecolor="grey", label="estimated / illustrative"),
    ]
    ax.legend(handles=handles, fontsize=8)
    ax.grid(alpha=0.3)


# ---------------------------------------------------------------------------
# New charts (chart functions take the shared data dict)
# ---------------------------------------------------------------------------
def plot_air_quality(ax, d):
    quality_line(ax, d["env"], "pm25_ugm3")
    ax.axhline(PM25_STANDARD, color="red", linestyle=":", linewidth=1.5)
    ax.text(d["env"]["year"].min(), PM25_STANDARD + 0.4, "Annual standard (40)",
            color="red", fontsize=8)
    ax.set_title("Air Quality: Annual PM2.5")
    ax.set_xlabel("Year")
    ax.set_ylabel("PM2.5 (µg/m³)  lower = cleaner")


def plot_job_growth(ax, d):
    econ = d["econ"]
    years = sorted(econ["year"].unique())
    x, width = np.arange(len(years)), 0.38
    for offset, city, color in ((-width / 2, HYD, C_HYD), (width / 2, BLR, C_BLR)):
        c = city_rows(econ, city)
        bars = ax.bar(x + offset, c["job_growth_pct"], width, color=color, label=city)
        for bar, quality in zip(bars, c["data_quality"]):
            if quality != "sourced":
                bar.set_hatch("///")
                bar.set_edgecolor("white")
    handles = [Patch(facecolor=C_HYD, label=HYD), Patch(facecolor=C_BLR, label=BLR),
               Patch(facecolor="grey", label="sourced"),
               Patch(facecolor="grey", hatch="///", edgecolor="white", label="estimated")]
    ax.legend(handles=handles, fontsize=8)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(years, rotation=45)
    ax.set_title("IT Job Growth per Year")
    ax.set_xlabel("Fiscal year (ending March)")
    ax.set_ylabel("Growth in IT employment (%)")
    ax.grid(alpha=0.3, axis="y")


def education_values(edu, city):
    latest = edu["year"].max()
    r = edu[(edu["city"] == city) & (edu["year"] == latest)].iloc[0]
    return latest, [r["school_fee_annual_inr"], r["engineering_fee_annual_inr"],
                    r["food_cost_monthly_inr"] * 12]


def plot_education_cost(ax, d):
    latest, hyd = education_values(d["edu"], HYD)
    _, blr = education_values(d["edu"], BLR)
    labels = ["School fee\n(per year)", "Engineering fee\n(per year)", "Food\n(12 months)"]
    x, width = np.arange(3), 0.35
    b1 = ax.bar(x - width / 2, np.array(hyd) / 1000, width, color=C_HYD, label=HYD)
    b2 = ax.bar(x + width / 2, np.array(blr) / 1000, width, color=C_BLR, label=BLR)
    ax.bar_label(b1, fmt="%.0f", fontsize=8, padding=2)
    ax.bar_label(b2, fmt="%.0f", fontsize=8, padding=2)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.margins(y=0.12)
    ax.set_title(f"Education & Food Costs ({latest}, illustrative)")
    ax.set_ylabel("₹ thousand per year")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, axis="y")


def plot_tech_ecosystem(ax, d):
    snap = d["snap"]
    metrics = [("gcc_units", "All GCC units"), ("global2000_gcc_units", "Global 2000\nGCC units")]
    x, width = np.arange(len(metrics)), 0.35
    hyd = [snap_value(snap, m, HYD) for m, _ in metrics]
    blr = [snap_value(snap, m, BLR) for m, _ in metrics]
    b1 = ax.bar(x - width / 2, hyd, width, color=C_HYD, label=HYD)
    b2 = ax.bar(x + width / 2, blr, width, color=C_BLR, label=BLR)
    ax.bar_label(b1, fmt="%.0f", fontsize=9, padding=2)
    ax.bar_label(b2, fmt="%.0f", fontsize=9, padding=2)
    ax.set_xticks(x)
    ax.set_xticklabels([label for _, label in metrics])
    ax.margins(y=0.12)
    ax.set_title("Tech Ecosystem: GCC Units (FY2026E)")
    ax.set_ylabel("Number of units")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, axis="y")


def plot_institution_infra(ax, d):
    quality_line(ax, d["edu"], "institution_infra_index")
    ax.set_title("Institution Infrastructure Index (illustrative)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Index (0-100)")


# ---------------------------------------------------------------------------
# Summaries: every number is computed from the data, nothing is hard-coded
# ---------------------------------------------------------------------------
def summary_population(d):
    h, b = city_rows(d["yearly"], HYD), city_rows(d["yearly"], BLR)
    h0, h1 = h["population"].iloc[0], h["population"].iloc[-1]
    b0, b1 = b["population"].iloc[0], b["population"].iloc[-1]
    y0, y1 = int(h["year"].iloc[0]), int(h["year"].iloc[-1])
    gh, gb = pct_change(h0, h1), pct_change(b0, b1)
    bigger = HYD if h1 > b1 else BLR
    faster = HYD if gh > gb else BLR
    return dict(
        shows="Population of each city over time. A steeper line means faster growth.",
        numbers=[f"Hyderabad: {h0/1e6:.1f}M to {h1/1e6:.1f}M ({gh:+.0f}%)",
                 f"Bangalore: {b0/1e6:.1f}M to {b1/1e6:.1f}M ({gb:+.0f}%)",
                 f"Larger city in {y1}: {bigger} by {abs(h1-b1)/1e6:.1f}M"],
        takeaway=f"{faster} grew faster between {y0} and {y1} ({max(gh,gb):.0f}% vs {min(gh,gb):.0f}%).",
        quality="Illustrative (simulated) data, not census figures.")


def summary_cost_of_living(d):
    y = d["yearly"]
    latest = y["year"].max()
    cols = {"Housing": "housing_cost", "Food": "food_cost", "Transport": "transport_cost",
            "Utilities": "utilities_cost", "Health": "health_cost"}
    h = y[(y["city"] == HYD) & (y["year"] == latest)].iloc[0]
    b = y[(y["city"] == BLR) & (y["year"] == latest)].iloc[0]
    th, tb = sum(h[c] for c in cols.values()), sum(b[c] for c in cols.values())
    gap = {k: abs(h[c] - b[c]) for k, c in cols.items()}
    biggest = max(gap, key=gap.get)
    cheaper = HYD if th < tb else BLR
    return dict(
        shows=f"Monthly cost by category for {latest}. Shorter bar = cheaper.",
        numbers=[f"Total per month: Hyderabad ₹{th:,.0f}, Bangalore ₹{tb:,.0f}",
                 f"Biggest gap: {biggest} (₹{gap[biggest]:,.0f})",
                 f"Overall difference: {abs(th-tb)/max(th,tb)*100:.0f}%"],
        takeaway=f"{cheaper} is cheaper overall, mostly because of {biggest.lower()}.",
        quality="Illustrative (simulated) data. Values are too low to be real rupee costs.")


def summary_climate(d):
    c = d["climate"]
    h = c[c["city"] == HYD]["temperature_celsius"]
    b = c[c["city"] == BLR]["temperature_celsius"]
    hotter = HYD if h.mean() > b.mean() else BLR
    wider = HYD if h.std() > b.std() else BLR
    return dict(
        shows="How often each daily temperature occurs. Wider histogram = more variable weather.",
        numbers=[f"Hyderabad: mean {h.mean():.1f}°C, range {h.min():.0f} to {h.max():.0f}°C",
                 f"Bangalore: mean {b.mean():.1f}°C, range {b.min():.0f} to {b.max():.0f}°C",
                 f"Spread (std dev): Hyderabad {h.std():.1f}, Bangalore {b.std():.1f}"],
        takeaway=f"{hotter} is hotter on average; {wider} has the less stable weather.",
        quality="Illustrative (simulated) daily temperatures for one year.")


def summary_income_happiness(d):
    inc = d["income"]
    lines, corrs = [], {}
    for city in (HYD, BLR):
        s = inc[inc["city"] == city]
        x, y = s["annual_income"].to_numpy(), s["happiness_score"].to_numpy()
        r = np.corrcoef(x, y)[0, 1]
        slope = np.polyfit(x, y, 1)[0] * 10000
        corrs[city] = r
        lines.append(f"{city}: r = {r:.2f}, +{slope:.2f} happiness per ₹10,000")
    stronger = max(corrs, key=corrs.get)
    return dict(
        shows="Each dot is a household. The dashed line is the straight-line trend.",
        numbers=lines,
        takeaway=f"Income and happiness rise together in both cities; the link is stronger in {stronger}. "
                 "This shows association, not proof that income causes happiness.",
        quality="Illustrative (simulated) household data.")


def summary_air_quality(d):
    e = d["env"]
    last_src = int(e[e["data_quality"] == "sourced"]["year"].max())
    h, b = city_rows(e, HYD), city_rows(e, BLR)
    hv = h[h["year"] == last_src]["pm25_ugm3"].iloc[0]
    bv = b[b["year"] == last_src]["pm25_ugm3"].iloc[0]
    h19 = h[h["year"] == 2019]["pm25_ugm3"].iloc[0]
    b19 = b[b["year"] == 2019]["pm25_ugm3"].iloc[0]
    n = len(h)
    ah, ab = int((h["pm25_ugm3"] > PM25_STANDARD).sum()), int((b["pm25_ugm3"] > PM25_STANDARD).sum())
    cleaner = HYD if hv < bv else BLR
    ch, cb = pct_change(h19, hv), pct_change(b19, bv)
    improver = HYD if ch < cb else BLR
    return dict(
        shows="Yearly average of fine particles (PM2.5). Lower is better; the red line is the 40 µg/m³ standard.",
        numbers=[f"{last_src} (latest sourced): Hyderabad {hv:.1f}, Bangalore {bv:.1f} µg/m³",
                 f"Change 2019 to {last_src}: Hyderabad {pct_change(h19, hv):+.0f}%, Bangalore {pct_change(b19, bv):+.0f}%",
                 f"Years above the standard: Hyderabad {ah}, Bangalore {ab} (of {n})"],
        takeaway=f"{cleaner} had cleaner air in {last_src}. {improver} improved more since 2019 "
                 f"({min(ch, cb):+.0f}% vs {max(ch, cb):+.0f}%).",
        quality="Filled markers are published figures (CPCB data via a Parliament reply and the Respirer 2025 report). "
                "Hollow markers are estimated.")


def summary_job_growth(d):
    e = d["econ"]
    h, b = city_rows(e, HYD), city_rows(e, BLR)
    y1 = int(h["year"].max())
    hs = h[h["data_quality"] == "sourced"]
    peak = hs.loc[hs["job_growth_pct"].idxmax()]
    hl, bl = h.iloc[-1], b.iloc[-1]
    return dict(
        shows="Yearly growth in IT jobs. Hatched bars are estimated; solid bars are published figures.",
        numbers=[f"Hyderabad {y1}: {hl['job_growth_pct']:+.1f}% (about {hl['jobs_added_lakh']*100000:+,.0f} jobs)",
                 f"Hyderabad peak: {peak['job_growth_pct']:.1f}% in {int(peak['year'])}",
                 f"Bangalore {y1} (estimated): {bl['job_growth_pct']:+.1f}%"],
        takeaway=f"Hyderabad's IT hiring slowed sharply from its {int(peak['year'])} peak and "
                 f"turned slightly negative in {y1}.",
        quality="Hyderabad = Telangana state IT/ITeS figures (state reports). Bangalore is modelled from two "
                "published anchors, so treat it as indicative.")


def summary_education(d):
    latest, hv = education_values(d["edu"], HYD)
    _, bv = education_values(d["edu"], BLR)
    names = ["School fee", "Engineering fee", "Food (12 months)"]
    lines = [f"{n}: Hyderabad ₹{a:,.0f}, Bangalore ₹{b:,.0f}" for n, a, b in zip(names, hv, bv)]
    cheaper = HYD if sum(hv) < sum(bv) else BLR
    return dict(
        shows=f"Typical yearly spending on schooling, engineering education and food ({latest}).",
        numbers=lines,
        takeaway=f"{cheaper} is cheaper on all three, by {abs(sum(hv)-sum(bv))/max(sum(hv),sum(bv))*100:.0f}% combined.",
        quality="ILLUSTRATIVE placeholder values, not real statistics. Replace with fee-regulator / survey data.")


def summary_tech(d):
    s = d["snap"]
    gh, gb = snap_value(s, "gcc_units", HYD), snap_value(s, "gcc_units", BLR)
    g2h, g2b = snap_value(s, "global2000_gcc_units", HYD), snap_value(s, "global2000_gcc_units", BLR)
    eh, eb = snap_value(s, "it_exports_lakh_crore", HYD), snap_value(s, "it_exports_lakh_crore", BLR)
    ic = snap_value(s, "it_companies", HYD)
    return dict(
        shows="A GCC (global capability centre) is a company's in-house tech or back-office unit in India.",
        numbers=[f"GCC units: Hyderabad {gh:.0f}, Bangalore {gb:.0f} ({gb/gh:.1f}x)",
                 f"Global 2000 GCC units: {g2h:.0f} vs {g2b:.0f}",
                 f"IT exports FY25 (state level): ₹{eh:.2f} vs ₹{eb:.2f} lakh crore",
                 f"IT companies: Hyderabad {ic:,.0f}+; no comparable Bangalore count found"],
        takeaway=f"Bangalore hosts about {gb/gh:.1f}x as many GCC units as Hyderabad.",
        quality="Sourced: Nasscom-Zinnov GCC Landscape Report 2026 and state government releases.")


def summary_infra(d):
    e = d["edu"]
    h, b = city_rows(e, HYD), city_rows(e, BLR)
    y0, y1 = int(h["year"].iloc[0]), int(h["year"].iloc[-1])
    hg = h["institution_infra_index"].iloc[-1] - h["institution_infra_index"].iloc[0]
    bg = b["institution_infra_index"].iloc[-1] - b["institution_infra_index"].iloc[0]
    return dict(
        shows="A 0-100 score for the quality of campuses, labs and facilities in each city.",
        numbers=[f"{y1}: Hyderabad {h['institution_infra_index'].iloc[-1]:.0f}, Bangalore {b['institution_infra_index'].iloc[-1]:.0f}",
                 f"Gain since {y0}: Hyderabad +{hg:.0f}, Bangalore +{bg:.0f}"],
        takeaway="Hyderabad is catching up, but Bangalore still leads on this index.",
        quality="ILLUSTRATIVE index, not measured. A better version: count each city's institutions in NIRF rankings.")


# ---------------------------------------------------------------------------
# Chart registry: one entry per visualiser
# ---------------------------------------------------------------------------
CHARTS = [
    dict(title="Population Growth", plot=lambda ax, d: v3.plot_population(ax, d["yearly"]), summary=summary_population),
    dict(title="Cost of Living", plot=lambda ax, d: v3.plot_cost_of_living(ax, d["yearly"]), summary=summary_cost_of_living),
    dict(title="Climate Variability", plot=lambda ax, d: v3.plot_climate(ax, d["climate"]), summary=summary_climate),
    dict(title="Income vs Happiness", plot=lambda ax, d: v3.plot_income_happiness(ax, d["income"]), summary=summary_income_happiness),
    dict(title="Air Quality (PM2.5)", plot=plot_air_quality, summary=summary_air_quality),
    dict(title="IT Job Growth", plot=plot_job_growth, summary=summary_job_growth),
    dict(title="Education & Food Costs", plot=plot_education_cost, summary=summary_education),
    dict(title="Tech Ecosystem (GCCs)", plot=plot_tech_ecosystem, summary=summary_tech),
    dict(title="Institution Infrastructure", plot=plot_institution_infra, summary=summary_infra),
]


# ---------------------------------------------------------------------------
# Page builders: each one draws onto a figure it is given
# ---------------------------------------------------------------------------
def draw_panel(ax, s):
    """Summary panel: rounded box with four labelled sections."""
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.03",
                                transform=ax.transAxes, facecolor="#f4f6fa",
                                edgecolor="#c9d1e0", linewidth=1.2))
    state = {"y": 0.965}

    def section(heading, lines, bullet=False):
        ax.text(0.06, state["y"], heading, transform=ax.transAxes, va="top",
                fontsize=9.5, fontweight="bold", color="#1f3a5f")
        state["y"] -= 0.05
        for line in lines:
            wrapped = textwrap.wrap(line, width=37,
                                    initial_indent="• " if bullet else "",
                                    subsequent_indent="  " if bullet else "")
            ax.text(0.06, state["y"], "\n".join(wrapped), transform=ax.transAxes,
                    va="top", fontsize=9.5, linespacing=1.35, color="#222222")
            state["y"] -= 0.034 * len(wrapped) + 0.012
        state["y"] -= 0.025

    section("WHAT THIS SHOWS", [s["shows"]])
    section("KEY NUMBERS", s["numbers"], bullet=True)
    section("TAKEAWAY", [s["takeaway"]])
    section("DATA QUALITY", [s["quality"]])


def build_chart_page(fig, chart, data):
    gs = fig.add_gridspec(1, 2, width_ratios=[2.1, 1], left=0.06, right=0.97,
                          top=0.88, bottom=0.10, wspace=0.10)
    ax = fig.add_subplot(gs[0])
    chart["plot"](ax, data)
    ax.title.set_fontsize(14)
    draw_panel(fig.add_subplot(gs[1]), chart["summary"](data))
    fig.suptitle(chart["title"], fontsize=18, fontweight="bold", x=0.06, ha="left", y=0.965)


def build_overview(fig, data):
    fig.suptitle("Urban Analytics Overview: Hyderabad vs Bangalore",
                 fontsize=17, fontweight="bold", y=0.985)
    with plt.rc_context({"font.size": 7, "axes.titlesize": 9, "axes.labelsize": 7.5,
                         "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 6}):
        axes = fig.subplots(3, 3).flatten()
        for ax, chart in zip(axes, CHARTS):
            chart["plot"](ax, data)
            for leg in [ax.get_legend()]:
                if leg:
                    for text in leg.get_texts():
                        text.set_fontsize(6)
    fig.tight_layout(rect=[0, 0.02, 1, 0.95])


def build_executive_summary(fig, data):
    y, e, ed, snap, env, econ, inc, clim = (data["yearly"], None, data["edu"], data["snap"],
                                            data["env"], data["econ"], data["income"], data["climate"])
    latest = y["year"].max()

    def cost_total(city):
        r = y[(y["city"] == city) & (y["year"] == latest)].iloc[0]
        return sum(r[c] for c in ["housing_cost", "food_cost", "transport_cost",
                                  "utilities_cost", "health_cost"])

    def last(df, city, col):
        return city_rows(df, city)[col].iloc[-1]

    last_src = int(env[env["data_quality"] == "sourced"]["year"].max())
    pm = lambda c: env[(env["city"] == c) & (env["year"] == last_src)]["pm25_ugm3"].iloc[0]
    temp = lambda c, f: f(clim[clim["city"] == c]["temperature_celsius"])

    # (label, hyd, bangalore, better, fmt, data note)
    rows = [
        (f"Population {latest} (millions)", last(y, HYD, "population") / 1e6, last(y, BLR, "population") / 1e6, None, "{:.1f}", "illustrative"),
        ("Total monthly living cost (₹)", cost_total(HYD), cost_total(BLR), "low", "{:,.0f}", "illustrative"),
        ("Average income (₹)", last(y, HYD, "avg_income"), last(y, BLR, "avg_income"), "high", "{:,.0f}", "illustrative"),
        ("Mean temperature (°C)", temp(HYD, np.mean), temp(BLR, np.mean), None, "{:.1f}", "illustrative"),
        ("Temperature spread (std, °C)", temp(HYD, np.std), temp(BLR, np.std), "low", "{:.1f}", "illustrative"),
        (f"PM2.5 {last_src} (µg/m³)", pm(HYD), pm(BLR), "low", "{:.1f}", "sourced"),
        (f"IT job growth {int(econ['year'].max())} (%)", last(econ, HYD, "job_growth_pct"), last(econ, BLR, "job_growth_pct"), "high", "{:+.1f}", "Hyd sourced, Blr est."),
        ("GCC units (FY26E)", snap_value(snap, "gcc_units", HYD), snap_value(snap, "gcc_units", BLR), "high", "{:,.0f}", "sourced"),
        ("IT exports FY25 (₹ lakh crore)", snap_value(snap, "it_exports_lakh_crore", HYD), snap_value(snap, "it_exports_lakh_crore", BLR), "high", "{:.2f}", "sourced (state)"),
        ("School fee per year (₹)", last(ed, HYD, "school_fee_annual_inr"), last(ed, BLR, "school_fee_annual_inr"), "low", "{:,.0f}", "illustrative"),
        ("Engineering fee per year (₹)", last(ed, HYD, "engineering_fee_annual_inr"), last(ed, BLR, "engineering_fee_annual_inr"), "low", "{:,.0f}", "illustrative"),
        ("Institution infra index", last(ed, HYD, "institution_infra_index"), last(ed, BLR, "institution_infra_index"), "high", "{:.0f}", "illustrative"),
    ]

    cell_text = []
    for label, h, b, better, fmt, note in rows:
        if better is None or h == b:
            edge = "-"
        elif (better == "high") == (h > b):
            edge = HYD
        else:
            edge = BLR
        cell_text.append([label, fmt.format(h), fmt.format(b), edge, note])

    fig.suptitle("Executive Summary", fontsize=18, fontweight="bold", x=0.06, ha="left", y=0.965)
    ax = fig.add_axes([0.06, 0.14, 0.90, 0.72])
    ax.axis("off")
    table = ax.table(cellText=cell_text,
                     colLabels=["Metric", "Hyderabad", "Bangalore", "Edge", "Data"],
                     colWidths=[0.36, 0.15, 0.15, 0.14, 0.20], loc="upper center", cellLoc="left")
    table.auto_set_font_size(False)
    table.set_fontsize(10.5)
    table.scale(1, 1.9)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor("#c9d1e0")
        if r == 0:
            cell.set_facecolor("#1f3a5f")
            cell.get_text().set_color("white")
            cell.get_text().set_fontweight("bold")
        elif r % 2 == 0:
            cell.set_facecolor("#f4f6fa")
    fig.text(0.06, 0.07,
             "Edge = the better side (lower cost, lower pollution, higher income/growth/capacity). "
             "Population and mean temperature are neutral.\n"
             "Rows marked illustrative use simulated placeholder data; do not quote them as real statistics.",
             fontsize=9, color="#444444", va="top")


# ---------------------------------------------------------------------------
# Pages, PDF export and the interactive viewer
# ---------------------------------------------------------------------------
def build_pages(data):
    pages = [("overview", lambda fig: build_overview(fig, data), (18, 10.5))]
    for chart in CHARTS:
        pages.append((chart["title"], lambda fig, c=chart: build_chart_page(fig, c, data), (14, 8)))
    pages.append(("summary", lambda fig: build_executive_summary(fig, data), (14, 8)))
    return pages


def add_footer(fig, index, total, hint=""):
    fig.text(0.97, 0.012, f"Page {index + 1} of {total}{hint}", ha="right", fontsize=8, color="#666666")


def export_pdf(pages, path, png_dir=None):
    with PdfPages(path) as pdf:
        for i, (name, builder, size) in enumerate(pages):
            fig = plt.figure(figsize=size)
            builder(fig)
            add_footer(fig, i, len(pages))
            pdf.savefig(fig)
            if png_dir is not None:
                png_dir.mkdir(exist_ok=True)
                fig.savefig(png_dir / f"page_{i + 1:02d}.png", dpi=110)
            plt.close(fig)
    print(f"Saved PDF report: {path}")


class Pager:
    """One window, flip pages with the arrow keys."""

    def __init__(self, pages):
        for key in ("keymap.back", "keymap.forward"):   # free the arrow keys
            plt.rcParams[key] = []
        self.pages, self.index = pages, 0
        self.fig = plt.figure(figsize=(14, 8))
        self.fig.canvas.mpl_connect("key_press_event", self.on_key)
        self.render()

    def render(self):
        self.fig.clf()
        _, builder, _ = self.pages[self.index]
        builder(self.fig)
        add_footer(self.fig, self.index, len(self.pages), "   |   Left / Right = flip pages")
        self.fig.canvas.draw_idle()

    def on_key(self, event):
        moves = {"right": 1, "left": -1}
        if event.key in moves:
            self.index = (self.index + moves[event.key]) % len(self.pages)
        elif event.key == "home":
            self.index = 0
        elif event.key == "end":
            self.index = len(self.pages) - 1
        else:
            return
        self.render()

    def run(self):
        plt.show()


def main(argv):
    data = load_extended_data()
    if data is None:
        return 1
    pages = build_pages(data)
    png_dir = OUT_DIR / "report_pages" if "--png" in argv else None
    export_pdf(pages, OUT_DIR / "urban_report_v4.pdf", png_dir)
    if "--no-show" not in argv:
        Pager(pages).run()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
