import csv
import random
from datetime import date, timedelta

random.seed(73)

# ---------------------------------
# Config
# ---------------------------------
START_DATE = date(2025, 1, 1)
END_DATE = date(2025, 12, 31)
OUTPUT_FILE = "marketing_roi_dummy_data.csv"

campaigns = [
    {"campaign": "Google Brand Search", "channel": "Google Ads", "intent": "Brand", "region": "National"},
    {"campaign": "Google Generic Safety Labels", "channel": "Google Ads", "intent": "Generic", "region": "National"},
    {"campaign": "Google Floor Marking", "channel": "Google Ads", "intent": "Product", "region": "West"},
    {"campaign": "Google Custom Signs", "channel": "Google Ads", "intent": "Product", "region": "East"},
    {"campaign": "Google LabelTac Printers", "channel": "Google Ads", "intent": "Product", "region": "National"},
    {"campaign": "Amazon Sponsored Products", "channel": "Amazon", "intent": "Marketplace", "region": "National"},
    {"campaign": "Amazon Sponsored Brands", "channel": "Amazon", "intent": "Marketplace", "region": "National"},
    {"campaign": "Retargeting - Display", "channel": "Google Display", "intent": "Retargeting", "region": "National"},
    {"campaign": "Remarketing - Cart Abandon", "channel": "Google Display", "intent": "Retargeting", "region": "National"},
    {"campaign": "SMB Search - West", "channel": "Google Ads", "intent": "SMB", "region": "West"},
    {"campaign": "Enterprise Search - East", "channel": "Google Ads", "intent": "Enterprise", "region": "East"},
    {"campaign": "Promo - Starter Kits", "channel": "Google Ads", "intent": "Promo", "region": "Central"},
]

base_spend = {
    "Google Brand Search": 650,
    "Google Generic Safety Labels": 1200,
    "Google Floor Marking": 500,
    "Google Custom Signs": 450,
    "Google LabelTac Printers": 900,
    "Amazon Sponsored Products": 850,
    "Amazon Sponsored Brands": 450,
    "Retargeting - Display": 300,
    "Remarketing - Cart Abandon": 260,
    "SMB Search - West": 420,
    "Enterprise Search - East": 520,
    "Promo - Starter Kits": 280,
}

# Relative performance tendencies
campaign_quality = {
    "Google Brand Search": 1.45,
    "Google Generic Safety Labels": 0.82,
    "Google Floor Marking": 1.08,
    "Google Custom Signs": 0.96,
    "Google LabelTac Printers": 1.18,
    "Amazon Sponsored Products": 1.05,
    "Amazon Sponsored Brands": 0.88,
    "Retargeting - Display": 1.30,
    "Remarketing - Cart Abandon": 1.52,
    "SMB Search - West": 1.12,
    "Enterprise Search - East": 0.91,
    "Promo - Starter Kits": 0.78,
}

# ---------------------------------
# Helpers
# ---------------------------------
def daterange(start_dt, end_dt):
    current = start_dt
    while current <= end_dt:
        yield current
        current += timedelta(days=1)

def month_factor(dt: date) -> float:
    return {
        1: 0.93, 2: 0.95, 3: 0.98, 4: 1.00, 5: 1.03, 6: 1.05,
        7: 0.97, 8: 0.98, 9: 1.02, 10: 1.09, 11: 1.16, 12: 1.13
    }[dt.month]

def weekday_factor(dt: date) -> float:
    return {0: 1.02, 1: 1.03, 2: 1.01, 3: 1.00, 4: 1.05, 5: 0.84, 6: 0.73}[dt.weekday()]

def campaign_type(campaign_name: str) -> str:
    if "Amazon" in campaign_name:
        return "Marketplace"
    if "Display" in campaign_name or "Remarketing" in campaign_name:
        return "Display / Retargeting"
    return "Search"

