---
name: document-processing
description: Document manipulation — PDF extraction (pymupdf/marker-pdf), DOCX table editing with merged cells, PPTX slide decks, and natural-language PDF editing.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [PDF, DOCX, PPTX, Documents, OCR, Text-Extraction, Table-Editing, Slide-Decks, Document-Generation]
    related_skills: []
---

# Document Processing — Unified Guide

This umbrella skill consolidates all document manipulation capabilities. Each tool serves a different document format:

- **ocr-and-documents**: PDF extraction (text-based and OCR/scanned)
- **docx-table-editing**: Word (.docx) table editing with merged cells
- **powerpoint**: PowerPoint (.pptx) slide deck creation and editing
- **nano-pdf**: Natural-language PDF editing

**Choose your tool based on the format:**

| Format | Primary Tool |
|--------|--------------|
| PDF (text-based, instant) | ocr-and-documents (pymupdf) |
| PDF (scanned/OCR) | ocr-and-documents (marker-pdf) — needs GPU |
| PDF / DOCX / XLSX / PPTX → Markdown (lightweight) | MarkItDown (no GPU needed) |
| DOCX (tables, merged cells) | docx-table-editing |
| PPTX (slide decks) | powerpoint |
| PDF (natural-language edits) | nano-pdf |

---

## 1. PDF & Document Extraction

### Decision Tree

```
Remote URL available?
├─ YES → Use web_extract first (Firecrawl, no local deps)
└─ NO → Local extraction needed
    ├─ Knowledge base / multi-format (PDF+DOCX+XLSX+PPTX) → MarkItDown (lightweight)
    ├─ Text-based PDF only → pymupdf (instant, ~25MB)
    └─ Scanned PDF / OCR / Equations → marker-pdf (~5GB, needs GPU)
```

### Tool Comparison

| Feature | pymupdf | marker-pdf | MarkItDown |
|---------|---------|------------|------------|
| **Text-based PDF** | ✅ | ✅ | ✅ |
| **Scanned PDF (OCR)** | ❌ | ✅ (90+ languages) | ⚠️ (via Azure AI, optional) |
| **Word (.docx)** | ❌ | ❌ | ✅ |
| **Excel (.xlsx)** | ❌ | ❌ | ✅ |
| **PPT (.pptx)** | ❌ | ❌ | ✅ |
| **HTML/URL** | ❌ | ❌ | ✅ |
| **Images** | ❌ | ❌ | ✅ (with AI description) |
| **Tables** | ✅ (basic) | ✅ (high accuracy) | ✅ |
| **Equations / LaTeX** | ❌ | ✅ | ❌ |
| **Code blocks** | ❌ | ✅ | ✅ |
| **Forms** | ❌ | ✅ | ❌ |
| **Headers/footers removal** | ❌ | ✅ | ❌ |
| **Reading order detection** | ❌ | ✅ | ❌ |
| **Install size** | ~25MB | ~3-5GB | ~50MB |
| **Speed** | Instant | ~1-14s/page (CPU), ~0.2s/page (GPU) | Instant |
| **GPU required** | ❌ | ✅ (CUDA torch) | ❌ |

**Decision tree for knowledge base / document-to-Markdown workloads:**

```
Server has GPU?
├─ YES → marker-pdf for PDFs, Pandoc for DOCX
└─ NO → MarkItDown (all formats) + Pandoc (DOCX only)

Need scanned PDF / equations / complex layout?
├─ YES → marker-pdf (GPU required) or Dolphin (lighter)
└─ NO → MarkItDown or pymupdf
```

**⚠️ marker-pdf pitfall on headless VPS:** marker-pdf depends on PyTorch with full CUDA/CUDA toolkit. On a server without NVIDIA GPU, pip installs all CUDA packages (~3GB+, takes 15+ minutes to download). Use MarkItDown instead — much lighter, multi-format, no GPU needed. For high-accuracy PDF without GPU, consider Microsoft's Azure Document Intelligence (MarkItDown supports it as optional backend).

### MarkItDown (Lightweight Multi-Format)

Microsoft's utility. Best for: knowledge base ingestion, LLM input preparation, batch document-to-Markdown workflows.

**Install:**
```bash
pip install 'markitdown[all]'
```

**CLI Usage:**
```bash
markitdown document.pdf -o output.md
markitdown document.docx -o output.md
markitdown spreadsheet.xlsx -o output.md
markitdown deck.pptx -o output.md
markitdown https://example.com -o page.md

# Batch convert all PDFs in a directory
for f in ~/knowledge-base/*.pdf; do
  markitdown "$f" -o "${f%.pdf}.md"
done
```

