from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
PORTAL = ROOT / "submission" / "AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md"
STRATEGY = ROOT / "submission" / "TARGET_JOURNAL_STRATEGY.md"
CHECKLIST = ROOT / "submission" / "SUBMISSION_CHECKLIST.md"
AUDIT = ROOT / "docs" / "FINAL_SUBMISSION_AUDIT.md"
COVER = ROOT / "submission" / "COVER_LETTER_ECOLOGY_CONCEPTS_SYNTHESIS.md"
FIT = ROOT / "submission" / "ECOLOGY_CONCEPTS_SYNTHESIS_FIT_AUDIT.md"
TEST = ROOT / "tests" / "test_ecology_concepts_synthesis_fit.py"
WORKFLOW = ROOT / ".github" / "workflows" / "_apply-ecology-cs-upgrade-tmp.yml"
SELF = Path(__file__)


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    i = text.index(start)
    j = text.index(end, i)
    return text[:i] + replacement.rstrip() + "\n\n" + text[j:]


abstract = r"""## Abstract

A recurring challenge in ecology is to extract general structure from interactions whose net effects vary among contexts. Flowers provide a tractable case because attraction can recruit mutualists and antagonists, while defence can reduce antagonist damage yet interfere with pollination or impose joint costs. We ask first not where attraction and defence are complementary, but where complementarity is impossible. After an explicit orientation gate, the local mixed fitness effect is organized as antagonist relief minus pollinator interference minus direct joint-cost curvature, \(W_{AD}=\rho-\iota-\kappa\). The decomposition is bookkeeping, but it yields a one-sided bound: when joint-cost curvature is non-negative, complementarity can occur only where antagonist relief exceeds pollinator interference. We prove this algebraically and use 2,592 evaluations across four response-shape variants to verify implementation and quantify looseness: about 23% of points inside this selectivity window remain substitutable. Theory then defines the evidence classes for a mechanism-first synthesis of 56 route-level records from 25 independent biological study clusters. Floral larceny reduces female fitness on average (log response ratio -0.210; 48 clusters), yet only 35/48 effects are negative, the 95% prediction interval spans -1.13 to +0.71, and declared moderators explain only 0-8% of heterogeneity. Constituent mechanisms and switching architectures therefore recur, but their realized balance is strongly context dependent. Direct \(A\times D\) evidence remains sparse and direct joint-cost curvature unmeasured. The study shows how mechanism-first synthesis can replace a search for universal mean effects with testable boundaries on what ecological interactions can do."""

intro_11 = r"""### 1.1 Ecological problem

A recurring problem in ecology is that net interaction outcomes can conceal opposing causal channels. The same trait can improve performance through one interaction partner while reducing it through another, so context-dependent net signs do not by themselves reveal a general mechanism. Flowers provide a tractable case because they interact simultaneously with organisms that increase reproduction and organisms that diminish it. Signals, rewards, and floral structures recruit pollinators, but the same flowers are exposed to florivores, nectar robbers, pathogens, and other exploiters. A trait that changes attraction or access can therefore alter several ecological pathways at once.

This creates two plausible but opposing expectations. Greater attraction can increase the reproductive value that defence protects, favouring complementarity. Yet defence can also obstruct legitimate visitors or add joint construction costs, making the same trait combination substitutable. The central problem is therefore not whether attraction and defence are universally synergistic or universally traded off, but **what determines the local sign of their interaction**."""

man = MAN.read_text(encoding="utf-8")

front_marker = "**ORCID(s):** [Insert available 16-digit ORCID identifiers after author approval.]\n\n## Abstract"
front_replacement = "**ORCID(s):** [Insert available 16-digit ORCID identifiers after author approval.]\n\n**Open Research statement:** Analysis code, source-adjudication products, and generated readouts are maintained in the public project repository. The exact immutable release, repository licence, and archival DOI for the submitted version are author-controlled release fields and will be inserted before submission.\n\n## Abstract"
if "**Open Research statement:**" not in man:
    if front_marker not in man:
        raise RuntimeError("front-matter marker not found")
    man = man.replace(front_marker, front_replacement, 1)

