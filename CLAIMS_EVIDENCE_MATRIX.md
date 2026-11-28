# Claims and evidence

| Claim | Evidence | Scope |
| --- | --- | --- |
| Fixed-parameter linear decision and witness algorithm | [Manuscript](paper/manuscript.pdf), Theorem 1 | Uniform probabilistic block, exact integer threshold, charged rational conversion |
| Separation from the published existential bound | [Literature check](audits/public_safe_reports/LITERATURE_AUDIT.md) | Earlier general methods give ordinary FPT with polynomial formula factor |
| Conditional lower bound | [Manuscript](paper/manuscript.tex), Section 5 | Vertex Cover reduction, under ETH |
| Exact finite checks | [Replay output](verification/logs/replay.txt) | Finite tests and witness checks against direct enumeration |
| Teaching example | [Explorer guide](visualization/README.md) | Exact instance with eight uniform assignments |

## Lean verification

For any satisfiable implication graph with involutive literal negation and contraposed edges, if its imposed units have no joint model then one or two source units already have no joint model. The proof constructs an extending model when propagation is consistent. Runtime and model counting remain in the paper. [Source and replay](formalization/README.md)
