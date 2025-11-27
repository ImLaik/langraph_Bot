BROKER_SCORE_CARD_DATA_DICTIONARY = """
# SPINNAKER ANALYTICS DATABASE
 
**Database:** mog_spinnaker_analytics
**Schema:** public

---
 
## Tables Overview
 
This database contains tables for Sales Prophet MOG module for industry Individual Life. This database contains 9 tables for analytics on insurance market data, agent performance, geographic information, and sales opportunities.
 
---
 
## Table: eb_bsc_inforce_es

**COLUMNS:**

index_col (BIGINT): Unique row identifier.
policy_number_x (BIGINT): Policy number associated with the record.
policy_name_x (VARCHAR): Name of the insurance policy.
benefit (VARCHAR): Benefit type or category.
group_office (VARCHAR): Office or region responsible for the group.
sales_rep (VARCHAR): Sales representative or agent responsible for the account.
policy_effective_date (TIMESTAMP): Original effective date of the policy.
renewal_date (TIMESTAMP): Policy renewal date.
benefit_effective_date (TIMESTAMP): Effective date of the benefit.
inforce_product_line (VARCHAR): Product line currently in force.
sic (BIGINT): Standard industrial classification code.
benefit_no_of_lives (BIGINT): Number of covered lives for the benefit.
sponsor_id (DOUBLE PRECISION): Identifier for the policy sponsor or group.
issued_state (VARCHAR): State in which the policy was issued.
market_segment_indicator (VARCHAR): Indicator specifying the market segment (e.g., small group, large group).
pol_status (VARCHAR): Policy status.
product_line (VARCHAR): Line of insurance product.
renewal_case_id (DOUBLE PRECISION): Identifier for the renewal case.
coverage (VARCHAR): Type of coverage.
original_eff_date (TIMESTAMP): Original effective date of the coverage or policy.
benefit_eff_date (TIMESTAMP): Effective date for the specific benefit.
size (VARCHAR): Size classification of the group or account.
coverage_no_of_lives (DOUBLE PRECISION): Number of lives covered under the coverage.
client_max_no_of_lives (DOUBLE PRECISION): Maximum number of lives allowed for the client or group.
total_eligible_lives (DOUBLE PRECISION): Total number of eligible insured lives.
inforce_prerenewal_premium (DOUBLE PRECISION): Premium amount in-force before renewal.
sold_premium (DOUBLE PRECISION): Premium amount sold or agreed upon.
formula_annual_premium (DOUBLE PRECISION): Formula-calculated annual premium.
uw_formula_annual_premium (DOUBLE PRECISION): Underwriting formula annual premium.
renewal_philosophy_annual_premium (DOUBLE PRECISION): Premium based on renewal philosophy.
quoted_premium (DOUBLE PRECISION): Quoted premium amount for the renewal.
final_app_adj_ann_premium (DOUBLE PRECISION): Final approved, adjusted annual premium.
manual_premium (DOUBLE PRECISION): Manually rated premium amount.
administration_system (VARCHAR): System used to administer the policy.
outlier (VARCHAR): Indicator for outlier classification.
aso (VARCHAR): Whether the case is administrative-services-only (ASO).
file_year (DOUBLE PRECISION): Filing or reporting year.
renewal_premium (DOUBLE PRECISION): Final renewal premium amount.
bds_id (DOUBLE PRECISION): Identifier from BDS system or database.
uid (VARCHAR): Unique identifier for the record.
lives_bin (VARCHAR): Binned or categorized number of lives.
sic_cat (VARCHAR): SIC category grouping.
sic_ind (VARCHAR): SIC industry indicator.
column1 (BIGINT): Additional or legacy column value.
renewal_date_1 (TIMESTAMP): Alternate or adjusted renewal date.
uid1 (VARCHAR): Alternate unique identifier.
lives_bin1 (VARCHAR): Secondary lives bin classification.


## Table: eb_bsc_pol_by_pol_es

**COLUMNS:**

column1 (BIGINT): General-purpose or legacy column identifier.
policy (BIGINT): Policy identifier associated with the record.
year_incurred (BIGINT): Year in which claims were incurred.
premium (BIGINT): Premium amount for the period.
incurred_claims (BIGINT): Total incurred claim amount.
claim_count (BIGINT): Number of claims incurred.
expense (DOUBLE PRECISION): Expense amount associated with the policy or period.
commissions (BIGINT): Total commission amount paid.
mgis_fee (BIGINT): MGIS or administrative fee amount.
premium_tax (DOUBLE PRECISION): Premium tax amount.
expected_claims (BIGINT): Expected or projected claim amount.
inforce_months (BIGINT): Number of months the policy was in force.
type (VARCHAR): Type or classification of the record.
lives (BIGINT): Number of covered lives.
sponsor_id (BIGINT): Identifier for the policy sponsor or group.
territory (VARCHAR): Territory, region, or geographic classification.
bds_id (DOUBLE PRECISION): Identifier from BDS system or database.
uid (VARCHAR): Unique identifier for the record.
year (BIGINT): Reporting or data year.
uid_1 (VARCHAR): Alternate or secondary unique identifier.
year_1 (DOUBLE PRECISION): Alternate or adjusted year value.


## Table: eb_bsc_renewals_with_brokers

policy_number (BIGINT): Unique identifier for the policy.
policy_name (VARCHAR): Name of the policy.
plan_status (VARCHAR): Status of the plan.
pol_status (VARCHAR): Additional or alternative policy status.
product_line (VARCHAR): Product line classification.
renewal_case_id (BIGINT): Identifier for the renewal case.
coverage (VARCHAR): Type of coverage.
issue_age_yes_no (VARCHAR): Indicates whether issue age applies.
billing_type (VARCHAR): Billing method.
sic_code (BIGINT): Standard Industry Classification code.
seq_num (DOUBLE PRECISION): Sequence number.
true_group_or_voluntary (VARCHAR): Indicates group vs voluntary classification.
territory (VARCHAR): Territory or region of business.
renew_month (VARCHAR): Renewal month.
renew_year (INTEGER): Renewal year.
market_segment (VARCHAR): Market segment classification.
financial_institution_ind (VARCHAR): Financial institution indicator.
generali (VARCHAR): Generali-related indicator or flag.
approved_by (VARCHAR): Person who approved.
underwriter (VARCHAR): Underwriter assigned.
user_who_risk_approved (VARCHAR): User who approved risk.
date_of_risk_approval (VARCHAR): Risk approval date.
block_of_business (VARCHAR): Block of business classification.
region (VARCHAR): Geographic region.
business_arrangement (VARCHAR): Business arrangement type.
distribution (VARCHAR): Distribution description.
distribution_channel (VARCHAR): Channel used for distribution.
sales_rep (VARCHAR): Sales representative.
primary_distributor_name (VARCHAR): Name of the primary distributor.
renewal_start_date (VARCHAR): Renewal start date.
renewal_date (VARCHAR): Renewal date.
original_eff_date (VARCHAR): Original effective date.
benefit_eff_date (VARCHAR): Benefit effective date.
size (VARCHAR): Size category.
coverage_no_of_lives (DOUBLE PRECISION): Number of lives covered.
client_max_no_of_lives (DOUBLE PRECISION): Maximum number of client lives.
total_eligible_lives (DOUBLE PRECISION): Total eligible lives.
mock_census_indicator (VARCHAR): Mock census indicator.
inforce_prerenewal_premium (BIGINT): In-force premium before renewal.
sold_premium (DOUBLE PRECISION): Sold premium.
formula_annual_premium (DOUBLE PRECISION): Formula-based annual premium.
uw_formula_annual_premium (DOUBLE PRECISION): Underwriting formula annual premium.
renewal_philosophy_annual_premium (DOUBLE PRECISION): Philosophy annual premium.
quoted_premium (DOUBLE PRECISION): Quoted premium.
hard_dollars (DOUBLE PRECISION): Hard dollar amount.
final_app_adj_ann_premium (DOUBLE PRECISION): Final approved adjusted annual premium.
soft_dollars (DOUBLE PRECISION): Soft dollar amount.
field_pool_annual (DOUBLE PRECISION): Field pool annual amount.
manual_premium (DOUBLE PRECISION): Manual premium.
philosophy_increase (DOUBLE PRECISION): Increase based on philosophy.
rating_method (VARCHAR): Rating method used.
total_benefit_volume (DOUBLE PRECISION): Total benefit volume.
original_rate_guarantee_period (INTEGER): Original rate guarantee period.
renewal_rate_guarantee_period (INTEGER): Renewal rate guarantee period.
rate_guarantee_expiring (VARCHAR): Expiration of rate guarantee.
renewal_rate_cap (INTEGER): Renewal rate cap.
target_lr_pol_by_pol (DOUBLE PRECISION): Target loss ratio (policy-level).
actual_lr_pol_by_pol (DOUBLE PRECISION): Actual loss ratio (policy-level).
premium_pol_by_pol (DOUBLE PRECISION): Premium (policy-level).
incrd_clms_pol_by_pol (DOUBLE PRECISION): Incurred claims (policy-level).
expctd_clsm_pol_by_pol (DOUBLE PRECISION): Expected claims (policy-level).
target_lr_rating (DOUBLE PRECISION): Target loss ratio for rating.
pre_renewal_rtf (DOUBLE PRECISION): Pre-renewal rating factor.
post_renewal_rtf (DOUBLE PRECISION): Post-renewal rating factor.
philosophy_adjustment_lr (DOUBLE PRECISION): Philosophy adjustment loss ratio.
formula_adjustment_lr (DOUBLE PRECISION): Formula adjustment loss ratio.
quoted_philosophy_lr (INTEGER): Quoted philosophy loss ratio.
anticipated_lr (DOUBLE PRECISION): Anticipated loss ratio.
coverage_benefit_name (VARCHAR): Coverage or benefit name.
conversion_indicator (VARCHAR): Conversion indicator.
fully_credible (INTEGER): Credibility indicator.
credibility (DOUBLE PRECISION): Credibility factor.
administration_system (VARCHAR): Administration system used.
uw_pool (DOUBLE PRECISION): Underwriting pool amount.
total_pool_charges (DOUBLE PRECISION): Total pool charges.
pool_reason_adjustment (VARCHAR): Adjustment reason for pool.
adjustment_note (TEXT): Notes on adjustments.
benefit_admin_platform (VARCHAR): Benefit administration platform.
digital_partnership_fee (DOUBLE PRECISION): Digital partnership fee.
service_fee (VARCHAR): Service fee.
private_exchange (VARCHAR): Private exchange indicator.
edx_feed_request (VARCHAR): EDX feed request indicator.
outlier (VARCHAR): Outlier indicator.
aso (VARCHAR): ASO indicator.
file_year (INTEGER): File year.
bds_firm_id (DOUBLE PRECISION): BDS firm ID.
bds_firm_name (VARCHAR): BDS firm name.
renewal_premium (DOUBLE PRECISION): Renewal premium.
sponsor_id (DOUBLE PRECISION): Sponsor ID.
renewals_uid (VARCHAR): Renewal unique identifier.
persistent_premium (INTEGER): Persistent premium value.
persistent_benefits (INTEGER): Persistent benefits count.
renewal_package_persistency_inclusion (INTEGER): Inclusion flag for persistency.
persistency_filter (VARCHAR): Filter applied for persistency.
renewals_uid1 (VARCHAR): Secondary renewal UID.
persistent_premium1 (INTEGER): Secondary persistent premium.
persistent_benefits1 (INTEGER): Secondary persistent benefits.
persistency_filter1 (VARCHAR): Secondary persistency filter.

## Table: eb_bsc_slf_broker_by_policy_prod

** COLUMNS:**

policy_number (BIGINT): Unique identifier for the policy.
sponsor_id (BIGINT): Unique ID of the sponsoring company or group.
sponsor_name (VARCHAR): Name of the sponsoring company or group.
territory (VARCHAR): Geographic territory associated with the policy or sponsor.
bds_firm_id (VARCHAR): BDS firm identifier.
bds_firm_name (VARCHAR): Name of the BDS firm.
product_line (VARCHAR): Product line classification.
uid (VARCHAR): Primary unique identifier for product or policy record.
renewals_uid (VARCHAR): Unique identifier used for renewals.
broker_rank (INTEGER): Rank or tier assigned to the broker.
broker_short_name (VARCHAR): Short name or abbreviation of the broker.
prod_policy (VARCHAR): Product-policy relationship indicator.
sponsor_product_uid (VARCHAR): Unique identifier for sponsor-product mapping.
short_product_name (VARCHAR): Shortened or abbreviated product name.
uid2 (VARCHAR): Secondary unique identifier.
renewals_uid2 (VARCHAR): Secondary renewals unique identifier.
prod_policy1 (VARCHAR): Secondary product-policy indicator.
sponsor_product_uid1 (VARCHAR): Secondary sponsor-product unique identifier.
short_product_name1 (VARCHAR): Secondary short product name.
territy_sort (DOUBLE PRECISION): Territory sorting or ranking value.

 
"""
