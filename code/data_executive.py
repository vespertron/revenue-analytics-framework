import csv
import random
from datetime import date

random.seed(73)

OUTPUT_FILE = "gold_marketing_performance.csv"

months = [
    (2025, 1), (2025, 2), (2025, 3), (2025, 4), (2025, 5), (2025, 6),
    (2025, 7), (2025, 8), (2025, 9), (2025, 10), (2025, 11), (2025, 12),
    (2026, 1), (2026, 2), (2026, 3),
]

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

base_monthly_spend = {
    "Google Brand Search": 22000,
    "Google Generic Safety Labels": 39000,
    "Google Floor Marking": 16500,
    "Google Custom Signs": 14500,
    "Google LabelTac Printers": 28000,
    "Amazon Sponsored Products": 25500,
    "Amazon Sponsored Brands": 13500,
    "Retargeting - Display": 9500,
    "Remarketing - Cart Abandon": 8200,
    "SMB Search - West": 12800,
    "Enterprise Search - East": 16200,
    "Promo - Starter Kits": 7600,
}

campaign_quality = {
    "Google Brand Search": 1.42,
    "Google Generic Safety Labels": 0.84,
    "Google Floor Marking": 1.09,
    "Google Custom Signs": 0.97,
    "Google LabelTac Printers": 1.19,
    "Amazon Sponsored Products": 1.06,
    "Amazon Sponsored Brands": 0.89,
    "Retargeting - Display": 1.28,
    "Remarketing - Cart Abandon": 1.51,
    "SMB Search - West": 1.10,
    "Enterprise Search - East": 0.93,
    "Promo - Starter Kits": 0.79,
}

month_seasonality = {
    1: 0.93, 2: 0.96, 3: 1.00, 4: 1.02, 5: 1.04, 6: 1.05,
    7: 0.98, 8: 0.99, 9: 1.03, 10: 1.10, 11: 1.17, 12: 1.14,
}

year_growth = {
    2025: 1.00,
    2026: 1.05,
}

def month_name(month_num: int) -> str:
    return date(2000, month_num, 1).strftime("%b")

def quarter(month_num: int) -> str:
    return f"Q{((month_num - 1) // 3) + 1}"

def campaign_type(name: str) -> str:
    if "Amazon" in name:
        return "Marketplace"
    if "Display" in name or "Remarketing" in name:
        return "Display / Retargeting"
    return "Search"

def avg_order_value(campaign_name: str) -> float:
    if "Printers" in campaign_name or "Enterprise" in campaign_name:
        return random.uniform(1100, 2100)
    if "Custom Signs" in campaign_name:
        return random.uniform(180, 380)
    if "Floor Marking" in campaign_name:
        return random.uniform(110, 260)
    if "Starter Kits" in campaign_name:
        return random.uniform(75, 125)
    if "Brand" in campaign_name or "Generic" in campaign_name:
        return random.uniform(160, 540)
    if "Amazon" in campaign_name:
        return random.uniform(70, 240)
    return random.uniform(120, 420)

def target_segment(intent: str) -> str:
    if intent == "Enterprise":
        return "Enterprise"
    if intent == "SMB":
        return "SMB"
    if intent == "Marketplace":
        return "Retail-like B2B"
    return random.choice(["SMB", "Retail-like B2B", "Enterprise"])

def recommendation(roas: float, spend: float, conversion_rate: float) -> str:
    if roas >= 4.0 and spend >= 20000:
        return "Scale budget"
    if roas >= 4.0 and spend < 20000:
        return "Test expansion"
    if roas < 2.0 and spend >= 20000:
        return "Reduce / optimize"
    if conversion_rate < 0.02 and spend >= 12000:
        return "Fix funnel / landing page"
    if 2.0 <= roas < 4.0:
        return "Monitor / refine"
    return "Low priority"

rows = []

for year, month_num in months:
    for c in campaigns:
        cname = c["campaign"]
        quality = campaign_quality[cname]
        seasonal_factor = month_seasonality[month_num] * year_growth[year]

        spend = base_monthly_spend[cname] * seasonal_factor * random.uniform(0.88, 1.14)
        spend = round(spend, 2)

        impressions = int(spend * random.uniform(110, 155))
        ctr = random.uniform(0.012, 0.082)
        clicks = max(1, int(impressions * ctr))
        cpc = round(spend / clicks, 2) if clicks else None

        lead_conv = random.uniform(0.020, 0.095) * quality
        leads = max(0, int(clicks * lead_conv))

        customer_conv = random.uniform(0.05, 0.23) * quality
        customers = max(0, int(leads * customer_conv))

        aov = avg_order_value(cname)
        attributed_revenue = round(customers * aov * random.uniform(0.93, 1.10), 2)

        roas = round(attributed_revenue / spend, 2) if spend else None
        cac = round(spend / customers, 2) if customers else ""
        lead_conversion_rate = round(leads / clicks, 4) if clicks else 0
        customer_conversion_rate = round(customers / clicks, 4) if clicks else 0

        rows.append({
            "year": year,
            "month_num": month_num,
            "month_name": month_name(month_num),
            "quarter": quarter(month_num),
            "month_start": f"{year}-{month_num:02d}-01",
            "campaign": cname,
            "campaign_type": campaign_type(cname),
            "channel": c["channel"],
            "intent": c["intent"],
            "region": c["region"],
            "target_segment": target_segment(c["intent"]),
            "spend": spend,
            "impressions": impressions,
            "clicks": clicks,
            "ctr": round(clicks / impressions, 4) if impressions else 0,
            "cpc": cpc,
            "leads": leads,
            "lead_conversion_rate": lead_conversion_rate,
            "customers": customers,
            "customer_conversion_rate": customer_conversion_rate,
            "avg_order_value": round(aov, 2),
            "attributed_revenue": attributed_revenue,
            "roas": roas,
            "cac": cac,
        })

# Add prior month revenue and growth %
rows.sort(key=lambda r: (r["campaign"], r["year"], r["month_num"]))
prior_map = {}

for row in rows:
    key = row["campaign"]
    prior_revenue = prior_map.get(key)
    row["prior_month_attributed_revenue"] = round(prior_revenue, 2) if prior_revenue is not None else ""

    if prior_revenue in (None, 0):
        row["revenue_growth_pct"] = ""
    else:
        row["revenue_growth_pct"] = round((row["attributed_revenue"] - prior_revenue) / prior_revenue, 4)

    rec = recommendation(
        roas=row["roas"] if row["roas"] is not None else 0,
        spend=row["spend"],
        conversion_rate=row["customer_conversion_rate"],
    )
    row["recommendation"] = rec

    prior_map[key] = row["attributed_revenue"]

fieldnames = [
    "year",
    "month_num",
    "month_name",
    "quarter",
    "month_start",
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
    "customer_conversion_rate",
    "avg_order_value",
    "attributed_revenue",
    "prior_month_attributed_revenue",
    "revenue_growth_pct",
    "roas",
    "cac",
    "recommendation",
]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows):,} rows to {OUTPUT_FILE}")