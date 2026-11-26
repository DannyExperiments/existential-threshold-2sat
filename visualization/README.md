# Watch the binary search

[Download the offline explorer ZIP](existential-threshold-2sat-explorer.zip?raw=1). Extract it and open index.html in a browser. Use the three search-node buttons and drag the cube or use the rotation slider. All eight exact $y_1y_2y_3$ assignments appear in the cube. Passing assignments also appear as text.

The formula is
$$
(\neg x_1\vee\neg x_2)\wedge(x_1\vee y_1)\wedge(x_2\vee y_2)\wedge(y_1\vee y_3).
$$
The threshold is $4$ satisfying assignments out of $8$.

| Node | Count tested | x-assumptions and decision |
| --- | ---: | --- |
| Root | $6/8$ | Force $x_1=x_2=1$. Since $x_1\to\neg x_2$, the active units conflict. |
| Allow $y_1$ | $4/8$ | Keep $x_2=1$, use $x_1=0$, and accept. |
| Allow $y_2$ | $3/8$ | Prune on the count before testing x-feasibility. |

A successful execution can finish in the first child. The animation includes the other branch to show how two feasible selections can have different count outcomes. The picture demonstrates one instance of the branching step. The paper proves the result for all finite input formulas in scope.

Rebuild the GIF from the candidate root with python3 visualization/render.py. The renderer uses Pillow and selects Arial on macOS or DejaVu Sans on Linux. The --font-dir option selects the folder explicitly.

The independent mathematical replay in verification/src/replay.py checks the exact three vertex sets and both candidate witnesses. The explorer computes the displayed counts directly from its Boolean condition.
