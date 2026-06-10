# AQI Assessor Report Template

<!-- Renderer guidance: this is the FULL-DISCLOSURE view. Everything renders:
     numerics, letters, evidence, caps, coupling, gate reasoning. Populate
     exclusively from the aggregated findings JSON — never restate scores from
     memory. {{double_braces}} = placeholders. -->

# AQI {{mode == "inputs" ? "Intake Review" : "Assessment Review"}} — {{subject.title}}

**Reference:** {{subject.reference}} · **Date:** {{subject.date}} · **Mode:** {{mode}}
**Complexity tier:** {{complexity.tier}}<<IF effort_tier != tier>> · **effort tier {{complexity.effort_tier}}** (conformity uplift — drives review depth, not severity)<<END IF>> — set by {{complexity.max_driver}}

## Verdict

| | |
|---|---|
| **Composite** | **{{composite.value}} ({{composite.letter}})** — raw mean {{composite.raw_weighted_mean}}, capped at {{composite.cap}}<<IF coupling>>; coupling cap {{coupling.cap}}<<END IF>> |
| **Gate** | **{{gate.decision}}** — {{gate.reasons, joined}} |
<<IF mode == "outputs">>| **Coupling** | input run {{coupling.input_run_ref}} (composite {{coupling.input_composite}}); independent discovery {{coupling.independent_discovery_evidenced ? "evidenced: " + refs : "not evidenced"}}<<IF coupling.breach>>; **BREACH — pre-cap mean exceeds what the inputs support**<<END IF>> |
| **Patternability** | {{patternability.flag}}<<IF pattern_ref>> — {{pattern_ref}}<<END IF>><<IF flag == "pattern_candidate">> — conditions: {{applicability_conditions}}<<END IF>> |<<END IF>>

## Dimension scores

| Dimension | Score | Letter | Gating | Evidence | Rationale |
|---|---|---|---|---|---|
| {{dim.id}} | {{dim.score}}{{dim.unscorable ? " (unscorable→0)" : ""}} | {{dim.letter}} | {{dim.gating ? "●" : ""}} | {{dim.evidence as artefact_id:location list}} | {{dim.rationale}} |

<!-- Clarity row additionally shows sub-scores: "surface {{a}} / specificity {{b}} → min" -->
<!-- Conformity row is annotated "neutral — excluded from composite; scrutiny signal only" -->

## Findings (prioritised — severity desc, effort asc)

| ID | Sev{{any tier_uplifted ? " (uplifted)" : ""}} | Effort | Dimension | Action | Evidence |
|---|---|---|---|---|---|
| {{f.finding_id}} | {{f.severity}}{{f.tier_uplifted ? "↑" : ""}} | {{f.effort}} | {{f.dimension}} | {{f.action}} | {{f.evidence_ref}} |

<<IF mode == "inputs" && gate.decision != "proceed">>
## Carried caveats
{{gate.caveats as list — these MUST appear in the eventual assessment's limitations section}}

## Requestor communication
Gap letter rendered separately per `gap-letter-template.md`. Confirm before sending: no dimension names, no numerics, every ask standalone.
<<END IF>>

<<IF mode == "outputs">>
## Limitations check
Input-gate caveats carried into the assessment's limitations section: {{verified yes/no, list any missing — a missing caveat is a consistency finding}}
<<END IF>>

## Run record
Aggregated by {{"scripts/aggregate.py" or "manual arithmetic (working shown below)"}} · schema {{aqi_version}} · artefact register: {{subject.artefacts as id/name/version/date table}}
