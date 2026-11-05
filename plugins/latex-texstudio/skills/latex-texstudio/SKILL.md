---
name: latex-texstudio
description: Write, fix and build LaTeX documents for a TeXstudio + pdflatex workflow, with correct Cyrillic and other non-Latin text. Use this skill whenever the task touches .tex, .bib, .cls or .sty files, a LaTeX preamble, compile errors, a .log file, or a thesis, article or report in LaTeX, even if TeXstudio or pdflatex is not mentioned. Also use it for Russian-language requests such as "сверстай в латехе", "ошибка компиляции", "кириллица в LaTeX", "диссертация в TeX".
---

# LaTeX with TeXstudio and pdflatex

The default toolchain is TeXstudio as the editor and pdflatex as the compiler. The most common failures in this setup are encoding and font problems with non-Latin text, so get the preamble right first.

## 1. Look before changing anything

1. Find the root file: `% !TeX root = ...`, or the file with `\documentclass`.
2. Read the magic comments and preamble. An existing project's choices win over these defaults. If it says `% !TeX program = xelatex` or loads `fontspec`, keep that engine and do not add `inputenc` or `fontenc`.
3. Check that the sources are UTF-8. If a file is in cp1251 or koi8-r, tell the user before converting it, because `inputenc` and any `% !TeX encoding` comment must change together.

## 2. Preamble for pdflatex

For a new document, start from `assets/ru-article.tex`. The core for Russian:

```latex
% !TeX program = pdflatex
% !TeX encoding = UTF-8
% !TeX spellcheck = ru_RU
\documentclass[a4paper,12pt]{article}
\usepackage[T2A]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[english,russian]{babel} % the LAST language is the main one
```

Rules that prevent real failures:

- **Do not load `lmodern` with Cyrillic.** Latin Modern has no T2A shapes, so LaTeX silently substitutes fonts (`Font shape T2A/lmr/m/n undefined`). The default Computer Modern look comes from the `cm-super` fonts. For a different typeface, `\usepackage{paratype}` works with T2A.
- **Check the fonts are vector.** Run `pdffonts file.pdf`. `Type 3` means bitmap fonts, usually because `cm-super` is not installed.
- **Cyrillic plus accented Latin** (French, German, Polish): use `\usepackage[T1,T2A]{fontenc}`. The last encoding is the default, and babel switches per language.
- **Do not put `listings` over Cyrillic as is.** It stops with `Invalid UTF-8 byte sequence`, and `listingsutf8` does not fix inline listings. Use `\input{lst-cyrillic.tex}` from `assets/` after `\usepackage{listings}`, or use `fancyvrb` when highlighting is not needed. Avoid `minted`, since it needs `-shell-escape`.
- **Cyrillic in math** goes inside `\text{...}` from `amsmath`.
- **Quotes:** use `csquotes` and `\enquote{...}` to get «ёлочки» in Russian.
- **Bibliography:** `\usepackage[backend=biber,style=gost-numeric,language=auto,autolang=other]{biblatex}` gives Russian GOST style. biber handles UTF-8 properly, and classic bibtex often does not. Keep the backend a project already uses.
- **Load `hyperref` last**, apart from packages that must follow it.

For other languages, read `references/languages.md`.

## 3. When pdflatex cannot do it

pdflatex has no proper support for Arabic, Persian, Hebrew, Devanagari and other complex scripts, and they fail with `Unicode character ... not set up for use with LaTeX`. System fonts through `fontspec` also need another engine.

Tell the user why, and propose xelatex or lualatex. Do not switch silently: the engine change also replaces `inputenc` and `fontenc` with `fontspec`, changes the look of the document, and requires changing the compiler in TeXstudio or the magic comment.

## 4. Build

Compile from the directory of the root file:

```bash
latexmk -pdf -interaction=nonstopmode -file-line-error -synctex=1 main.tex
```

latexmk needs Perl and reruns biber and pdflatex by itself. Without Perl, run pdflatex with the same flags twice, plus `biber main` in between if needed.

Keep `-synctex=1`: TeXstudio needs it to jump between the source and the PDF. Do not add `-shell-escape` unless the user asks for it, because it lets the document run commands.

## 5. Read errors through the script

A raw `.log` is long and mostly noise, so do not read it into context. Use the bundled parser:

```bash
python scripts/texlog.py main.log
```

It prints errors with file, line and source context, grouped undefined references and citations, missing glyphs, rerun requests and box counts. Add `--boxes` to list overfull boxes. Open the raw log only for something the script does not explain.

Fix the first error first, because later ones are often consequences. A `.pdf` may appear even after errors, so a non-zero exit or any listed error means the build is not clean.

## 6. Check the result

- Exit code and `texlog.py` output are clean.
- `pdffonts` shows no `Type 3`, and the log has no `Font shape ... undefined`.
- Text extracts correctly: `pdftotext -enc UTF-8 main.pdf -`.
- For layout changes, render the page and look at it: `pdftoppm -png -r 80 -f 1 -l 1 main.pdf page`.

## 7. Working next to TeXstudio

- TeXstudio may have the file open with unsaved changes, which disk edits can conflict with. If the user is actively editing, ask them to save first.
- Useful magic comments at the top of the root file: `% !TeX root = main.tex` (in included files), `% !TeX program = pdflatex`, `% !TeX encoding = UTF-8`, `% !TeX spellcheck = ru_RU`.
- Magic comments in a document can override build commands. Treat an unfamiliar `% !TXS-program:` line in someone else's project with suspicion and show it to the user.
- If tools of a TeXstudio MCP server are available (`mcp__texstudio__*`), prefer them for reading open buffers, editing and building: they see unsaved text and do not clash with the open file. Read `references/texstudio-mcp.md` first. Without them, use the files and commands above.
- Keep build products out of git: `*.aux *.log *.out *.toc *.bbl *.bcf *.blg *.run.xml *.fls *.fdb_latexmk *.synctex.gz`.