man = replace_between(man, "## Abstract", "**Keywords:**", abstract)
man = replace_between(man, "### 1.1 Ecological problem", "### 1.2 Existing theories", intro_11)

mechanism_pattern_anchor = (
    "The logic is therefore **Mechanism \\(\\rightarrow\\) Pattern**, not theory \\(\\rightarrow\\) validation. Part I first defines the mechanism classes and derives the structural constraint; those theory-defined classes then determine what counts as relevant evidence in Part II. The empirical synthesis therefore does not search for a pattern and infer a mechanism afterward. It asks whether the already-defined constituent routes, same-system combinations, switching architectures, and identification gaps recur independently across biological systems, while keeping direct estimation of the full mixed partial separate."
)
mechanism_pattern_add = mechanism_pattern_anchor + (
    "\n\nThis ordering is also the paper's broader contribution to ecological synthesis. When heterogeneous studies cannot estimate one common focal interaction, theory can first define exclusion conditions and evidence classes, after which synthesis can ask which components recur without promoting them to the full interaction. What is intended to generalize is this inference sequence, not the specific floral inequality: any application to another ecological system would require re-deriving its causal channels, orientations, and sign premises."
)
if mechanism_pattern_anchor not in man:
    raise RuntimeError("Mechanism→Pattern anchor not found")
man = man.replace(mechanism_pattern_anchor, mechanism_pattern_add, 1)

selectivity_anchor = (
    "Part I gives the recurrent route-separation Pattern a precise role. Under non-negative joint-cost curvature, antagonist relief must exceed pollinator interference before complementarity is possible. Spatial, temporal, chemical, and attack-mode separation can therefore move a system into a permissive selectivity window, but they cannot by themselves determine the sign of \\(W_{AD}\\). The failed converse is essential: recurrent discrimination mechanisms identify where complementarity is allowed, not where it must occur."
)
selectivity_add = selectivity_anchor + (
    "\n\nBiologically, the selectivity window is best read as a discrimination condition rather than as a label attached to a defence trait. Guarded defence, consumer-specific barriers, attack-mode filtering, and visitor routing can generate empirical states consistent with large antagonist relief relative to pollinator interference. These studies do not directly estimate \\(\\rho-\\iota\\), however, so their role is to show that the required route separation is biologically realizable, not to classify individual systems as inside the window."
)
if selectivity_anchor not in man:
    raise RuntimeError("selectivity discussion anchor not found")
man = man.replace(selectivity_anchor, selectivity_add, 1)

joint_anchor = (
    "The sparse direct layer therefore identifies two distinct empirical gaps. Total \\(W_{AD}\\) requires a focal attraction × defence design on a common outcome; the strict total-outcome candidate remains sign-unresolved, while crossed floral-trait evidence shows consumer-context-dependent channel interactions without identifying total curvature. Direct joint-cost curvature has zero strict estimates in the admitted evidence layer, so \\(\\kappa\\) remains unidentified, not zero. Under the one-sided theorem, a negative joint-cost curvature is the only escape route from the selectivity window in the declared family, and it must be sufficiently negative relative to the relief-interference difference."
)
joint_add = joint_anchor + (
    "\n\nShared construction, allocation, or physiological constraints are plausible biological sources of joint-cost curvature, but the strict audit recovered marginal attraction costs, marginal defence costs, trait integration or covariance, and inferred resource reallocation rather than a direct estimate of the additional cost of simultaneous investment in distinct \\(A\\) and \\(D\\) axes. These observations therefore motivate hypotheses about \\(\\kappa\\); they do not identify it."
)
if joint_anchor not in man:
    raise RuntimeError("joint-cost discussion anchor not found")
