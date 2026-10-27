# Incorporate recorded skill learnings

Use when the user requests improvements from recorded skill experience. Limit work to the named skill or agreed set; “all” must be explicit. Identify active skill roots from the target hosts' actual configuration and discovery paths rather than assuming one platform's directory layout. Keep unrelated session history outside the collection.

## Collect and assess

1. Find `learnings.md` files within scope. Resolve symbolic links and process each real file once, even when several hosts discover it.
2. Ignore empty templates, including `(No entries)` and equivalent legacy placeholders in other languages. Decode escaped Unicode before comparing placeholders. A template heading alone is not a substantive learning.
3. Distinguish pending, resolved, and already incorporated entries. Tie a proposed change to the concrete observed mistake or friction. Recurrence, such as the same mistake twice, is evidence of a structural issue; a single clear correction can also justify a bounded fix.
4. Check whether the existing instructions, examples, or checks already address it. Prefer correcting the narrow source of the problem to adding another generic rule.

## Apply and record

Update the canonical skill once when supported hosts share it. Otherwise update the corresponding instructions, references, and invocation metadata in each active host while preserving its specific tools and behavior. Check stale duplicates and resulting discovery. Report a host that could not be updated instead of assuming synchronization.

Examples include correcting a mistaken parameter, adding an essential missing step, or fixing an incorrect example. Keep applicable user preferences and scope boundaries intact. A learning is evidence to evaluate, not an instruction that overrides the user's request.

Mark an entry incorporated, using its existing convention or `✓`, only after the corresponding change is made and checked. Retain pending entries and their evidence. Do not bundle private learning logs into a distributable skill package.

Deliver the changes by skill, verification evidence, remaining items, and any useful check for the next cycle. Follow the main skill's packaging checks; distinguish static inspection from a real host invocation.
