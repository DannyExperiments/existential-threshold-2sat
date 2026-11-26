#!/usr/bin/env python3
"""Exact reference implementation and independent brute force for Catalog Q74."""
from itertools import combinations, product
import random


def implication_graph(clauses, n):
    graph = [[] for _ in range(2 * n)]
    index = lambda a: 2 * (abs(a) - 1) + (a < 0)
    for c in clauses:
        a, b = c[0], c[-1]
        graph[index(-a)].append(index(b))
        graph[index(-b)].append(index(a))
    return graph


def solve_base(graph):
    """Kosaraju, with iterative traversals. Return one model or None."""
    n = len(graph)
    reverse = [[] for _ in graph]
    for u, neighbors in enumerate(graph):
        for v in neighbors:
            reverse[v].append(u)
    seen = set()
    order = []
    for i in range(n):
        if i in seen:
            continue
        seen.add(i)
        stack = [(i, iter(graph[i]))]
        while stack:
            v, neighbors = stack[-1]
            u = next(neighbors, None)
            if u is None:
                order.append(v)
                stack.pop()
            elif u not in seen:
                seen.add(u)
                stack.append((u, iter(graph[u])))
    component = [-1] * n
    for i in reversed(order):
        if component[i] >= 0:
            continue
        component[i] = i
        stack = [i]
        while stack:
            for u in reverse[stack.pop()]:
                if component[u] < 0:
                    component[u] = i
                    stack.append(u)
    rank = {v: i for i, v in enumerate(reversed(order))}
    if any(component[i] == component[i ^ 1] for i in range(0, n, 2)):
        return None
    return [rank[component[i]] > rank[component[i ^ 1]] for i in range(0, n, 2)]