man = man.replace(joint_anchor, joint_add, 1)

context_anchor = (
    "The environmental analysis likewise yields a balance, not a verbal rule that more antagonists must favour complementarity or more pollinators must favour substitutability. In the larceny synthesis, antagonist exposure reduces female fitness on average, yet the prediction interval spans both signs and the declared moderators explain little of the heterogeneity. The current context axes therefore do not locate the selectivity window reliably in a new system."
)
context_add = context_anchor + (
    "\n\nEcologically, context is therefore better treated as a coupled state of consumer identity, attack mode, reward or resource conditions, exposure, and response stage than as a single named pressure variable. The recurrent sign/state switches in Part II are not noise around one universal effect; they are evidence that the balance among causal channels itself changes among ecological states."
)
if context_anchor not in man:
    raise RuntimeError("context discussion anchor not found")
man = man.replace(context_anchor, context_add, 1)

falsification_anchor = (
    "A separate **full attraction × defence factorial** has a harder purpose: estimating total \\(W_{AD}\\) and its channel allocation. That design must manipulate the two focal traits in the same biological units and measure compatible mutualist contribution, antagonist loss, direct cost, and total fitness. The remaining unknowns are therefore no longer open-ended gaps inside the present argument. They are two explicit next tests: a cheap applicability/falsification gate followed, when needed, by full mechanistic calibration."
)
falsification_add = falsification_anchor + (
    "\n\nThe mechanism-first order therefore turns synthesis into experimental triage. The literature need not be enlarged indefinitely once the structural uncertainty has been localized: a comparatively cheap test of \\(\\kappa\\) can challenge applicability of the bound, whereas only a channel-resolved factorial can calibrate the full interaction. The synthesis thus resolves an empirical ambiguity by converting heterogeneous evidence into an ordered sequence of falsification and calibration rather than another call for undirected data collection."
)
if falsification_anchor not in man:
    raise RuntimeError("falsification discussion anchor not found")
man = man.replace(falsification_anchor, falsification_add, 1)

scope_section = r"""### 6.5 What transfers beyond the floral case

Nothing in the inferential sequence requires flowers, although the biological decomposition developed here does. In another multi-partner ecological system, the focal variables and outcome would first need to be declared, the net interaction decomposed into biologically defensible channels, and any one-sided constraint re-derived under explicit sign premises. Only then should those theory-defined channels be used to organize heterogeneous evidence. What transfers is therefore the workflow—**constraint before pattern**—not the particular floral route signs or the inequality derived from them. This distinction permits broader conceptual use without turning a bounded floral result into an unsupported universal law."""
if "### 6.5 What transfers beyond the floral case" not in man:
    man = man.replace("\n\n## 7. Conclusions", "\n\n" + scope_section + "\n\n## 7. Conclusions", 1)

conclusion_anchor = (
    "The remaining uncertainty has become experimentally specific rather than conceptually open-ended. Direct joint-cost curvature is unidentified, not zero, and a sufficiently negative value is the unique escape route from the one-sided bound in the declared family. A 2 × 2 allocation experiment can test that applicability gate, whereas a full attraction × defence factorial is still required to estimate total \\(W_{AD}\\) and allocate it among ecological channels. The theory therefore ends not with a request for more broad evidence, but with a concrete falsification test and a separate calibration experiment."
)
conclusion_add = conclusion_anchor + (
    "\n\nMore broadly, the paper offers a strategy for synthesis under context dependence: derive a mechanistic exclusion before searching for a universal mean effect, then use the resulting evidence architecture to identify which mechanisms recur and which minimal measurements can falsify the boundary."
)
if conclusion_anchor not in man:
    raise RuntimeError("conclusion anchor not found")
man = man.replace(conclusion_anchor, conclusion_add, 1)

