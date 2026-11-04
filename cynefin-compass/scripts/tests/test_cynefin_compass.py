#!/usr/bin/env python3
"""Regression tests for cynefin-compass. Standard library only.

Run: python3 scripts/tests/test_cynefin_compass.py
Exit: 0 = all tests pass, 1 = failures.

The good examples are the shipped examples/*.json, so examples and tools are
tested against each other. Failure cases are built by changing a copy of a good
example in memory.
"""

import copy
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(os.path.dirname(HERE))
SCRIPTS = os.path.join(SKILL, "scripts")
sys.path.insert(0, SCRIPTS)

import gate_log  # noqa: E402
import lint_report  # noqa: E402
import render_report  # noqa: E402
import validate_assessment as va  # noqa: E402


def load(name):
    with open(os.path.join(SKILL, "examples", name), encoding="utf-8") as fh:
        return json.load(fh)


def run(script, *args):
    return subprocess.run(
        [sys.executable, os.path.join(SCRIPTS, script), *args],
        capture_output=True, text=True,
    )


def fails_of(doc):
    return va.validate(doc).fails


def has(fails, needle):
    return any(needle in line for line in fails)


class GoodExamples(unittest.TestCase):
    def test_every_example_validates(self):
        for path in sorted(glob.glob(os.path.join(SKILL, "examples", "*.json"))):
            with self.subTest(example=os.path.basename(path)):
                r = run("validate_assessment.py", path)
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_examples_have_no_warnings(self):
        for path in sorted(glob.glob(os.path.join(SKILL, "examples", "*.json"))):
            with self.subTest(example=os.path.basename(path)):
                with open(path, encoding="utf-8") as fh:
                    self.assertEqual(va.validate(json.load(fh)).warns, [])

    def test_all_four_domains_are_covered_by_examples(self):
        seen = set()
        for path in glob.glob(os.path.join(SKILL, "examples", "*.json")):
            with open(path, encoding="utf-8") as fh:
                seen |= {p["domain"] for p in json.load(fh)["pieces"]}
        self.assertEqual(seen, set(va.DOMAINS))

    def test_render_then_lint_passes(self):
        for path in sorted(glob.glob(os.path.join(SKILL, "examples", "*.json"))):
            with self.subTest(example=os.path.basename(path)):
                with open(path, encoding="utf-8") as fh:
                    text = render_report.render(json.load(fh))
                self.assertEqual(lint_report.lint(text), [])

    def test_json_flag(self):
        path = os.path.join(SKILL, "examples", "activation-drop.json")
        r = run("validate_assessment.py", "--json", path)
        out = json.loads(r.stdout)
        self.assertTrue(out["ok"])
        self.assertEqual(out["fails"], [])


class Classification(unittest.TestCase):
    def test_eval_classification_cases(self):
        with open(os.path.join(SKILL, "evals", "evals.json"), encoding="utf-8") as fh:
            cases = json.load(fh)["classification_cases"]
        self.assertGreaterEqual(len(cases), 8)
        for c in cases:
            with self.subTest(case=c["id"]):
                self.assertEqual(va.classify_from_answers(c["answers"]), c["expected_domain"])

    def test_malformed_answers(self):
        self.assertIsNone(va.classify_from_answers({"active_crisis": True}))
        self.assertIsNone(va.classify_from_answers(None))

    def test_domain_disagreeing_with_answers_fails(self):
        doc = load("activation-drop.json")
        doc["pieces"][1]["procedure_answers"]["hindsight_only"] = False
        doc["pieces"][1]["procedure_answers"]["expert_can_determine_before_acting"] = True
        self.assertTrue(has(fails_of(doc), "procedure answers give 'complicated'"))

    def test_override_reason_accepts_disagreement(self):
        doc = load("activation-drop.json")
        piece = doc["pieces"][1]
        piece["procedure_answers"]["hindsight_only"] = False
        piece["procedure_answers"]["expert_can_determine_before_acting"] = True
        piece["override_reason"] = "Two senior experts disagree about the cause so far."
        self.assertEqual(fails_of(doc), [])

    def test_all_no_answers_means_confused_and_fails(self):
        doc = load("activation-drop.json")
        for k in va.PROCEDURE_KEYS:
            doc["pieces"][0]["procedure_answers"][k] = False
        self.assertTrue(has(fails_of(doc), "Confused"))

    def test_confused_domain_is_rejected(self):
        doc = load("activation-drop.json")
        doc["pieces"][0]["domain"] = "confused"
        self.assertTrue(has(fails_of(doc), "decompose"))


