# Service versioning memory update — submission failed

The shared project decision page below is also retained for later reconciliation;
it has not been submitted after the preference write failed. Re-read both targets
before retrying rather than overwriting intervening changes.

23 October 2026. Bruno explicitly requested persistent memory of the version-bump
proposal rule. Destination: preferences/interaction.md, section sec_3a1709.
Requested auto_apply=true through the configured OAuth PKB Service.

The service returned isError=true: Git refused /srv/llm-wiki/data/bruno due to
detected dubious ownership. No proposal ID or publication receipt was returned;
durable proposal state is unknown. Do not blindly retry or change server trust
configuration merely to clear this failure. Re-read the canonical page and
inspect pending state after the service owner repairs repository access.

The rule is saved in AGENTS.md and CLAUDE.md in all three affected repositories.
Shared PKB publication is unconfirmed. The complete proposed section follows:

+<a id="sec_3a1709"></a>
## Coding Agent Workflow

- Read existing docs and code before proposing changes.
- Prefer targeted inspection over loading an entire repository.
- Follow existing local patterns, frameworks, helper APIs, and naming conventions.
- Check existing definitions before proposing new conventions, schema fields, enum values, or abstractions.
- Prefer deterministic, explicit logic over heuristics.
- Prefer small, coherent, self-contained changes over broad speculative refactors.
- Avoid broad refactors unless they are necessary for the requested change.
- Keep behaviour changes, documentation, docstrings, architecture notes, and operational assumptions in sync.
- Run the narrowest relevant tests first, then broaden testing when the risk or blast radius warrants it.
- Summarise residual risk, skipped checks, and assumptions clearly.
- Treat LLMs as useful for planning, routing, drafting, and explanation, but not as the authority for durable source records or computed facts.
- Confirmed 23 October 2026: before committing a significant set of changes to a service/component in the Knowledge Base System repositories, Codex and Claude Code should propose an explicit patch or minor application-version bump, stating the affected components, old/new versions and rationale. Compatible fixes normally warrant patches and compatible new features minors; breaking changes need a separate major-version discussion. Keep the rule prominent in AGENTS.md and CLAUDE.md, not only conversational memory. Keep reported versions, build identity and package metadata consistent, distinguish protocol versions, and preserve separate deployment approvals.
