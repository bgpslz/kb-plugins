# Brief for personal-rag: session changes and decision history

Prepared 22 October 2026. Bruno requested this feature after finding that an open
wiki review session blocked a personal-KB documentation update. Implementation
belongs in **personal-rag**, not kb-plugins. This is a handover brief, not an
implemented or deployed change.

## Problem

The Wiki Proposal Review Application mainly shows pending proposals. Accepted
changes disappear from that list and are visible again only by opening **Merge**,
which doubles as a read-only preview. Rejected changes also disappear after a
reload, with no history view. This makes it difficult to remember what has been
decided or tell whether a session is safe to close.

In the live PKB app, branch `wiki-review/9b45c99a934e` contained three accepted,
committed but unmerged changes, although Bruno thought it might be empty. The
preview confirmed proposals 3, 7 and 6. No merge or discard was performed.

## Requested behaviour

### Session changes

Add a clearly labelled **Session changes** control beside the session summary.
It opens a read-only view without requiring the user to initiate Merge.

- Show the session identity and clear counts for accepted changes awaiting
  publication. Show rejected decisions associated with that session where that
  association is known. Keep the existing page-centric pending-review workflow.
- List proposal ID, page/section, action, summary, decision time, reviewer where
  recorded, and reviewer notes. Make clear which content was edited on acceptance.
- Let the user inspect accepted content and the combined publication diff,
  including navigation/history changes, by reusing existing merge-preview logic.
- Explain the available actions: **Merge publishes accepted changes**;
  **Discard session returns accepted changes to pending review**. Neither opening
  nor closing the inspection view changes anything.
- Display a useful empty state so “no accepted changes awaiting publication” is
  explicit. Do not infer that there were no rejections from an accepted count of zero.

Keep Merge as a separate explicit action with its existing preview, confirmation,
Git-tip freshness checks, locking and validation. Inspection must not publish.

### Decision history

Add an easy-to-find **Decision history** view that survives reloads and session
closure. Start with recent decisions; provide pagination and filters for outcome,
page/proposal ID and session. Add reviewer filtering only where reliable identity
is recorded. All views retain the applicable service's existing access controls.

Show proposal identity and summary, decision time, outcome, session/publication
state where applicable, reviewer where known, notes, and inspectable content.
Use plain labels to distinguish:

- **Accepted — awaiting publication**.
- **Published** after the associated session is merged.
- **Rejected**: effective immediately, with nothing awaiting Merge.
- **Returned to pending** after session discard, while preserving the earlier
  acceptance decision and any reviewer-edited content in history.

Support create, edit and delete proposals. Do not promise a historical before/after
diff when the original content cannot be reconstructed: display available content
and say what is missing. History must not offer an active review form for a change
that is no longer pending. Undo/reopen/re-review actions are outside this feature.

## Data and implementation constraints

Inspected source already stores proposal status, decision time, reviewer notes,
final content, session/commit references and session merge/discard state. However:

- Rejection currently does **not** associate the decision with a session or record
  the authenticated reviewer. `requested_by` identifies the proposer, not reviewer.
- Discard resets accepted rows to pending and clears session, commit, final content
  and decision time. Those mutable rows alone cannot provide durable history.
- Automatic-publication failures can also mark proposals rejected. Do not label
  these as human rejections or mix them into “my decisions” without distinction.

Use existing data where sufficient. Add the minimum durable decision metadata
needed for future reviewer/session attribution and preservation across discard;
use the project's established schema/migration workflow. Historical missing
identity/session links must remain unknown, not inferred from date, proposer or
the current user. Existing rows should remain visible with those limitations.

Inspection/history requests must not create a review session, create a worktree,
or change proposal state. The current main review GET calls `_ensure_open_session`;
do not reuse that side effect for these read-only views. Preserve permission and
tenant boundaries, including the distinction between reviewer-visible private
notes and published wiki text. Do not implement the separately proposed
multi-editor permissions redesign as an incidental part of this feature.

## Starting points

In personal-rag:

- `src/personal_rag/wiki/review_app.py`: shell, pending selector, submit/reject,
  merge preview, discard and client-side row updates.
- `src/personal_rag/wiki/storage.py` and `schema.py`: proposal/session records,
  committed-list queries and discard reset behaviour.
- `src/personal_rag/wiki/git_ops.py`: existing net session diff.
- `src/personal_rag/wiki/publication.py`: automatic outcomes and recovery boundary.
- `docs/wiki_review_ui_design.md`, `ARCHITECTURE.md`, `OPERATIONS.md` and the
  existing wiki review/storage/publication tests.

Older sections of the design document describe superseded behaviour. Reconcile
against current source and its dated deployment notes before implementing.

## Acceptance

1. A user can inspect all accepted, unmerged changes through **Session changes**
   without opening Merge or changing state; counts match the merge preview.
2. Rejected decisions remain discoverable after reload. Their immediate effect
   and exclusion from publication are clear.
3. Merge moves accepted entries to published history; discard returns proposals
   to pending while preserving prior decisions and reviewer-edited content.
4. Old records with unknown attribution remain readable and honestly labelled.
   Automatic failures are distinguishable from human decisions.
5. Inspecting an empty/closed session or history creates no session/worktree.
   Concurrent decisions/publication refresh or invalidate stale views correctly.
6. Tests cover state/filter/pagination behaviour, legacy records, all proposal
   actions, access isolation, and unchanged merge freshness/validation safeguards.
   Verify keyboard use and a narrow/mobile layout visually.
7. Document source changes, any migration, tests and outstanding limitations.
   Report live deployment separately. Existing sessions and decisions must not be
   merged, discarded or recovered merely to test or deploy this feature.

## Additional approved requirement: empty sessions must not block publication

Bruno subsequently confirmed that an empty review session should not block an
otherwise authorised automatic publication. After his Merge, a live read-only
preview showed zero accepted changes and no net differences, yet automatic
publication still failed. The review GET calls `_ensure_open_session`, so returning
there after Merge/Discard can immediately recreate an empty session.

Implement this lifecycle correction in personal-rag alongside, or separately from,
the visibility feature. Prefer lazy session creation when the first actual review
write needs a branch. Existing harmless empty sessions must also stop blocking
otherwise permitted automatic publication; a mere open row is insufficient.

Under the existing repository mutation lock, distinguish an empty human review
session from real work: no accepted/unmerged proposal records, no unpublished
commits, and no dirty/staged/untracked work in its worktree. A zero proposal count
or net-zero diff alone does not prove that no work would be lost. Preserve pending
proposals, rejected decisions/history and any unrelated review work. An accepted
batch or an interrupted automatic/lifecycle session must keep its existing safety
and recovery handling. Empty-session handling does not grant automatic approval
to organisation KBs or protected policy pages.

Test automatic publication with no session, an empty existing human session,
accepted changes, dirty/untracked work, unpublished commits with no net diff,
concurrent first review submission, and interrupted automatic publication. Verify
that Merge/Discard/inspection does not leave a new empty session that blocks the
next permitted operation. Rejections already take effect and must not themselves
become a reason to require a merge.

This adds no authority to merge or discard nonempty live sessions, deploy backend
changes or mutate the VPS without its separate approval.
