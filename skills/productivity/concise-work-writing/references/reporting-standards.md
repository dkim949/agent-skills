# Reporting Standards

Read only the sections selected by `SKILL.md`. These are compact operating rules, not substitutes for current official guidance.

## Consulting mode

Optimize for a time-constrained reader making a decision.

- Lead with the governing answer or recommendation and the reason it matters.
- Use a small number of distinct supporting arguments. At each level, they should answer the same parent question at a comparable level of abstraction, without material overlap or omission.
- Use context, tension, and the reader's question only when they make the governing answer easier to understand.
- Prefer insight headings such as `Late-stage delays account for most of the variance` over topic labels such as `Delay analysis`.
- Make the comparison explicit: current versus prior period, target, plan, peer, counterfactual, or scenario.
- Explain why each major finding changes the decision, then state the implication, risk, opportunity, or monitoring point.
- For a recommendation, name the strongest credible alternative and the decisive trade-off or assumption.
- Put the ask, owner, timing, and decision threshold in the close when the evidence supports action.

Do not confuse consulting quality with brand mimicry. Neutral typography, disciplined spacing, consistent notation, and traceable evidence matter more than copying a firm's colors or page furniture.

The answer-first and context-question patterns are informed by Barbara Minto's published overview of the Pyramid Principle and SCQ framework. Use the concepts in original language; do not reproduce proprietary course or book content.

Primary source: [Barbara Minto](https://barbaraminto.com/)

## Academic mode

Optimize for validity, transparency, and reproducibility. Identify the venue, track or article/output type, and study design; use their current instructions first. Reporting standards supplement rather than override them.

- State the research question, contribution, and main result without overstating novelty or certainty.
- Use the structure expected by the field and study design. IMRaD is common, not universal.
- Report enough detail to evaluate the population or data, sampling, exclusions, measures, procedures, analysis, and uncertainty.
- Distinguish planned, primary, secondary, exploratory, and post-hoc analyses when relevant.
- Report null or negative results and robustness checks when they change interpretation.
- Explain missing data, deviations from protocol, conflicts, funding, ethics, and data or code availability when applicable.
- For computational studies, report versioned data, code, and model artifacts; preprocessing and splits; environment; randomness and repeats; selection protocol; and the resources needed to reproduce material results, as applicable.
- For quantitative results, report estimates or effect sizes with uncertainty on the correct unit of analysis; disclose repeated-run, multiplicity, or model-selection effects when they can change the conclusion.
- Keep limitations concrete: name the affected claim, plausible failure mechanism, and direction of uncertainty.

Route to the current official checklist when the study type has one:

- Psychology or APA-aligned social and behavioral science: [APA Journal Article Reporting Standards](https://www.apa.org/pubs/journals/resources/apa-style-jars.html)
- Health research guideline directory: [EQUATOR Network](https://www.equator-network.org/library/)
- Randomized trials: [CONSORT](https://www.equator-network.org/reporting-guidelines/consort/)
- Systematic reviews and meta-analyses: [PRISMA](https://www.prisma-statement.org/prisma-2020), its applicable extension, or a field-specific guideline
- Observational epidemiologic studies: [STROBE](https://www.equator-network.org/reporting-guidelines/strobe/)

For ML, engineering, economics, or another field not covered above, check the current venue and discipline-specific primary guidance rather than borrowing a biomedical checklist by analogy.

Use checklists to test reporting completeness, not to certify study design, evidence quality, or causal validity. If current venue guidance cannot be accessed, mark compliance as unverified and request the relevant instructions rather than claiming conformity.

## Visual communication

Design each visual around one analytical question.

- Choose chart families by relationship: comparison, trend, composition, change, distribution, or association.
- Use a common scale and aligned layout for comparisons; avoid 3D effects and decorative marks that distort reading.
- Use direct labels when they reduce lookup effort. Show units, time range, denominator, and relevant sample size.
- Use color sparingly and consistently. Do not rely on color alone to encode meaning.
- Distinguish actual, target, plan, forecast, and scenario consistently throughout one artifact.
- Annotate the evidence needed to understand the takeaway; keep interpretation in adjacent prose.
- Provide alt text, a textual takeaway, or an accessible data table for material visuals.
- Use spacious demonstration tables for a small argument and separate dense reference tables for audit or reuse.

Useful primary guidance:

- [International Business Communication Standards](https://www.ibcs.com/IBCS/) for consistent business-report notation and conceptual design
- [Royal Statistical Society: Best Practices for Data Visualisation](https://royal-statistical-society.github.io/datavisguide/) for chart choice, design, and accessibility
- [UK Government Analysis Function](https://analysisfunction.civilservice.gov.uk/support/communicating-analysis/) for accessible communication of statistics and analysis

## Reuse and attribution

- IBCS standards are published under CC BY-SA 4.0. Follow attribution and share-alike requirements before copying or adapting their protected expression.
- The Royal Statistical Society guide states that its editorial content is CC BY 4.0; attribute adapted material.
- Minto's books and course materials are copyrighted. Use the high-level concepts described on the official site and write original operating rules.
- Recheck licenses and current versions at the primary source before distributing a substantial adaptation.
