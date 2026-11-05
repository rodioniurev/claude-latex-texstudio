# Working through the TeXstudio MCP server

Use this when tools of a TeXstudio MCP server are available (they look like `mcp__texstudio__get_project`). The server runs inside the user's editor on `127.0.0.1` and works only with open files of the active project. If it is not configured, work with files and commands as described in SKILL.md.

Behavior below was checked against API 1.7. Do not rely on version numbers: call `get_capabilities` first and look at `features`, `permissions` and `limits`.

## Workflow

1. `get_capabilities`: which features exist and which permissions the user granted (`read`, `edit`, `build` are separate switches in TeXstudio settings).
2. `get_project`: root file, project files with `dirty` flags, compiler. `get_selection` when the user says "here" or "this".
3. `read_document`: the editor buffer, including unsaved text. Keep `content_hash`. It continues with `next_start_line` when truncated.
4. `apply_edits`: replace exact fragments (`old_text` to `new_text`), pass `expected_hash` from the last read. All edits of one call succeed or none do, and one call is one Undo step. The cursor does not move. Use `near_line` when a fragment occurs several times.
5. `save_documents`, then `build`. A build refuses unsaved files (`unsaved_document`). The result already carries status, counts and the errors with file, line and `source_line`, so a separate call is rarely needed.
6. After a failed build fix the first error first. `get_diagnostics` gives more; warnings are omitted by default (`diagnostics_omitted`), ask with `severity: all`. `needs_rerun` and `pdf_updated` are reported separately.
7. `get_outline` shows sections, labels and references. Use `scope: project` to see every project file, otherwise only the active file is shown.
8. `reveal` moves the user's cursor and view. Use it only to show a place, never as part of editing.

## Errors and what to do

| code | Meaning | Action |
|---|---|---|
| `ui_blocked` | A dialog is open in TeXstudio, or a build command was overridden by the document | Read `window_title` or `reason`; ask the user to close the dialog or run the build manually |
| `permission_denied` | The switch is off in settings | Ask the user to enable it |
| `stale_document` | The buffer changed after the last read | `read_document`, then repeat the edit |
| `no_match`, `ambiguous_match` | The fragment is missing or occurs several times | Copy an exact fragment from the buffer, add `near_line` or more context |
| `unsaved_document` | Build with dirty files | `save_documents` first |
| `build_busy` | Another build is running | Wait, poll `get_build`, or `cancel_build` |
| `out_of_project` | File is outside the project directory | Use plain file tools, or ask |
| `not_found` | Unknown build id (history is lost on restart) | Start a new build |

## Magic comments

`% !TeX program = pdflatex` with an exact built-in program name is accepted. Overrides such as `% !TXS-program:...` and unknown program names are blocked, and the answer names the file, line and text. Never try to get around it; show the user the line and let them decide.

## Things that look like API faults but are not

- `latexmk` started by TeXstudio can fail with "could not find the script engine perl" when Perl is not on TeXstudio's PATH. The message comes from MiKTeX. Suggest `pdflatex` or installing Perl.
- Build ids do not survive a restart of TeXstudio.
