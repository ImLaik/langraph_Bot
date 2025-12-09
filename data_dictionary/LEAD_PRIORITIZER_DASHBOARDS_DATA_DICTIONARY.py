LEAD_PRIORITIZER_DASHBOARDS_DATA_DICTIONARY = f"""
# SPINNAKER ANALYTICS DATABASE
 
**Database:** mog_spinnaker_analytics
**Schema:** lead_prioritizer

---
 
## Tables Overview
 
This database contains tables for Lead Prioritizer Product for industry Employee Benefits. This contains 1 table for analytics on insurance market data and prioritizing cases for underwriters.
---

Table: demo_il_lp_dashboard_data

case_id (NUMERIC): Unique identifier for the case/application.
submit_date (TEXT): Date the case was submitted (e.g., ISO-8601 string "YYYY-MM-DD").
client_name (TEXT): Full name of the client/applicant.
gender (TEXT): Client gender label (e.g., Male/Female/Other).
age (NUMERIC): Client age in years.
age_rand (NUMERIC): Randomized/perturbed age for anonymization or testing purposes.
age_bin (TEXT): Age bucket label (e.g., "18–24", "25–34").
bmi (NUMERIC): Client Body Mass Index value.
bmi_rand (NUMERIC): Randomized/perturbed BMI for anonymization or testing.
bmi_bin (TEXT): BMI bucket label (e.g., "Normal", "Overweight").
alcohol (TEXT): Alcohol usage category or disclosure (e.g., "None", "Moderate", "Heavy").
tobacco (TEXT): Tobacco usage category or disclosure (e.g., "Non-smoker", "Smoker").
income (NUMERIC): Client annual income.
income_rand (NUMERIC): Randomized/perturbed income for anonymization or testing.
income_bin (TEXT): Income bucket label (e.g., "<50k", "50–100k").
state_cd (TEXT): State or region code (e.g., US state abbreviation).
state_rand (NUMERIC): Randomized surrogate or numeric index for state/region used for anonymization or sorting.
app_type (TEXT): Type of application (e.g., "Online", "Agent-assisted").
product (TEXT): Product applied for (e.g., policy or plan type).
face_amount (NUMERIC): Requested policy face amount (coverage amount).
fa_bin (TEXT): Face amount bucket label (e.g., "<100k", "100–250k").
broker (TEXT): Broker or agent associated with the case.
underwriter (TEXT): Underwriter or underwriting team handling the case.
gender_score (NUMERIC): Model score contribution attributable to gender.
age_score (NUMERIC): Model score contribution attributable to age.
bmi_score (NUMERIC): Model score contribution attributable to BMI.
alcohol_score (NUMERIC): Model score contribution attributable to alcohol usage.
tobacco_score (NUMERIC): Model score contribution attributable to tobacco usage.
income_score (NUMERIC): Model score contribution attributable to income.
state_score (NUMERIC): Model score contribution attributable to state/region.
type_score (NUMERIC): Model score contribution attributable to application type.
product_score (NUMERIC): Model score contribution attributable to product type.
fa_score (NUMERIC): Model score contribution attributable to face amount.
broker_score (NUMERIC): Model score contribution attributable to broker/agent factors.
lead_score (NUMERIC): Overall lead score combining feature contributions.
priority_action (TEXT): Recommended next-best action or priority (e.g., "Call now", "Email follow-up").
sold_flag (TEXT): Indicator if the case resulted in a sale (e.g., "Y"/"N").
case_count (NUMERIC): Count of cases in the cohort or aggregation associated with this record.
closing_ratio (NUMERIC): Ratio or percentage of cases closed/sold for this record or segment.
sold_flag_duplicate (TEXT): Duplicate of sold_flag used for reporting/aggregation convenience.
case_count_duplicate (NUMERIC): Duplicate of case_count used for reporting/aggregation convenience.
lead_score_bin_25 (NUMERIC): Indicator or index for lead_score binned at 25% intervals (e.g., quartile membership).
lead_score_bin_50 (NUMERIC): Indicator or index for lead_score binned at 50% intervals (e.g., top-half membership).
lead_score_bin_50_sort (NUMERIC): Sort key derived from the 50% lead score bin for ordered displays.
lead_score_bin_25_sort (NUMERIC): Sort key derived from the 25% lead score bin for ordered displays.
unsold_flag (TEXT): Indicator if the case did not result in a sale (e.g., "Y"/"N").
sold_flag_cat (TEXT): Categorical label of sale status (e.g., "Sold", "Unsold").
avg_closing_ratio (NUMERIC): Average closing ratio for the relevant group/segment/time window.
premium (NUMERIC): Actual written premium associated with the case (if sold).
expected_premium (NUMERIC): Predicted/expected premium estimated by the model.

"""
