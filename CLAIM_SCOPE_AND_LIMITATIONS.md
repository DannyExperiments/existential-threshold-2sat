# Claim scope and limitations

The theorem takes a 2-CNF over two disjoint finite variable lists and an exact integer count threshold between 1 and $2^{n_y}$, where $n_y$ counts the specified probabilistic variables. Probabilistic assignments are uniform. The result decides whether there is an $x$-assignment that reaches the threshold and constructs one on acceptance.

The formula-dependent time is $O((1/p)^c|\varphi|)$ word operations with $c=1+2/\log_2(4/3)<5.82$. The word size is $\Theta(\log(2+|\varphi|))$ and the indexed formula size includes declared variables. Counts use per-bit entries and amortized carry propagation. A rational threshold with at most $L$ bits for each integer adds $O((n_y+L)L)$ bit operations for exact conversion. A fixed real is interpreted through its exact count threshold.

The strict comparison uses $\lfloor 2^{n_y}p\rfloor+1$. The Vertex Cover reduction gives a conditional lower bound on subexponential dependence in $\log(1/p)$ under ETH. The exponent $c$ is an upper bound. Nonuniform distributions, higher clause widths and counting the good $x$-assignments are outside the proved scope.

The literature search supports the comparison against Akmal’s published XP bound. Earlier general methods imply a weaker bound with a polynomial factor in formula size. Historical priority remains open.
