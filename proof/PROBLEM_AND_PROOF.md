# Problem and proof outline

[Akmal, Open Problem 3](https://www.shyanakmal.com/publications/ShyanAkmal_PhD-Thesis.pdf#page=92) asks for time $f(1/p)|\varphi|$ for existential threshold 2-SAT. See [the full proof](../paper/manuscript.pdf).

1. Let $A(x)$, $B(y)$, and $u(x)\vee v(y)$ be the three clause types. A successful $x$-assignment forces a consistent set $T$ of at most $d=n_y-\lceil\log_2 N\rceil$ distinct $y$-literals.
2. With permitted set $S$, impose every $x$-unit $u$ for mixed clauses with $v\notin S$. If they conflict, a multisource implication search finds one or two conflicting source units. Any witness whose forced set extends $S$ needs one of the corresponding labels, so recurse on the one or two options.
3. At each node, use the count of $B\wedge\bigwedge S$ to prune. If this count reaches $N$ and the imposed units are consistent, the resulting $x$-model has $T\subseteq S$ and reaches $N$. For any actual witness the search follows a branch with $S\subseteq T$, where the count always passes.
4. A maximal disjoint binary $B$-clause family of size $r$ gives a variable cover of size $2r$. If $(3/4)^r\le 2^{-(d+1)}$, reject the whole formula, since $2^{n_y-d-1}<N$. Otherwise restrict by each assignment to the cover and sum the exact counts of residual unit systems. The paper bounds $r<(d+1)/\log_2(4/3)$ and gives the amortized per-bit carry argument.