def assumptions(graph, base, active):
    """Return a saved model updated by implication closure or source labels."""
    source = [None] * len(graph)
    todo = []
    for u, label in active:
        i = 2 * (abs(u) - 1) + (u < 0)
        if source[i] is None:
            source[i] = label
            todo.append(i)
    for i in todo:
        if source[i ^ 1] is not None:
            return None, tuple(dict.fromkeys((source[i], source[i ^ 1])))
        for j in graph[i]:
            if source[j] is None:
                source[j] = source[i]
                todo.append(j)
    model = base.copy()
    for i in todo:
        model[i // 2] = not (i & 1)
    return tuple(model), ()


def clause_cover(clauses, d):
    """Greedy cover and exact matching cutoff. None means the input fails."""
    cover = set()
    three_power = 1
    for clause in clauses:
        if len(clause) == 2 and cover.isdisjoint(map(abs, clause)):
            cover.update(map(abs, clause))
            three_power *= 3
            exponent = len(cover) - d - 1
            if three_power.bit_length() <= exponent:
                return None
    return sorted(cover)


def count_with_cover(clauses, units, cover, n_y):
    digits = [0] * (n_y + 1)
    for values in product((False, True), repeat=len(cover)):
        beta = dict(zip(cover, values))
        marks = {}
        for c in (*clauses, *((u,) for u in units)):
            if any(abs(u) in beta and beta[abs(u)] == (u > 0) for u in c):
                continue
            residual = [u for u in c if abs(u) not in beta]
            if not residual:
                break
            assert len(residual) == 1
            u = residual[0]
            if abs(u) in marks and marks[abs(u)] != (u > 0):
                break
            marks[abs(u)] = u > 0
        else:
            i = n_y - len(cover) - len(marks)
            while digits[i]:
                digits[i] = 0
                i += 1
            digits[i] = 1
    # The reference replay extracts a Python integer for cross-checking.
    # The proof's implementation compares the digits with N directly.
    return int("".join(str(v) for v in reversed(digits)), 2)


def search(formula, n_x, n_y, threshold):
    """Variables are numbered 1 through n_x+n_y and x comes first."""
    if not 1 <= threshold <= 2**n_y:
        raise ValueError("count threshold out of range")
    a, b, mixed = [], [], []
    for c in formula:
        if any(-u in c for u in c):
            continue
        c = tuple(dict.fromkeys(c))
        if not c:
            return None, 0
        left = tuple(u for u in c if abs(u) <= n_x)
        right = tuple((abs(u) - n_x) * (1 if u > 0 else -1)
                      for u in c if abs(u) > n_x)
        if left and right:
            mixed.append((left[0], right[0]))
        elif left:
            a.append(left)
        else:
            b.append(right)
    g = implication_graph(a, n_x)
    base = solve_base(g)
    if base is None:
        return None, 0
    depth = n_y - (threshold - 1).bit_length()
    cover = clause_cover(b, depth)
    if cover is None:
        return None, 0
    calls = 0
    pending = [frozenset()]
    while pending:
        allowed = pending.pop()
        calls += 1
        if len(allowed) > depth or any(-u in allowed for u in allowed):
            continue
        if count_with_cover(b, allowed, cover, n_y) < threshold:
            continue
        model, conflict = assumptions(g, base, ((u, v) for u, v in mixed if v not in allowed))
        if model is not None:
            return model, calls
        pending.extend(allowed | {v} for v in reversed(conflict))
    return None, calls


def direct_count(formula, x, y_size):
    return sum(all(any(z[abs(u) - 1] == (u > 0) for u in c) for c in formula)
               for y in product((False, True), repeat=y_size)
               for z in (x + y,))


def check(formula, nx, ny, thresholds):
    by_x = {x: direct_count(formula, x, ny) for x in product((False, True), repeat=nx)}
    best = max(by_x.values())
    for t in thresholds:
        model, calls = search(formula, nx, ny, t)
        assert (model is not None) == (best >= t), (formula, nx, ny, t)
        if model is not None:
            assert by_x[model] >= t
        assert calls <= 2 ** (ny - (t - 1).bit_length() + 2) - 1
    return len(thresholds)


def worked_example():
    # y1,y2,y3 are 3,4,5 in the shared variable indexing.
    formula = ((-1, -2), (1, 3), (2, 4), (3, 5))
    evidence = []
    for allowed in ((), (1,), (2,)):
        cube = ["".join(str(int(v)) for v in y)
                for y in product((False, True), repeat=3)
                if (y[0] or y[2]) and all(y[i - 1] for i in allowed)]
        evidence.append(cube)
    assert evidence == [
        ["001", "011", "100", "101", "110", "111"],
        ["100", "101", "110", "111"],
        ["011", "110", "111"],
    ]
    assert search(formula, 2, 3, 4)[0] == (False, True)
    assert direct_count(formula, (False, True), 3) == 4
    assert direct_count(formula, (True, False), 3) == 3
    return evidence


def main():
    cases = pairs = 0
    for nx, ny in ((0, 0), (0, 1), (1, 0), (1, 1), (2, 1), (1, 2)):
        literals = tuple(i for k in range(1, nx + ny + 1) for i in (k, -k))
        clauses = [(u,) for u in literals] + [c for c in combinations(literals, 2) if c[0] != -c[1]]
        for mask in range(1 << len(clauses)):
            formula = tuple(c for i, c in enumerate(clauses) if mask >> i & 1)
            pairs += check(formula, nx, ny, range(1, 2**ny + 1))
            cases += 1
    print(f"Exhaustive normalized formulas: {cases:,} | exact threshold pairs: {pairs:,}")
    rng = random.Random(74)
    random_pairs = 0
    for _ in range(1000):
        nx, ny = rng.randrange(6), rng.randrange(8)
        literals = [i for k in range(1, nx + ny + 1) for i in (k, -k)]
        formula = tuple(tuple(rng.choice(literals) for _ in range(rng.randrange(1, 3)))
                        for _ in range(rng.randrange(24))) if literals else ()
        if rng.randrange(20) == 0:
            formula += ((),)
        random_pairs += check(formula, nx, ny, range(1, 2**ny + 1))
    print(f"Seeded random formulas: 1,000 | exact threshold pairs: {random_pairs:,}")
    assert check(((1, 2), (3, 4), (5, 6)), 0, 6, (27, 28, 32, 64)) == 4
    assert check(((1, 3), (1, 4), (-1, 3), (-1, 4)), 2, 2, (1, 2, 3, 4)) == 4
    print("Targeted early cutoff and repeated label/assumption cases: 8 exact threshold pairs")
    print("Worked example counts: root B = 6/8, allow y1 = 4/8, allow y2 = 3/8")
    worked_example()
    print("PASS: exact decisions, returned models, and search call ceilings")


if __name__ == "__main__":
    main()
