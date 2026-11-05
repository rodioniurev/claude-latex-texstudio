# LaTeX + TeXstudio skill

A skill for writing, fixing and building LaTeX documents with TeXstudio and pdflatex, with correct Cyrillic and other non-Latin text. Claude loads it by itself whenever a task involves `.tex`, `.bib` or `.sty` files, a LaTeX preamble, compile errors or a `.log` file.

## What it does

- Gives tested preambles for pdflatex: Russian, mixed Latin and Cyrillic, Greek and Chinese. Each one was compiled with a real pdflatex build.
- Prevents failures that are easy to miss: `lmodern` with Cyrillic silently substitutes fonts, `listings` stops on Russian comments, and missing `cm-super` produces bitmap fonts.
- Parses a long LaTeX `.log` into a short list of errors, with file, line and source text, so Claude does not have to read the whole log.
- Says so when pdflatex is not suitable (Arabic, Hebrew, Devanagari) and proposes xelatex or lualatex. It never switches the compiler silently.
- Respects the choices of an existing project, including its magic comments and its engine.

## What it runs on your machine

Everything is local. The plugin has no network access, no servers and no hooks, and it stores and sends no data.

When the skill is active, Claude may run these commands in your project directory, through its normal permission prompts:

- `latexmk -pdf -interaction=nonstopmode -file-line-error -synctex=1 main.tex`, or `pdflatex` and `biber` directly. `-shell-escape` is never used unless you ask for it.
- `python scripts/texlog.py main.log`, the bundled log parser. It only reads the log file and prints a summary. It uses the Python standard library.
- `pdffonts`, `pdftotext` and `pdftoppm` from Poppler, to check fonts and the rendered result.

If the user has configured a TeXstudio MCP server, Claude can also use its tools. The plugin itself does not start, install or contact any server: the user adds one explicitly with `claude mcp add`, and it only listens on `127.0.0.1`.

The skill also includes a starter template (`assets/ru-article.tex`), a helper for Cyrillic in `listings` (`assets/lst-cyrillic.tex`) and a table of languages (`references/languages.md`).

## Requirements

A TeX distribution (MiKTeX or TeX Live) and Python 3 for the log parser. TeXstudio is not required.

## Tested on

MiKTeX 25.4 on Windows 11. Reports from TeX Live and other systems are welcome in the repository issues.

## Install

```bash
claude plugin marketplace add rodioniurev/claude-latex-texstudio
claude plugin install latex-texstudio@rodioniurev-latex
```

## Скилл для LaTeX + TeXstudio (кратко по-русски)

Скилл помогает писать, исправлять и собирать LaTeX-документы в связке TeXstudio и pdflatex с правильной кириллицей. Преамбулы проверены настоящей сборкой, а длинный лог компиляции превращается в короткий список ошибок. Всё работает локально, без доступа к сети. Если pdflatex не подходит для языка, скилл говорит об этом и предлагает xelatex или lualatex.

## License

MIT
