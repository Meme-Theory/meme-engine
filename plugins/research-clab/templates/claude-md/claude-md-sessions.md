# sessions/ — Session Outputs

<!-- DEPLOY: project-root/sessions/CLAUDE.md -->

All session outputs live here, organized chronologically. Each session is a discrete research event — a team meeting, a computation sprint, a debate, a review.

## Structure

```
sessions/
├── session-01/                 # First session
│   ├── session-01-meeting.md   # Meeting minutes / main output
│   └── session-01-handoff.md   # Handoff document for next session
├── session-02/
├── ...
├── session-plan/               # Planning documents: prompts, agendas, handoffs
├── framework/                  # Cross-session mechanism discussions
└── misc/                       # One-off or grouping files
```

## Session Naming

- **Directories**: `session-NN/` — zero-padded session number
- **Files**: `session-NNx-descriptor.md` — where `x` is optional sub-session letter
- **Examples**: `session-01-first-contact.md`, `session-14b-spectral-action.md`

## Session Formats

Choose the right format for each session. See `sessions/session-plan/format-selection-guide.md` for the full decision tree.

| Format | Use When |
|:-------|:---------|
| **A — First Contact Review** | Opening investigation of new material |
| **B — Adversarial Debate** | Stress-testing claims between opposing agents |
| **C — Collaborative Deep-Dive** | Focused investigation with 2-4 agents |
| **D — Workshop** | Multi-round deliberation with structured handoffs |
| **E — Investigation Arc** | Multi-phase gated investigation |
| **F — Decisive Computation** | Single-objective computation sprint |
| **G — Mass Parallel Assessment** | 8-17 agents reviewing in parallel |
| **H — Decision Gate** | Binary yes/no routing decision |
| **I — Formalization** | Status consolidation and documentation |

## What Belongs Here

- Meeting minutes and session transcripts
- Synthesis documents produced during sessions
- Gate verdict records
- Handoff documents
- Session-specific analysis outputs

## What Does NOT Belong Here

- Agent definitions → `.claude/agents/`
- Reference papers → `researchers/`
- Computation scripts → `{{COMPUTATION_DIR}}/`
- Knowledge index → `tools/`
- Source PDFs → `artifacts/`

## Rules

- **One directory per session** — don't mix session outputs across directories
- **Handoff documents are mandatory** — every session produces one (see root CLAUDE.md for format)
- **One writer per file** — if multiple agents contribute, designate a single writer who incorporates input
- **Session files feed the knowledge index** — after editing session files, run `/weave --update`
- **Chronological order is sacred** — never renumber sessions
