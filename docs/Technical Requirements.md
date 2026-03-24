# Technical Requirements

## Overview
**Project Name:** Executive Performance Dashboard
**Owner:** Analytics
**BI Tool:** Tableau Public
**Warehouse:** Excel
**Data Latency:** Static, 1-time upload
**Grain:** Transaction / Monthly

---

## Architecture & Data Flow

| Layer  | Table Name                 | Description          | Input Source   | Output Use |
| ------ | -------------------------- | -------------------- | -------------- | ---------- |
| Bronze | raw_netsuite_transactions  | Raw ERP data         | NetSuite API   | Silver     |
| Bronze | raw_hubspot_deals          | CRM deals            | HubSpot API    | Silver     |
| Bronze | raw_google_ads             | Ad spend             | Google Ads API | Silver     |
| Silver | stg_revenue                | Cleaned revenue data | Bronze         | Gold       |
| Silver | stg_customers              | Unified customer IDs | Bronze         | Gold       |
| Gold   | fact_monthly_revenue       | Aggregated revenue   | Silver         | Dashboard  |
| Gold   | fact_marketing_performance | Spend + revenue      | Silver         | Dashboard  |

---

## Source Systems

| Source     | Table        | Extraction Method  | Frequency | Notes             |
| ---------- | ------------ | ------------------ | --------- | ----------------- |
| NetSuite   | Transactions | API / Saved Search | Daily     | Source of truth   |
| HubSpot    | Deals        | API                | Daily     | Not final revenue |
| Google Ads | Campaigns    | API                | Daily     | Spend data        |

---

## Data Model

**fact_monthly_revenue**
| Column              | Type   | Description       | Grain |
| ------------------- | ------ | ----------------- | ----- |
| month               | Date   | Month bucket      | Month |
| channel             | String | Marketing channel |       |
| product_category    | String | Product grouping  |       |
| revenue             | Float  | Total revenue     |       |
| prior_month_revenue | Float  | Lag revenue       |       |
| revenue_growth_pct  | Float  | MoM growth        |       |

**fact_marketing_performance**

---

## Transformations

| Layer  | Step        | Input    | Logic                       | Output             |
| ------ | ----------- | -------- | --------------------------- | ------------------ |
| Silver | Filter      | NetSuite | status = ‘posted’           | valid_transactions |
| Silver | Currency    | NetSuite | Convert FX → USD            | revenue_usd        |
| Silver | Cleaning    | HubSpot  | exclude non-closed deals    | clean_deals        |
| Silver | Join        | All      | join on email → customer_id | unified_customer   |
| Gold   | Aggregation | Silver   | SUM revenue by month        | monthly_revenue    |
| Gold   | Window      | Gold     | LAG(revenue)                | prior_month        |
| Gold   | KPI         | Gold     | (rev - prior)/prior         | growth_pct         |


---

## Data Refresh & Scheduling

| Layer  | Job Name          | Frequency | Type            | SLA    |
| ------ | ----------------- | --------- | --------------- | ------ |
| Bronze | ingest_netsuite   | none      | API pull        | 2 hrs  |
| Silver | transform_revenue | none      | SQL/dbt         | 1 hr   |
| Gold   | aggregate_kpis    | none      | SQL/dbt         | 30 min |
| BI     | tableau_refresh   | none      | Extract refresh | 15 min |

---

## Performance & Optimization

| Area        | Strategy           | Example           |
| ----------- | ------------------ | ----------------- |
| Aggregation | Pre-calc in Gold   | Monthly revenue   |
| Joins       | Reduce at BI layer | Join in warehouse |
| Data Volume | Partition by date  | month partition   |
| Tableau     | Extracts vs Live   | Use extracts      |

---

## Access & Security

| Layer  | Access     | Users          | Notes     |
| ------ | ---------- | -------------- | --------- |
| Bronze | Restricted | Data Eng       | Raw data  |
| Silver | Limited    | Analytics      | Cleaned   |
| Gold   | Open       | Business users | Trusted   |
| BI     | Open       | Execs          | Dashboard |

---

## Dependencies & Monitoring

| Dependency       | Risk           | Monitoring       | Action    |
| ---------------- | -------------- | ---------------- | --------- |
| NetSuite API     | Failure        | Job alert        | Retry     |
| HubSpot data     | Missing fields | Validation check | Flag      |
| FX rates         | Incorrect      | Daily check      | Reprocess |
| Revenue mismatch | High impact    | Reconciliation   | Alert     |