**Python API:**
```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("report.pdf")
print(result.markdown)
```

**What it does well:** DOCX/XLSX/PPTX → Markdown (Microsoft formats, richer output). HTML/URL → Markdown. PDF → Markdown (uses pdfminer, basic but clean for text-based PDFs).

**What it doesn't do:** Scanned PDF OCR (needs Azure Document Intelligence add-on). Complex layouts/tables may lose structure. No image extraction (only placeholders).

**Reference:** `references/markitdown-knowledge-base.md` — batch conversion patterns and workflow scripts.
**Post-processing:** See `references/pdf-markdown-cleaning.md` — strip repeated headers/footers AND semantic reflow (join hard wraps, split by article boundaries, clean pipe artifacts). Scripts: `scripts/clean-pdf-markdown.py` (basic), `scripts/semantic-reflow-md.py` (advanced, for knowledge base).

### pymupdf (Lightweight)

**Install:**
```bash
pip install pymupdf pymupdf4llm
```

**Usage via helper script:**
```bash
python scripts/extract_pymupdf.py document.pdf              # Plain text
python scripts/extract_pymupdf.py document.pdf --markdown    # Markdown
python scripts/extract_pymupdf.py document.pdf --tables      # Tables
python scripts/extract_pymupdf.py document.pdf --images out/ # Extract images
python scripts/extract_pymupdf.py document.pdf --metadata    # Title, author, pages
python scripts/extract_pymupdf.py document.pdf --pages 0-4   # Specific pages
```

**Inline Python:**
```python
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
```

### marker-pdf (High-Quality OCR)

**Check disk space first:**
```bash
python scripts/extract_marker.py --check
```

**Install:**
```bash
pip install marker-pdf
```

**Usage:**
```bash
python scripts/extract_marker.py document.pdf                # Markdown
python scripts/extract_marker.py document.pdf --json         # JSON with metadata
python scripts/extract_marker.py document.pdf --output_dir out/  # Save images
python scripts/extract_marker.py scanned.pdf                 # Scanned PDF (OCR)
python scripts/extract_marker.py document.pdf --use_llm      # LLM-boosted accuracy
```

**CLI:**
```bash
marker_single document.pdf --output_dir ./output
marker /path/to/folder --workers 4    # Batch
```

### Arxiv Papers

```bash
# Abstract only (fast)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# Full paper
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])

# Search
web_search(query="arxiv GRPO reinforcement learning 2026")
```

### Split, Merge & Search (pymupdf)

**Split:**
```python
import pymupdf
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5):
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")
```

**Merge:**
```python
result = pymupdf.open()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")
```

**Search:**
```python
doc = pymupdf.open("report.pdf")
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results:
        print(f"Page {i+1}: {len(results)} match(es)")
```

---

## 2. DOCX Table Editing

### Overview

Process Word (.docx) files, especially tables with merged cells (colspan/rowspan).

### Use Cases

- Read tables with merged cells
- Create tables with merged cells
- Template filling (Mail Merge)
- Format-preserving document generation

### Core Problem

| Problem | Cause | Solution |
|---------|-------|----------|
| python-docx can't read colspan/rowspan | High-level API doesn't expose `w:gridSpan` and `w:vMerge` | Parse XML directly |
| Merged cells show empty | Merged cells are same object in memory | Check `_tc` element is same |
| Can't create merged cells | python-docx has no `merge_cells()` | Use `cell.merge(other_cell)` or XML |

### Technical Choices

| Scenario | Recommended | Library |
|----------|-------------|---------|
| Simple tables (no merge) | python-docx | `pip install python-docx` |
| Complex tables (merged cells) | Aspose.Words | `pip install aspose-words` |
| Template filling | docx-mailmerge | `pip install python-docx-mailmerge` |
| Jinja2 templates | docxtpl | `pip install docxtpl` |
| Format extraction + reproduction | docx-format-replicator | See references |

### Diagnosis Tool

```bash
python scripts/docx_table_inspector.py <file.docx>
```

### Reading Merged Cells (python-docx + XML)

```python
from docx import Document
from lxml import etree

ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

doc = Document("template.docx")
table = doc.tables[0]

for row_idx, row in enumerate(table.rows):
    for cell in row.cells:
        tcPr = cell._tc.find('w:tcPr', ns)
        if tcPr is not None:
            grid_span = tcPr.find('w:gridSpan', ns)
            v_merge = tcPr.find('w:vMerge', ns)
            colspan = int(grid_span.get('{http://...}val', 1)) if grid_span is not None else 1
            rowspan = v_merge is not None
```

