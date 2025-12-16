INTELLIGENT_GOAL_SETTER_DATA_DICTIONARY = """
# SPINNAKER ANALYTICS DATABASE
 
**Database:** mog_spinnaker_analytics
**Schema:** public

---
 
## Tables Overview
 
This database contains tables for Sales Prophet Sales Planning module for industries Individual Life, Employee Benefits and Property & Casualty. This database contains 1 table for analytics on insurance market data sales goals.
 
---
 
## Table: sales_goals

**COLUMNS:**


region (TEXT): Geographic region associated with the sales or organizational area.
field_office (TEXT): Name or identifier of the field office.
field_office_manager (TEXT): Manager responsible for the field office.
sales_target (INTEGER): Assigned sales target for the office or region.
current_sales (INTEGER): Current sales achieved to date.
sales_goal (NUMERIC): Overall sales goal set for the office or region.
sales_target_increment_percent (NUMERIC): Percentage increase applied to the sales target.
sales_increment (NUMERIC): Amount of sales increase needed or achieved.
ul (NUMERIC): Sales value or metric for UL product category.
wl (NUMERIC): Sales value or metric for WL product category.
tl (NUMERIC): Sales value or metric for TL product category.
iul (NUMERIC): Sales value or metric for IUL product category.
vul (NUMERIC): Sales value or metric for VUL product category.
sales_target_in_million (TEXT): Sales target expressed in millions.
country (TEXT): Country designation for the field office or sales region.

"""
