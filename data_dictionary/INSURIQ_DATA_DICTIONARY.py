INSURIQ_DATA_DICTIONARY = """
# SPINNAKER ANALYTICS DATABASE
 
**Database:** mog_spinnaker_analytics
**Schema:** public

---
 
## Tables Overview
 
This database contains tables for Sales Prophet InsurIQ module for industry Property & Casualty. This database contains 2 tables for analytics on insurance market data.
 
---
 

##Table: insuriq_company_data

**Columns:**

state (TEXT): U.S. state or territory for the insurance data.
line_of_business (TEXT): Insurance line of business (e.g., Property, Casualty).
direct_premiums_earned (NUMERIC): Total direct premiums earned by the company.
loss_incurred_usd (NUMERIC): Losses incurred by the company in USD.
loss_adjust_expense_usd (NUMERIC): Loss adjustment expenses in USD.
general_expense_usd (NUMERIC): General administrative expenses in USD.
selling_expense_usd (NUMERIC): Selling and marketing expenses in USD.
other_expenses_usd (NUMERIC): Any other expenses not included in above categories, in USD.

##Table: insuriq_market_data

**Columns:**

state (TEXT): U.S. state or territory for the market-wide insurance data.
line_of_business (TEXT): Insurance line of business (e.g., Property, Casualty).
direct_premiums_earned (NUMERIC): Total direct premiums earned in the market.
loss_incurred_usd (NUMERIC): Losses incurred in the market in USD.
loss_adjust_expense_usd (NUMERIC): Loss adjustment expenses in USD.
general_expense_usd (NUMERIC): General administrative expenses in USD.
selling_expense_usd (NUMERIC): Selling and marketing expenses in USD.
other_expenses_usd (NUMERIC): Other expenses not included above, in USD.

"""