### Creating Merged Cells (python-docx)

```python
from docx import Document

doc = Document()
table = doc.add_table(rows=3, cols=4)

# Horizontal merge (colspan)
table.cell(0, 0).merge(table.cell(0, 2))  # Merge first 3 cells

# Vertical merge (rowspan)
table.cell(0, 0).merge(table.cell(2, 0))  # Merge first 3 rows
```

### Template Filling (Mail Merge)

```python
from mailmerge import MailMerge

document = MailMerge("template.docx")
document.merge(name="张三", company="ABC公司", amount="10000")
document.write("output.docx")
```

### Format Extraction & Reproduction

```bash
# Extract format template
python scripts/extract_format.py template.docx format_template.json

# Generate new document
python scripts/generate_document.py format_template.json content.json output.docx
```

### Pitfalls

1. **python-docx merged cell detection:** `row.cells[0] == row.cells[1]` is True for merged, but can't distinguish colspan/rowspan. Must parse XML.

2. **Aspose.Words CellMerge:** `cell.cell_format.horizontal_merge` may return `NONE` even if merged. Check XML or text content.

3. **docxtpl table row loops:** Jinja2 tags can't span table rows. Use special syntax `{% for item in items %}` inside table rows.

4. **Format loss:** python-docx new tables have no style by default. Set `table.style = 'Table Grid'`.

5. **Backup first:** Modify existing docx only after backup. write_file is full overwrite, content loss irreversible.

---

## 3. PowerPoint (PPTX)

### Overview

Use this skill whenever a .pptx file is involved — creating, reading, editing, combining, splitting slide decks.

### Quick Reference

| Task | Guide |
|------|-------|
| Read/analyze content | `python -m markitdown presentation.pptx` |
| Edit or create from template | Read `references/editing.md` |
| Create from scratch | Read `references/pptxgenjs.md` |

### Reading Content

```bash
# Text extraction
python -m markitdown presentation.pptx

# Visual overview
python scripts/thumbnail.py presentation.pptx

# Raw XML
python scripts/office/unpack.py presentation.pptx unpacked/
```

### Editing Workflow

1. Analyze template with `thumbnail.py`
2. Unpack → manipulate slides → edit content → clean → pack

### Creating from Scratch

Use when no template or reference presentation available.

### Design Principles

**Before starting:**
- Pick bold, content-informed color palette
- Dominance over equality (60-70% one color, 1-2 supporting, 1 accent)
- Dark/light contrast (dark for title/conclusion, light for content)
- Commit to ONE visual motif (rounded frames, icons in circles, thick borders)

**Color Palettes:**

| Theme | Primary | Secondary | Accent |
|-------|---------|-----------|--------|
| Midnight Executive | `1E2761` (navy) | `CADCFC` (ice blue) | `FFFFFF` (white) |
| Forest & Moss | `2C5F2D` (forest) | `97BC62` (moss) | `F5F5F5` (cream) |
| Coral Energy | `F96167` (coral) | `F9E795` (gold) | `2F3C7E` (navy) |
| Warm Terracotta | `B85042` (terracotta) | `E7E8D1` (sand) | `A7BEAE` (sage) |
| Ocean Gradient | `065A82` (deep blue) | `1C7293` (teal) | `21295C` (midnight) |
| Charcoal Minimal | `36454F` (charcoal) | `F2F2F2` (off-white) | `212121` (black) |
| Teal Trust | `028090` (teal) | `00A896` (seafoam) | `02C39A` (mint) |
| Berry & Cream | `6D2E46` (berry) | `A26769` (dusty rose) | `ECE2D0` (cream) |
| Sage Calm | `84B59F` (sage) | `69A297` (eucalyptus) | `50808E` (slate) |
| Cherry Bold | `990011` (cherry) | `FCF6F5` (off-white) | `2F3C7E` (navy) |

**For each slide:**
- Every slide needs visual element (image, chart, icon, shape)
- Layout options: two-column, icon+text rows, 2x2 grid, half-bleed image
- Data display: large stat callouts, comparison columns, timeline/process flow
- Visual polish: icons in colored circles, italic accent text

**Typography:**

| Header Font | Body Font |
|-------------|-----------|
| Georgia | Calibri |
| Arial Black | Arial |
| Calibri | Calibri Light |
| Cambria | Calibri |
| Trebuchet MS | Calibri |
| Impact | Arial |
| Palatino | Garamond |
| Consolas | Calibri |

| Element | Size |
|---------|------|
| Slide title | 36-44pt bold |
| Section header | 20-24pt bold |
| Body text | 14-16pt |
| Captions | 10-12pt muted |

