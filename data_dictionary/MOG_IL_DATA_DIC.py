 
MOG_DATA_DICTIONARY = f"""
# SPINNAKER ANALYTICS DATABASE
 
**Database:** mog_spinnaker_analytics
**Schema:** public

---
 
## Tables Overview
 
This database contains 9 tables for analytics on insurance market data, agent performance, geographic information, and sales opportunities.
 
---
 
## Table: il_mi_master_geo
 
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
 
## Table: il_mi_market
 
Historical insurance data by year, state, zipcode, and product , for entire market(USA)
 
**Columns:**
- year (INT): Year of data
- state (VARCHAR): State abbreviation
- zipcode (INT): Zipcode
- product (VARCHAR): Insurance product type
- premium (NUMERIC): Premium amount (Market)
- policies (NUMERIC): Number of policies (Market)
- face_amount (NUMERIC): Face amount of policies (Market)
- metric (VARCHAR): Metric type
- zipcode_state (VARCHAR) **[FOREIGN KEY → master_geo.zipcode_state]**: Combined zipcode and state key
 
---
## Table: il_mi_client_dummy
 
Historical data for client by year, state, zipcode, and product.
 
**Columns:**
- year (INT): Year of data
- state (VARCHAR): State abbreviation
- zipcode (INT): Zipcode
- product (VARCHAR): Insurance product type
- premium (NUMERIC): Premium amount
- policies (NUMERIC): Number of policies
- face_amount (NUMERIC): Face amount of policies
- metric (VARCHAR): Metric type
- zipcode_state (VARCHAR) **[FOREIGN KEY → master_geo.zipcode_state]**: Combined zipcode and state key
 
---
 
 
 
## Table: il_mi_sales_opty
 
Sales opportunity analysis by territory and market.
 
**Columns:**
- year (INT): Year of data
- state (VARCHAR): State abbreviation
- territory (INT): Territory code
- msa (VARCHAR): Metropolitan Statistical Area
- product (VARCHAR): Insurance product type
- market_size (NUMERIC): Total market size
- historical_sales (INT): Historical sales count
- market_share (NUMERIC): Current market share percentage
- sales_premium_opportunity (NUMERIC): Total sales opportunity
- incremental_sales_premium_opportunity (NUMERIC): Additional opportunity
- agent_recruiting_opty (NUMERIC): Agent recruiting opportunity
 
---
 
## Table: il_mi_agent_performance
 
Agent performance metrics by territory and MSA.
 
**Columns:**
- state (VARCHAR): State abbreviation
- year (NUMERIC): Year of data
- territory (NUMERIC): Territory code
- msa (VARCHAR): Metropolitan Statistical Area
- life_appointed_agents (NUMERIC): Number of appointed life agents
- life_agents (NUMERIC): Total life agents
- company_agents (NUMERIC): Company agents count
- active_company_agents (NUMERIC): Active company agents
- active_agent_apps (NUMERIC): Applications by active agents
- active_agents_premium (NUMERIC): Premium from active agents
- incremental_sales_opty (NUMERIC): Incremental sales opportunity
- active_ratio (NUMERIC): Ratio of active agents
- premium_per_agent (VARCHAR): Premium per agent
- productivity_target (NUMERIC): Productivity target
- market_premium (NUMERIC): Total market premium
- premium_share (NUMERIC): Premium share percentage
- premium_share_norm (NUMERIC): Normalized premium share
- agent_share (NUMERIC): Agent share percentage
- agent_share_norm (NUMERIC): Normalized agent share
- sales_effectivess_per_agent (NUMERIC): Sales effectiveness metric
- sales_effectivess_per_agent_norm (NUMERIC): Normalized effectiveness
- marketing_spend (NUMERIC): Marketing spend amount
- marketing_spend_norm (NUMERIC): Normalized marketing spend
- premium_earned_per_usd_of_spend (NUMERIC): ROI metric
- premium_earned_per_usd_of_spend_norm (NUMERIC): Normalized ROI
- members (NUMERIC): Number of members
- members_norm (NUMERIC): Normalized members count
- population (NUMERIC): Population count
- population_norm (NUMERIC): Normalized population
- members_share (NUMERIC): Members share percentage
- members_share_norm (NUMERIC): Normalized members share
- members_score (NUMERIC): Members score
- members_score_norm (NUMERIC): Normalized members score
- number_of_policies (NUMERIC): Total policies
- number_of_policies_norm (NUMERIC): Normalized policies count
- number_of_policies_per_member (NUMERIC): Policies per member ratio
- number_of_policies_per_member_norm (NUMERIC): Normalized ratio
- apps_per_agent (NUMERIC): Applications per agent
 
---
 
## Table: il_mi_life_agents_by_zipcode
 
Life insurance agents distribution by zipcode.
 
**Columns:**
- year (INT): Year of data
- state (TEXT): State abbreviation
- zipcode (INT): Zipcode
- agent_count (INT): Total number of agents
- client_agents (INT): Total number of client agents
- zipcode_int (INT): Zipcode as integer
- zipcode_state (VARCHAR) **[FOREIGN KEY → master_geo.zipcode_state]**: Combined zipcode and state key
 
---
 
## Table: il_mi_income
 
Income statistics by zipcode.
 
**Columns:**
- year (INT): Year of data
- state (VARCHAR): State abbreviation
- zipcode (VARCHAR): Zipcode
- total_income (NUMERIC): Total income amount
- total_household (NUMERIC): Total households
- zipcode_state (VARCHAR) **[FOREIGN KEY → master_geo.zipcode_state]**: Combined zipcode and state key
 
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
- zipcode_state (VARCHAR) **[FOREIGN KEY → master_geo.zipcode_state]**: Combined zipcode and state key
 
---
 
## Table: il_mi_map_data
 
Geographic visualization data for mapping applications.
 
**Columns:**
- year (VARCHAR): Year of data
- state (VARCHAR): State abbreviation
- product (VARCHAR): Insurance product type
- msa (VARCHAR): Metropolitan Statistical Area
- metric (VARCHAR): Metric type
- value (INT): Metric value
- legend (VARCHAR): Legend classification
- color (INT): Color code
- year_state_product_msa (VARCHAR): Composite key
- color_adj (INT): Adjusted color code
- product_msa (VARCHAR): Product and MSA combination
 
---
 
## Key Relationships
 
- **all_mog_data.zipcode_state** → master_geo.zipcode_state
- **life_agents_by_zipcode.zipcode_state** → master_geo.zipcode_state
- **income_data.zipcode_state** → master_geo.zipcode_state
- **population.zipcode_state** → master_geo.zipcode_state
 
Use the `zipcode_state` column to JOIN MOG Product related tables together.
 
---
 
## Important Notes
 
1. **Date Range**: Data typically ranges from 2020-2023
2. **Geographic Scope**: Primarily US data with state and zipcode granularity
3. **Product Types**: Life insurance products (exact types in the product column)
4. **Metric Types**: Various business metrics (premium, policies, face_amount, etc.)
5. **NULL Handling**: Some columns may contain NULL values - handle appropriately
6. **Join Key**: Always use `zipcode_state` for joining geographic tables
"""
 
 