# Table Handling in Research Paper Writing

## Current State

The `research-paper-writing` skill does **not** include automated LaTeX table generation. The workflow is:

```
实验结果(JSON) → 手动分析 → 手动编写 LaTeX tabular
```

Results are stored in structured JSON (`results/<experiment>/<task>/<strategy>/result.json`), but there is no script to convert these to LaTeX tables.

## What Exists

| Component | Status |
|-----------|--------|
| Experiment result storage (JSON) | ✅ Implemented |
| Statistical analysis scripts | ✅ Implemented |
| Markdown monitoring tables | ✅ Implemented |
| LaTeX tabular generation | ❌ Manual only |

## Recommended Fix Pattern

Future sessions should create `scripts/results_to_latex_table.py` with:

```python
#!/usr/bin/env python3
"""Convert experiment JSON results to LaTeX tabular format."""
import json
import sys
from pathlib import Path
from typing import Optional

def load_results(results_dir: str) -> dict:
    """Load all result.json files from directory structure."""
    results = {}
    for f in Path(results_dir).rglob("result.json"):
        parts = f.relative_to(results_dir).parts
        if len(parts) >= 3:
            exp, task, strategy = parts[0], parts[1], parts[2]
            with open(f) as fp:
                data = json.load(fp)
            results.setdefault(exp, {}).setdefault(task, {})[strategy] = data
    return results

def to_latex_table(
    results: dict,
    experiment: str,
    metrics: list[str],
    bold_best: bool = True,
    significance_markers: bool = True,
) -> str:
    """Generate LaTeX tabular from results dict."""
    # Implementation: iterate tasks × strategies, format metrics
    # Support: error bars, p-values, significance (*, **, ***)
    pass

if __name__ == "__main__":
    results_dir = sys.argv[1] if len(sys.argv) > 1 else "results/"
    results = load_results(results_dir)
    # Print LaTeX table to stdout
```

## DOCX Table Alternative

For Word-based paper drafting (collaborative editing), use the `document-processing` skill:
- Simple tables: `python-docx`
- Merged cells: Parse XML (`w:gridSpan`, `w:vMerge`) or use `Aspose.Words`
- Template filling: `docxtpl` or `MailMerge`

See `document-processing/SKILL.md` for full implementation.

## Reporting Standards (from skill)

When creating tables, always include:
- Sample sizes (n=X problems/tasks)
- Number of runs (K independent runs)
- Error bars (std dev or std error)
- 95% confidence intervals for key results
- Significance test p-values
- Effect sizes (Cohen's d or h)

## Pitfalls

1. **No automated converter exists** — agents must manually write LaTeX tabular code
2. **Markdown tables ≠ LaTeX tables** — monitoring reports use Markdown, but papers require LaTeX
3. **DOCX merged cells require XML parsing** — python-docx high-level API doesn't expose `w:gridSpan`/`w:vMerge`