if "## Acknowledgments" not in man:
    ack = (
        "## Acknowledgments\n\n"
        "[Author-controlled acknowledgments to be completed before submission.]\n\n"
        "OpenAI ChatGPT and Anthropic Claude were used during analysis and manuscript development for code-generation assistance, structured literature triage, reproducibility checks, and manuscript drafting and editing, as described in Section 4.3. AI-generated output was not treated as empirical evidence, and the authors retain responsibility for all scientific claims, citations, code, and text. The exact submitted disclosure must be confirmed by all authors.\n\n"
    )
    man = man.replace("## Statements and Declarations", ack + "## Statements and Declarations", 1)

MAN.write_text(man, encoding="utf-8")

# Synchronize portal metadata with the upgraded abstract and primary target.
portal = PORTAL.read_text(encoding="utf-8")
portal = portal.replace("- Article type: **Regular Article**", "- Article type: **Concepts & Synthesis**", 1)
portal = portal.replace("- Target journal: **Theoretical Ecology**", "- Target journal: **Ecology**", 1)
portal = replace_between(portal, "### Abstract", "### Keywords", abstract.replace("## Abstract", "### Abstract", 1))
portal = portal.replace("all authors agree to submission to Theoretical Ecology", "all authors agree to submission to Ecology", 1)
portal = portal.replace("cover letter names Theoretical Ecology and the canonical Mechanism → Pattern manuscript", "cover letter names Ecology, the Concepts & Synthesis article type, and the canonical Mechanism → Pattern manuscript", 1)

ai_old = "### Use of generative AI or language tools\n\nRecord any journal-required disclosure concerning language editing, coding assistance, or generative-AI use. Authors remain responsible for all claims, citations, code, and text."
ai_new = "### Open Research statement\n\nCurrent title-page statement:\n\n> Analysis code, source-adjudication products, and generated readouts are maintained in the public project repository. The exact immutable release, repository licence, and archival DOI for the submitted version are author-controlled release fields and will be inserted before submission.\n\nBefore portal submission, replace the release placeholders with the exact immutable release/tag, licence, archival DOI, and final submission commit.\n\n### Use of generative AI or language tools\n\nCurrent disclosure state: OpenAI ChatGPT and Anthropic Claude were used for code-generation assistance, structured literature triage, reproducibility checks, and manuscript drafting/editing. The manuscript contains a section-specific disclosure in Section 4.3 and an additional Acknowledgments disclosure. The same use must be disclosed in the Ecology submission form, and all authors must confirm the exact submitted wording. Authors remain responsible for all claims, citations, code, and text."
if ai_old not in portal:
    raise RuntimeError("portal AI block not found")
portal = portal.replace(ai_old, ai_new, 1)
PORTAL.write_text(portal, encoding="utf-8")

