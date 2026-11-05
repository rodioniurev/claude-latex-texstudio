#!/usr/bin/env python3
"""Print a compact summary of a LaTeX .log file. Standard library only.

Usage: python texlog.py main.log [--boxes] [--max N]
Exit code: 0 if the log has no errors, 1 if it has, 2 if it cannot be read.
"""
import argparse
import re
import sys

WRAP = 79  # TeX wraps log lines at this many bytes
STATS_MARKER = "Here is how much of TeX's memory"  # only statistics follow

FILE_LINE_ERROR = re.compile(r"^(.+?\.[A-Za-z]\w*):(\d+): (.*)$")
TEX_ERROR = re.compile(r"^! (.*)$")
CONTEXT = re.compile(r"^l\.(\d+) ?(.*)$")
WARNING = re.compile(r"^(?:LaTeX|(?:Package|Class) \S+) (?:Font )?Warning: (.*)$")
INPUT_LINE = re.compile(r"\s+on input line (\d+)\.?$")
UNDEF_REF = re.compile(r"^Reference [`'](.+?)' on page \d+ undefined")
UNDEF_CITE = re.compile(r"^Citation [`'](.+?)' on page \d+ undefined")
MISSING_CHAR = re.compile(r"^Missing character: There is no (.+?) in font (.+?)!")
BOX = re.compile(r"^(Overfull|Underfull) \\[hv]box .*?(?:at lines? (\d+)(?:--(\d+))?)?$")
RERUN = re.compile(r"Rerun to get|Label\(s\) may have changed|Please \(?re\)?run|Please rerun")


def decode(raw):
    """Decode log bytes, including the ^^xx escapes TeX may write for 8-bit bytes."""
    raw = re.sub(rb"\^\^([0-9a-f]{2})", lambda m: bytes([int(m.group(1), 16)]), raw)
    return raw.decode("utf-8", errors="replace")


def unwrap(text):
    """Join lines TeX broke at the wrap limit."""
    joined, buffer = [], ""
    for line in text.splitlines():
        buffer += line
        if len(line.encode("utf-8", errors="replace")) >= WRAP:
            continue
        joined.append(buffer)
        buffer = ""
    if buffer:
        joined.append(buffer)
    return joined


def parse(lines):
    result = {"errors": [], "warnings": [], "refs": [], "cites": [],
              "missing": [], "boxes": [], "rerun": False}
    for i, line in enumerate(lines):
        if line.startswith(STATS_MARKER):
            break
        match = FILE_LINE_ERROR.match(line)
        tex_error = TEX_ERROR.match(line)
        if (match and not line.startswith("(")) or tex_error:
            file_name, number, message = (match.groups() if match
                                          else (None, None, tex_error.group(1)))
            source = ""
            for following in lines[i + 1:i + 15]:
                context = CONTEXT.match(following)
                if context:
                    number = number or context.group(1)
                    source = context.group(2).strip()
                    break
            result["errors"].append((file_name, number, message, source))
            continue
        match = WARNING.match(line)
        if match:
            message = match.group(1).strip()
            ref, cite = UNDEF_REF.match(message), UNDEF_CITE.match(message)
            if ref:
                result["refs"].append(ref.group(1))
            elif cite:
                result["cites"].append(cite.group(1))
            elif RERUN.search(message):
                result["rerun"] = True
            else:
                number = INPUT_LINE.search(message)
                message = INPUT_LINE.sub("", message)
                result["warnings"].append((number.group(1) if number else None, message))
            continue
        match = MISSING_CHAR.match(line)
        if match:
            result["missing"].append("%s (%s)" % match.groups())
            continue
        match = BOX.match(line)
        if match:
            result["boxes"].append((match.group(1), match.group(2)))
            continue
        if RERUN.search(line):
            result["rerun"] = True
    return result


def unique(items):
    return list(dict.fromkeys(items))


def report(result, show_boxes, limit):
    errors = unique(result["errors"])
    warnings = unique(result["warnings"])
    print("errors: %d, warnings: %d, overfull/underfull boxes: %d"
          % (len(errors), len(warnings), len(result["boxes"])))
    for file_name, number, message, source in errors[:limit]:
        place = ":".join(part for part in (file_name, number) if part) or "?"
        print("ERROR %s: %s" % (place, message))
        if source:
            print("  > %s" % source)
    if len(errors) > limit:
        print("... and %d more errors" % (len(errors) - limit))
    if result["refs"]:
        print("undefined references: " + ", ".join(unique(result["refs"])))
    if result["cites"]:
        print("undefined citations: " + ", ".join(unique(result["cites"])))
    if result["missing"]:
        print("missing glyphs: " + ", ".join(unique(result["missing"])[:limit]))
    for number, message in warnings[:limit]:
        print("warning%s: %s" % (" line " + number if number else "", message))
    if len(warnings) > limit:
        print("... and %d more warnings" % (len(warnings) - limit))
    if show_boxes:
        for kind, number in unique(result["boxes"])[:limit]:
            print("%s box%s" % (kind, " at line " + number if number else ""))
    if result["rerun"]:
        print("rerun needed")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("log")
    parser.add_argument("--boxes", action="store_true", help="list overfull/underfull boxes")
    parser.add_argument("--max", type=int, default=20, help="items per section")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        with open(args.log, "rb") as log:
            raw = log.read()
    except OSError as error:
        print("cannot read log: %s" % error, file=sys.stderr)
        return 2
    result = parse(unwrap(decode(raw)))
    report(result, args.boxes, args.max)
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
