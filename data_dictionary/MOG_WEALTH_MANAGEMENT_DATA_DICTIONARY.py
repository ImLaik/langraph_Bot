MOG_WEALTH_MANAGEMENT_DATA_DICTIONARY = """
# SPINNAKER ANALYTICS DATABASE
 
**Database:** mog_spinnaker_analytics
**Schema:** public

---
 
## Tables Overview
 
This database contains tables for Sales Prophet MOG module for industry Worksite. This database contains 9 tables for analytics on insurance market data, agent performance, geographic information, and sales opportunities.
 
---
 
## Table: mi_master_geo
 
Geographic reference table containing zipcode and location information.
 
**Columns:**
- zipcode (VARCHAR): Zipcode as text
- zip_code (INT): Zipcode as integer
- locale_name (VARCHAR): Locality name
- physical_delivery_address (VARCHAR): Physical delivery address
- physical_city (VARCHAR): City name
- physical_state (VARCHAR): State abbreviation
- physical_zip (NUMERIC): Physical zipcode
- physical_zip_4 (NUMERIC): Zipcode +4 extension
- zcta (NUMERIC): ZIP Code Tabulation Area
- po_name (VARCHAR): Post office name
- zip_type (VARCHAR): Type of zipcode
- zip_join_type (VARCHAR): Join type classification
- county_fips (NUMERIC): County FIPS code
- primary_state (VARCHAR): Primary state
- state_id (NUMERIC): State identifier
- county_id (NUMERIC): County identifier
- county_name (VARCHAR): Full county name
- county_name_short (VARCHAR): Short county name
- county_state (VARCHAR): County and state combined
- county_state_name (VARCHAR): County and state full name
- msa_id (VARCHAR): Metropolitan Statistical Area ID
- msa_name (VARCHAR): MSA full name
- msa_name_short (VARCHAR): MSA short name
- msa_name_type (VARCHAR): MSA type classification
- latitude (NUMERIC): Latitude coordinate
- longitude (NUMERIC): Longitude coordinate
- population_2021 (NUMERIC): Population as of 2021
- household (NUMERIC): Number of households
- household_income (NUMERIC): Median household income
- market_agents (NUMERIC): Number of market agents
- zipcode_state (VARCHAR) **[PRIMARY KEY]**: Combined zipcode and state key
 
---

## Table: il_mi_population
 
Population demographics by zipcode.
 
**Columns:**
- zipcode (INT): Zipcode
- total_population (INT): Total population
- hispanic_population (INT): Hispanic population count
- county (VARCHAR): County name
- state (VARCHAR): State abbreviation
- county_state (VARCHAR): County and state combined
- zipcode_state (VARCHAR) **[FOREIGN KEY → mi_master_geo.zipcode_state]**: Combined zipcode and state key 
 
 ---
 
  
## Table: il_mi_income
 
Income statistics by zipcode.
 
**Columns:**
- year (INT): Year of data
- state (VARCHAR): State abbreviation
- zipcode (VARCHAR): Zipcode
- total_income (NUMERIC): Total income amount
- total_household (NUMERIC): Total households
- zipcode_state (VARCHAR) **[FOREIGN KEY → mi_master_geo.zipcode_state]**: Combined zipcode and state key
 

## Key Relationships
 
- **income_data.zipcode_state** → mi_master_geo.zipcode_state
- **population.zipcode_state** → mi_master_geo.zipcode_state
 
Use the `zipcode_state` column to JOIN MOG Wealth Management Product related tables together.
 
---
 
## Important Notes
 
1. **Geographic Scope**: Primarily US data with state and zipcode granularity
2. **Join Key**: Always use `zipcode_state` for joining geographic tables
"""
