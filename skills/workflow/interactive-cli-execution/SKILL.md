---
name: interactive-cli-execution
description: Workflow for executing and interacting with CLI scripts that prompt for continuous standard input.
---
# Interactive CLI Execution

When asked to run a script or tool that requires interactive user input (e.g., Python scripts using `input()`, setup wizards, configuration CLI tools), standard shell commands will fail or be blocked. Follow this specific procedure.

## Trigger
- You need to interact with a script that asks sequential questions.
- A foreground `terminal` call fails with `EOFError: EOF when reading a line` or hangs.
- Piping text via `echo` or `printf` into a script is blocked or unsupported by the tool.

## Execution Steps
1. **Spawn Background Process with PTY**
   Initialize the interactive terminal using the `terminal` tool with `pty=true` and `background=true`.
   `call:default_api:terminal{command: "python3 script.py", background: true, pty: true}`
   *Save the returned `session_id`.*

2. **Poll to Read Prompts**
   Check what the script is asking for.
   `call:default_api:process{action: "poll", session_id: "proc_12345"}`
   *Read the `output_preview` to see the prompt exactly as a user would.*

3. **Submit Input**
   Send the requested answer using the `process` tool's `submit` action.
   `call:default_api:process{action: "submit", data: "my_answer", session_id: "proc_12345"}`
   *Note: `submit` automatically appends a newline (like pressing Enter). If you need raw data without a newline, use the `write` action instead.*

4. **Iterate**
   Repeat Steps 2 and 3 sequentially for every prompt the script produces. Always `poll` between submissions to ensure the previous input was accepted and the next prompt is fully rendered.

5. **Wait and Terminate**
   Once the final input is submitted, wait for the script to cleanly exit.
   `call:default_api:process{action: "wait", session_id: "proc_12345"}`

## Pitfalls to Avoid
- **Foreground Hangs**: Never run an interactive script in the foreground. It has no stdin and will either crash (`EOFError`) or hang indefinitely.
- **Blind Submissions**: Do not submit input sequentially without polling in between. The CLI might take time to process and render the subsequent prompt; if you submit blindly, inputs may get buffered or misaligned.
- **Command Piping Issues**: Piping output (e.g. `printf "a\nb" | script`) is brittle and sometimes triggers environment security blocks. Explicitly using PTY and background process controls is the robust solution.