import csv
import random
from datetime import date, timedelta

random.seed(42)

# -----------------------------
# Config
# -----------------------------
START_DATE = date(2024, 1, 1)
END_DATE = date(2026, 3, 25)
OUTPUT_FILE = "executive_performance_dummy_data.csv"

channels = ["Direct", "Google Ads", "Amazon", "Distributor"]
customer_segments = ["Enterprise", "SMB", "Retail-like B2B"]
regions = ["West", "Central", "East", "South"]
product_categories = {
    "Label Printers": [
        ("LT100", "LabelTac LT100"),
        ("LT200", "LabelTac LT200"),
        ("LT300", "LabelTac LT300"),
    ],
    "Label Supply": [
        ("LS-WHT-4", "4in White Supply"),
        ("LS-YLW-4", "4in Yellow Supply"),
        ("LS-RED-2", "2in Red Supply"),
        ("LS-BLK-1", "1in Black Supply"),
    ],
    "Floor Marking": [
        ("FM-STD-Y", "Standard Yellow Tape"),
        ("FM-IND-B", "Industrial Blue Tape"),
        ("FM-HAZ-RY", "Hazard Red/Yellow Tape"),
    ],
    "Custom Signs": [
        ("CS-STD", "Standard Custom Sign"),
        ("CS-IND", "Industrial Custom Sign"),
        ("CS-PRE", "Premium Custom Sign"),
    ],
    "Safety Accessories": [
        ("SA-CUT", "Safety Cutter"),
        ("SA-DISP", "Dispenser"),
        ("SA-KIT", "Starter Kit"),
    ],
}

# Weighted SKU importance to simulate 80/20 concentration
sku_weights = {
    "LT200": 10,
    "LT300": 8,
    "LS-WHT-4": 12,
    "LS-YLW-4": 9,
    "FM-STD-Y": 8,
    "CS-STD": 7,
    "CS-PRE": 6,
    "SA-KIT": 5,
    "LT100": 4,
    "LS-RED-2": 4,
    "LS-BLK-1": 3,
    "FM-IND-B": 3,
    "FM-HAZ-RY": 2,
    "CS-IND": 2,
    "SA-CUT": 2,
    "SA-DISP": 2,
}

# Base SKU pricing and cost profile
sku_meta = {
    "LT100": {"price": 1195, "cost_pct": 0.58, "category": "Label Printers"},
    "LT200": {"price": 1995, "cost_pct": 0.54, "category": "Label Printers"},
    "LT300": {"price": 2995, "cost_pct": 0.51, "category": "Label Printers"},
    "LS-WHT-4": {"price": 115, "cost_pct": 0.38, "category": "Label Supply"},
    "LS-YLW-4": {"price": 125, "cost_pct": 0.39, "category": "Label Supply"},
    "LS-RED-2": {"price": 72, "cost_pct": 0.37, "category": "Label Supply"},
    "LS-BLK-1": {"price": 54, "cost_pct": 0.35, "category": "Label Supply"},
    "FM-STD-Y": {"price": 89, "cost_pct": 0.42, "category": "Floor Marking"},
    "FM-IND-B": {"price": 109, "cost_pct": 0.44, "category": "Floor Marking"},
    "FM-HAZ-RY": {"price": 139, "cost_pct": 0.46, "category": "Floor Marking"},
    "CS-STD": {"price": 145, "cost_pct": 0.47, "category": "Custom Signs"},
    "CS-IND": {"price": 210, "cost_pct": 0.49, "category": "Custom Signs"},
    "CS-PRE": {"price": 340, "cost_pct": 0.52, "category": "Custom Signs"},
    "SA-CUT": {"price": 19, "cost_pct": 0.33, "category": "Safety Accessories"},
    "SA-DISP": {"price": 26, "cost_pct": 0.36, "category": "Safety Accessories"},
    "SA-KIT": {"price": 89, "cost_pct": 0.40, "category": "Safety Accessories"},
}

sku_names = {
    sku: name
    for items in product_categories.values()
    for sku, name in items
}

# -----------------------------
# Helpers
# -----------------------------
def daterange(start_dt, end_dt):
    current = start_dt
    while current <= end_dt:
        yield current
        current += timedelta(days=1)

def month_factor(dt: date) -> float:
    # Mild seasonality
    factors = {
        1: 0.92, 2: 0.95, 3: 0.98, 4: 1.00, 5: 1.03, 6: 1.05,
        7: 0.96, 8: 0.97, 9: 1.02, 10: 1.08, 11: 1.15, 12: 1.12
    }
    return factors[dt.month]

def weekday_factor(dt: date) -> float:
    # Lower on weekends
    return {
        0: 1.00, 1: 1.03, 2: 1.02, 3: 1.01, 4: 1.05, 5: 0.52, 6: 0.40
    }[dt.weekday()]

def channel_order_volume(channel: str) -> int:
    return {
        "Direct": 18,
        "Google Ads": 24,
        "Amazon": 20,
        "Distributor": 8,
    }[channel]

