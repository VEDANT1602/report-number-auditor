# Numerical evidence experiment

The typed auditor meets 20/20 authored contracts, compared with 10/20 for numerical-presence checking. There are 7 valid claims and 13 invalid claims. False accepts are 0 versus 9.

This experiment deliberately targets known report failure boundaries. Number-presence is a weak ablation, not a mature fact-checking product. Both methods receive the same artifact and authored claims.

My approach binds the bytes, metric, population, denominator, operation, units and rounding tolerance before accepting a number. The useful result is an inspectable rejection reason. The next step is independently annotated real report sidecars; no LLM prose or automatic publishing was evaluated.
