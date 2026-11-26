# Status

[Version 1.0.0](https://github.com/DannyExperiments/existential-threshold-2sat/releases/tag/v1.0.0) · 27 November 2026 · [Version DOI](https://doi.org/10.5281/zenodo.24567308)

It answers the linear-formula-time question in Open Problem 3 of Shyan Akmal’s thesis in the exact count-threshold model. Earlier methods give ordinary fixed-parameter tractability with a polynomial formula factor. The exact Python replay corroborates the proof on finite inputs.

Internal mathematical review covered the stated result and its scope. External peer review and formal verification have not been conducted. The exact replay compares 1,603,370 formula and threshold pairs against direct enumeration and checks every returned witness.

The repository verification, replay and PDF build workflows succeeded on the [reviewed commit](https://github.com/DannyExperiments/existential-threshold-2sat/commit/9f7bb6c92ddbaa4bcd515a16b86ee69d28b86816). See the [literature and priority audit](audits/public_safe_reports/LITERATURE_AUDIT.md).
