# AQI Clarity Calibration — Specificity Protocol v0.1

Companion to `aqi-rubric-anchors-v0.1.md` §3.5 / §4.6. This replaces the adjective-based specificity anchors with a **countable, claim-level procedure**, then validates it against a graded sample set. The goal is run-to-run stability for automated scoring: an LLM asked "is this specific?" drifts; an LLM asked to extract claims, classify each against three named criteria, and apply threshold rules does not.

---

## 1. The protocol

**Step 1 — Extract claims.** List every assertion the document makes about a security property, control, or behaviour. One claim per row.

**Step 2 — Mark security relevance.** A claim is **security-relevant (SR)** if, were it false, the risk position of the assessment would change. Everything else is peripheral. Only SR claims drive the score.

**Step 3 — Classify each claim** against three criteria:

| Criterion | Test |
|---|---|
| **Mechanism** | Names a concrete control, protocol, product configuration, or version — not a control *category*. "TLS 1.3" passes; "encryption" alone does not; "AWS WAF" without ruleset/mode is category-level. |
| **Location** | Names where the control applies — component, boundary, path, or segment specific enough to point at on a diagram. |
| **Verification** | Names how enforcement is or will be confirmed — scan profile, test, policy object, automated check — or names an owner and trigger for a deferred confirmation. |

Classification:

- **S (Specific):** Mechanism + Location + Verification. Falsifiable by inspection without follow-up questions.
- **P (Partial):** Mechanism + Location, but verification absent or vague. Falsifiable only after a follow-up.
- **U (Unfalsifiable):** Fails Mechanism or Location. Cannot be checked against the system as written.

**Step 4 — Score from the SR claim distribution:**

| Score | Threshold rule |
|---|---|
| 4 | Every SR claim is S. No U claims on any material point. |
| 3 | Every SR claim is S or P; any P claim either covers a lower-stakes control or names an owner and trigger for the deferred detail. U claims peripheral only. |
| 2 | Every SR claim is at least P — mechanism and location pinned throughout — but verification paths are broadly absent. |
| 1 | One or more SR claims are U, or hedging language dominates the SR claims (see §2). |
| 0 | SR claims are predominantly U, or the document never reaches claim level — posture language with no verifiable commitment anywhere. |

Dimension score remains **min(surface_clarity, specificity)** per the rubric.

**Surface-clarity quick test** (unchanged in spirit, made operational): can each SR claim be located and restated after a single read? Structural failures (key facts only recoverable by cross-referencing three sections; undefined acronyms doing load-bearing work) drop this sub-score; prose style alone does not.

---

## 2. Hedge-signal lexicon (indicative, not determinative)

Presence of these patterns in an SR claim is a strong prompt to classify U — but classification is decided by the three criteria, not by the lexicon. A sentence containing "appropriate" can still be S if it then specifies.

- **Category-without-instance:** "industry-standard encryption", "robust firewall controls", "secure protocols", "best-practice configuration"
- **Unowned future passive:** "will be ensured", "will be implemented", "is to be considered", "shall be addressed"
- **Scope escape hatches:** "where appropriate", "as required", "where applicable", "as needed"
- **Borrowed authority without mapping:** "aligned with ISO 27001 / NIST / best practice" with no control mapping
- **Tautology:** "security requirements will be met in accordance with security requirements"
- **Posture nouns:** "defence-in-depth approach", "security-first mindset", "holistic protection" — when carrying the sentence rather than introducing specifics

---

## 3. Calibration sample set

Five passages, one scenario (public ingress to a payments API — matching the worked example fixtures), graded 4→0. Each includes its claim table. These double as few-shot exemplars for the skill.

### Sample A — Score 4

> External traffic terminates at the application load balancer `alb-pay-prod-01` in the DMZ VPC. TLS 1.3 is enforced at the listener via policy `ELBSecurityPolicy-TLS13-1-2-2021-06`; HTTP listeners are disabled. AWS WAF (ruleset `payments-waf-v7`, block mode, managed groups Core and SQLi) fronts the listener. Between the load balancer and the payments service (`pay-api`, app subnets az-a/az-b), traffic is re-encrypted at TLS 1.2+ using the internal CA; certificate rotation is automated through ACM at 90-day validity. Enforcement is verified by the weekly Qualys profile `PAY-EXT`, reporting to dashboard SEC-114.

| # | Claim | SR | Mech | Loc | Verif | Class |
|---|---|---|---|---|---|---|
| 1 | TLS 1.3 at external listener, HTTP disabled | Y | ✓ | ✓ | ✓ (via 5) | S |
| 2 | WAF block mode, named ruleset/groups | Y | ✓ | ✓ | ✓ (via 5) | S |
| 3 | Internal re-encryption TLS 1.2+, internal CA | Y | ✓ | ✓ | ✓ (via 5) | S |
| 4 | Automated cert rotation, 90-day | Y | ✓ | ✓ | ✓ | S |
| 5 | Weekly scan profile + dashboard | Y | ✓ | ✓ | ✓ | S |

All SR claims S → **4**.

### Sample B — Score 3

> External traffic terminates at the application load balancer in the DMZ, with TLS 1.3 enforced at the listener and plain HTTP disabled. A WAF in block mode fronts the load balancer using the AWS managed core rules. Traffic between the load balancer and the payments service is re-encrypted using certificates issued by the internal CA, with rotation automated. External scan coverage will be confirmed with the vulnerability management team before go-live.

