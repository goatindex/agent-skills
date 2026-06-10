# AQI Gap Letter Template v0.1

<!-- AUTHORING RULES (renderer guidance — never emitted to the requestor)

The rubric is NOT published. This letter is its only public face, so every ask
must stand alone as a complete specification. Apply these translation rules
when rendering findings into asks:

1. STANDALONE ASKS. Each ask states what to provide, in what form, covering
   what, with what provenance (dated/versioned/attributed) — sufficient for a
   requestor with no rubric access to satisfy it in one pass.
2. NEUTRAL REGISTER. Clarity/specificity findings become specification
   requests, never quality accusations. "Reads as boilerplate" renders as
   "please state which TLS version is enforced, and at which component."
3. NO SCORES. No per-dimension numerics or letters. Only the composite letter
   and the gate decision appear, once, in the summary.
4. NO RUBRIC LANGUAGE. Dimension names (completeness, conformity, etc.) and
   anchor phrasing must not appear. Group asks by document, not by dimension.
5. SUPPRESSION. Findings with requestor_ask = null are assessor-internal and
   never rendered.
6. MUST-FIX vs RECOMMENDED. must_fix=true asks block resubmission acceptance
   and are listed first. Recommended asks are clearly optional.
7. ORDERING. Within each group: severity descending, then effort ascending
   (cheap critical fixes first) — same sort as the assessor view.

Placeholders use {{double_braces}}. Conditional blocks use
<<IF condition>> ... <<END IF>>.
-->

---

**To:** {{subject.requestor}}
**From:** {{issuing_team}}
**Date:** {{run_date}}
**Re:** Security assessment intake — {{subject.title}} ({{subject.reference}})

## Outcome

<<IF gate.decision == "return">>
Your submission has been reviewed for assessment readiness and is being
**returned** before assessment. The material provided does not yet give us
enough to assess the change reliably, and proceeding now would produce an
assessment we could not stand behind. Overall readiness rating: **{{composite.letter}}**.

The specific items needed are listed below. Once the **required items** are
addressed, please resubmit and intake review will be repeated — typically
faster on a second pass.
<<END IF>>

<<IF gate.decision == "proceed_with_caveats">>
Your submission has been reviewed for assessment readiness and the assessment
will **proceed**. Overall readiness rating: **{{composite.letter}}**.

Some gaps were identified that the assessment will need to work around. These
are listed below — addressing the **required items** during the assessment
window will materially improve the confidence of the final assessment;
anything left unresolved will be recorded as a limitation in the assessment
report.
<<END IF>>

<<IF gate.decision == "proceed">>
Your submission has been reviewed for assessment readiness and the assessment
will **proceed**. Overall readiness rating: **{{composite.letter}}**.
The items below are recommendations only; none blocks the assessment.
<<END IF>>

## What we need

<!-- Repeat the block below for each document group. Groups are ordered:
     groups containing must_fix asks first, then by ask count descending. -->

### {{group.document}}

<!-- Required asks (must_fix = true), severity desc then effort asc -->
**Required before {{"resubmission" if gate.decision == "return" else "assessment completion"}}:**

- **{{ask.id}}** — {{ask.ask_text}}
  *Suggested owner: {{ask.suggested_owner}}*

<!-- Recommended asks (must_fix = false) -->
**Recommended:**

- **{{ask.id}}** — {{ask.ask_text}}
  *Suggested owner: {{ask.suggested_owner}}*

<!-- End repeat -->

## Provenance standard

All documents provided or updated in response to this letter should be
**dated, version-numbered, and attributed to an owner**, and should state
whether they describe the *current* system or the *proposed end-state*.
Undated or unattributed material may need to be re-requested, which slows
the assessment down for everyone.

## What happens next

<<IF gate.decision == "return">>
1. Address each item marked **Required** above.
2. Resubmit the full updated artefact set to {{intake_channel}}, citing
   reference {{subject.reference}} and the ask IDs addressed.
3. Intake review will be repeated; if the required items are satisfied, the
   assessment will be scheduled immediately.
<<END IF>>

<<IF gate.decision == "proceed_with_caveats">>
1. The assessment begins on {{assessment_start_date}}.
2. Items marked **Required** should be provided to the assessor by
   {{caveat_deadline}}; the assessor may contact {{subject.requestor}} or the
   suggested owners directly.
3. Any required item unresolved at assessment completion will appear in the
   report's limitations section.
<<END IF>>

<<IF gate.decision == "proceed">>
1. The assessment begins on {{assessment_start_date}}.
2. Recommended items may be provided at any point during the assessment
   window and will be incorporated if received.
<<END IF>>

Questions about any item can be directed to {{intake_contact}} citing the
ask ID.

---

<!-- WORKED EXAMPLE ASK TRANSLATIONS (authoring guidance — never emitted)

Finding (assessor view):
  dimension: completeness, severity: high, effort: medium
  action: "Obtain network diagram covering the new ingress path"
Renders as:
  "Provide a network diagram showing the new public ingress path end-to-end,
   including the load balancer, WAF placement, and the zone boundary it
   crosses into the application tier. The diagram should be dated, versioned,
   and reflect the proposed end-state."

Finding (assessor view):
  dimension: clarity (specificity sub-test), severity: medium, effort: low
  action: "Submission asserts 'industry-standard encryption' — unfalsifiable"
Renders as:
  "Please state the specific encryption applied to data in transit between
   the API gateway and the payments service: protocol and version (e.g.
   TLS 1.3), where it is terminated, and how enforcement is verified."

Finding (assessor view):
  dimension: consistency, severity: high, effort: low
  action: "Prose section 3.2 asserts encrypted replication; diagram D2 shows
   plaintext path between DB nodes"
Renders as:
  "Section 3.2 and diagram D2 describe the database replication link
   differently. Please confirm whether replication between the database nodes
   is encrypted, and update whichever artefact is out of date so both agree."

Note the third example: inconsistencies CAN name the conflicting artefacts —
that is specification, not rubric language. What it must not do is say
"this scored 1/4 on consistency."
-->
