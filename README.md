# LaTeX + TeXstudio skill for Claude Code

A Claude Code skill for writing and building LaTeX documents with TeXstudio and pdflatex, with correct Cyrillic and other non-Latin text.

- Preambles checked with real pdflatex builds, for Russian, mixed Latin and Cyrillic, Greek and Chinese.
- Fixes for failures that are easy to miss: `lmodern` with Cyrillic, `listings` with Russian comments, bitmap fonts.
- `texlog.py`, a parser that turns a long `.log` into a short list of errors. This saves tokens and needs only Python.
- Tells the user when pdflatex is not suitable (Arabic, Hebrew, Devanagari) and proposes xelatex or lualatex, without switching silently.

## Install

```bash
claude plugin marketplace add rodioniurev/claude-latex-texstudio
```

```bash
claude plugin install latex-texstudio@rodioniurev-latex
```

The skill then loads by itself when a task involves LaTeX.

Needs a TeX distribution (MiKTeX or TeX Live) and Python 3. TeXstudio is not required.

## Tested on

MiKTeX 25.4 on Windows 11. Reports from TeX Live and other systems are welcome in Issues.

---

# Скилл LaTeX + TeXstudio для Claude Code

Скилл для работы с LaTeX через TeXstudio и pdflatex с правильной кириллицей и другими языками.

- Преамбулы проверены настоящей сборкой: русский, кириллица с латиницей, греческий, китайский.
- Решения для типичных ловушек: `lmodern` с кириллицей, `listings` с русскими комментариями, растровые шрифты.
- `texlog.py` превращает длинный `.log` в короткий список ошибок и экономит токены.
- Если pdflatex не подходит, скилл объясняет почему и предлагает xelatex или lualatex.

Установка: команды выше. Нужны MiKTeX или TeX Live и Python 3. Сам TeXstudio необязателен.

## License

MIT