| # | Claim | SR | Mech | Loc | Verif | Class |
|---|---|---|---|---|---|---|
| 1 | TLS 1.3 at listener, HTTP disabled | Y | ✓ | ✓ | ✗ | P |
| 2 | WAF block mode, managed core rules | Y | ✓ | ✓ | ✗ | P |
| 3 | Internal re-encryption, internal CA, rotation | Y | ✓ | ✓ | ✗ | P |
| 4 | Scan coverage deferred — named owner + trigger | Y | — | — | owner+trigger | P (compliant deferral) |

All SR claims S or P; deferral carries owner and trigger → **3**.

### Sample C — Score 2

> All external traffic is encrypted using TLS terminated at the load balancer, and a web application firewall is deployed in front of the payments API. Internal traffic between the load balancer and the application is also encrypted. Certificates are managed centrally.

| # | Claim | SR | Mech | Loc | Verif | Class |
|---|---|---|---|---|---|---|
| 1 | TLS at load balancer | Y | ✓ (no version) | ✓ | ✗ | P |
| 2 | WAF in front of API | Y | ✓ (no mode/rules) | ✓ | ✗ | P |
| 3 | Internal traffic encrypted | Y | ✓ (no protocol) | ✓ | ✗ | P |
| 4 | Central cert management | Y | ✓ (no system) | △ | ✗ | P |

Everything pinned to mechanism+location, nothing verifiable as written → **2**.

### Sample D — Score 1

> The solution leverages industry-standard encryption to protect data in transit, and appropriate firewall controls will be implemented in line with best practice. Security monitoring will be ensured through the organisation's existing tooling, and certificates will be managed in accordance with policy.

| # | Claim | SR | Mech | Loc | Verif | Class |
|---|---|---|---|---|---|---|
| 1 | "industry-standard encryption" in transit | Y | ✗ category | ✗ | ✗ | U |
| 2 | "appropriate firewall controls… best practice" | Y | ✗ category | ✗ | ✗ | U |
| 3 | "monitoring will be ensured… existing tooling" | Y | ✗ | ✗ | ✗ | U |
| 4 | "certificates… in accordance with policy" | Y | ✗ | ✗ | ✗ | U |

SR claims U; four hedge-lexicon hits in four sentences → **1**.

### Sample E — Score 0

> Security is a foundational pillar of this initiative and has been embedded throughout the design lifecycle. The solution adopts a defence-in-depth posture aligned with recognised frameworks, ensuring robust protection of customer data at every layer. All security requirements will be met in accordance with the organisation's security requirements, and continuous improvement will be maintained as the threat landscape evolves.

Claim extraction yields **zero claims at control level** — no control category is even named for any boundary or flow. Posture language plus one tautology → **0**.

---

## 4. Boundary notes

**3 / 2 boundary — verification.** Both have mechanism+location on every SR claim. A 3 either includes verification on the highest-stakes claims or formally defers it (owner + trigger). A 2 has no verification story anywhere. The discriminating question: *could the assessor check any of this without first asking who would know?*

**2 / 1 boundary — commitment.** A 2 commits to a checkable mechanism at a place, even if shallow ("TLS at the load balancer"). A 1 retreats to categories and unowned futures. The discriminating question: *if this claim were false, could anyone be shown to be wrong?* For a 2, yes; for a 1, no — the hedge absorbs the falsehood.

**1 / 0 boundary — claim level.** A 1 still names real control categories (encryption, firewall, monitoring, certificates) attached, however loosely, to this system. A 0 never descends from posture to controls. Both are slop; a 1 is slop *about* the system, a 0 is slop about nothing.

**Brevity is not slop.** A terse T1 change record with three claims, all S, scores 4. Expected claim *count* is tier-relative (per the tier table); specificity is judged per claim, never by volume. Conversely, **jargon density is not specificity** — naming a product is not naming its configuration (Sample C's "web application firewall" vs Sample A's ruleset/mode).

**Pointers count as S only if the target is in the artefact register.** "Encryption per HLD §4.2" is S when the HLD is registered, dated, and current — which couples specificity to Completeness and Currency rather than letting references launder hedges.

---

## 5. Drop-in anchor replacement for rubric §3.5 / §4.6 (sub-test B)

| Score | Anchor (operational) |
|---|---|
| 4 | Claim audit: every SR claim classifies S; no material U claims. |
| 3 | Every SR claim S or P; P claims are lower-stakes or carry a named owner and trigger; U claims peripheral only. |
| 2 | Every SR claim at least P (mechanism + location pinned); verification paths absent. |
| 1 | One or more SR claims U, or hedge patterns dominate the SR claims. |
| 0 | SR claims predominantly U, or no claim reaches control level at all. |

---

## 6. Validation status — read before relying on this

The sample set above was authored to *exhibit* the anchor boundaries, so it tests **discriminability** (do the rules cleanly separate adjacent grades?) — which it passes — but not **field validity**. Self-authored calibration sets always pass their own protocol; the test that matters is a blind run against real submissions, including at least one known-slop document and one terse-but-good T1 change record. Until that run, treat scores at the 3/2 and 2/1 boundaries as provisional and route them to human review. Recommended validation: score 5–10 real artefacts twice in independent runs; if any dimension score differs by ≥2 between runs, the relevant anchor needs tightening before the skill ships.
