# Programming explanations

Use actual relevant code before describing codebase behavior. Show a small excerpt when it makes the mechanism easier to follow; avoid dumping a whole file.

Trace one concrete input through the important steps: initial state, branches, changes, and result. Explain a pattern's name when it helps the reader connect examples, rather than requiring pattern vocabulary upfront.

Separate what the code does, why that design may be useful, and when its assumptions fail. Treat intent inferred from code as an inference unless comments, tests, or design documents establish it.

If the user's mental model predicts a different result, identify the specific difference and trace that case. For an abstract explanation that failed, start with the example; for an example that hid the general rule, state the rule and its limits.
