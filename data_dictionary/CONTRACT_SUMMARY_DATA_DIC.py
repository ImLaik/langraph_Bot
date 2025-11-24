CONTRACT_SUMMARY_DATA_DICTIONARY = """
# SPINNAKER ANALYTICS DATABASE
 
**Database:** mog_spinnaker_analytics
**Schema:** public
 
---
 
## Tables Overview
 
This database contains 1 tables for analytics on contract summary.
 
## Table: contract_summary
 
Historical data for contracts of various Carriers.
 
**Please Follow the Below Table Structure**
<column-name> (datatype) : <description> : <importance-level> : <importance-identification>  

**Columns:**
  - contract_id (VARCHAR) : Contract ID : High : Unique Count of Contract ID is no.of Unique Contracts i.e. 1 Unique Contract ID signifies 1 Contract
  - carrier (VARCHAR) : Carrier Name : Low : Should be returned in order to tie-up the details
  - ingestion_date (Date) : Contract Ingestion Date: Low : ""
  - year (INT) : Year : Low : ""
  - program_name (VARCHAR) : Program Name : Low : Should be returned in order to tie-up the details
  - bonus_type (VARCHAR): Bonus Type : Medium : Should be returned in order to tie-up the details
  - threshold_applied_to (VARCHAR): Threshold applied to : Medium : Should be returned in order to tie-up the details
  - threshold   (VARCHAR): Threshold Value / Range : High : Best Combination of EWP and Loss Ratio where EWP is not ridiculiosly high and Loss Ratio is not ridiculiosly low
  - bonus   (NUMERIC) : Bonus percentage : Very high : Higher the better
  - effective_date (Date) : Contract Effective Date : Low : Should be returned in order to tie-up the details
  - expiration_date (Date) : Contract Expiration Date : Low : Should be returned in order to tie-up the details
  - source_document (VARCHAR) : Source Document Name : Very Low : ""
  - notes (VARCHAR) : Additional Notes : Low : ""

---
 
"""
 