class GateRules(unittest.TestCase):
    def test_skip_with_pieces_fails(self):
        doc = load("gate-skip.json")
        doc["pieces"] = load("outage-chaotic.json")["pieces"]
        self.assertTrue(has(fails_of(doc), "pieces must be empty"))

    def test_apply_without_pieces_fails(self):
        doc = load("outage-chaotic.json")
        doc["pieces"] = []
        self.assertTrue(has(fails_of(doc), "At least one piece"))

    def test_single_problem_flag_must_match(self):
        doc = load("activation-drop.json")
        doc["is_single_problem"] = True
        self.assertTrue(has(fails_of(doc), "is_single_problem"))
        doc = load("outage-chaotic.json")
        doc["is_single_problem"] = False
        self.assertTrue(has(fails_of(doc), "At least 2 pieces"))

    def test_duplicate_piece_ids_fail(self):
        doc = load("activation-drop.json")
        doc["pieces"][1]["id"] = doc["pieces"][0]["id"]
        self.assertTrue(has(fails_of(doc), "duplicate id"))

    def test_gate_reason_required(self):
        doc = load("gate-skip.json")
        doc["gate"]["reason"] = ""
        self.assertTrue(has(fails_of(doc), "gate.reason"))

    def test_skip_report_renders_and_lints(self):
        text = render_report.render(load("gate-skip.json"))
        self.assertTrue(text.startswith("# Cynefin gate:"))
        self.assertEqual(lint_report.lint(text), [])


class ComplexRules(unittest.TestCase):
    def setUp(self):
        self.doc = load("activation-drop.json")
        self.piece = self.doc["pieces"][1]

    def test_no_probes_fails(self):
        self.piece["approach"]["probes"] = []
        self.assertTrue(has(fails_of(self.doc), "1-3 safe-to-fail probes"))

    def test_four_probes_fail_as_a_plan(self):
        probe = self.piece["approach"]["probes"][0]
        self.piece["approach"]["probes"] = [copy.deepcopy(probe) for _ in range(4)]
        self.assertTrue(has(fails_of(self.doc), "is a plan"))

    def test_irreversible_probe_fails(self):
        self.piece["approach"]["probes"][0]["safe_to_fail"]["reversible"] = False
        self.assertTrue(has(fails_of(self.doc), "not safe to fail"))

    def test_missing_signal_fails(self):
        del self.piece["approach"]["probes"][1]["signal"]
        self.assertTrue(has(fails_of(self.doc), "probes[1].signal"))

    def test_missing_amplify_dampen_fail(self):
        del self.piece["approach"]["probes"][0]["amplify_if"]
        del self.piece["approach"]["probes"][0]["dampen_if"]
        f = fails_of(self.doc)
        self.assertTrue(has(f, "amplify_if") and has(f, "dampen_if"))

    def test_phased_plan_wording_fails(self):
        for text in ("Phase 1: design the new flow.", "Build a roadmap for Q3.", "Draft the comprehensive plan."):
            with self.subTest(text=text):
                doc = load("activation-drop.json")
                doc["pieces"][1]["approach"]["summary"] = text
                self.assertTrue(has(fails_of(doc), "Complex-as-Complicated"))

    def test_wrong_sequence_fails(self):
        self.piece["approach"]["sequence"] = "sense-analyse-respond"
        self.assertTrue(has(fails_of(self.doc), "probe-sense-respond"))


class OtherDomainRules(unittest.TestCase):
    def test_chaotic_needs_single_text_action(self):
        doc = load("outage-chaotic.json")
        doc["pieces"][0]["approach"]["stabilising_action"] = ["Roll back", "Page on-call"]
        self.assertTrue(has(fails_of(doc), "ONE action"))

    def test_chaotic_needs_sense_after(self):
        doc = load("outage-chaotic.json")
        del doc["pieces"][0]["approach"]["sense_after"]
        self.assertTrue(has(fails_of(doc), "sense_after"))

    def test_clear_needs_boundary_risk(self):
        doc = load("certificate-renewal-clear.json")
        doc["pieces"][0]["boundary_risk"] = None
        self.assertTrue(has(fails_of(doc), "complacency"))

    def test_clear_rejects_probes(self):
        doc = load("certificate-renewal-clear.json")
        doc["pieces"][0]["approach"]["probes"] = load("activation-drop.json")["pieces"][1]["approach"]["probes"]
        self.assertTrue(has(fails_of(doc), "Do not add probes"))

    def test_complicated_needs_experts_and_analysis(self):
        doc = load("activation-drop.json")
        del doc["pieces"][0]["approach"]["experts"]
        del doc["pieces"][0]["approach"]["analysis_needed"]
        f = fails_of(doc)
        self.assertTrue(has(f, "experts") and has(f, "analysis_needed"))