strategy = r"""# Target journal strategy — mechanism-first Concepts & Synthesis paper

## Primary target

**Ecology — Concepts & Synthesis**

Canonical title:

> **When are floral attraction and defence complementary? A one-sided mechanistic bound and cross-system patterns**

## Why the paper now fits this section

The manuscript is not a conventional review and not a theory paper followed by empirical validation. It uses a floral attraction–defence problem to develop a broader inference strategy for ecology under strong context dependence:

1. define the focal interaction and its causal channels;
2. derive a one-sided exclusion before asking where the positive state occurs;
3. let the theory define the evidence classes used in synthesis;
4. map recurrence and switching without forcing heterogeneous outcomes onto one common effect scale;
5. convert the remaining uncertainty into an ordered falsification and calibration programme.

This matches the current Ecology Concepts & Synthesis expectation that papers conceptually advance ecology, go beyond the literature being reviewed, and provide new syntheses, directions, or resolutions of old questions. Ecology also explicitly prioritizes generalizations potentially applicable beyond one species or system. The manuscript meets that generality requirement by making **constraint before pattern** the transferable contribution while keeping the floral inequality itself biologically bounded.

## Scientific spine to foreground

The bookkeeping identity is

```text
W_AD = rho - iota - kappa
```

but the structural contribution is one-sided:

```text
if kappa >= 0 and W_AD > 0, then rho > iota
```

Under non-negative direct joint-cost curvature, complementarity cannot occur outside the selectivity window where antagonist relief exceeds pollinator interference. The converse fails; about 23% of tested in-window evaluations remain substitutable.

Part II then asks whether the mechanism classes defined by Part I recur. The frozen empirical state remains:

```text
56 route-level records
25 independent biological study clusters
same-system multi-route: 14
context/sign-switch:     17
context-only programs:    7, outside route-ledger N
direct total A x D:       1 strict sign-unresolved cluster
direct joint cost:        0 strict estimates
```

The Leal larceny reanalysis supports an average antagonist-pressure cost but strong context dependence; it does not estimate `rho`, `iota`, `kappa`, or total `W_AD`. The Sasidharan module supports shared consumer tracking at the assembled cross-study level but not a causal paired consumer-role difference.

## Concepts & Synthesis positioning

The cover letter and Abstract should lead with four points:

1. **old problem resolved more sharply:** context-dependent net effects are replaced by a mechanistic exclusion boundary;
2. **new synthesis logic:** Mechanism -> Pattern, not Pattern -> mechanism and not theory -> validation;
3. **broad conceptual use:** the transferable object is the inference workflow, not a universal floral sign rule;
4. **constructive endpoint:** uncertainty is compressed to a cheap 2 x 2 joint-cost falsification gate followed, only when needed, by a full channel-resolved factorial.

Do not sell the elementary algebra as mathematical novelty. Do not claim that attraction-defence balance, correlational selection, pollinator-herbivore non-additivity, defence-associated pollination costs, or context dependence are new.

## Ecology initial-submission requirements to enforce

Current Ecology author guidance (revised April 2026) requires or states for Concepts & Synthesis:

- manuscript page limit: 30 pages for normal submissions; manuscripts over 30 pages require a detailed cover-letter justification;
- Abstract limit: 350 words;
- keywords: 6-12, alphabetical;
- continuous line numbering on all manuscript pages;
- manuscript title and author list must match the ScholarOne form and supporting information;
- Open Research statement on the title page and in the portal;
- AI use beyond ordinary spelling/grammar editing must be disclosed in the relevant manuscript section, again in Acknowledgments, and in the submission form.

The source manuscript is kept under the 350-word Abstract maximum and retains six alphabetized keywords. Continuous line numbering is a final rendered-file task. Immutable release/licence/DOI fields remain author-controlled blockers.

## Submission cascade

```text
Ecology — Concepts & Synthesis
    ↓ if declined or rejected on fit/general reach
Oikos — Forum (requires a <=600-word presubmission proposal)
    ↓
Theoretical Ecology — Regular Article
```

The Oikos fallback is strong because Forum explicitly seeks conceptual unification, synthesis across boundaries, theory development, and tractable future research directions. Theoretical Ecology remains the conservative scope-fit fallback.

## Current decision

Scientific state remains **GO / FROZEN**. No additional broad evidence search is required for the Ecology upgrade. The remaining work is journal-facing presentation, author-controlled metadata/declarations/reviewers/licence, immutable release/archive DOI, final line-numbered Word rendering, and authenticated portal submission.
"""
STRATEGY.write_text(strategy, encoding="utf-8")

