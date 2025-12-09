CROSS_SELL_ENGINE_DATA_DICTIONARY = f"""


# SPINNAKER ANALYTICS DATABASE
 
**Database:** mog_spinnaker_analytics
**Schema:** cartalize

---
 
## Tables Overview
 
This database contains tables for Cartalize Product's Cross Sell Engine  module for industry Employee Benefits. This database contains 1 table for analytics on insurance market data, agent performance, geographic information, and sales opportunities.
 
---

Table: eb_cse_cross_sell_engine_data

id (INTEGER): Unique record identifier.
support_a_b (NUMERIC): Joint support value for product A and B.
confidence_a_b (NUMERIC): Confidence level of A predicting B.
lift_a_b (NUMERIC): Lift score for A→B association.
product_a_transactions (INTEGER): Count of transactions where product A appears.
product_b_transactions (INTEGER): Count of transactions where product B appears.
both_product_transactions (INTEGER): Count where both A and B appear together.
support_a (NUMERIC): Support value of product A.
support_b (NUMERIC): Support value of product B.
score (NUMERIC): Model score for cross-sell recommendation.
exclusive_counts_a (INTEGER): Count where only A is purchased.
exclusive_counts_b (INTEGER): Count where only B is purchased.
serial_number_for_sort (INTEGER): Sorting serial value.
rank (INTEGER): Rank of association rules.
exclusive_count_a (INTEGER): Alternate field for exclusive A counts.
exclusive_count_b (INTEGER): Alternate field for exclusive B counts.
score_transformed (NUMERIC): Transformed score for normalized ranking.
column_18 (NUMERIC): Miscellaneous numeric value.
column_19 (INTEGER): Miscellaneous integer value.
total_count_for_2_products (INTEGER): Total count referencing two-product sets.
a_percent (NUMERIC): Percent of records with product A.
b_percent (NUMERIC): Percent of records with product B.
both_percent (NUMERIC): Percent where both appear.
new_product_b (TEXT): Product B label used for BI display.
a_percent_slicer (TEXT): Slicer label for A percent.
b_percent_slicer (TEXT): Slicer label for B percent.
both_percent_slicer (TEXT): Slicer label for both percent.
product_a (TEXT): Product A identifier.
product_b (TEXT): Product B identifier.

"""
 