# Technical Requirements: Executive Performance Dashboard - Technical Requirements

## Data Source

- File: executive_performance_dummy_data.csv
- Grain: **1 row per order**
- Time grain: daily

## Key Fields

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

## Calculated Fields (Tableau)

| **KPI** | **Calculation** | **Settings** 
| --- | --- | --- |
| Revenue | SUM(\[revenue\]) ||
| Gross Margin % | SUM(\[gross_profit\]) / SUM(\[revenue\]) ||
| Revenue Growth % (MoM) | (SUM(\[revenue\]) - LOOKUP(SUM(\[revenue\]), -1)) / ABS(LOOKUP(SUM(\[revenue\]), -1)) | Set table calc to: - compute using **month** |
| ROAS | SUM(\[revenue\]) / SUM(\[ad_spend\]) ||
| Top Product Contribution | IF \[top_product_group\] = "Top 10% Product" THEN "Top 10%" ELSE "Long Tail" END ||


## Dashboard Structure

### Layout

- Top: KPI cards
- Middle left: Revenue trend
- Middle right: Revenue by Channel
- Bottom left: Margin by Product Category
- Bottom right: Top Product Contribution

### Filters (Global)

- Date (default: last 90 days or YTD)
- Channel
- Region
- Product Category

## Performance Considerations

- Use aggregated calculations (SUM, not row-level calcs)
- Limit number of filters
- Avoid excessive table calculations
- Use extracts if dataset grows

## Data Validation Checks

- Revenue matches sum of dataset
- Gross Margin % within expected range (~30-60%)
- ROAS within realistic bounds
- No null or missing critical fields