---
name: sql-style-guide
description: Formats SQL with leading commas and explicit aliases. Use when writing, rewriting, reviewing, or explaining SQL, including partial snippets; preserve query semantics and honor an explicitly requested alternative style.
license: MIT
metadata:
  category: data-science
---

# SQL Style Guide

Use this style for readable SQL. Formatting alone must preserve query behavior.

## Formatting

- Capitalize SQL keywords, including `SELECT`, `FROM`, `WHERE`, `JOIN`, `ON`,
  `GROUP BY`, `ORDER BY`, `QUALIFY`, `LIMIT`, and `AS`.
- Use lowercase `snake_case` for new aliases and names, with explicit `AS`.
- In vertical select, group, order, and partition lists, place each additional
  item on a separate line with a leading comma. Use four spaces before the first
  item and two spaces before subsequent commas, aligning the expressions.
- Align logical `AND` and `OR` conditions on separate lines.
- Put `WITH` on its own line and separate CTE blocks clearly.
- Keep each join beside its `ON` conditions.
- Preserve quoted identifiers, fully qualified table names, and existing aliases
  when only formatting an existing query.
- Use ordinary comma-separated arguments inside functions when they fit naturally
  on one line; leading commas apply to vertical field lists.

```sql
SELECT
    o.order_id
  , o.customer_id
  , o.created_at AS order_created_at
  , o.total_amount
FROM `project.dataset.orders` AS o
WHERE o.created_date = DATE '2026-01-15'
  AND o.order_status = 'completed'
ORDER BY
    o.created_at
  , o.order_id
LIMIT 100;
```

## Comments and final check

Preserve existing comments; put new explanatory comments on their own lines.
Retain any query header required by the applicable project workflow. Use blank
lines where they separate meaningful clauses or CTEs.

Before returning a query or snippet, check vertical lists for leading commas and
confirm that aliases, expressions, joins, filters, and dialect syntax retain their
meaning. This style guide supplies formatting, not permission to run a query or
evidence that its scan cost or logic is safe.
