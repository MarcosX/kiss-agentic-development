# Slicing Guide

Break a spec into independently-implementable slices using tracer bullet (vertical slice) principles.

## Tracer bullet principle

Each slice cuts through ALL integration layers end-to-end — NOT a horizontal slice of one layer.

```
Good (vertical):  schema → API → logic → tests → UI
Bad (horizontal): all schema work → all API work → all logic work → ...
```

A completed slice is demoable or verifiable on its own. Prefer many thin slices over few thick ones.

## HITL vs AFK

Each slice is one of two types:

- **HITL** (Human-In-The-Loop): requires human interaction — architectural decision, design review, product question. The agent pauses and waits for input.
- **AFK** (Away-From-Keyboard): can be implemented and merged without human interaction. Prefer AFK over HITL where possible.

## Dependency ordering

Identify which slices must complete before others can start. Publish blockers first so you can reference real identifiers.

## Anti-stale principle

Issue descriptions should not contain specific file paths or code snippets — they go stale. Exception: prototype-produced decision-rich snippets (state machine, reducer, schema, type shape) that encode decisions more precisely than prose. Inline them and note they came from a prototype.

## Proof step per slice

Each slice ends with a Proof step so it's verifiable as runnable, not just testable. State the **expected outcome** explicitly — that's what makes evaluation objective. Declare **real vs. stubbed** dependencies; a blocked/external dependency means capture behavior up to that boundary and log the stub so the human knows the coverage limit.

**Proof must be runtime observation.** The evidence must come from a running system — logs, HTTP responses, DB query results, screenshots, process output. Test output, git diff, type-check, and lint are NEVER proof of runtime behavior; they prove code exists and compiles, not that the application behaves correctly.

## Slice template

```
### Slice N: [Title]

**Type**: HITL | AFK
**Blocked by**: [other slice IDs, or "None"]
**User stories covered**: [which requirements this addresses]

**What to build**:
End-to-end behavior description, not layer-by-layer implementation.

**Acceptance criteria**:
- [ ] Criterion 1
- [ ] Criterion 2

**Proof**:
- Proof type: [log | http-response | db-state | screenshot | process-output | file-system | queue-state]
- Command(s) to run the slice in isolation (with stubs for dependencies it doesn't own)
- Expected outcome: what the evidence must show in concrete, observable terms
- Real vs. stubbed dependencies
```