checklist = CHECKLIST.read_text(encoding="utf-8")
checklist = checklist.replace("# Theoretical Ecology submission checklist — canonical paperization state", "# Ecology Concepts & Synthesis submission checklist — canonical paperization state", 1)
checklist = checklist.replace("Abstract stays within the current repository-enforced journal word limit and defines “log response ratio”", "Abstract remains under Ecology's 350-word Concepts & Synthesis maximum and defines “log response ratio”", 1)
checklist = checklist.replace("Six keywords remain synchronized", "Six alphabetized keywords remain synchronized and satisfy Ecology's 6–12 keyword requirement", 1)
checklist = checklist.replace("AI-assisted workflow disclosure remains in Methods with author responsibility explicit", "AI-assisted workflow disclosure remains in Methods and is duplicated in Acknowledgments, with author responsibility explicit", 1)
checklist = checklist.replace("## 5. References and journal-facing structure — PASS / final check pending", "## 5. Ecology journal-facing structure — SOURCE PASS / final-render checks pending", 1)
checklist = checklist.replace("- [x] Statements and Declarations follow References", "- [x] Title page carries a provisional Open Research statement with immutable release/licence/DOI explicitly pending\n- [x] Abstract remains below the 350-word Concepts & Synthesis limit\n- [x] Six keywords are alphabetized and within the required 6–12 range\n- [x] AI use is disclosed in the relevant Methods section and again in Acknowledgments\n- [x] Ecology Concepts & Synthesis cover letter is present\n- [ ] Add continuous line numbering to every page of the final Word submission\n- [ ] Confirm final formatted manuscript remains within 30 pages or add the required >30-page cover-letter justification\n- [x] Statements and Declarations follow References", 1)
checklist = checklist.replace("Upload through authenticated journal portal", "Upload through the authenticated Ecology ScholarOne portal", 1)
CHECKLIST.write_text(checklist, encoding="utf-8")

audit = AUDIT.read_text(encoding="utf-8")
target_line = "\n\nPrimary submission target after journal-fit re-evaluation: **Ecology — Concepts & Synthesis**, with Oikos Forum and Theoretical Ecology retained as ordered fallbacks. This target change does not alter the frozen scientific claims."
anchor = "The governing scientific claim is a **one-sided mechanistic theorem plus a recurrent but context-dependent empirical Pattern**."
if target_line.strip() not in audit:
    if anchor not in audit:
        raise RuntimeError("final audit target anchor not found")
    audit = audit.replace(anchor, anchor + target_line, 1)
AUDIT.write_text(audit, encoding="utf-8")

cover = r"""# Cover letter — Ecology, Concepts & Synthesis

Dear Editors,

Please consider our manuscript, **“When are floral attraction and defence complementary? A one-sided mechanistic bound and cross-system patterns,”** for publication as a **Concepts & Synthesis** article in *Ecology*.

The manuscript addresses a broad ecological problem: when net interaction effects vary strongly among systems, what kind of general statement can remain robust? We use floral attraction and defence as a tractable case. Rather than first searching for a cross-system pattern and inferring a mechanism afterward, we define the mechanism classes first and derive a one-sided exclusion: under non-negative direct joint-cost curvature, local attraction–defence complementarity cannot occur unless antagonist relief exceeds pollinator interference. The algebra is elementary; the conceptual contribution is identifying the ecological impossibility boundary, the assumption that can break it, and the evidence architecture that follows from it.

We then let that theory determine what counts as relevant cross-system evidence. A source-adjudicated synthesis contains 56 route-level records from 25 independent biological study clusters, while quantitative meta-analysis is restricted to effect-compatible modules. The synthesis shows recurrent constituent mechanisms and switching architectures rather than a universal sign. Floral larceny reduces female fitness on average, but its prediction interval spans both signs and declared moderators explain little of the heterogeneity. Direct total attraction × defence evidence remains sparse, and the decisive direct joint-cost curvature has no strict empirical estimate in the admitted evidence layer.

The paper therefore goes beyond review in two ways. First, it converts a familiar context-dependence problem into a mechanistic exclusion boundary: it asks where complementarity cannot occur before asking where it does. Second, it converts the remaining uncertainty into an ordered experimental programme. A simple 2 × 2 allocation design can first test the joint-cost sign that controls applicability of the bound; only then is a full channel-resolved attraction × defence factorial needed for calibration.

We believe this fits *Ecology*'s Concepts & Synthesis section because the contribution is a new synthesis logic rather than a taxon-specific catalogue. The transferable claim is **constraint before pattern**: in other multi-partner ecological systems, causal channels and sign premises would have to be re-derived, but the same mechanism-first sequence can organize heterogeneous evidence without manufacturing a universal mean effect.

The scientific claims, numerical results, and evidence boundaries are frozen and fully versioned in the associated repository. The final immutable repository release, licence, archival DOI, author metadata, acknowledgments, and declarations will be completed before portal submission. AI-assisted work is transparently disclosed in the relevant Methods section and in Acknowledgments, with authors retaining responsibility for all content.

[Author confirmation required before submission: this manuscript is not under consideration elsewhere, all authors approve the submitted version, and all authors agree to submission to *Ecology*.]

## Potential reviewers

1. [Name — institution — e-mail — expertise — conflict check]
2. [Name — institution — e-mail — expertise — conflict check]
3. [Name — institution — e-mail — expertise — conflict check]
4. [Name — institution — e-mail — expertise — conflict check]
5. [Name — institution — e-mail — expertise — conflict check]

## Opposed reviewer, if justified

[Name — concrete conflict rationale; leave blank if none.]

Sincerely,

[Corresponding author — author-controlled]
"""
COVER.write_text(cover, encoding="utf-8")

