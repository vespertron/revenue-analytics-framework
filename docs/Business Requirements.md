# Business Requirements

## Overview
**Project Name:** Executive Performance Dashboard
**Business Owner:** CFO
**Stakeholders:** Marketing, Sales, Finance
**Objective:** Improve visibility into revenue & ROI
**Success Criteria:** Trusted metrics, reduced Excel usage
**Timeline:** 90-day phased rollout
**Data Sources:** NetSuite, HubSpot, Google Ads

---

## Business Questions

| ID  | Business Question            | Priority | Owner     | Notes                     |
| --- | ---------------------------- | -------- | --------- | ------------------------- |
| BQ1 | Are we growing or declining? | High     | Exec      | MoM + YoY                 |
| BQ2 | Are we profitable?           | High     | Finance   | Margin focus              |
| BQ3 | What’s driving results?      | High     | Exec      | Channel + product         |
| BQ4 | Where should we take action? | High     | All       | Identify underperformance |
| BQ5 | Which channels drive ROI?    | High     | Marketing | ROAS                      |

---

## KPI Requirements

| KPI Name         | Business Question | Definition            | Calculation                 | Source              | Grain   | Owner     | Status   |
| ---------------- | ----------------- | --------------------- | --------------------------- | ------------------- | ------- | --------- | -------- |
| Revenue          | BQ1               | Total invoiced sales  | SUM(invoice_amount)         | NetSuite            | Monthly | Finance   | Approved |
| Revenue Growth % | BQ1               | MoM revenue change    | (Rev - Prior Rev)/Prior Rev | Gold Layer          | Monthly | Finance   | Approved |
| Gross Margin %   | BQ2               | Profitability ratio   | Gross Profit / Revenue      | NetSuite            | Monthly | Finance   | Approved |
| ROAS             | BQ5               | Revenue per ad dollar | Revenue / Ad Spend          | Marketing + Finance | Monthly | Marketing | Pending  |
| CAC              | BQ5               | Cost per customer     | Spend / Customers           | Marketing           | Monthly | Marketing | Pending  |

---

## Data Requirements

| Field Name     | Business Concept    | Source System | Source Field   | Transformation        | Output Field      | Notes               |
| -------------- | ------------------- | ------------- | -------------- | --------------------- | ----------------- | ------------------- |
| invoice_amount | Revenue             | NetSuite      | invoice_amount | Convert to USD        | revenue_usd       | FX normalized       |
| deal_amount    | Revenue (non-final) | HubSpot       | deal_amount    | Exclude unless closed | deal_amount_clean | Not source of truth |
| email          | Customer ID         | Both          | email          | Map to unified ID     | customer_id       | Identity resolution |
| ad_spend       | Marketing Cost      | Google Ads    | cost           | None                  | ad_spend          |                     |

---

## Dashboard Requirements

| Section | KPI / Visual       | Business Question | Visual Type | Grain    | Notes       |
| ------- | ------------------ | ----------------- | ----------- | -------- | ----------- |
| KPI Row | Revenue            | BQ1               | Big Number  | Monthly  |             |
| KPI Row | Revenue Growth %   | BQ1               | Big Number  | Monthly  | Color coded |
| KPI Row | Gross Margin %     | BQ2               | Big Number  | Monthly  |             |
| Chart   | Revenue Trend      | BQ1               | Line        | Month    |             |
| Chart   | Revenue by Channel | BQ3               | Bar         | Channel  |             |
| Chart   | Margin by Product  | BQ2               | Bar         | Category |             |
| Chart   | ROAS by Channel    | BQ5               | Bar         | Channel  |             |

---

## Filters & Interactions

| Filter           | Type         | Applies To | Default        | Notes |
| ---------------- | ------------ | ---------- | -------------- | ----- |
| Date             | Range        | All        | Last 12 months |       |
| Channel          | Multi-select | All        | All            |       |
| Product Category | Multi-select | All        | All            |       |
| Region           | Multi-select | All        | All            |       |
| Customer Segment | Multi-select | All        | All            |       |

---

## Data Quality & Validation

| Check Type     | Metric          | Rule               | Threshold  | Frequency | Owner     | Action      |
| -------------- | --------------- | ------------------ | ---------- | --------- | --------- | ----------- |
| Reconciliation | Revenue         | BI = NetSuite      | ±1%        | Daily     | Analytics | Alert       |
| Completeness   | Orders          | No missing records | 0% missing | Daily     | Data Eng  | Investigate |
| Consistency    | KPI Definitions | Matches dictionary | 100%       | Ongoing   | Analytics | Review      |

---

## Risks & Assumptions

| Type       | Description                    | Impact | Mitigation                 |
| ---------- | ------------------------------ | ------ | -------------------------- |
| Risk       | Customer matching inconsistent | High   | Build identity mapping     |
| Risk       | Marketing attribution unclear  | High   | Define attribution rules   |
| Assumption | NetSuite = revenue truth       | High   | Confirm with Finance       |
| Assumption | Monthly grain sufficient       | Medium | Validate with stakeholders |

