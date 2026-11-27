# Research desk

Investigate public decisions affecting American sovereignty, foreign commitments, surveillance, government contracting, and the influence of private capital on policy and media. Start with Tucker and his immediate family. A good assignment identifies a decision, payment, appointment, or disclosure that a document could clarify. Give evidence that weakens a proposed connection the same prominence as evidence that supports it.

[Pick a P1 assignment](https://github.com/JakeShieldsTryingToSpell/carlson-osint/issues?q=is%3Aissue+is%3Aopen+in%3Atitle+P1) · [All open issues](https://github.com/JakeShieldsTryingToSpell/carlson-osint/issues) · [Family directory](people/README.md)

## How to pick the next issue

| Priority | When to use it | First assignments |
| --- | --- | --- |
| **P1 · Immediate family and consequential checks** | A specific record could change our understanding of Tucker or his immediate family, or resolve a disputed claim about an institution, financial interest, or public decision. An independent review of a high-stakes result also belongs here. | Date Tucker’s direct public contact with Thiel. Compare the accounts of Richard’s intelligence-related work with contemporary records. |
| **P2 · Missing profiles and connections** | Give an unresearched relative a sourced starting profile, or test the weakest link in a plausible connection. Move it to P1 when multiple findings depend on it or a specific consequential decision turns on it. | Disambiguate Charles Carlson, check his reported public employment, and record what is still unknown. Choose a second thin profile when it unlocks a family or institutional link. |
| **P3 · Background** | Additional ancestry, low-impact details and routine independent checks. An untagged research or review issue defaults here. | Distant cousin lines with no active public-interest question. |

Use issue titles such as `Research: [P1] …`, `Profile: [P2] …`, `Connection: [P2] …`, and `Review: [P1] …`. Assign a review the priority of the claim it gates. Within a tier, the CLI offers independent reviews first, then the oldest issue. A maintainer can change priority by editing the title. A new profile for a private relative can consist of one sourced family relationship and the remaining gap.

## What a worker needs

Give each issue one person whose research file will receive the result, a bounded question, the decision or interpretation it could change, the sources already checked, and a success or stopping condition. Keep reports person-specific. Link a shared claim ID or original source across profiles. A case brief can coordinate several single-person assignments. Record a separate source for each link in a chain, including disputed or missing links. For a claim of influence, identify the relevant decision and look for evidence someone took part in it.

Reserve the issue using `python3 archive.py start`. A first pass can cover two named collections or about 15 minutes. Stop when the route is exhausted. Post the sources, search terms, dates, result and reopening condition. A maintainer can park the issue by closing it or using `[Parked]` in its title. Reopen it when there is a new record or approach. Every factual result needs a passage and independent check before it becomes a headline. A correction or decisive negative result counts as a completed assignment.

## Existing case briefs

| Assignment | Route and completion condition |
|---|---|
| **Check the chart’s Miller and Nickel generations** | Work from the historical family chart in *Lombardi v. Blois*, printed p. 196, and the factual history in *Estate of Vaughan*. Transcribe each relevant parent-child link with its page. Resolve Mary’s different surnames and mark any missing generation. [Chart comparison](cases/family-chart.md) |
| **Check the Fulbright–Swanson link** | Start at Carol Swanson Price’s obituary. Identify the intervening person or couple in the claim that Patricia was J. William Fulbright’s niece. Document whether the path passes through a marriage. A discrepancy, or a precise record of an unsuccessful search, is a result. [Patricia](people/patricia-swanson-carlson/README.md) |
| **Find a contemporary record for the 2019 Rockbridge gathering** | Search archived programs, public remarks and organizer material from the event year. Distinguish the Ohio gathering from later summits. Return a dated record and locator or the archives, date ranges and terms already searched. [Rockbridge case](cases/rockbridge.md) |
| **Audit what the Rockbridge reporting actually attributes** | Independently read the first-hand and reported accounts of the gathering. Trace reprints to their upstream source. Separate attendance, convening and formal office into individual statements, and say which remain open. This approach can run alongside the archive search. [Rockbridge case](cases/rockbridge.md) |
| **Reproduce the maternal-grandmother finding** | Start with California appeal F077628. Extract the two links and the passages supporting them before comparing your reading with the existing evidence. Note any shared source dependency. [Evidence chain](evidence/mary-nickel-james--maternal-grandparent-of--tucker-carlson.json) |

For an independent check, record the PR, revision, claim IDs and `Researcher: @HANDLE` on the review issue. Give any serious contradiction or material correction the same priority as the original finding.