fit = r"""# Ecology Concepts & Synthesis fit audit

Checked against *Ecology* author guidance current on 2026-08-21 (guidance revised April 2026).

## Editorial fit

**PASS, with the manuscript framed as a conceptual synthesis rather than a universal floral sign rule.**

The target section describes Concepts & Synthesis papers as work that conceptually advances ecology, goes well beyond the reviewed literature, and develops new syntheses, directions, or resolutions of old questions. Ecology also prefers generalizations potentially applicable to other species, populations, communities, or ecosystems.

The manuscript now presents its broad contribution as a mechanism-first inference sequence:

```text
declare focal interaction
-> decompose causal channels
-> derive a one-sided exclusion
-> use theory-defined classes to organize heterogeneous evidence
-> identify the minimal falsification gate
-> calibrate only when needed
```

The floral theorem remains biologically bounded. The generalization is the inference workflow, not the claim that the same route signs apply outside flowers.

## Source-level requirement audit

- Abstract: <350 words — PASS
- Keywords: 6–12 and alphabetical — PASS (6)
- Provisional Open Research statement on title page — PASS; immutable release/licence/DOI still pending
- Section-specific AI disclosure — PASS
- Additional AI disclosure in Acknowledgments — PASS
- Ecology Concepts & Synthesis cover letter — PASS
- Portal metadata target/article type synchronized — PASS
- Continuous line numbering — PENDING FINAL WORD RENDER
- <=30-page final formatted manuscript — PENDING FINAL WORD RENDER
- title/author-list match across manuscript, portal, and supporting files — author fields PENDING

## Scientific invariants preserved

No change to the theorem, proof, 2,592 evaluations, 77.2% window precision, 56/25 Pattern architecture, Leal pooled results, Sasidharan boundaries, direct A×D state, joint-cost evidence state, or falsification/calibration distinction.

## Fallbacks

1. Oikos Forum — excellent conceptual fit, but requires a <=600-word presubmission proposal.
2. Theoretical Ecology Regular Article — conservative scope-fit fallback; existing house-style assets are retained rather than deleted.
"""
FIT.write_text(fit, encoding="utf-8")

