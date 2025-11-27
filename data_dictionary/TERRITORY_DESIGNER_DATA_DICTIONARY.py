TERRITORY_DESIGNER_DATA_DICTIONARY = f"""


# SPINNAKER ANALYTICS DATABASE
 
**Database:** mog_spinnaker_analytics
**Schema:** public

---
 
## Tables Overview
 
This database contains tables for Sales Prophet Territory Designer module for industry Property & Casualty. This database contains 25 tables for analytics on insurance market data based on different Territories.
 
---



Table: rep_level_data_output

Columns:
territory (TEXT): Territory assigned to the rep.
rep (TEXT): Representative name or ID.
catholic_market_sales_premium (NUMERIC): Sales premium in the Catholic market.
catholic_population (NUMERIC): Catholic population in the rep's territory.
cuf_paid_premium (NUMERIC): Paid premium tracked by CUF.
cuf_sold_policies (NUMERIC): Number of policies sold tracked by CUF.

Table: sales_opty_annuity

Columns:
msa (TEXT): Metropolitan Statistical Area name.
county_number (NUMERIC): County number identifier.
county (TEXT): County name.
state (TEXT): State of the county.
market_size_life_premium (NUMERIC): Market size for life insurance premiums.
market_size_life_policies (NUMERIC): Market size for life insurance policies.
market_size_annuity_premium (NUMERIC): Market size for annuity premiums.
market_size_annuity_policies (NUMERIC): Market size for annuity policies.
market_population (NUMERIC): Total market population.
catholic_population (NUMERIC): Catholic population in the market.
cuf_life_sales_premium (NUMERIC): CUF life insurance sales premium.
cuf_life_sold_policies (NUMERIC): CUF life insurance sold policies.
cuf_annuity_sales_premium (NUMERIC): CUF annuity sales premium.
cuf_annuity_sales_policies (NUMERIC): CUF annuity sold policies.
cuf_life_members (NUMERIC): Number of CUF life members.
cuf_annuity_members (NUMERIC): Number of CUF annuity members.
cuf_active_parishes (NUMERIC): Number of active CUF parishes.
cuf_5_year_grants (NUMERIC): CUF grants paid over the last 5 years.
cuf_5_year_sold_policies (NUMERIC): CUF sold policies over the last 5 years.
cuf_reps_in_county (NUMERIC): Number of CUF reps in the county.
cuf_reps_within_50_miles (NUMERIC): Number of CUF reps within 50 miles.
cuf_life_sales_opty_policies (NUMERIC): Life insurance sales opportunity policies.
cuf_life_sales_opty_premium (NUMERIC): Life insurance sales opportunity premium.
cuf_life_sales_opty_reps (NUMERIC): Life insurance sales opportunity reps.
cuf_life_incremental_opty_policies (NUMERIC): Incremental life opportunity policies.
cuf_life_incremental_opty_premium (NUMERIC): Incremental life opportunity premium.
cuf_annuity_target_share (NUMERIC): Annuity target share.
cuf_annuity_sales_opty_policies (NUMERIC): Annuity sales opportunity policies.
cuf_annuity_sales_opty_premium (NUMERIC): Annuity sales opportunity premium.
cuf_annuity_sales_opty_reps (NUMERIC): Annuity sales opportunity reps.
cuf_annuity_incremental_opty_policies (NUMERIC): Incremental annuity opportunity policies.
cuf_annuity_incremental_opty_premium (NUMERIC): Incremental annuity opportunity premium.
cuf_l_plus_a_sales_opty_policies (NUMERIC): Life + annuity sales opportunity policies.
cuf_l_plus_a_sales_opty_premium (NUMERIC): Life + annuity sales opportunity premium.
cuf_l_plus_a_sales_opty_reps (NUMERIC): Life + annuity sales opportunity reps.
cuf_l_plus_a_incr_opty_policies (NUMERIC): Life + annuity incremental opportunity policies.
cuf_l_plus_a_incr_opty_premium (NUMERIC): Life + annuity incremental opportunity premium.
cuf_l_plus_a_incr_opty_reps (NUMERIC): Life + annuity incremental opportunity reps.
cuf_total_sales_premium (NUMERIC): Total CUF sales premium.
cuf_total_sold_policies (NUMERIC): Total CUF sold policies.

Table: territory_designer_sales_opty_life_table

Columns:
msa (TEXT): Metropolitan Statistical Area name.
county_number (NUMERIC): County number.
county (TEXT): County name.
state (TEXT): State of the county.
market_size_life_premium (NUMERIC): Market size for life insurance premiums.
market_size_life_policies (NUMERIC): Market size for life insurance policies.
market_size_annuity_premium (NUMERIC): Market size for annuity premiums.
market_size_annuity_policies (NUMERIC): Market size for annuity policies.
market_population (NUMERIC): Total market population.
catholic_population (NUMERIC): Catholic population in the market.
cuf_life_sales_premium (NUMERIC): CUF life insurance sales premium.
cuf_life_sold_policies (NUMERIC): CUF life insurance sold policies.
cuf_annuity_sales_premium (NUMERIC): CUF annuity sales premium.
cuf_annuity_sold_policies (NUMERIC): CUF annuity sold policies.
cuf_life_members (NUMERIC): Number of CUF life members.
cuf_annuity_members (NUMERIC): Number of CUF annuity members.
cuf_active_parishes (NUMERIC): Number of active CUF parishes.
cuf_5_year_grants (NUMERIC): CUF grants over last 5 years.
cuf_5_year_sold_policies (NUMERIC): CUF sold policies over last 5 years.
cuf_reps_in_county (NUMERIC): Number of CUF reps in county.
cuf_reps_within_50_miles (NUMERIC): Number of CUF reps within 50 miles.
cuf_life_sales_opty_policies (NUMERIC): Life insurance sales opportunity policies.
cuf_life_sales_opty_premium (NUMERIC): Life insurance sales opportunity premium.
cuf_life_sales_opty_reps (NUMERIC): Life insurance sales opportunity reps.
cuf_life_incr_opty_policies (NUMERIC): Life insurance incremental opportunity policies.
cuf_life_incr_opty_premium (NUMERIC): Life insurance incremental opportunity premium.
cuf_annuity_target_share (NUMERIC): Annuity target share.
annuity_sales_opty_policies (NUMERIC): Annuity sales opportunity policies.
cuf_annuity_sales_opty_premium (NUMERIC): CUF annuity sales opportunity premium.
cuf_annuity_sales_opty_reps (NUMERIC): CUF annuity sales opportunity reps.
cuf_annuity_sales_opty_policies (NUMERIC): CUF annuity sales opportunity policies.
cuf_annuity_incr_opty_premium (NUMERIC): CUF annuity incremental opportunity premium.
cuf_l_plus_a_sales_opty_policies (NUMERIC): Life + annuity sales opportunity policies.
cuf_l_plus_a_sales_opty_premium (NUMERIC): Life + annuity sales opportunity premium.
cuf_l_plus_a_sales_opty_reps (NUMERIC): Life + annuity sales opportunity reps.
cuf_l_plus_a_incr_opty_policies (NUMERIC): Life + annuity incremental opportunity policies.
cuf_l_plus_a_incr_opty_premium (NUMERIC): Life + annuity incremental opportunity premium.
cuf_l_plus_a_incr_opty_reps (NUMERIC): Life + annuity incremental opportunity reps.
cuf_total_sales_premium (NUMERIC): Total CUF sales premium.
cuf_total_sales_policies (NUMERIC): Total CUF sales policies.

Table: territory_designer_total_population

Columns:
year (NUMERIC): Year of population data.
state (TEXT): State of the population data.
zipcode (NUMERIC): Zip code of the population.
total_pop (NUMERIC): Total population in the zip code.

Table: territory_designer_mog_combined

Columns:
year (NUMERIC): Year of data.
state (TEXT): State of data.
zipcode (NUMERIC): Zip code.
income_level (NUMERIC): Income level category.
product (TEXT): Product type.
inforce_policies (NUMERIC): Number of inforce policies.
inforce_face_amount (NUMERIC): Inforce face amount.
inforce_premium (NUMERIC): Inforce premium amount.
sales_premium (NUMERIC): Sales premium amount.
sales_policies (NUMERIC): Number of sales policies.
sales_face_amount (NUMERIC): Sales face amount.
inc_lev (NUMERIC): Income level code.

Table: territory_designer_msa_distance_annuity

Columns:
msa (TEXT): MSA name.
num_of_reps_in_50_miles (NUMERIC): Number of reps within 50 miles of the MSA.

Table: new_team_geo_cuf_option

Columns:
county_num (NUMERIC): County number.
county (TEXT): County name.
state (TEXT): State name.
new_team_cuf_based (TEXT): New team assignment based on CUF.
new_region (TEXT): New region assignment.

Table: territory_designer_new_team_geo_market_option

Columns:
county_num (NUMERIC): County number.
county (TEXT): County name.
state (TEXT): State name.
new_team_mkt_based (TEXT): New team assignment based on market.
new_region (TEXT): Region assignment.
new_team_dei (TEXT): DEI-based team name.
new_team_name_color (NUMERIC): Team color code.
new_territory (TEXT): New territory name.

Table: territory_designer_recruiting_opty_table

Columns:
msa (TEXT): MSA name.
county_num (NUMERIC): County number.
county (TEXT): County name.
state (TEXT): State name.
market_size_life_premium (NUMERIC): Life market premium.
market_size_life_policies (NUMERIC): Life policies.
market_size_annuity_premium (NUMERIC): Annuity premium.
market_size_annuity_policies (NUMERIC): Annuity policies.
market_population (NUMERIC): Total population in market.
catholic_population (NUMERIC): Catholic population.
cuf_life_sales_premium (NUMERIC): CUF life insurance sales premium.
cuf_life_sold_policies (NUMERIC): CUF life insurance sold policies.
cuf_annuity_sales_premium (NUMERIC): CUF annuity sales premium.
cuf_annuity_sold_policies (NUMERIC): CUF annuity sold policies.
cuf_life_members (NUMERIC): Number of CUF life members.
cuf_annuity_members (NUMERIC): Number of CUF annuity members.
cuf_active_parishes (NUMERIC): Active parishes.
cuf_5_year_grants (NUMERIC): Grants in last 5 years.
cuf_5_year_sold_policies (NUMERIC): Sold policies last 5 years.
cuf_reps_in_county (NUMERIC): Reps in county.
cuf_reps_within_50_miles (NUMERIC): Reps within 50 miles.
cuf_life_sales_opty_policies (NUMERIC): Life insurance sales opportunity policies.
cuf_life_sales_opty_premium (NUMERIC): Life insurance sales opportunity premium.
cuf_life_sales_opty_reps (NUMERIC): Life insurance sales opportunity reps.
cuf_life_incr_opty_policies (NUMERIC): Life incremental opportunity policies.
cuf_life_incr_opty_premium (NUMERIC): Life incremental opportunity premium.
cuf_annuity_target_share (NUMERIC): Annuity target share.
cuf_annuity_sales_opty_policies (NUMERIC): Annuity sales opportunity policies.
cuf_annuity_sales_opty_premium (NUMERIC): Annuity sales opportunity premium.
cuf_annuity_sales_opty_reps (NUMERIC): Annuity sales opportunity reps.
cuf_annuity_incr_opty_policies (NUMERIC): Annuity incremental opportunity policies.
cuf_annuity_incr_opty_premium (NUMERIC): Annuity incremental opportunity premium.
cuf_l_plus_a_sales_opty_policies (NUMERIC): Life + annuity sales opportunity policies.
cuf_l_plus_a_sales_opty_premium (NUMERIC): Life + annuity sales opportunity premium.
cuf_l_plus_a_sales_opty_reps (NUMERIC): Life + annuity sales opportunity reps.
cuf_l_plus_a_incr_opty_policies (NUMERIC): Life + annuity incremental opportunity policies.
cuf_l_plus_a_incr_opty_premium (NUMERIC): Life + annuity incremental opportunity premium.
cuf_l_plus_a_incr_opty_reps (NUMERIC): Life + annuity incremental opportunity reps.
total_policy (NUMERIC): Total policies.
cuf_total_sales_premium (NUMERIC): Total CUF sales premium.
cuf_total_sold_policies (NUMERIC): Total CUF sold policies.



Table: territory_designer_rep_distance_to_counties

Columns:
state (TEXT): State of the county.
msa_county (TEXT): MSA and county name combined.
county_lat_long (TEXT): Latitude and longitude of the county.
rep_id (NUMERIC): Representative ID.
rep_zip_code (NUMERIC): Representative zip code.
rep_lat_long (NUMERIC): Representative latitude and longitude.
county_rep_distance_miles (NUMERIC): Distance from rep to county in miles.
rep_within_50_miles (TEXT): Indicator if rep is within 50 miles.
msa_order (NUMERIC): MSA sort order.
rep_name (TEXT): Representative name.

Table: territory_designer_life_mog

Columns:
year (NUMERIC): Year of data.
state (TEXT): State of data.
zipcode (NUMERIC): Zip code of the data.
income_level (NUMERIC): Income level of the population.
product (TEXT): Insurance product type.
inforce_policies (NUMERIC): Number of inforce policies.
inforce_face_amount (NUMERIC): Face amount of inforce policies.
inforce_premium (NUMERIC): Premium of inforce policies.
sales_premium (NUMERIC): Sales premium.
sales_policies (NUMERIC): Number of sales policies.
sales_face_amount (NUMERIC): Sales face amount.

Table: territory_designer_life_opty_map_data

Columns:
msa (TEXT): Metropolitan Statistical Area name.
metric (TEXT): Metric type being measured.
value (NUMERIC): Value of the metric.
variable (TEXT): Variable name.
value_win (NUMERIC): Winning value for comparison.

Table: territory_designer_master_geo_lookup

Columns:
zipcode (NUMERIC): Zip code.
state (TEXT): State.
county (TEXT): County name.
county_num (NUMERIC): County number identifier.
msa_name (TEXT): MSA name.
msa_sort (NUMERIC): Sort order for MSA.

Table: territory_designer_cuf_rep_assignment

Columns:
zip (TEXT): Zip code.
city (TEXT): City.
state (TEXT): State.
rep_id (TEXT): Representative ID.
rep_first_name (TEXT): Representative first name.
rep_last_name (TEXT): Representative last name.
rep_full_name (TEXT): Full representative name.
team_name (TEXT): Team name.
title (TEXT): Title of representative.
region (TEXT): Region code.
region_name (TEXT): Region name.
rep_address_1 (TEXT): Address line 1.
rep_address_2 (TEXT): Address line 2.
city_1 (TEXT): City (duplicate column for cleaning).
state_1 (TEXT): State (duplicate column).
zip_code (TEXT): Zip code (duplicate column).
in_new_file (TEXT): Flag for new file inclusion.
in_new_file_1 (TEXT): Duplicate flag for new file.
rep_full_name_new (TEXT): New full rep name.
rep_id_new (TEXT): New rep ID.
new_rep_name (TEXT): New rep name.
rep_order (NUMERIC): Representative order.
region_sort (NUMERIC): Region sort order.
new_rep_name_2 (TEXT): Alternate new rep name.
de_identified_team_name (TEXT): De-identified team name.
de_identified_team_name_color (TEXT): Team color code.
de_identified_region_map (TEXT): Region mapping.
de_identified_rep_name (TEXT): De-identified rep name.
de_identified_rep_name_order_2 (NUMERIC): De-identified rep order.
de_identified_territory_name (TEXT): De-identified territory name.

Table: territory_designer_cuf_sales_data

Columns:
face_amount (NUMERIC): Face amount of policy.
status (TEXT): Policy status.
status_description (TEXT): Description of policy status.
cu_user_id (TEXT): Customer or policy ID.
issue_age (NUMERIC): Age at policy issue.
segment (TEXT): Market segment.
catholic (TEXT): Catholic indicator.
gender (TEXT): Gender of insured.
city (TEXT): City of policyholder.
state (TEXT): State of policyholder.
zip_code (TEXT): Zip code of policyholder.
council (TEXT): Council name.
member_rank (TEXT): Member rank.
servicing_rep_team (TEXT): Servicing representative team.
servicing_rep_region (TEXT): Servicing rep region.
region_name (TEXT): Region name.
team_id (NUMERIC): Team ID.
team_name (TEXT): Team name.
paid_premium (NUMERIC): Paid premium amount.
servicing_rep_id (NUMERIC): Servicing representative ID.
servicing_rep_name (TEXT): Servicing representative name.
writing_rep_id (NUMERIC): Writing representative ID.
writing_rep_name (TEXT): Writing representative name.

Table: territory_designer_income_data

Columns:
year (NUMERIC): Year of income data.
state (TEXT): State of data.
inc_lev (TEXT): Income level category.
zipcode (TEXT): Zip code.
n1 (NUMERIC): Numeric income variable 1.
a00100 (NUMERIC): Numeric income variable 2.

Table: territory_designer_inforce_coverage

Columns:
zip (TEXT): Zip code.
city (TEXT): City.
state (TEXT): State.
rep_id (TEXT): Representative ID.
rep_first_name (TEXT): Representative first name.
rep_last_name (TEXT): Representative last name.
rep_full_name (TEXT): Representative full name.
team_name (TEXT): Team name.
title (TEXT): Title.
region (TEXT): Region code.
region_name (TEXT): Region name.
rep_address_1 (TEXT): Address line 1.
rep_address_2 (TEXT): Address line 2.
city_1 (TEXT): City (duplicate).
state_1 (TEXT): State (duplicate).
zip_code (TEXT): Zip code (duplicate).
in_new_file (TEXT): Flag for new file inclusion.
in_new_file_1 (TEXT): Duplicate flag.
rep_full_name_new (TEXT): New full rep name.
rep_id_new (TEXT): New rep ID.
new_rep_name (TEXT): New rep name.
check_flag (TEXT): Check indicator.
region_sort (NUMERIC): Region sort order.
include_policies (TEXT): Include policies flag.

Table: territory_designer_cuf_inforce_data_by_year

Columns:
policy_num (TEXT): Policy number.
plan_type (TEXT): Type of plan.
plan_code (TEXT): Plan code.
product (TEXT): Product type.
policies_overlap_2021_active (NUMERIC): Policies overlapping 2021 active.
policies_overlap_2022_active (NUMERIC): Policies overlapping 2022 active.
paid_premium_2021_active (NUMERIC): Paid premium for 2021 active.
paid_premium_2022_active (NUMERIC): Paid premium for 2022 active.
annuity_deposit_2021_active (NUMERIC): Annuity deposit 2021 active.
annuity_deposit_2022_active (NUMERIC): Annuity deposit 2022 active.
annualized_life_premium (NUMERIC): Annualized life premium.
face_amount (NUMERIC): Face amount of policy.
policy_status (TEXT): Policy status.
issue_date (TEXT): Policy issue date.
cu_user_id (TEXT): Customer ID.
age (NUMERIC): Age of policyholder.
catholic (TEXT): Catholic indicator.
gender (TEXT): Gender of insured.
city (TEXT): City.
state (TEXT): State.
zip_code (TEXT): Zip code.
council (TEXT): Council name.
member_rank (TEXT): Member rank.
permanent_rank (TEXT): Permanent rank.
term_rank (TEXT): Term rank.
annuity_rank (TEXT): Annuity rank.
segment_name (TEXT): Segment name.
servicing_rep_id (NUMERIC): Servicing representative ID.
servicing_rep_name (TEXT): Servicing rep name.
servicing_rep_team (TEXT): Servicing rep team.
servicing_rep_region (TEXT): Servicing rep region.
year (NUMERIC): Year.
paid_premium (NUMERIC): Paid premium amount.
paid_policies (NUMERIC): Number of paid policies.
policies_overlap_2023_active (NUMERIC): Policies overlapping 2023 active.
paid_premium_2023_active (NUMERIC): Paid premium 2023 active.
annuity_deposit_2023_active (NUMERIC): Annuity deposit 2023 active.
life_premium_paid_2023 (NUMERIC): Life premium paid in 2023.
annuity_deposits_2023 (NUMERIC): Annuity deposits in 2023.




Table: territory_designer_cuf_parish_data

Columns:
id (NUMERIC): Unique ID for the record.
id_in_old_file (TEXT): ID in the old file.
council_number (TEXT): Council number.
council_name (TEXT): Council name.
org_type (TEXT): Organization type (e.g., Parish).
name (TEXT): Name of the parish or organization.
address (TEXT): Address line 1.
address_2 (TEXT): Address line 2.
state (TEXT): State.
in_scope (TEXT): Flag indicating if the record is in scope.
city (TEXT): City.
zip_code (TEXT): Zip code.
diocese (TEXT): Diocese name.
grants_paid_2018_2022 (NUMERIC): Grants paid between 2018–2022.
old_file_label (TEXT): Label in the old file.

Table: territory_designer_cuf_inforce_data

Columns:
policy_num (TEXT): Policy number.
plan_type (TEXT): Type of insurance plan.
plan_code (TEXT): Plan code.
product (TEXT): Product type (e.g., Life, Annuity).
policies_overlap_2021_active (NUMERIC): Policies overlapping 2021 active.
policies_overlap_2022_active (NUMERIC): Policies overlapping 2022 active.
paid_premium_2021_active (NUMERIC): Paid premium for 2021 active.
paid_premium_2022_active (NUMERIC): Paid premium for 2022 active.
annuity_deposit_2021_active (NUMERIC): Annuity deposit 2021 active.
annuity_deposit_2022_active (NUMERIC): Annuity deposit 2022 active.
premium_2021 (NUMERIC): Premium amount in 2021.
premium_2022 (NUMERIC): Premium amount in 2022.
annualized_life_premium (NUMERIC): Annualized life premium.
face_amount (NUMERIC): Face amount of policy.
policy_status (TEXT): Policy status.
issue_date (TEXT): Date of policy issue.
cu_user_id (TEXT): Customer ID.
age (NUMERIC): Age of policyholder.
catholic (TEXT): Catholic indicator.
gender (TEXT): Gender of insured.
city (TEXT): City.
state (TEXT): State.
zip_code (TEXT): Zip code.
council (TEXT): Council name.
member_rank (TEXT): Member rank.
permanent_rank (TEXT): Permanent rank.
term_rank (TEXT): Term rank.
annuity_rank (TEXT): Annuity rank.
segment_name (TEXT): Segment name.
servicing_rep_id (NUMERIC): Servicing representative ID.
servicing_rep_name (TEXT): Servicing representative name.
servicing_rep_team (TEXT): Servicing representative team.
servicing_rep_region (TEXT): Servicing representative region.
policy_issue_year (NUMERIC): Year policy was issued.
policies_overlap_2023_active (NUMERIC): Policies overlapping 2023 active.
paid_premium_2023_active (NUMERIC): Paid premium for 2023 active.
annuity_deposit_2023_active (NUMERIC): Annuity deposit 2023 active.
premium_2023 (NUMERIC): Premium amount in 2023.
life_premium_paid_2023 (NUMERIC): Life premium paid in 2023.
annuity_deposits_2023 (NUMERIC): Annuity deposits in 2023.

Table: territory_designer_annuity_mog

Columns:
year (NUMERIC): Year of data.
state (TEXT): State.
zipcode (TEXT): Zip code.
inc_lev (TEXT): Income level category.
product (TEXT): Product type (e.g., Annuity).
sales_premium (NUMERIC): Sales premium amount.
inforce_premium (NUMERIC): Inforce premium amount.

Table: territory_designer_catholic_population

Columns:
year (NUMERIC): Year of data.
state (TEXT): State.
zipcode (TEXT): Zip code.
catholic_est (NUMERIC): Estimated Catholic population.

Table: territory_designer_five_year_issued_policy

Columns:
zipcode (TEXT): Zip code.
policy_count (NUMERIC): Number of policies issued over five years.

"""
