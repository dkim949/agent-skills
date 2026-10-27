---
name: explain
description: "Explains concepts, repairs explanations that did not land, and interprets conversations in context. Use for first principles, ELI5, 'you lost me', chronological conversation translation, or understanding what participants claim and why a discussion changed direction. Supports explicitly requested learning or exercises. Use tldr for source-faithful compression."
license: MIT
metadata:
  category: productivity
---

# Explain

## When to use

Answer in the user's language and at the depth their question needs. A simple question can receive a simple answer; it does not need a lesson structure.

## Workflow

### Repair the previous explanation first

When the user did not understand the previous answer, repair it before expanding the topic:

1. Find the missing premise, unclear term, or unexplained connection from the conversation. Check whether the original claim introduced an unsupported inference; verify the relevant source or code when needed and correct the claim before explaining it again.
2. Re-pitch with the missing context, the main connection, and a concrete example when helpful. Usually use one to three short paragraphs; honor a requested length. Clarity may require adding a missing premise rather than deleting words.
3. Use plain language and the project's established terms. Consult `GLOSSARY.md`, following `GLOSSARY-MAP.md` when present, only for the relevant domain. Define necessary technical words by what they do. For English, favor the direct, simple wording associated with Simplified Technical English; formal standards compliance is not required.
4. Change the angle that failed: show a concrete case, trace a sequence, or replace an unhelpful analogy. Answer directly when the unclear part is evident. Ask one focused question only when distinct interpretations would materially change the repair.

### Explain a new concept

- Lead with the answer or mechanism. Build from the simplest true starting point needed for this question, with each step connected to the next.
- Use a concrete example, analogy, diagram, or execution trace when it helps; explain where a simplification stops being accurate. Match the format to the subject.
- Ground claims about supplied material or a codebase in the actual source. Distinguish verified facts, assumptions, and illustrative examples. Read [context gathering](references/context-gathering.md) when source selection or missing context affects the explanation.
- For code, use [programming explanations](references/programming-explanation.md) when a concrete execution trace or design rationale would help.
- Adapt to the user's follow-up, then stop when the question is answered. Keep quizzes and staged understanding checks for explicit requests. Store learning notes or preferences only when the user requests storage in a specified or established destination.

### Optional learning

Read [progressive learning](references/progressive-learning.md) only when the user asks for a learning sequence, guided practice, exercises, or quizzes. A request to explain something does not activate it. Keep lessons in the conversation unless the user requests an artifact or a persistent learning workspace.

### Interpret a conversation

When the user asks what a chat, email chain, meeting discussion, or message screenshot means, read [conversation interpretation](references/conversations.md). Explain the chronological claims, evidence, and changes in direction. Translate exchanges when requested; a short outcome-only recap belongs to `tldr` when installed, or can be summarized directly.

## Output

Deliver the explanation or correction requested, with source locations when relevant. Stop when the question is answered. Use [behavior examples](references/behavior-examples.md) when checking routing boundaries or repairing an ambiguous result.
