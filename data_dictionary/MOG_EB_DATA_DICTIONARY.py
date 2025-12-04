MOG_EB_DATA_DICTIONARY = """
# SPINNAKER ANALYTICS DATABASE
 
**Database:** mog_spinnaker_analytics
**Schema:** public

---
 
## Tables Overview
 
This database contains tables for Sales Prophet InsurIQ module for industry Employee Benefits. This database contains 5 tables for analytics on insurance market data.
 
---
 

##Table: public.eb_mog_premium_and_policies_by_zipcode
**Columns:**
zipcode (TEXT): 5-digit U.S. ZIP Code for the observation.
state (TEXT): U.S. state associated with the ZIP Code (e.g., two-letter abbreviation or state name).
product (TEXT): Insurance product or line of business (e.g., Auto, Home).
premium (NUMERIC): Aggregate premium amount for the ZIP Code, product, and year.
policies (NUMERIC): Count of policies associated with the ZIP Code, product, and year.
client_a_premium (NUMERIC): Premium amount attributable to Client A for the ZIP Code, product, and year.
client_a_policies (NUMERIC): Number of policies attributable to Client A for the ZIP Code, product, and year.
year (NUMERIC): Calendar year of the record (YYYY).
zipcode_state (TEXT): Composite key combining ZIP Code and state for joining (e.g., "02139-MA"); exact format may vary.

##Table: public.eb_mog_employees_and_establishments
**Columns:**
year (NUMERIC): Calendar year of the measurement (YYYY).
zipcode (TEXT): 5-digit U.S. ZIP Code for the observation.
number_of_establishments (NUMERIC): Number of business establishments located in the ZIP Code during the year.
num_of_employees (NUMERIC): Total number of employees across all establishments in the ZIP Code during the year.

##Table: mi_master_geo
**Columns:**
zip_code (TEXT): State-prefixed ZIP identifier from the source (e.g., "WI99999").
zipcode (TEXT): 5-digit U.S. ZIP Code without state prefix (e.g., "99999").
locale_name (TEXT): Locale or region code/name associated with the record (often a state abbreviation).
physical_delivery_address (TEXT): Physical delivery address string as recorded in USPS or source data.
physical_city (TEXT): City name associated with the physical delivery address.
physical_state (TEXT): Two-letter U.S. state abbreviation for the physical delivery address.
physical_zip (TEXT): ZIP Code associated with the physical delivery address.
physical_zip_4 (TEXT): ZIP+4 extension (the last 4 digits) for more precise mail routing.
zcta (TEXT): ZIP Code Tabulation Area (ZCTA) identifier used by the U.S. Census.
po_name (TEXT): USPS Post Office city name serving the ZIP Code.
zip_type (TEXT): ZIP Code type classification (e.g., Standard, PO Box, Unique).
zip_join_type (TEXT): Method or classification used to join ZIPs to geographic areas (e.g., direct, PO-box-adjusted).
county_fips (TEXT): 5-digit FIPS code identifying the county (SSCCC format).
primary_state (TEXT): Primary state abbreviation associated with the ZIP Code.
state_id (TEXT): State FIPS code or internal state identifier.
county_id (TEXT): County identifier (may mirror county FIPS or be an internal ID).
county_name (TEXT): Full county name (e.g., "Dane County").
county_name_short (TEXT): Shortened county name (e.g., "Dane").
county_state (TEXT): County and state abbreviation combined (e.g., "Dane, WI").
county_state_name (TEXT): County and full state name combined (e.g., "Dane County, Wisconsin").
msa_id (TEXT): Metropolitan Statistical Area (MSA/CBSA) identifier.
msa_name (TEXT): Full name of the MSA/CBSA (e.g., "Madison, WI Metro Area").
msa_name_short (TEXT): Shortened or standardized MSA/CBSA name.
msa_name_type (TEXT): Area type indicator (e.g., MSA, Micropolitan, CBSA).
latitude (NUMERIC): Latitude coordinate for the ZIP centroid or representative point.
longitude (NUMERIC): Longitude coordinate for the ZIP centroid or representative point.
zipcode_state (TEXT): Composite key combining ZIP Code and state (e.g., "99999, WI").
msa_state (TEXT): MSA/CBSA paired with state abbreviation(s), or the state(s) covered by the MSA.

##Table: il_mi_income
**Columns:**
zip_code (TEXT): State-prefixed ZIP identifier from the source (e.g., "WI99999").
zipcode (TEXT): 5-digit U.S. ZIP Code without state prefix (e.g., "99999").
locale_name (TEXT): Locale or region code/name associated with the record (often a state abbreviation).
physical_delivery_address (TEXT): Physical delivery address string as recorded in USPS or source data.
physical_city (TEXT): City name associated with the physical delivery address.
physical_state (TEXT): Two-letter U.S. state abbreviation for the physical delivery address.
physical_zip (TEXT): ZIP Code associated with the physical delivery address.
physical_zip_4 (TEXT): ZIP+4 extension (the last 4 digits) for more precise mail routing.
zcta (TEXT): ZIP Code Tabulation Area (ZCTA) identifier used by the U.S. Census.
po_name (TEXT): USPS Post Office city name serving the ZIP Code.
zip_type (TEXT): ZIP Code type classification (e.g., Standard, PO Box, Unique).
zip_join_type (TEXT): Method or classification used to join ZIPs to geographic areas (e.g., direct, PO-box-adjusted).
county_fips (TEXT): 5-digit FIPS code identifying the county (SSCCC format).
primary_state (TEXT): Primary state abbreviation associated with the ZIP Code.
state_id (TEXT): State FIPS code or internal state identifier.
county_id (TEXT): County identifier (may mirror county FIPS or be an internal ID).
county_name (TEXT): Full county name (e.g., "Dane County").
county_name_short (TEXT): Shortened county name (e.g., "Dane").
county_state (TEXT): County and state abbreviation combined (e.g., "Dane, WI").
county_state_name (TEXT): County and full state name combined (e.g., "Dane County, Wisconsin").
msa_id (TEXT): Metropolitan Statistical Area (MSA/CBSA) identifier.
msa_name (TEXT): Full name of the MSA/CBSA (e.g., "Madison, WI Metro Area").
msa_name_short (TEXT): Shortened or standardized MSA/CBSA name.
msa_name_type (TEXT): Area type indicator (e.g., MSA, Micropolitan, CBSA).
latitude (NUMERIC): Latitude coordinate for the ZIP centroid or representative point.
longitude (NUMERIC): Longitude coordinate for the ZIP centroid or representative point.
zipcode_state (TEXT): Composite key combining ZIP Code and state (e.g., "99999, WI").
msa_state (TEXT): MSA/CBSA paired with state abbreviation(s), or the state(s) covered by the MSA.

##Table: il_mi_population
**Columns:**
zipcode (TEXT): 5-digit U.S. ZIP Code for the observation.
county (TEXT): County name associated with the ZIP Code.
state (TEXT): Two-letter U.S. state abbreviation.
total_population_2021 (NUMERIC): Total resident population in 2021 for the ZIP Code.
hispanic_population_2021 (NUMERIC): Number of residents identifying as Hispanic or Latino in 2021 for the ZIP Code.
catholic_population_2020 (NUMERIC): Estimated number of Catholic residents in 2020 for the ZIP Code.
zipcode_state (TEXT): Composite key combining ZIP Code and state (e.g., "00501, NY").

"""
