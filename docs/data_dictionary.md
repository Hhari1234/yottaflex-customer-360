# Data Dictionary

## customers.csv
| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| customer_id | String | Source customer ID | PK in source |
| first_name | String | First name | Required |
| last_name | String | Last name | Required |
| email | String | Email address | May be null/invalid |
| phone | String | Phone number | May be null |
| address | String | Address | Optional |
| date_of_birth | Date | DOB | Optional |
| created_at | Timestamp | Creation time | Optional |

## accounts.csv
| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| account_id | String | Account ID | PK |
| customer_id | String | FK to customer | Required |
| account_type | String | Account type | checking/savings/credit/loan |
| account_status | String | Status | active/inactive/suspended |
| balance | Float | Account balance | Optional |
| opened_date | Date | Open date | Optional |

## orders.csv
| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| order_id | String | Order ID | PK |
| customer_id | String | FK to customer | Required |
| order_date | Timestamp | Order date | Required |
| order_status | String | Status | completed/pending/cancelled/refunded |
| total_amount | Float | Order total | Required |
| payment_method | String | Payment method | Optional |

## interactions.csv
| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| interaction_id | String | Interaction ID | PK |
| customer_id | String | FK to customer | Required |
| interaction_type | String | Type | call/email/chat/in_person |
| interaction_date | Timestamp | Interaction date | Required |
| agent_id | String | Agent ID | Optional |
| notes | String | Notes | Optional |

## unified_customers (output)
| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| unified_customer_id | String | Canonical customer ID | PK |
| first_name/last_name/email/phone | String | Customer details | From canonical source |
| account_count | Integer | Number of accounts | Aggregated |
| total_orders | Integer | Number of orders | Aggregated |
| total_order_amount | Float | Total spend | Aggregated |
| interaction_count | Integer | Number of interactions | Aggregated |
| last_order_date | Timestamp | Most recent order | Aggregated |
| last_interaction_date | Timestamp | Most recent interaction | Aggregated |
| source_record_ids | String | Pipe-delimited source customer_ids | Lineage |
| data_quality_status | String | Quality status | valid/warning |
| run_id | String | Pipeline run ID | Lineage |