test = r'''from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
PORTAL = ROOT / "submission" / "AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md"
COVER = ROOT / "submission" / "COVER_LETTER_ECOLOGY_CONCEPTS_SYNTHESIS.md"
STRATEGY = ROOT / "submission" / "TARGET_JOURNAL_STRATEGY.md"
FIT = ROOT / "submission" / "ECOLOGY_CONCEPTS_SYNTHESIS_FIT_AUDIT.md"


def _abstract(text: str) -> str:
    return text.split("## Abstract\n\n", 1)[1].split("\n\n**Keywords:**", 1)[0].strip()


def _words(text: str) -> list[str]:
    text = re.sub(r"\\\(|\\\)|[{}*_`]", " ", text)
    return re.findall(r"\b[\w+×-]+\b", text, flags=re.UNICODE)


def test_ecology_target_and_article_type_are_active() -> None:
    portal = PORTAL.read_text(encoding="utf-8")
    strategy = STRATEGY.read_text(encoding="utf-8")
    assert "- Article type: **Concepts & Synthesis**" in portal
    assert "- Target journal: **Ecology**" in portal
    assert "**Ecology — Concepts & Synthesis**" in strategy
    assert "Oikos — Forum" in strategy
    assert "Theoretical Ecology — Regular Article" in strategy


def test_ecology_abstract_and_keywords_fit_current_limits() -> None:
    text = MAN.read_text(encoding="utf-8")
    abstract = _abstract(text)
    assert 150 <= len(_words(abstract)) <= 350
    keyword_line = next(line for line in text.splitlines() if line.startswith("**Keywords:**"))
    keywords = [item.strip() for item in keyword_line.split(":", 1)[1].split(";") if item.strip()]
    assert 6 <= len(keywords) <= 12
    assert keywords == sorted(keywords, key=str.casefold)


def test_portal_abstract_stays_exactly_synchronized() -> None:
    manuscript = MAN.read_text(encoding="utf-8")
    portal = PORTAL.read_text(encoding="utf-8")
    pabs = portal.split("### Abstract\n\n", 1)[1].split("\n\n### Keywords", 1)[0].strip()
    assert pabs == _abstract(manuscript)


def test_broad_concepts_and_synthesis_framing_is_bounded() -> None:
    text = MAN.read_text(encoding="utf-8")
    assert "A recurring problem in ecology is that net interaction outcomes can conceal opposing causal channels" in text
    assert "This ordering is also the paper's broader contribution to ecological synthesis" in text
    assert "### 6.5 What transfers beyond the floral case" in text
    assert "constraint before pattern" in text
    assert "not the particular floral route signs or the inequality derived from them" in text
    assert "unsupported universal law" in text


def test_open_research_and_esa_ai_disclosure_surfaces_are_present() -> None:
    text = MAN.read_text(encoding="utf-8")
    front = text.split("## Abstract", 1)[0]
    assert "**Open Research statement:**" in front
    assert "immutable release" in front
    assert "repository licence" in front
    assert "archival DOI" in front
    methods = text.split("### 4.3 Computational and AI-assisted workflow transparency", 1)[1].split("## 5.", 1)[0]
    assert "OpenAI" in methods and "Anthropic" in methods
    ack = text.split("## Acknowledgments", 1)[1].split("## Statements and Declarations", 1)[0]
    assert "OpenAI ChatGPT" in ack
    assert "Anthropic Claude" in ack
    assert "authors retain responsibility" in ack


def test_ecology_cover_letter_has_conceptual_advance_and_five_reviewer_slots() -> None:
    text = COVER.read_text(encoding="utf-8")
    assert "Concepts & Synthesis" in text
    assert "constraint before pattern" in text
    assert "goes beyond review" in text
    slots = re.findall(r"^[1-5]\. \[Name — institution — e-mail — expertise — conflict check\]$", text, flags=re.MULTILINE)
    assert len(slots) == 5


def test_fit_audit_keeps_release_and_render_gates_open() -> None:
    text = FIT.read_text(encoding="utf-8")
    assert "PENDING FINAL WORD RENDER" in text
    assert "immutable release/licence/DOI still pending" in text
    assert "Scientific invariants preserved" in text
'''
TEST.write_text(test, encoding="utf-8")

# Remove this one-shot patch mechanism from the permanent diff.
if WORKFLOW.exists():
    WORKFLOW.unlink()
if SELF.exists():
    SELF.unlink()
