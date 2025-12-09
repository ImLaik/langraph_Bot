LEAD_PRIORITIZER_DATA_DICTIONARY = f"""

# SPINNAKER ANALYTICS DATABASE
 
**Database:** mog_spinnaker_analytics
**Schema:** lead_prioritizer

---
 
## Tables Overview
 
This database contains tables for Lead Prioritizer Product for industry Employee Benefits. This contains 2 table for analytics on insurance market data and prioritizing cases for underwriters.
---

Table: demo_lp_il_scores

variable (TEXT): Variable category being scored (e.g., Product, Income, Age).
attribute (TEXT): Specific attribute value of the variable category (e.g., “IUL” for Product).
score (NUMERIC): Score assigned to the attribute based on the scoring model.
percentile_rank (NUMERIC): Rank from 0–1 representing the percentile position of the attribute relative to others.

Table: demo_lp_il_workinventory

id (NUMERIC): Unique identifier for each lead/case record.
submit_date (TEXT): Date the lead was submitted.
client_name (TEXT): Name of the client/applicant (may be blank if not provided).
gender (TEXT): Gender of the applicant.
age (NUMERIC): Applicant’s age in years.
bmi (NUMERIC): Applicant’s calculated Body Mass Index.
bmi_bin (TEXT): Binned BMI category (e.g., “25–30”).
alcohol (TEXT): Whether the applicant consumes alcohol (“Yes”/“No”).
tobacco (TEXT): Whether the applicant uses tobacco (“Yes”/“No”).
income (NUMERIC or TEXT): Annual income of the applicant.
income_bin (TEXT): Binned income category (e.g., “$100–150k”).
state_cd (TEXT): U.S. state abbreviation of applicant location.
app_type (TEXT): Type of application (e.g., “Formal”).
product (TEXT): Insurance product applied for (e.g., Whole Life, IUL).
face_amount (NUMERIC): Requested face amount (coverage amount).
premium (NUMERIC): Annual premium amount quoted.
fa_bin (TEXT): Binned face amount category (e.g., “$500k–$1M”).
broker (TEXT): Broker or distribution partner associated with the case.
underwriter (TEXT): Underwriter assigned to evaluate the case.
assessment (TEXT): Underwriter’s assessment or internal status/notes.
gender_score (NUMERIC): Score associated with the applicant’s gender.
age_score (NUMERIC): Score associated with the applicant’s age.
bmi_score (NUMERIC): Score based on BMI category.
alcohol_score (NUMERIC): Score assigned based on alcohol use.
tobacco_score (NUMERIC): Score assigned based on tobacco use.
income_score (NUMERIC): Score associated with the applicant's income.
state_score (NUMERIC): Score assigned to the applicant’s state.
type_score (NUMERIC): Score assigned to app type.
product_score (NUMERIC): Score associated with selected product.
fa_score (NUMERIC): Score based on face amount category.
broker_score (NUMERIC): Score based on broker performance.
gender_pct (NUMERIC): Percentile rank for gender (0–1).
age_pct (NUMERIC): Percentile rank for age (0–1).
bmi_pct (NUMERIC): Percentile rank for BMI (0–1).
alcohol_pct (NUMERIC): Percentile rank for alcohol (0–1).
tobacco_pct (NUMERIC): Percentile rank for tobacco (0–1).
income_pct (NUMERIC): Percentile rank for income (0–1).
state_pct (NUMERIC): Percentile rank for state (0–1).
type_pct (NUMERIC): Percentile rank for application type (0–1).
product_pct (NUMERIC): Percentile rank for product type (0–1).
fa_pct (NUMERIC): Percentile rank for face amount (0–1).
broker_pct (NUMERIC): Percentile rank for broker (0–1).
status (TEXT): Workflow status of the lead (e.g., “Open”).
lead_score (NUMERIC): Final aggregated lead score combining all attributes.
lead_action (TEXT): Recommended action category (e.g., “High Priority”).

"""
