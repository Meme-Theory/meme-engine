## Prior-Results Query Before New Work

Before stating a new theorem, conjecture, or proof attempt, query the project knowledge base:

```
/weave --show theorems            # proven results
/weave --show conjectures         # open stated claims
/weave --show lemmas              # reusable intermediates
/weave --show counterexamples     # refuted conjectures (don't re-state them)
/weave --show definitions         # project glossary
/weave --trace <name>             # evidence chain for a named result
```

Rule: do not re-derive a result the project has already proven. Do not re-state a conjecture the project has already refuted. Do not re-define a term the project has already formalized (unless proposing a replacement definition, in which case cite the old one explicitly).

If the knowledge base does not contain an expected result, that is information too — either the result has not been established yet, or its entity was never indexed. In the latter case, flag the gap and add the entity via `/weave --update`.
