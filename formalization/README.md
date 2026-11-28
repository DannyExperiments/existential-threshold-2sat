# Lean verification

For any satisfiable implication graph with involutive literal negation and contraposed edges, if its imposed units have no joint model then one or two source units already have no joint model. The proof constructs an extending model when propagation is consistent. Runtime and model counting remain in the paper.

The checked declaration is `BinaryUnitConflict.two_sources`. [Source](Conflict.lean) · [Pinned CI](../.github/workflows/lean.yml)

```sh
lean -DwarningAsError=true formalization/Conflict.lean
```

CI compares the compiler output with the committed axiom report.