**Spacing:**
- 0.5" minimum margins
- 0.3-0.5" between content blocks
- Leave breathing room

### Avoid (Common Mistakes)

- Don't repeat same layout — vary columns, cards, callouts
- Don't center body text — left-align paragraphs and lists
- Don't skimp on size contrast — titles need 36pt+
- Don't default to blue — pick colors reflecting topic
- Don't mix spacing randomly — choose 0.3" or 0.5" gaps consistently
- Don't style one slide and leave rest plain
- Don't create text-only slides — add images, icons, charts
- Don't forget text box padding
- Don't use low-contrast elements
- **NEVER use accent lines under titles** — hallmark of AI-generated slides

### QA (Required)

**Content QA:**
```bash
python -m markitdown output.pptx
```
Check for missing content, typos, wrong order.

**Check for leftover placeholders:**
```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```

**Visual QA (USE SUBAGENTS):**

Convert to images, then inspect:
```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

Look for:
- Overlapping elements
- Text overflow or cut off
- Decorative lines positioned for single-line text but title wrapped
- Source citations colliding with content
- Elements too close (< 0.3" gaps)
- Uneven gaps
- Insufficient margin from slide edges (< 0.5")
- Columns not aligned consistently
- Low-contrast text/icons
- Text boxes too narrow causing excessive wrapping
- Leftover placeholder content

**Verification Loop:**
1. Generate slides → Convert to images → Inspect
2. List issues found (if none, look again more critically)
3. Fix issues
4. Re-verify affected slides
5. Repeat until full pass reveals no new issues

**Do not declare success until at least one fix-and-verify cycle completed.**

### Converting to Images

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

Creates `slide-01.jpg`, `slide-02.jpg`, etc.

To re-render after fixes:
```bash
pdftoppm -jpeg -r 150 -f N -l N output.pdf slide-fixed
```

### Dependencies

- `pip install "markitdown[pptx]"` — text extraction
- `pip install Pillow` — thumbnail grids
- `npm install -g pptxgenjs` — creating from scratch
- LibreOffice (`soffice`) — PDF conversion
- Poppler (`pdftoppm`) — PDF to images

---

## 4. nano-pdf (Natural-Language PDF Editing)

### Overview

Edit PDFs with natural-language instructions. Modify text, fix typos, update titles, make content changes to specific pages.

### Prerequisites

```bash
# Install with uv (recommended)
uv pip install nano-pdf

# Or with pip
pip install nano-pdf
```

### Usage

```bash
nano-pdf edit <file.pdf> <page_number> "<instruction>"
```

### Examples

```bash
# Change title on page 1
nano-pdf edit deck.pdf 1 "Change title to 'Q3 Results' and fix typo in subtitle"

# Update date on page 3
nano-pdf edit report.pdf 3 "Update date from January to February 2026"

# Fix content
nano-pdf edit contract.pdf 2 "Change client name from 'Acme Corp' to 'Acme Industries'"
```

### Notes

- Page numbers may be 0-based or 1-based depending on version — if wrong page, retry with ±1
- Always verify output PDF after editing
- Uses LLM under hood — requires API key (check `nano-pdf --help`)
- Works well for text changes; complex layout modifications may need different approach

---

## Quick Reference

| Format | Tool | Install | Key Command |
|--------|------|---------|-------------|
| PDF (text) | pymupdf | `pip install pymupdf` | `python scripts/extract_pymupdf.py file.pdf` |
| PDF (OCR) | marker-pdf | `pip install marker-pdf` | `python scripts/extract_marker.py file.pdf` |
| PDF (URL) | web_extract | built-in | `web_extract(urls=["https://..."])` |
| DOCX tables | docx-table-editing | `pip install python-docx` | `python scripts/docx_table_inspector.py file.docx` |
| PPTX | powerpoint | `pip install markitdown[pptx]` | `python -m markitdown file.pptx` |
| PDF edit | nano-pdf | `pip install nano-pdf` | `nano-pdf edit file.pdf 1 "instruction"` |

---

## Pitfalls Summary

1. **PDF extraction:** Always try `web_extract` first for URLs. pymupdf for text-based, marker-pdf for OCR.
2. **DOCX merged cells:** python-docx can't read colspan/rowspan at high level. Parse XML or use Aspose.Words.
3. **PPTX QA:** Always do visual QA with subagents. One fix often creates another problem.
4. **nano-pdf:** Page numbering may differ between versions. Verify output.
5. **Backup:** Always backup before modifying existing documents.