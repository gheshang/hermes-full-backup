---
name: zoom-out
description: Tell the agent to zoom out and give broader context or a higher-level perspective. Use when you're unfamiliar with a section of code or need to understand how it fits into the bigger picture.
disable-model-invocation: true
---

# Zoom Out

Step back and see the bigger picture:

1. **What system is this part of?** — What's the parent module, service, or architecture layer?
2. **What does this component do at a high level?** — One sentence summary.
3. **What are its inputs and outputs?** — What does it consume? What does it produce?
4. **What are the key dependencies?** — What does it rely on? What relies on it?
5. **What are the failure modes?** — What happens when things go wrong?

**Rules:**
- Don't dive into implementation details. Stay at the abstraction level above.
- If you can't answer these questions, you don't understand the code well enough to work on it.
- Use this skill before making architectural changes or touching unfamiliar code.