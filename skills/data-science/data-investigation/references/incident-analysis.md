# Incident Analysis

Use for a retrospective of a service, data, pipeline, or model incident. Establish
whether the user wants evidence analysis, a recovery plan, or an authorized recovery
operation. A retrospective request does not authorize operational changes.

## Reconstruct impact and sequence

1. Define expected behavior and observed impact: affected users, records, regions,
   runs, or model slices; onset, peak, duration, and recovery status. Distinguish
   verified bounds from gaps in detection or available evidence.
2. Build a concise timeline from logs, metrics, releases, configuration changes,
   and recorded decisions. Preserve source references and explicit time zones.
   Separate event time from detection, ingestion, and reporting time when relevant.
3. Check evidence coverage. Missing logs are not proof that an event did not occur;
   recovery of a headline metric does not establish that delayed or corrupted data
   has been repaired.

## Explain the mechanism

Distinguish the triggering event, enabling conditions, propagation, detection gaps,
and recovery factors. Several conditions may combine; do not force a single cause
or infer fault from a person's proximity to the event.

Test the strongest competing explanation against chronology, affected versus
unaffected populations, prior runs, and configuration or release differences.
Temporal coincidence and improvement after a rollback are supporting observations,
not automatically proof of the entire proposed mechanism. State what additional
check would distinguish alternatives.

If an active incident remains unresolved, report current impact and the smallest
reversible recovery candidate alongside its verification and rollback conditions.
Respect the host's exact authorization requirements before executing it.

## Make follow-up reviewable

For each proposed corrective action, name the failure mechanism it addresses and
how completion and effectiveness would be verified. Distinguish recovery, repair
of affected data, detection improvements, and prevention. Suggest an owner or due
date only when supported; otherwise leave assignment to the responsible people.

Report impact, timeline, supported contributing factors, remaining alternatives,
recovery evidence, and prioritized follow-up. Label unverified causes and unrun
checks. Do not restart services, roll back releases, backfill data, add production
instrumentation, or send incident communications without the necessary authority.
