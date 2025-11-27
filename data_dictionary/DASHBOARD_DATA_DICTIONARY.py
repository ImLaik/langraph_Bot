DASHBOARD_DATA_DICTIONARY = f"""


# SPINNAKER ANALYTICS DATABASE
 
**Database:** mog_spinnaker_analytics
**Schema:** 4qast

---
 
## Tables Overview
 
This database contains tables for 4Qast Product's 4Qast Dashboard module. This database contains 9 tables for analytics on insurance market data, agent performance, geographic information, and sales opportunities.
 
---


Table: il_4qast_console_data

Columns:

year (INTEGER): Calendar year associated with the record.
id (INTEGER): Unique identifier for each console data record.
sales_actual (DOUBLE PRECISION): Actual sales recorded for the month or period.
fcast_sales_a (INTEGER): Forecasted sales under scenario A.
fcast_sales_b (INTEGER): Forecasted sales under scenario B.
sales_forecast (INTEGER): Main forecast value for sales.
lower_bound (INTEGER): Lower confidence boundary for sales forecast.
upper_bound (INTEGER): Upper confidence boundary for sales forecast.
sales_last_year (DOUBLE PRECISION): Sales amount from the same period in the prior year.
sales_goal (DOUBLE PRECISION): Target or goal amount for sales.
sales_prior_forecast (INTEGER): Forecast value from the previous forecast cycle.
ytd_forecast (DOUBLE PRECISION): Year-to-date forecasted sales.
ytd_forecast_prior (DOUBLE PRECISION): Prior cycle’s year-to-date forecast.
sold_month (INTEGER): Numeric month when sales were recognized.
lives_sort (INTEGER): Category or sort order for lives count grouping.
segment (VARCHAR): Business or market segment for the record.
month (VARCHAR): Month label corresponding to the sales or forecast entry.
unique_id (VARCHAR): Unique key linking console data to waterfall data.
ytd_index (VARCHAR): Indicator flag showing whether record contributes to YTD metrics.
current_yr_ind (VARCHAR): Flag indicating if the record belongs to the current year.
drop_column (VARCHAR): Helper transformation column (typically ignored in reporting).
month_order (VARCHAR): Sort ordering value for months.
fcast_ind (VARCHAR): Indicator specifying whether the row is forecast-related.
territory (VARCHAR): Sales territory associated with the record.
sales_region (VARCHAR): Sales region classification.
sales_territory (VARCHAR): Territory identifier used for sales reporting.
product_category (VARCHAR): Product grouping classification.
product (VARCHAR): Specific product represented in the record.
lives_cat (VARCHAR): Category of covered lives (size grouping).

Table: il_4qast_waterfall_tab

Columns:

year (INTEGER): Calendar year of the waterfall record.
sales (NUMERIC): Sales amount for the given waterfall component.
sold_month (INTEGER): Numeric month of sale recognition.
unique_id (VARCHAR): Key linking waterfall data to console data.
sales_region (VARCHAR): Regional classification associated with the waterfall entry.
sales_territory (VARCHAR): Territory identifier for waterfall reporting.
product (VARCHAR): Product represented in the waterfall entry.
lives_cat (VARCHAR): Group/category for lives count.
segment (VARCHAR): Business or customer segment.
month (VARCHAR): Month label used in waterfall reporting.
forecast_ind (CHARACTER): Indicator specifying forecast contribution.
ytd_ind (CHARACTER): Flag identifying YTD rows.
current_yr_ind (CHARACTER): Flag showing if the row relates to the current year.
waterfall_type (VARCHAR): Type of waterfall component (e.g., actual, delta, adjustment).

"""
