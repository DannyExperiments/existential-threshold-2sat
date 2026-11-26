# Reproducibility

From the root, run **python3 verification/src/replay.py** using Python 3.10 or later. The replay uses the standard library. It checks search outcomes, witnesses and call ceilings using brute-force assignment counts. The expected summary is in [the replay log](verification/logs/replay.txt).

Run **python3 scripts/verify_repository.py** to check the file inventory, SHA-256 ledger and ZIP members. Use the [paper build instructions](paper/BUILD.md) to rebuild the PDF and the [visualization guide](visualization/README.md) to rebuild the GIF. The explorer runs offline.
