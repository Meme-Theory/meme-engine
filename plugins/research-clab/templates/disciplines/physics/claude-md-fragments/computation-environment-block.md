<!-- Slot: computation-environment -->
<!-- Source: brief injection pointing at the detailed computation-environment rule -->
<!-- This fragment is inserted into the project root CLAUDE.md by the unfold process. -->

## Computation Environment

Hardware specs (CPU / GPU / RAM / OS), Python venv, torch stack, and the GPU-preference / CPU-thread-cap rules for heavy linear algebra are documented in `.claude/rules/computation-environment.md`. Every compute-mode agent should consult that rule before choosing a linear-algebra backend or running a parallel compute.
