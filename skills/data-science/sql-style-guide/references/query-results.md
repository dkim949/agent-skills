# Exploratory queries and result inspection

Use for drafting a new exploratory query or explaining returned rows. Formatting an existing query does not authorize changing its semantics, filters, row limit, or scope.

## Draft a query

1. State the question and the input/output row grain. For a substantive exploratory query, use a short `Purpose / Before / After` comment header when it improves understanding.
2. Verify table and field names from actual schema or supplied evidence. Preserve the user's base query and requested scope. Start with the smallest raw query; add joins, buckets, metrics or deduplication only when needed and explain their effect.
3. Apply appropriate partition and context filters before joins or array expansion. Use a modest display limit (normally 100 rows) for previews; a row limit restricts displayed results and does not necessarily reduce BigQuery bytes scanned. Do not apply a preview limit when complete output is explicitly needed.
4. Explain any meaningful grain change from joins, `UNNEST`, grouping, window selection or offsets. Keep STRUCT access and ARRAY expansion consistent with the verified schema. Retain material eligibility conditions when simplifying.
5. Use the project's read-only/dry-run checks where authorized. Query creation is not permission for data mutation or execution against protected resources.

## Explain the result

State what one row represents. Select a small representative sample, usually five to ten rows, covering relevant outcomes and boundary cases rather than merely the first rows. Preserve original field names, values and necessary join keys, subject to applicable privacy constraints. For wide results, split the sample or explicitly identify omitted columns.

Explain the raw sample after showing it. Distinguish observed facts, hypotheses, and what the sample cannot establish; a selected sample does not prove population frequency or a causal effect. State the next smallest query/check only when useful. Use fewer rows or a shorter answer when the request is narrower.

This generalizes the former local query-result explanation procedure. Company-specific schema, identifiers, filters and interpretation rules remain outside this public skill.
