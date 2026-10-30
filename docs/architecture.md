# Architecture

## Overview
The pipeline follows a modular ETL design with clear separation of concerns.

## Components
1. **Ingestion** (`src/ingestion/`) - Reads CSV files, validates file existence
2. **Validation** (`src/validation/`) - Schema/format validation, rejects invalid records
3. **Matching** (`src/matching/`) - Deterministic customer deduplication
4. **Transformation** (`src/transformation/`) - Unifies data across entities
5. **Storage** (`src/storage/`) - SQLite persistence
6. **Pipeline** (`src/pipeline/`) - Orchestration and monitoring
7. **Utils** (`src/utils/`) - Common utilities (logging, IDs, normalization)

## Data Flow
1. Read all four source CSVs
2. Validate required fields, formats
3. Quarantine rejected records with reasons
4. Normalize and deduplicate customers
5. Aggregate and unify across accounts/orders/interactions
6. Load to SQLite and export CSV outputs
7. Log run metrics

## Design Decisions
- **Deterministic matching**: Use normalized email/phone for reproducibility
- **Grain preservation**: Unified at customer level with aggregations
- **Idempotency**: Run IDs track executions
- **Traceability**: All outputs include run_id and source lineage
- **Separation of concerns**: Each stage in separate module
- **Local-first**: No external dependencies/services
