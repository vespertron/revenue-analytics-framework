**Business Requirements**

**Title**

**Executive Performance Dashboard - Business Requirements**

**Objective**

Provide leadership with a **clear, trusted view of business performance**, enabling fast decisions on revenue, profitability, and marketing efficiency.

**Key Business Questions**

This is the most important section.

- How is revenue trending over time?
- Which channels are driving the most revenue?
- Which products are most and least profitable?
- Are we operating efficiently (ROAS, CAC)?
- Where should we focus or adjust investment?

**Primary KPIs**

**Revenue**

- Total Revenue
- Revenue Growth %
- Revenue by Channel
- Revenue by Product Category

**Profitability**

- Gross Margin %
- Gross Profit
- Margin by Product Category

**Efficiency**

- ROAS
- CAC _(optional if not fully modeled yet)_

**Dimensions / Filters**

- Date (Day / Month / Quarter)
- Channel (Direct, Google Ads, Amazon, Distributor)
- Product Category
- Region
- Customer Segment

**Required Visuals**

**KPI Summary (Top Row)**

- Revenue
- Revenue Growth %
- Gross Margin %
- ROAS

**Trends**

- Revenue over time (line chart)

**Breakdown**

- Revenue by Channel (bar chart)
- Margin by Product Category (bar chart)

**Distribution / Insight**

- Revenue by Top Product Group (Top 10% vs Long Tail)

**Success Criteria**

- KPIs are consistent and aligned with definitions
- Dashboard loads quickly and is easy to interpret
- Enables identification of high- and low-performing areas
- Supports executive-level decision-making



**Technical Requirements (Executive Dashboard)**

**Title**

**Executive Performance Dashboard - Technical Requirements**

**Data Source**

- File: executive_performance_dummy_data.csv
- Grain: **1 row per order**
- Time grain: daily

**Key Fields**

**Dimensions**

- order_date
- channel
- product_category
- region
- customer_segment
- top_product_group

**Measures**

- revenue
- gross_profit
- cogs
- ad_spend
- units
- orders

**Calculated Fields (Tableau)**

**Revenue**

SUM(\[revenue\])

**Gross Margin %**

SUM(\[gross_profit\]) / SUM(\[revenue\])

**Revenue Growth % (MoM)**

(SUM(\[revenue\]) - LOOKUP(SUM(\[revenue\]), -1))  
/ ABS(LOOKUP(SUM(\[revenue\]), -1))

Set table calc to:

- compute using **month**

**ROAS**

SUM(\[revenue\]) / SUM(\[ad_spend\])

**Top Product Contribution**

IF \[top_product_group\] = "Top 10% Product" THEN "Top 10%"  
ELSE "Long Tail"  
END

**Dashboard Structure**

**Layout**

- Top: KPI cards
- Middle left: Revenue trend
- Middle right: Revenue by Channel
- Bottom left: Margin by Product Category
- Bottom right: Top Product Contribution

**Filters (Global)**

- Date (default: last 90 days or YTD)
- Channel
- Region
- Product Category

**Performance Considerations**

- Use aggregated calculations (SUM, not row-level calcs)
- Limit number of filters
- Avoid excessive table calculations
- Use extracts if dataset grows

**Data Validation Checks**

- Revenue matches sum of dataset
- Gross Margin % within expected range (~30-60%)
- ROAS within realistic bounds
- No null or missing critical fields