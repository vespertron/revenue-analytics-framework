import csv
import random
from datetime import date

random.seed(42)

OUTPUT_FILE = "gold_executive_performance.csv"

months = [
    (2025, 1), (2025, 2), (2025, 3), (2025, 4), (2025, 5), (2025, 6),
    (2025, 7), (2025, 8), (2025, 9), (2025, 10), (2025, 11), (2025, 12),
    (2026, 1), (2026, 2), (2026, 3),
]

channels = ["Direct", "Google Ads", "Amazon", "Distributor"]
product_categories = ["Label Printers", "Label Supply", "Floor Marking", "Custom Signs", "Safety Accessories"]
regions = ["West", "Central", "East", "South"]
customer_segments = ["Enterprise", "SMB", "Retail-like B2B"]

channel_weights = {
    "Direct": 1.00,
    "Google Ads": 1.15,
    "Amazon": 0.95,
    "Distributor": 0.70,
}

category_weights = {
    "Label Printers": 1.20,
    "Label Supply": 1.35,
    "Floor Marking": 0.95,
    "Custom Signs": 0.85,
    "Safety Accessories": 0.65,
}

segment_weights = {
    "Enterprise": 1.10,
    "SMB": 1.00,
    "Retail-like B2B": 0.80,
}

region_weights = {
    "West": 1.05,
    "Central": 0.95,
    "East": 1.00,
    "South": 0.92,
}

month_seasonality = {
    1: 0.94, 2: 0.97, 3: 1.00, 4: 1.02, 5: 1.05, 6: 1.06,
    7: 0.98, 8: 0.99, 9: 1.03, 10: 1.10, 11: 1.17, 12: 1.14,
}

growth_drift = {
    2025: 1.00,
    2026: 1.04,
}

margin_profiles = {
    "Label Printers": 0.46,
    "Label Supply": 0.61,
    "Floor Marking": 0.54,
    "Custom Signs": 0.48,
    "Safety Accessories": 0.57,
}

ad_spend_rates = {
    "Direct": 0.03,
    "Google Ads": 0.16,
    "Amazon": 0.10,
    "Distributor": 0.01,
}

base_orders = {
    "Label Printers": 75,
    "Label Supply": 240,
    "Floor Marking": 110,
    "Custom Signs": 80,
    "Safety Accessories": 125,
}

base_aov = {
    "Label Printers": 1850,
    "Label Supply": 145,
    "Floor Marking": 210,
    "Custom Signs": 290,
    "Safety Accessories": 95,
}

def month_name(month_num: int) -> str:
    return date(2000, month_num, 1).strftime("%b")

def quarter(month_num: int) -> str:
    return f"Q{((month_num - 1) // 3) + 1}"

rows = []

# Build current-period values first
for year, month_num in months:
    for channel in channels:
        for category in product_categories:
            for region in regions:
                for segment in customer_segments:
                    orders = int(
                        base_orders[category]
                        * channel_weights[channel]
                        * category_weights[category]
                        * segment_weights[segment]
                        * region_weights[region]
                        * month_seasonality[month_num]
                        * growth_drift[year]
                        * random.uniform(0.82, 1.18)
                    )
                    orders = max(8, orders)

                    aov = base_aov[category] * random.uniform(0.93, 1.08)
                    revenue = round(orders * aov, 2)

                    gross_margin_pct = margin_profiles[category] * random.uniform(0.95, 1.05)
                    gross_margin_pct = max(0.20, min(0.75, gross_margin_pct))
                    gross_profit = round(revenue * gross_margin_pct, 2)
                    cogs = round(revenue - gross_profit, 2)

                    avg_units_per_order = {
                        "Label Printers": 1.2,
                        "Label Supply": 4.8,
                        "Floor Marking": 2.7,
                        "Custom Signs": 2.0,
                        "Safety Accessories": 2.9,
                    }[category]
                    units = int(orders * avg_units_per_order * random.uniform(0.90, 1.12))

                    ad_spend = round(revenue * ad_spend_rates[channel] * random.uniform(0.85, 1.15), 2)
                    roas = round(revenue / ad_spend, 2) if ad_spend else None

                    rows.append({
                        "year": year,
                        "month_num": month_num,
                        "month_name": month_name(month_num),
                        "quarter": quarter(month_num),
                        "month_start": f"{year}-{month_num:02d}-01",
                        "channel": channel,
                        "product_category": category,
                        "region": region,
                        "customer_segment": segment,
                        "orders": orders,
                        "units": units,
                        "revenue": revenue,
                        "cogs": cogs,
                        "gross_profit": gross_profit,
                        "gross_margin_pct": round(gross_margin_pct, 4),
                        "ad_spend": ad_spend,
                        "roas": roas,
                    })

# Add prior month revenue and growth %
rows.sort(key=lambda r: (
    r["channel"],
    r["product_category"],
    r["region"],
    r["customer_segment"],
    r["year"],
    r["month_num"],
))

prior_map = {}

for row in rows:
    key = (row["channel"], row["product_category"], row["region"], row["customer_segment"])
    prior_revenue = prior_map.get(key)
    row["prior_month_revenue"] = round(prior_revenue, 2) if prior_revenue is not None else ""

    if prior_revenue in (None, 0):
        row["revenue_growth_pct"] = ""
    else:
        row["revenue_growth_pct"] = round((row["revenue"] - prior_revenue) / prior_revenue, 4)

    prior_map[key] = row["revenue"]

fieldnames = [
    "year",
    "month_num",
    "month_name",
    "quarter",
    "month_start",
    "channel",
    "product_category",
    "region",
    "customer_segment",
    "orders",
    "units",
    "revenue",
    "prior_month_revenue",
    "revenue_growth_pct",
    "cogs",
    "gross_profit",
    "gross_margin_pct",
    "ad_spend",
    "roas",
]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows):,} rows to {OUTPUT_FILE}")