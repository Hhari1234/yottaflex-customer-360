# Design Decisions and Trade-offs

## Key Decisions

### 1. Matching Strategy
- **Choice**: Email-first, then phone-based matching with normalization
- **Rationale**: Email is most stable unique identifier; deterministic and explainable
- **Trade-off**: May miss duplicates without matching identifiers; better than name-based fuzzy matching

### 2. Technology Stack
- **Choice**: Pandas + SQLite
- **Rationale**: Simple, local, sufficient for 100k+ records, easy to test
- **Trade-off**: Not distributed, but meets requirements

### 3. Data Storage
- **Choice**: Both CSV outputs and SQLite
- **Rationale**: CSV for portability, SQLite for querying/reconciliation
- **Trade-off**: Some duplication but provides flexibility

### 4. Error Handling
- **Choice**: Quarantine invalid records rather than fail entire batch
- **Rationale**: Partial success is acceptable per requirements
- **Trade-off**: Need careful tracking of rejected records

### 5. Idempotency
- **Choice**: Track runs with run_id, append with lineage
- **Rationale**: Supports reruns and auditing
- **Trade-off**: Simple approach; production would need deduplication keys

## Limitations
- Fuzzy name matching not implemented (intentional per rules)
- Phone normalization assumes digits
- Large datasets (100k+) may be memory-intensive with pandas (acceptable for this scope)
- Simple conflict resolution

## Future Improvements
- Add data quality scoring
- Implement incremental loading
- Add more sophisticated matching with confidence scores
- Parallel processing for large files