def channel_ad_spend_multiplier(channel: str) -> float:
    return {
        "Direct": 0.04,
        "Google Ads": 0.16,
        "Amazon": 0.08,
        "Distributor": 0.01,
    }[channel]

def weighted_sku_choice():
    skus = list(sku_weights.keys())
    weights = list(sku_weights.values())
    return random.choices(skus, weights=weights, k=1)[0]

def segment_for_channel(channel: str) -> str:
    if channel == "Distributor":
        return random.choices(
            ["Enterprise", "SMB", "Retail-like B2B"],
            weights=[0.55, 0.35, 0.10],
            k=1
        )[0]
    if channel == "Amazon":
        return random.choices(
            ["Retail-like B2B", "SMB", "Enterprise"],
            weights=[0.70, 0.25, 0.05],
            k=1
        )[0]
    return random.choices(
        ["SMB", "Enterprise", "Retail-like B2B"],
        weights=[0.50, 0.25, 0.25],
        k=1
    )[0]

def units_for_sku(sku: str, channel: str) -> int:
    if sku.startswith("LT"):  # printers
        return random.choices([1, 1, 1, 2, 2, 3], weights=[40, 25, 15, 10, 6, 4], k=1)[0]
    if sku.startswith("LS"):  # supply
        base = random.choices([1, 2, 3, 4, 5, 6, 8], weights=[8, 15, 18, 18, 16, 15, 10], k=1)[0]
        if channel in ("Amazon", "Google Ads"):
            return base
        return max(1, base + random.choice([0, 1, 2]))
    if sku.startswith("FM"):  # tape
        return random.choices([1, 2, 3, 4, 5], weights=[15, 25, 25, 20, 15], k=1)[0]
    if sku.startswith("CS"):  # custom signs
        return random.choices([1, 1, 2, 2, 3, 4], weights=[30, 25, 20, 12, 8, 5], k=1)[0]
    return random.choices([1, 2, 3, 4], weights=[30, 30, 25, 15], k=1)[0]

def price_with_variation(base_price: float, channel: str, segment: str) -> float:
    price = base_price
    if channel == "Amazon":
        price *= 0.97
    elif channel == "Distributor":
        price *= 0.91
    elif segment == "Enterprise":
        price *= 0.96  # negotiated pricing
    return round(price * random.uniform(0.97, 1.03), 2)

def top_product_flag(sku: str) -> str:
    return "Top 10% Product" if sku in {"LT200", "LT300", "LS-WHT-4", "LS-YLW-4"} else "Long Tail"

# -----------------------------
# Generate rows
# -----------------------------
rows = []
order_id = 100000

for dt in daterange(START_DATE, END_DATE):
    daily_factor = month_factor(dt) * weekday_factor(dt)

    for channel in channels:
        order_count = max(1, int(channel_order_volume(channel) * daily_factor * random.uniform(0.75, 1.30)))

        for _ in range(order_count):
            order_id += 1
            sku = weighted_sku_choice()
            meta = sku_meta[sku]
            segment = segment_for_channel(channel)
            region = random.choices(regions, weights=[0.30, 0.20, 0.28, 0.22], k=1)[0]
            units = units_for_sku(sku, channel)
            unit_price = price_with_variation(meta["price"], channel, segment)
            revenue = round(units * unit_price, 2)
            cogs = round(revenue * meta["cost_pct"] * random.uniform(0.97, 1.03), 2)
            gross_profit = round(revenue - cogs, 2)
            gross_margin_pct = round(gross_profit / revenue, 4) if revenue else 0

            # Approximate attributable spend at row level for KPI prototyping
            ad_spend = round(revenue * channel_ad_spend_multiplier(channel) * random.uniform(0.75, 1.20), 2)

            rows.append({
                "order_date": dt.isoformat(),
                "year": dt.year,
                "month_num": dt.month,
                "month_name": dt.strftime("%b"),
                "quarter": f"Q{((dt.month - 1) // 3) + 1}",
                "channel": channel,
                "customer_segment": segment,
                "region": region,
                "product_category": meta["category"],
                "sku": sku,
                "product_name": sku_names[sku],
                "top_product_group": top_product_flag(sku),
                "order_id": order_id,
                "orders": 1,
                "units": units,
                "revenue": revenue,
                "cogs": cogs,
                "gross_profit": gross_profit,
                "gross_margin_pct": gross_margin_pct,
                "ad_spend": ad_spend,
            })

# -----------------------------
# Write CSV
# -----------------------------
fieldnames = [
    "order_date",
    "year",
    "month_num",
    "month_name",
    "quarter",
    "channel",
    "customer_segment",
    "region",
    "product_category",
    "sku",
    "product_name",
    "top_product_group",
    "order_id",
    "orders",
    "units",
    "revenue",
    "cogs",
    "gross_profit",
    "gross_margin_pct",
    "ad_spend",
]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows):,} rows to {OUTPUT_FILE}")