# MarkItDown — Knowledge Base Batch Conversion Patterns

Install: `pip install 'markitdown[all]'`

## Batch Convert a Directory of Mixed Formats

```bash
for f in ~/knowledge-base/*.{pdf,docx,xlsx,pptx}; do
  [ -f "$f" ] || continue
  out_dir=~/knowledge-base-md/
  mkdir -p "$out_dir"
  ~/python-practice/.venv/bin/markitdown "$f" -o "$out_dir/$(basename "${f%.*}").md"
done
```

## Python Batch Script

```python
from pathlib import Path
from markitdown import MarkItDown

def batch_convert(input_dir, output_dir, formats=(".pdf", ".docx", ".xlsx", ".pptx")):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    md = MarkItDown()
    for f in input_path.rglob("*"):
        if f.suffix in formats:
            try:
                result = md.convert(str(f))
                out_file = output_path / f"{f.stem}.md"
                out_file.write_text(result.markdown, encoding="utf-8")
                print(f"✓ {f.name} → {out_file.name}")
            except Exception as e:
                print(f"✗ {f.name}: {e}")

batch_convert("~/knowledge-base", "~/knowledge-base-md")
```

## PDF Limitations

- Uses pdfminer (text-based extraction) — no OCR by default
- Scanned PDFs → plain text only (no layout retention)
- For scanned PDFs: add Azure Document Intelligence backend
  ```bash
  pip install 'markitdown[az-doc-intel]'
  ```
  Then set env vars `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT` and `AZURE_DOCUMENT_INTELLIGENCE_KEY`
