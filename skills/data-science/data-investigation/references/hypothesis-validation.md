# Hypothesis Validation

Use for an empirical claim, metric difference, suspected mechanism, or proposed
prescription whose evidence is incomplete.

## Make explanations distinguishable

Describe the observation independently of its explanation. For each leading
hypothesis, state what should differ, in which population and period, and what
finding would weaken it. Include a measurement or selection explanation when
credible. Avoid inventing alternatives to fill a quota.

Choose a check by information gained relative to cost. Record the predicted result
under the strongest alternatives and a decision rule before examining new results.
An inconclusive result should remain inconclusive. Evidence gathered after many
exploratory cuts needs confirmation before being presented as a preplanned test.

## Protect the comparison

- Confirm numerator, denominator, units, row grain, eligibility, missingness,
  survivorship, outcome conditioning, and coverage in both groups.
- Check join expansion, duplicate keys, label or feature leakage, and collection
  changes that could create the apparent effect.
- Separate composition changes from within-group changes. For contribution
  analysis, reconcile components with the total and explain any residual.
- Compare the full eligible population where possible. A large-error subset can
  describe that subset, but cannot establish population-wide model bias.
- Check whether the proposed cause explains a difference from a relevant baseline
  exposed to the same conditions. For example, imbalance alone does not explain
  why only one of two models regresses.

## Calibrate the claim

Association supports a relationship; an accounting decomposition identifies where
a change occurred. A causal explanation additionally needs a defensible comparison
that addresses confounding, selection, and reverse causation. State identification
assumptions and the strongest remaining alternative when making causal claims.

Report magnitude, sample size, dispersion, and uncertainty where available and
relevant. Check meaningful heterogeneity rather than inferring uniformity from an
average. Statistical significance alone does not establish practical importance,
and a nonsignificant result does not establish equivalence.

For a prescription, identify the supporting result and ask what the same action
predicts for the control or baseline. Explain the expected benefit and material
tradeoffs. Keep extrapolation beyond tested settings explicit.

Stop deeper questioning when another why cannot change the decision or cannot be
tested within scope. Return the supported explanation, remaining alternative, and
smallest check that could change the conclusion.
