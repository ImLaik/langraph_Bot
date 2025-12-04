CROSS_SELL_DASHBOARD_DATA_DICTIONARY = f"""



# SPINNAKER ANALYTICS DATABASE
 
**Database:** mog_spinnaker_analytics
**Schema:** cartalize

---
 
## Tables Overview
 
This database contains tables for Cartalize Product's Cross Sell Dashboard module for industry Employee Benefits. This database contains 1 tables for analytics on insurance market data, agent performance, geographic information, and sales opportunities.
 
---


Table: cross_sell_dashboard_data

Columns:
sr_no (NUMERIC): Sequential identifier for each row in the dashboard.
product_a (TEXT): Name of Product A in the cross-sell pair.
product_b (TEXT): Name of Product B in the cross-sell pair.
support_a_b (NUMERIC): Support metric for the co-occurrence of Product A and Product B.
confidence_a_b (NUMERIC): Confidence metric indicating the likelihood of Product B given Product A.
lift_a_b (NUMERIC): Lift metric showing the strength of association between Product A and Product B relative to random occurrence.
product_a_transactions (NUMERIC): Total number of transactions containing Product A.
product_b_transactions (NUMERIC): Total number of transactions containing Product B.
both_transactions (NUMERIC): Total number of transactions where both Product A and Product B were purchased together.
support_a (NUMERIC): Support metric for Product A individually.
support_b (NUMERIC): Support metric for Product B individually.
score (NUMERIC): Calculated score representing the strength or importance of the cross-sell pair.
exclusive_counts_a (NUMERIC): Count of transactions that include Product A but exclude Product B.
exclusive_counts_b (NUMERIC): Count of transactions that include Product B but exclude Product A.
sr_no_for_sort (NUMERIC): Serial number used specifically for sorting dashboard results.
rank (NUMERIC): Rank of the cross-sell pair based on score, lift, or other prioritization metric.
exclusive_count_a (INTEGER): Integer version of exclusive transactions for Product A.
exclusive_count_b (INTEGER): Integer version of exclusive transactions for Product B.
score_transformed (NUMERIC): Normalized or transformed score for better comparability across pairs.
total_count_for_2_prod (NUMERIC): Total number of transactions involving either Product A, Product B, or both.
new_product_b (TEXT): Updated or alternate designation for Product B if applicable.
a_percent (NUMERIC): Percentage of total transactions containing Product A.
b_percent (NUMERIC): Percentage of total transactions containing Product B.
both_percent (NUMERIC): Percentage of total transactions containing both Product A and Product B.
a_percent_slicer (TEXT): Categorical slicer derived from a_percent for filtering in dashboards.
b_percent_slicer (TEXT): Categorical slicer derived from b_percent for filtering in dashboards.
both_percent_slicer (TEXT): Categorical slicer derived from both_percent for filtering in dashboards.

"""
