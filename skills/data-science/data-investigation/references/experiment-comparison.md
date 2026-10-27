# Experiment Comparison

Use when comparing experiments or evaluating whether a data or model intervention
supports its stated hypothesis. Planning or analyzing a run does not launch it.

## Establish comparability

Record the hypothesis, baseline, configuration differences, dataset and split,
evaluation window, metric definitions, preprocessing, environment, and available
run or artifact identifiers. Reuse existing records rather than requiring a new
tracking system. Mark missing information and its effect on the comparison.

Align objectives, eligibility, evaluation data, calibration, and operating points
before attributing a difference to model class or architecture. When alignment is
impossible, report the combined change and limit attribution accordingly.

Isolate the intended intervention when feasible. Multiple simultaneous changes
require an ablation or another defensible design before assigning their individual
effects. Choose repeats, seeds, or uncertainty estimates appropriate to observed
variability and decision cost; no fixed run count applies.

## Interpret results

- Report baseline and candidate values, absolute or relative changes with clear
  units, sample sizes, and relevant uncertainty. Retain negative and inconclusive
  results alongside favorable ones.
- Examine material subgroup and tail tradeoffs; an overall gain can hide a slice
  regression. Separate a uniform prediction shift from improved residual structure
  when calibration can explain the metric change.
- Check leakage, test-set reuse, multiple comparisons, incomplete training, and
  small-sample selection before generalizing. A smoke test demonstrates execution
  only to the extent it exercised the pipeline; performance conclusions need an
  evaluation suited to the intended claim.
- Distinguish a promising candidate, a supported mechanism, and readiness for
  deployment. State the next evidence needed for the actual decision.

Keep the hypothesis, exact configuration and data identities, executed results,
conclusion, and artifact locations inspectable. Propose the smallest next experiment
that could change the decision, including expected outcomes under the leading
alternatives. Execution follows the user's authorized resource and cost scope.