class EvidenceAndReadings(unittest.TestCase):
    def test_generic_evidence_fails(self):
        for label in ("It is complex.", "Many stakeholders", "high stakes"):
            with self.subTest(label=label):
                doc = load("activation-drop.json")
                doc["pieces"][1]["evidence"] = [label]
                self.assertTrue(has(fails_of(doc), "generic label"))

    def test_short_evidence_warns(self):
        doc = load("activation-drop.json")
        doc["pieces"][1]["evidence"] = ["Users leave early."]
        f = va.validate(doc)
        self.assertTrue(f.ok)
        self.assertTrue(has(f.warns, "under 6 words"))

    def test_empty_evidence_fails(self):
        doc = load("activation-drop.json")
        doc["pieces"][0]["evidence"] = []
        self.assertTrue(has(fails_of(doc), "evidence"))

    def test_second_reading_must_differ(self):
        doc = load("activation-drop.json")
        doc["pieces"][0]["second_reading"]["domain"] = "complicated"
        self.assertTrue(has(fails_of(doc), "must differ"))

    def test_tipping_condition_required(self):
        doc = load("activation-drop.json")
        doc["pieces"][0]["second_reading"]["tipping_condition"] = "later"
        self.assertTrue(has(fails_of(doc), "tipping_condition"))

    def test_reclassify_triggers_required(self):
        doc = load("activation-drop.json")
        doc["pieces"][0]["reclassify_triggers"] = []
        self.assertTrue(has(fails_of(doc), "reclassify_triggers"))

    def test_schema_version_and_mode(self):
        doc = load("outage-chaotic.json")
        doc["schema_version"] = "2"
        doc["mode"] = "huge"
        f = fails_of(doc)
        self.assertTrue(has(f, "schema_version") and has(f, "mode"))

    def test_non_object_input(self):
        self.assertTrue(has(fails_of([]), "JSON object"))


class Cli(unittest.TestCase):
    def test_validator_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = os.path.join(tmp, "bad.json")
            with open(bad, "w", encoding="utf-8") as fh:
                json.dump({"schema_version": "1"}, fh)
            self.assertEqual(run("validate_assessment.py", bad).returncode, 1)
            self.assertEqual(run("validate_assessment.py", os.path.join(tmp, "none.json")).returncode, 2)
            self.assertEqual(run("validate_assessment.py").returncode, 2)

    def test_render_refuses_invalid_input(self):
        doc = load("activation-drop.json")
        doc["pieces"][1]["approach"]["probes"] = []
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "a.json")
            out = os.path.join(tmp, "r.md")
            with open(src, "w", encoding="utf-8") as fh:
                json.dump(doc, fh)
            r = run("render_report.py", src, "-o", out)
            self.assertEqual(r.returncode, 1)
            self.assertFalse(os.path.exists(out))

    def test_render_cli_writes_file_and_lint_cli_passes(self):
        src = os.path.join(SKILL, "examples", "outage-chaotic.json")
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "r.md")
            self.assertEqual(run("render_report.py", src, "-o", out).returncode, 0)
            self.assertEqual(run("lint_report.py", out).returncode, 0)


class ReportLint(unittest.TestCase):
    def good(self):
        return render_report.render(load("activation-drop.json"))

    def test_missing_heading_fails(self):
        text = self.good().replace("## 5. What would change the diagnosis", "## Five")
        self.assertTrue(has(lint_report.lint(text), "missing heading"))

    def test_probe_without_signal_fails(self):
        text = re.sub(r"\n  - Signal: [^\n]*", "", self.good())
        self.assertTrue(has(lint_report.lint(text), "'Signal:'"))

    def test_bad_domain_fails(self):
        text = self.good().replace("**Primary domain:** Complex", "**Primary domain:** Tricky")
        self.assertTrue(has(lint_report.lint(text), "Primary domain must be"))

    def test_piece_mismatch_fails(self):
        text = self.good().replace("### Piece behaviour: Why real users do not activate (", "### Piece other: Why real users do not activate (")
        self.assertTrue(has(lint_report.lint(text), "differ"))

    def test_too_many_probes_fail(self):
        extra = "- **Probe 4:** more\n  - Signal: s\n  - Amplify if: a\n  - Dampen if: d\n  - Time box: t\n  - Safe to fail: x\n"
        text = self.good().replace("## 5.", extra * 2 + "\n## 5.")
        self.assertTrue(has(lint_report.lint(text), "1-3 probes"))

    def test_wrong_title_fails(self):
        text = self.good().replace("# Cynefin assessment:", "# Report:", 1)
        self.assertTrue(has(lint_report.lint(text), "line 1"))


