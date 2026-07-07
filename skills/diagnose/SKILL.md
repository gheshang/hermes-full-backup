---
name: diagnose
description: Disciplined diagnosis loop for hard bugs and performance regressions. Reproduce → minimise → hypothesise → instrument → fix → regression-test. Use when user says "diagnose this" / "debug this", reports a bug, says something is broken/throwing/failing, or describes a performance regression.
---

# Diagnose

Disciplined diagnosis loop for hard bugs and performance regressions:

1. **Reproduce** — Can you reproduce it reliably? If not, what's the minimum set of conditions needed?
2. **Minimise** — Strip away everything non-essential. What's the smallest reproduction case?
3. **Hypothesise** — What's the most likely root cause? Write it down before looking at code.
4. **Instrument** — Add logs/assertions/breakpoints at the hypothesised failure point. Don't guess — measure.
5. **Fix** — Apply the minimum fix that addresses the root cause, not the symptom.
6. **Regression-test** — Write a test that would have caught this. If you can't, you don't understand the bug.

**Rules:**
- Never skip step 1. If you can't reproduce, you can't fix.
- Never fix without a hypothesis. Random changes are not diagnosis.
- Always write a regression test. If the bug doesn't have a test, it will come back.