def avg_order_value(campaign_name: str) -> float:
    if "Printers" in campaign_name or "Enterprise" in campaign_name:
        return random.uniform(850, 1850)
    if "Custom Signs" in campaign_name:
        return random.uniform(140, 340)
    if "Floor Marking" in campaign_name:
        return random.uniform(90, 230)
    if "Starter Kits" in campaign_name:
        return random.uniform(75, 120)
    if "Brand" in campaign_name or "Generic" in campaign_name:
        return random.uniform(140, 520)
    if "Amazon" in campaign_name:
        return random.uniform(65, 240)
    return random.uniform(110, 380)

def target_segment(intent: str) -> str:
    if intent == "Enterprise":
        return "Enterprise"
    if intent == "SMB":
        return "SMB"
    if intent == "Marketplace":
        return "Retail-like B2B"
    return random.choice(["SMB", "Retail-like B2B", "Enterprise"])

def recommendation(roas, spend, conv_rate):
    if roas >= 4.0 and spend >= 700:
        return "Scale budget"
    if roas >= 4.0 and spend < 700:
        return "Test expansion"
    if roas < 2.0 and spend >= 700:
        return "Reduce / optimize"
    if conv_rate < 0.02 and spend >= 400:
        return "Fix funnel / landing page"
    if 2.0 <= roas < 4.0:
        return "Monitor / refine"
    return "Low priority"

# ---------------------------------
# Generate rows
# ---------------------------------
rows = []

for dt in daterange(START_DATE, END_DATE):
    season = month_factor(dt) * weekday_factor(dt)

    for c in campaigns:
        cname = c["campaign"]
        quality = campaign_quality[cname]

        spend = base_spend[cname] * season * random.uniform(0.82, 1.22)

        # marketing funnel behavior
        impressions = int(spend * random.uniform(95, 150))
        ctr = random.uniform(0.012, 0.085)
        clicks = max(1, int(impressions * ctr))

        cpc = spend / clicks if clicks else 0
        landing_conv = random.uniform(0.018, 0.095) * quality
        leads = max(0, int(clicks * landing_conv))

        lead_to_customer = random.uniform(0.05, 0.22) * quality
        customers = max(0, int(leads * lead_to_customer))

        aov = avg_order_value(cname)
        attributed_revenue = round(customers * aov * random.uniform(0.92, 1.12), 2)

        roas = round((attributed_revenue / spend), 2) if spend else 0
        cac = round((spend / customers), 2) if customers else None
        conversion_rate = round((customers / clicks), 4) if clicks else 0
        lead_conversion_rate = round((leads / clicks), 4) if clicks else 0

        # recommendation fields
        rec = recommendation(roas, spend, conversion_rate)

        rows.append({
            "date": dt.isoformat(),
            "year": dt.year,
            "month_num": dt.month,
            "month_name": dt.strftime("%b"),
            "quarter": f"Q{((dt.month - 1) // 3) + 1}",
            "campaign": cname,
            "campaign_type": campaign_type(cname),
            "channel": c["channel"],
            "intent": c["intent"],
            "region": c["region"],
            "target_segment": target_segment(c["intent"]),
            "spend": round(spend, 2),
            "impressions": impressions,
            "clicks": clicks,
            "ctr": round((clicks / impressions), 4) if impressions else 0,
            "cpc": round(cpc, 2),
            "leads": leads,
            "lead_conversion_rate": lead_conversion_rate,
            "customers": customers,
            "conversion_rate": conversion_rate,
            "avg_order_value": round(aov, 2),
            "attributed_revenue": attributed_revenue,
            "roas": roas,
            "cac": cac if cac is not None else "",
            "recommendation": rec,
        })

# ---------------------------------
# Write CSV
# ---------------------------------
fieldnames = [
    "date",
    "year",
    "month_num",
    "month_name",
    "quarter",
    "campaign",
    "campaign_type",
    "channel",
    "intent",
    "region",
    "target_segment",
    "spend",
    "impressions",
    "clicks",
    "ctr",
    "cpc",
    "leads",
    "lead_conversion_rate",
    "customers",
    "conversion_rate",
    "avg_order_value",
    "attributed_revenue",
    "roas",
    "cac",
    "recommendation",
]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows):,} rows to {OUTPUT_FILE}")