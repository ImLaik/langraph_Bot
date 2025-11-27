LEADERSHIP_DATA_DICTIONARY = """



# SPINNAKER ANALYTICS DATABASE
 
**Database:** mog_spinnaker_analytics
**Schema:** 4qast

---
 
## Tables Overview
 
This database contains tables for 4Qast Product's Leadership Dashboard module for industry Individual Life. This database contains 9 tables for analytics on insurance market data, agent performance, geographic information, and sales opportunities.
 
---


#Table: leadership_db_core_revenue

Columns:

biz_segment (TEXT): Business segment associated with the core revenue record.
region (TEXT): Geographic region tied to the revenue entry.
profit_center (TEXT): Internal profit center responsible for revenue performance.
core_revenue_actual (NUMERIC): Actual core revenue recognized for the period.
core_revenue_budget (NUMERIC): Budgeted or planned revenue for the period.
core_revenue_prior (NUMERIC): Revenue value from the prior comparable period.
uid (TEXT): Unique identifier for the revenue record.
date_field (TIME WITHOUT TIME ZONE): Time-based key aligned with the date dimension table.

#Table: leadership_db_date_dimension

Columns:

date_field (TIME WITHOUT TIME ZONE): Base date/time used for mapping all time-series data.
year (INTEGER): Year extracted from the date.
month (TEXT): Month name corresponding to the date.
month_number (INTEGER): Numeric month (1–12).
quarter (TEXT): Fiscal quarter designation (e.g., Q1, Q2).
effective_slicer (TEXT): Calendar grouping key used for BI/PowerBI filters.
date_eom (TIME WITHOUT TIME ZONE): End-of-month date for the given period.
running_month (INTEGER): Relative month counter used for sequential time analysis.

Table: leadership_db_fast_output

Columns:

date_field (TIME WITHOUT TIME ZONE): Calendar date associated with the metric.
actuals (NUMERIC): Actual reported amount for the metric category.
region (TEXT): Region associated with the metric.
account (TEXT): Accounting account tied to financial reporting.
subaccount (TEXT): Sub-level accounting detail for finer categorization.
metric_category (TEXT): High-level performance metric grouping.
month_num (INTEGER): Numeric month for time-based calculations.
ap_combined_forecast_prior_month (NUMERIC): Forecast amount from prior month’s snapshot.
ap_combined_forecast_curr_month (NUMERIC): Forecast value generated in the current month.
prior (NUMERIC): Equivalent metric value from a prior period.
fast_aug (NUMERIC): FAST system projection for August.
date_month_start (TIME WITHOUT TIME ZONE): First day of the month for the record.
fast_current_month (NUMERIC): FAST forecast for the current month.
fast_prior_month (NUMERIC): FAST forecast from the previous month.
fast_sep (NUMERIC): FAST forecast for September.
biz_segment (TEXT): Business segment tied to the metric. 
fast_oct (NUMERIC): FAST forecast for October.
fast_nov (NUMERIC): FAST forecast for November.
fast_dec (NUMERIC): FAST forecast for December.
budget (NUMERIC): Planned or budgeted value for the metric.
fast_jan (NUMERIC): FAST forecast for January.
fast_feb (NUMERIC): FAST forecast for February.
fast_mar (NUMERIC): FAST forecast for March.
fast_apr (NUMERIC): FAST forecast for April.
fast_may (NUMERIC): FAST forecast for May.
fast_jun (NUMERIC): FAST forecast for June.
fast_jul (NUMERIC): FAST forecast for July.
fast_jan_25 (NUMERIC): FAST forecast for January 2025.

*Table: leadership_db_fast_output_unpivoted

Columns:

date_field (TIME WITHOUT TIME ZONE): Calendar date used for metric alignment.
region (TEXT): Reporting region.
metric_category (TEXT): Category grouping for the metric.
account (TEXT): Accounting account descriptor.
subaccount (TEXT): Subaccount classification detail.
value_type (TEXT): Indicates whether value is actual, forecast, budget, etc.
value (NUMERIC): Numeric amount for the unpivoted metric.
date_month_start (TIME WITHOUT TIME ZONE): First day of the month.
biz_segment (TEXT): Business segment related to the metric.

*Table: leadership_db_master_file

Columns:

metric_category (TEXT): Top-level metric grouping (e.g., revenue, expense).
metric_type (TEXT): Type of metric (actual, budget, variance, etc.).
metric (TEXT): Specific metric name.
actual (NUMERIC): Actual performance value.
prior (NUMERIC): Prior period metric value.
budget (TEXT): Budgeted or planned value.
profit_center (TEXT): Internal profit center identifier.
year (INTEGER): Year for the metric entry.
month (TEXT): Month name.
month_number (INTEGER): Numeric month (1–12).
uid (TEXT): Unique identifier for the master file record.
full_date (TEXT): Combined date stamp as text.
blank (TEXT): Placeholder field, often unused.
drivers (TEXT): Driver description for metric calculations.
date (TEXT): Date stored as text.
time (TEXT): Time stored as text.
segment (TEXT): Business segment classification.
metrics_detailed (TEXT): More granular metric descriptor.
forecast (TEXT): Forecasted value.
uid_revnet (TEXT): Unique key linking to revenue network logic.
business_segment (TEXT): Business segment detail.
platform (TEXT): Platform or system where metric originates.
uid_core_revenue (TEXT): Link to core revenue UID.
line_of_business (TEXT): Product or service line classification.
region (TEXT): Region assigned to the metric.
region_original (TEXT): Historical or original region assignment.

*Table: leadership_db_master_file_unpivoted

Columns:

metric_category (TEXT): High-level metric grouping.
metric_type (TEXT): Type of metric (actual, forecast, etc.).
metric (TEXT): Name of the metric.
profit_center (TEXT): Profit center responsible for performance.
region (TEXT): Geographic region.
year (INTEGER): Calendar year.
month (TEXT): Calendar month.
month_num (INTEGER): Numeric month.
uid (TEXT): Unique identifier for the unpivoted record.
drivers (TEXT): Drivers influencing the metric.
segment (TEXT): Business segment classification.
time_field (TIME WITHOUT TIME ZONE): Time component of the timestamp.
metrics_detailed (TEXT): Granular metric description.
biz_segment (TEXT): Business segment.
platform (TEXT): Platform source of metric.
line_of_business (TEXT): Business line grouping.
value_type (TEXT): The type of metric value (actual, forecast, etc.).
value (NUMERIC): Measured or calculated value.

"""
