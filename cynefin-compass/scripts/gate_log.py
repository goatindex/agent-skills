#!/usr/bin/env python3
"""Log and summarise Cynefin Compass runs. Standard library only.

Each run adds one JSON line. The summary shows how often the gate skips the
framework, how the domains are spread, and how often assessments fail the
validator. Use it to tune the skill description and the gate.

Usage:
  python3 gate_log.py append <assessment.json> [--log PATH]
  python3 gate_log.py summary [--log PATH]
Log path: --log, else env CYNEFIN_COMPASS_LOG, else ./cynefin-compass-log.jsonl
Exit: 0 = ok, 2 = usage/IO error. (append logs invalid assessments too.)
"""

import collections
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_assessment import validate  # noqa: E402

DEFAULT_LOG = "cynefin-compass-log.jsonl"


def log_path(args):
    if "--log" in args:
        i = args.index("--log")
        if i + 1 >= len(args):
            return None, args
        path = args[i + 1]
        return path, args[:i] + args[i + 2:]
    return os.environ.get("CYNEFIN_COMPASS_LOG", DEFAULT_LOG), args


def make_record(doc):
    f = validate(doc)
    gate = doc.get("gate") if isinstance(doc, dict) else None
    pieces = doc.get("pieces") if isinstance(doc, dict) else None
    return {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "mode": doc.get("mode") if isinstance(doc, dict) else None,
        "changes_approach": gate.get("changes_approach") if isinstance(gate, dict) else None,
        "domains": [
            p.get("domain") for p in pieces if isinstance(p, dict)
        ] if isinstance(pieces, list) else [],
        "valid": f.ok,
        "fail_count": len(f.fails),
        "warn_count": len(f.warns),
    }


def summarise(records):
    total = len(records)
    if not total:
        return "No runs logged."
    skipped = sum(1 for r in records if r.get("changes_approach") is False)
    invalid = sum(1 for r in records if not r.get("valid"))
    domains = collections.Counter(d for r in records for d in r.get("domains", []))
    multi = sum(1 for r in records if len(r.get("domains", [])) > 1)
    lines = [
        f"runs: {total}",
        f"gate skipped: {skipped} ({100 * skipped // total}%)",
        f"decomposed (2+ pieces): {multi}",
        f"failed validation: {invalid} ({100 * invalid // total}%)",
        "domains: " + (", ".join(f"{d}={n}" for d, n in sorted(domains.items())) or "none"),
    ]
    return "\n".join(lines)


def main(argv):
    path, args = log_path(argv[1:])
    if path is None or not args:
        print(__doc__, file=sys.stderr)
        return 2
    cmd = args[0]
    if cmd == "append" and len(args) == 2:
        try:
            with open(args[1], encoding="utf-8") as fh:
                doc = json.load(fh)
        except (OSError, ValueError) as exc:
            print(f"cannot read {args[1]}: {exc}", file=sys.stderr)
            return 2
        rec = make_record(doc)
        try:
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec) + "\n")
        except OSError as exc:
            print(f"cannot write {path}: {exc}", file=sys.stderr)
            return 2
        print(f"logged to {path}")
        return 0
    if cmd == "summary" and len(args) == 1:
        records = []
        try:
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    if line.strip():
                        records.append(json.loads(line))
        except FileNotFoundError:
            pass
        except (OSError, ValueError) as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        print(summarise(records))
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
