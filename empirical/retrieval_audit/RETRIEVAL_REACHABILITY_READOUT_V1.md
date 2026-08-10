# Retrieval reachability readout v1

Reproduce with:

```bash
python scripts/audit_data_retrieval_reachability.py empirical/retrieval_audit 10
```

This readout exists because "the extraction is blocked" should be evidence in the repository, not
an assertion in a commit message. It records which hosts a literature synthesis needs and which
ones this execution environment can actually reach.

## 1. Result

31 declared hosts probed. **7 reachable, 24 blocked.**

| role | reachable | blocked |
|---|---|---|
| bibliographic API (Crossref, OpenAlex, Semantic Scholar, Unpaywall) | 0 | 4 |
| full-text archive (Europe PMC, PMC/E-utilities) | 0 | 3 |
| data repository (Dryad, Zenodo, Figshare, OSF, Dataverse, DataCite) | 0 | 6 |
| publisher (Wiley, ESA, BES, OUP, Springer, PLOS, Nature, PeerJ) | 0 | 8 |
| preprint / archive | 0 | 2 |
| package index | 1 (PyPI) | 1 (CRAN) |
| code hosting | 6 | 0 |

Reachable: `github.com`, `api.github.com`, `raw.githubusercontent.com`, `codeload.github.com`,
`gitlab.com`, `bitbucket.org`, `pypi.org`.

Blocked hosts return no HTTP status at all — the egress proxy refuses to open the tunnel and
records a policy denial. That is an organization egress policy, not a rate limit, a paywall, or a
transient failure, and it cannot be worked around from inside the session.

## 2. What this rules out

Every step of a conventional large-scale literature synthesis is unavailable:

- **Corpus-scale candidate discovery.** No bibliographic API answers, so there is no way to run a
  declared query and enumerate candidate records. The reading queue cannot be grown systematically.
- **Identifier verification.** DOIs recorded from search results cannot be checked against
  Crossref or DataCite, so they stay flagged `unverified_from_search_result`.
- **Abstract and full-text screening.** No archive or publisher answers.
- **Deposited-dataset extraction.** Dryad, Zenodo, Figshare, OSF, and Dataverse are all blocked,
  which matters most: the manipulative nectar-chemistry literature of the declared target stratum
  was published between roughly 2005 and 2017 and deposits to Dryad, not to code hosting.

## 3. What remains open, and its limit

Anonymous `git clone` of a public repository works, and was verified end to end: the deposited
data and code for Wenzell, Skogen and Fant (Oikos, doi:10.1111/oik.09708) — a study already
carrying a direction record in this registry — clone and read correctly.

The limit is discovery, not download. GitHub's own search is refused: `github.com/search` returns
403, and `api.github.com/search/repositories` returns "sessions are bound to their configured
repositories". A repository can therefore only be cloned if its `owner/name` is already known, and
the only discovery channel left is general web search, which indexes journal pages far better than
it indexes research data repositories.

That combination — clone anything you can name, but no way to enumerate what exists — is why this
channel does not scale. It can confirm a specific known deposit. It cannot assemble a stratum.

## 4. What would unblock the extraction

The four candidate routes were checked rather than listed, and they are not equally live.

**Route A — enable the PubMed connector in this chat. Live, and by far the cheapest.**
A PubMed MCP connector is already installed for this account, requires no OAuth
(`isAuthless: true`), and exposes `search_articles`, `get_article_metadata`,
`find_related_articles`, `lookup_article_by_citation`, `convert_article_ids`,
`get_full_text_article`, and `get_copyright_status`. It is simply toggled off for this
conversation (`enabledInChat: false`), so its tools are not loaded. Turning it on in the chat's
connector settings restores declared-query candidate discovery, screening, and open-access full
text **without any change to the network policy**, because connector traffic does not traverse
this session's egress proxy. The pre-registered search strategy that would then execute is in
`empirical/broad_reality_evidence/iota_pathway/IOTA_PATHWAY_SEARCH_STRATEGY_v1.md`.

**Route B — widen the environment's network policy.** Permitting the bibliographic and
data-repository hosts in section 1 is the only change that restores *everything*, including Dryad
and Zenodo deposits that no literature connector can reach. The policy is chosen when the
execution environment is created and is documented at
https://code.claude.com/docs/en/claude-code/claude-code-on-the-web. This is the route for the
declared target stratum specifically, whose manipulative literature deposits to Dryad.

**Route C — authorize the pending connector. Dead end.** The unauthenticated MCP server in this
session is Canva. It has no bearing on literature retrieval, and authorizing it would not help.

**Route D — run retrieval in another environment. Not available.** The account has exactly one
environment (`rach`, Anthropic cloud). Egress policy is a property of the environment, so a
session spawned there inherits the same denials; there is no second environment with a different
policy to move the work to.

**Route E — supply the sources directly.** Full texts, supplementary tables, or deposited datasets
placed in the repository can be extracted under the declared protocol with no network at all.
This remains available regardless of the others.

## 5. Boundary

This audit records network reachability at the time it was run. It is a property of the execution
environment's egress policy, not of the literature: a blocked host says nothing about whether the
data exist or are open access. Re-running it after any environment change is the correct way to
re-test, and the summary JSON carries the machine-readable result.
