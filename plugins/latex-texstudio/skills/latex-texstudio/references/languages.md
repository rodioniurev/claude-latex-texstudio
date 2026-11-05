# Languages with pdflatex

Each "tested" row was compiled with pdflatex (MiKTeX 25.4). The last language in the babel option list is the main one.

| Language | fontenc | babel | Notes |
|---|---|---|---|
| Russian | `T2A` | `russian` | Tested |
| Russian + French, German | `T1,T2A` | `french,german,english,russian` | Tested. Use `\foreignlanguage{french}{...}` for inline text |
| Ukrainian, Belarusian, Bulgarian, Serbian (Cyrillic) | `T2A` | `ukrainian`, `belarusian`, `bulgarian`, `serbianc` | Same pattern as Russian, not tested here |
| Western and Central European | `T1` | language name | Same pattern, not tested here. `lmodern` is fine without Cyrillic |
| Greek with Russian | `LGR,T2A` | `greek,english,russian` | Tested. Use `\foreignlanguage{greek}{...}` |
| Chinese | none needed | none | Tested: `\usepackage{CJKutf8}` and `\begin{CJK}{UTF8}{gbsn}...\end{CJK}`. Needs CJK fonts |
| Japanese, Korean | none needed | none | `CJKutf8` with fonts `min` or `mj`, not tested here. Prefer xelatex or lualatex for long texts |
| Arabic, Persian, Hebrew, Devanagari, Thai | not suitable | | Tested for Arabic: pdflatex fails. Propose xelatex or lualatex |

## Switching to xelatex or lualatex

Replace `inputenc` and `fontenc` with:

```latex
% !TeX program = xelatex
\usepackage{fontspec}
\setmainfont{Noto Serif}       % must be installed and cover the scripts in use
\usepackage[english,russian]{babel}
```

Change the compiler in TeXstudio too (Options > Configure TeXstudio > Build), or rely on the `% !TeX program` comment.
