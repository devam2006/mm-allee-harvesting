# AI acknowledgement and human verification

The final report and notebook must acknowledge **every actually used platform and its role**, with external sources cited separately. WP05 owner consolidates the log; everyone supplies their own entries. Do not claim a platform was unused because only one member used it.

| Date | Member | Platform/model if known | Role and affected files | Human checks | PR |
|---|---|---|---|---|---|
| 2026-10-19 | Devam (repository setup requester; package unassigned) | OpenAI ChatGPT/Codex | Initial work allocation, repository scaffold, shared numerical functions, starter tests and documentation | Setup verification recorded in `BOOTSTRAP_VALIDATION.md`; team scientific review still required | Bootstrap upload `04332ecd913a808929fcb08fa9b2567aeb3e89b3`; all five task choices still pending |

| 2026-10-19 | Devam (repository guidance requester; task unassigned) | OpenAI ChatGPT/Codex | Shared agent onboarding, Claude entry file, plain-language task introductions and teaching workflow | Official entry-file docs checked; links, import target and repository checks recorded in the onboarding PR | Agent onboarding/team-setup PR |

Add actual usage rows as work happens. Do not invent model identifiers when unknown. Important prompts or short summaries can be retained in PR descriptions without credentials or unrelated personal material.

On 19 October 2026, Devam selected WP03. ChatGPT/Codex recorded the choice in `team.json`, regenerated ownership displays, clarified the task's calculus/ODE background and recorded Devam's report that collaborator invitations had been sent. This metadata update does not claim any WP03 scientific implementation or human understanding check.

Later the same day, Devam reported Prem → WP04 and Rohan → WP05, and clarified that four-member approval is for project work, not repository setup. ChatGPT/Codex updated the roster and generated docs, clarified that scope in the agent/human workflow files, and prepared the verified setup PR for owner-authorised merge. Scientific task checklists remain open.

At final task allocation on 19 October 2026, Devam assigned AshChan07 → WP02 and RaghavSinghal15 → WP01. ChatGPT/Codex synchronised the remaining owner displays and reviewed all five task briefs against testing/integration requirements. Shared instructions and the project PR template now explicitly require claim-to-test/experiment evidence, independent expectations, boundary cases and justified tolerances. The ownership-sync test fixture was corrected to preserve its progress assertion regardless of the live owner; notebook starter labels now describe pending implementation instead of unclaimed tasks. No scientific task was marked complete by this setup update.

Each owner confirms they can explain their section's equations, stability argument, numerical method, algorithm, configuration, test evidence and limitations. All members read the final integrated report and understand the complete story before presentation. AI-assisted review does not replace this understanding or the four human PR approvals.

Suggested final wording must be adapted to actual use: “We used [platforms] for [specific roles]. The authors checked the derivations, implementation and results and take responsibility for the submitted work.” Never submit the bracketed template unchanged.

31 October 2026: at Devam's explicit request to fix the outstanding PRs and build a separate WP01-WP03 integration PR, OpenAI ChatGPT/Codex applied the WP01 compatibility/review corrections and ran focused tests. 189 WP01 tests passed, including 90-digit independent roots for both reported close-fold examples and rejection of unsupported rtol before any output. Near-fold roots are solved in offsets; simple-root signs/derivatives use the factored cubic. The existing standalone fold-band policy is unchanged pending the separate integration PR. These changes are authored as Devam-assisted fixes, not an approval or statement of the original owner's understanding.
