# Report Number Auditor

A number appearing in an artifact does not make a report claim supported.

This independent portfolio experiment by Vedant Thaker runs locally on Python 3.11. All inputs are original fictional or synthetic fixtures. It requires no cloud account, paid API, credentials, external weights or employer data.

## The decision

I narrowed technical report review to typed numeric sidecars. A number-only lookup can accept the right digits from the wrong population, stale experiment or incompatible unit. My pipeline verifies source bytes, metric identity, denominator, transformation and declared rounding before accepting the claim. It never executes arbitrary arithmetic or auto-publishes prose.

## Reproduce and inspect

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python run.py --output runs/ci
```

The default `python run.py` refreshes committed `results/`; `--output` writes a fresh run to an ignored directory. The seeded generator in `generate.py` writes the original input fixtures to `data/`. [Measured results](results/report.md), [raw metrics](results/metrics.json), and [source/data/result digests](results/manifest.json) make the experiment inspectable. Tests verify known answers and failure boundaries, not just successful execution.

## Measured comparison and next decision

On **20 authored claim contracts**, typed evidence checking accepts all valid claims and rejects all invalid claims: **20/20 correct**, compared with **10/20** for number-presence checking. False accepts are **0 versus 9**. These are targeted protocol cases, not a general factuality score.

My next decision is to test independently annotated report sidecars and stronger evidence-aware baselines before expanding beyond structured numeric claims.

## What the result can support

The authored contracts measure protocol conformance. The system does not read unrestricted prose, infer scientific causality, authenticate an experiment owner, or establish whether the source measurement itself is correct. A trusted artifact plus a structured claim is required.

The claim's `digits` field sets the numerical tolerance to half a unit in its last declared decimal place, plus a small floating-point allowance. It does not enforce display formatting or guarantee that the supplied value is rendered with exactly that many decimal places. Text formatting needs a separate check.

The next decision follows from the recorded comparison, including weak or negative outcomes. No synthetic result is presented as an employer deployment or a real-world business improvement.

See [data card](docs/data-card.md) and [reference credits](docs/provenance.md). Original code and fixtures are MIT licensed.