class GateLog(unittest.TestCase):
    def test_append_and_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = os.path.join(tmp, "log.jsonl")
            for name in ("activation-drop.json", "gate-skip.json", "outage-chaotic.json"):
                src = os.path.join(SKILL, "examples", name)
                self.assertEqual(run("gate_log.py", "append", src, "--log", log).returncode, 0)
            bad = os.path.join(tmp, "bad.json")
            with open(bad, "w", encoding="utf-8") as fh:
                json.dump({"schema_version": "1"}, fh)
            self.assertEqual(run("gate_log.py", "append", bad, "--log", log).returncode, 0)
            with open(log, encoding="utf-8") as fh:
                records = [json.loads(l) for l in fh]
            self.assertEqual(len(records), 4)
            r = run("gate_log.py", "summary", "--log", log)
            self.assertEqual(r.returncode, 0)
            self.assertIn("runs: 4", r.stdout)
            self.assertIn("gate skipped: 1", r.stdout)
            self.assertIn("failed validation: 1", r.stdout)
            self.assertIn("complex=1", r.stdout)

    def test_summary_of_missing_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = run("gate_log.py", "summary", "--log", os.path.join(tmp, "none.jsonl"))
            self.assertEqual(r.returncode, 0)
            self.assertIn("No runs logged", r.stdout)

    def test_usage_error(self):
        self.assertEqual(run("gate_log.py").returncode, 2)
        self.assertEqual(run("gate_log.py", "bogus").returncode, 2)

    def test_make_record_handles_garbage(self):
        rec = gate_log.make_record([])
        self.assertFalse(rec["valid"])
        self.assertEqual(rec["domains"], [])


class SkillPackage(unittest.TestCase):
    """The skill checks itself: frontmatter, referenced files, eval shape."""

    def skill_md(self):
        with open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8") as fh:
            return fh.read()

    def test_frontmatter(self):
        m = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n", self.skill_md())
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), os.path.basename(SKILL))
        self.assertLessEqual(len(m.group(2)), 1024)

    def test_every_referenced_path_exists(self):
        paths = set(re.findall(r"`((?:scripts|references|examples|evals)/[A-Za-z0-9_./*-]*)`", self.skill_md()))
        self.assertTrue(paths)
        for p in paths:
            with self.subTest(path=p):
                self.assertTrue(glob.glob(os.path.join(SKILL, p.rstrip("/"))) or os.path.exists(os.path.join(SKILL, p)), p)

    def test_every_script_is_named_in_skill_md(self):
        text = self.skill_md()
        for path in glob.glob(os.path.join(SCRIPTS, "*.py")):
            with self.subTest(script=os.path.basename(path)):
                self.assertIn(os.path.basename(path), text)

    def test_schema_is_valid_json_with_expected_domains(self):
        with open(os.path.join(SKILL, "references", "assessment-schema.json"), encoding="utf-8") as fh:
            schema = json.load(fh)
        self.assertEqual(set(schema["$defs"]["domain"]["enum"]), set(va.DOMAINS))
        self.assertEqual(
            set(schema["$defs"]["approach"]["properties"]["sequence"]["enum"]),
            set(va.SEQUENCE.values()),
        )
        self.assertEqual(
            set(schema["$defs"]["piece"]["properties"]["procedure_answers"]["required"]),
            set(va.PROCEDURE_KEYS),
        )

    def test_gate_cases_shape(self):
        with open(os.path.join(SKILL, "evals", "evals.json"), encoding="utf-8") as fh:
            cases = json.load(fh)["gate_cases"]
        ids = [c["id"] for c in cases]
        self.assertEqual(len(ids), len(set(ids)))
        yes = [c for c in cases if c["expect_changes_approach"]]
        no = [c for c in cases if not c["expect_changes_approach"]]
        self.assertGreaterEqual(len(yes), 10)
        self.assertGreaterEqual(len(no), 10)
        for c in cases:
            self.assertTrue(c["prompt"].strip())


if __name__ == "__main__":
    unittest.main(verbosity=1)
