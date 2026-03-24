# Technical Specifications

## Overview

**Project Name:** Revenue Analytics Framework
**Author:** Analytics
**Version:** v1.0
**Last Updated:** 2026/03/25
**BI Tool:** Tableau
**Data Platform:** Excel
**Grain:** Month x Channel x Product

---

## System Architecture

| Layer  | Table Name                 | Storage   | Description     | Downstream |
| ------ | -------------------------- | --------- | --------------- | ---------- |
| Bronze | raw_netsuite_transactions  | Warehouse | Raw ERP data    | Silver     |
| Bronze | raw_hubspot_deals          | Warehouse | CRM deals       | Silver     |
| Bronze | raw_google_ads             | Warehouse | Campaign data   | Silver     |
| Silver | stg_revenue                | Warehouse | Clean revenue   | Gold       |
| Silver | stg_customers              | Warehouse | Unified IDs     | Gold       |
| Gold   | fact_monthly_revenue       | Warehouse | KPI-ready table | Tableau    |
| Gold   | fact_marketing_performance | Warehouse | Campaign KPIs   | Tableau    |

---

## Source-to-Target Mapping

| Source System | Source Field   | Transformation Logic | Target Field        | Layer  | Notes               |
| ------------- | -------------- | -------------------- | ------------------- | ------ | ------------------- |
| NetSuite      | invoice_amount | Convert FX → USD     | revenue_usd         | Silver | Source of truth     |
| NetSuite      | status         | Filter = ‘posted’    | valid_flag          | Silver | Exclude drafts      |
| HubSpot       | deal_amount    | Keep if closed_won   | deal_amount_clean   | Silver | Non-final           |
| HubSpot       | email          | Map to customer_id   | customer_id         | Silver | Identity resolution |
| Google Ads    | cost           | None                 | ad_spend            | Silver |                     |
| Silver        | revenue_usd    | SUM by month         | revenue             | Gold   |                     |
| Gold          | revenue        | LAG(revenue)         | prior_month_revenue | Gold   |                     |
| Gold          | revenue        | (rev - prior)/prior  | revenue_growth_pct  | Gold   |                     |

---

## Table Schemas

**fact_monthly_revenue**
| Column              | Type   | Nullable | Description       |
| ------------------- | ------ | -------- | ----------------- |
| month_start         | DATE   | No       | Month bucket      |
| channel             | STRING | No       | Marketing channel |
| product_category    | STRING | No       | Product grouping  |
| region              | STRING | Yes      | Geography         |
| customer_segment    | STRING | Yes      | Segment           |
| revenue             | FLOAT  | No       | Total revenue     |
| prior_month_revenue | FLOAT  | Yes      | Previous period   |
| revenue_growth_pct  | FLOAT  | Yes      | MoM growth        |
| gross_profit        | FLOAT  | Yes      |                   |
| gross_margin_pct    | FLOAT  | Yes      |                   |
| ad_spend            | FLOAT  | Yes      |                   |
| roas                | FLOAT  | Yes      |                   |

---

## Transformation Logic (SQL-Level)

### Revenue Aggregation

```
SELECT
  DATE_TRUNC('month', order_date) AS month_start,
  channel,
  product_category,
  SUM(revenue_usd) AS revenue
FROM stg_revenue
GROUP BY 1,2,3
```

### Prior Month Revenue

```
LAG(revenue) OVER (
  PARTITION BY channel, product_category
  ORDER BY month_start
)
```

### Revenue Growth %

```
CASE 
  WHEN prior_month_revenue = 0 THEN NULL
  ELSE (revenue - prior_month_revenue) / prior_month_revenue
END
```

### roas

```
revenue / ad_spend
```

---

## KPI Definitions

| KPI              | SQL Logic              | Layer | Owner     |
| ---------------- | ---------------------- | ----- | --------- |
| Revenue          | SUM(revenue)           | Gold  | Finance   |
| Revenue Growth % | See window calc        | Gold  | Finance   |
| Gross Margin %   | gross_profit / revenue | Gold  | Finance   |
| ROAS             | revenue / ad_spend     | Gold  | Marketing |
| CAC              | ad_spend / customers   | Gold  | Marketing |

---

## Data Refresh & Pipelines

| Job              | Layer  | Frequency | Tool      | Dependency |
| ---------------- | ------ | --------- | --------- | ---------- |
| ingest_netsuite  | Bronze | Daily     | API       | NetSuite   |
| ingest_hubspot   | Bronze | Daily     | API       | HubSpot    |
| ingest_ads       | Bronze | Daily     | API       | Google Ads |
| transform_silver | Silver | Daily     | dbt / SQL | Bronze     |
| build_gold       | Gold   | Daily     | dbt / SQL | Silver     |
| tableau_refresh  | BI     | Daily     | Tableau   | Gold       |

---

## Data Quality Rules

| **Check**              | **Logic**       | **Threshold** | **Action**   |
| ---------------------- | --------------- | ------------- | -------- |
| Revenue reconciliation | BI vs NetSuite  | ±1%         | Alert    |
| Missing records        | COUNT check     | 0 missing   | Fail job |
| Null revenue           | revenue IS NULL | Not allowed | Fail     |
| Duplicate customers    | COUNT DISTINCT  | No dupes    | Flag     |

---

## Error Handling & Monitoring

| **Scenario**     | **Detection**   | **Action**    |
| ---------------- | --------------- | ------------- |
| API failure      | Job failure     | Retry + alert |
| Missing data     | Row count drop  | Alert         |
| Revenue mismatch | Reconciliation  | Investigate   |
| Schema change    | Column mismatch | Fail job      |

