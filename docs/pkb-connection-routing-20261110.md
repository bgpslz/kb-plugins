# PKB connection routing correction — 10 November 2026

KBs source 1.4.4 is a published compatible patch over 1.4.3. Local
Codex Desktop/CLI setup prefers **PKB Service (OAuth)** (formerly **PKB Service v2**); cloud
ChatGPT setup uses **PKB Service (token)**. Preserve working native OAuth as well.
Cloud OAuth investigation remains open. No credential, connection, installed
cache, user instruction, capture installation or backend deployment was changed.

## Findings and packaging decision

The source `chatgpt/kbs` app mappings, manifest, README and skills matched the
installed `/Users/brunoprior/.codex/plugins/cache/workspace-directory/kbs/1.4.3`
copy before editing. Directory-only differences were an empty source
`.claude-plugin` directory and Python cache files. The source package really did
map only MCP Service and the token PKB app and explicitly exclude OAuth apps.

The OpenAI [packaging documentation](https://developers.openai.com/plugins/build/plugins)
documents registered app mappings and setup onboarding. It does not establish
per-client alternatives in one app mapping. Do not claim that unsupported
selectors exist or force both PKB routes on cloud users. The shared package now
declares only MCP Service; setup names/recommends the appropriate existing PKB
app. Removing the dependency mapping does not uninstall a user's connection.
A future verified alternative-dependency contract could replace this arrangement.

The [skill invocation documentation](https://learn.chatgpt.com/docs/build-skills)
says `allow_implicit_invocation: false` prevents automatic invocation from prompts
while allowing explicit invocation. Both setup and build previously had that
policy. Their absence from one chat's advertised skills does not establish a
packaging/discovery defect. Setup now permits natural-language invocation only
for setup/repair requests, and the manifest declares setup as its onboarding
skill. Build remains explicit-only. Actual routing still needs client acceptance.

The plugin-management dependency lookup could not resolve this private
`kbs@workspace-directory` package as a public listed release. A plugin search did
not return the private PKB Service v2 app. Neither result proves uninstall,
revocation, or expired authentication. The previous diagnosis's saved tool
catalog, DNS/timeouts and Install plugin screenshot remain supplied historical
evidence; this work did not reproduce those observations or test the saved v2
grant. Public discovery attempts through the web tool here were inaccessible;
the earlier successful discovery remains user-supplied evidence only.

## Source changes and versions

- KBs OpenAI and Claude package inventories/manifests: **1.4.3 → 1.4.4**, patch
  for compatible setup repair; status **published**. Shared copies stay aligned.
- Setup and bootstrap skill text: **1.3.6 → 1.3.7**. Other skill versions stay put.
- Collector **1.1.0**, backend services and KB/registry/system-wiki protocols are
  unchanged. No backend version is proposed merely for this handover artifact.
- Canonical OpenAI client guide is now `setup/openai-client-setup.md`, generated
  into the OpenAI package. It names both exact app IDs, recovery states, Casdoor
  reauthentication, user-friendly connection names and verification boundaries.
- The native adapter requires `--codex-apps-checked` before new Codex native
  endpoints. This records an assistant/operator check, not automated app discovery.
  Existing endpoint reuse and instruction plans remain available without it.
  Previously generated plans must be regenerated; no credentials are changed.
- Managed instructions preserve app-backed v2 OAuth alongside native OAuth.

## Release-owned system-wiki handover

MCP Service startup loaded complete index/local-Codex pages at revision
`sha256:1768cfbaff67989907bfff418c562382630e4cade3239aaefaa104579dc62192`.
That local-Codex page still directs assistants to separately configured OAuth
MCP servers and needs the same correction. Runtime guidance remains at that
revision; repository work does not change it.

[The proposed backend patch](personal-rag-pkb-routing.patch) updates the existing
`personal-rag/src/personal_rag/system_wiki/content/` pages `local-codex.md`,
`connections.md` and `other-harnesses.md`. It matches the plugin's route and
recovery guidance. `git apply --check` passed against the local personal-rag
checkout without applying the patch. Backend review/release and authenticated
post-deployment descriptor/page checks are pending. Follow personal-rag's own
repository and release process; do not publish system guidance via KB proposals.
Keep its published plugin-version statement at 1.4.3 until 1.4.4 is published.

## Validation and outstanding acceptance

Source validation: **93 setup tests and 8 collector regressions passed**;
canonical sync and package checks passed. New native tests exercise Desktop/CLI
absence of app evidence, refusal to apply missing/false checks, and native reuse.
These are isolated fixture tests, not fresh-user client acceptance.

The existing `casdoor_pkb_service` native connection returned KB Protocol 1 with
wiki/build capabilities and full root/project wiki reads in this chat. This
establishes native retrieval only. No app-backed v2 tools were exposed here;
no v2 grant or reauthentication test was completed. The token route was not
used as a substitute to claim OAuth readiness.

| Acceptance case | Required evidence | Current result |
| --- | --- | --- |
| Fresh Desktop user | Install source release via supported manager; natural-language setup recommends v2; Casdoor consent; exact app capability + substantive wiki read; fresh-chat guidance | Pending |
| Existing Desktop installation | Reuse v2 identity and grant, repair connection as indicated; no duplicate native entry; exact app read and fresh-chat guidance | Pending |
| Fresh CLI user | Correct recommended app/verified supported route; sign-in and exact-route read; fresh-session guidance | Pending |
| Existing CLI installation | Existing OAuth preserved, app/native inventories distinguished; reauth when needed; exact-route read | Native read passed here; full flow pending |
| Cloud ChatGPT token | Setup recommends token app without OAuth prerequisite; credential entered privately; capability + wiki read through token app | Guidance changed; live flow pending |
| Cloud OAuth investigation | Actual app/client registration, callback/resource/scopes, Casdoor exchange and authenticated content read | Open; discovery alone is insufficient |
| Live MCP Service guide | Release patch in personal-rag, then matching-revision authenticated index/surface reads | Patch prepared and check passed; deployment pending |

Do not claim overall setup completion from unit tests, app-detail metadata or
one client's native read. Source publication, supported client update, user
browser consent and each client's fresh/existing flow remain separate steps.

## Project knowledge record

The authorised `maintain-project-docs` workflow updated the existing personal
project component page through `casdoor_pkb_service`: change **113**, origin
`f2613f005c764f5f8f312662d531a64b`, status **applied**. The record distinguishes
unreleased source, successful native retrieval, prepared system-wiki patch and
pending client acceptance. No shared operating guide was published through the
PKB, and no organisation-wiki rollout claim was made.

## Naming and publication follow-up

Bruno requested the display name **PKB Service (OAuth)** alongside **PKB Service
(token)**, and authorised publishing 1.4.4 before reconnecting on the MacBook.
The guidance now uses the explicit authentication name and recognises the old
**PKB Service v2** name as a transition alias. The app ID and endpoint are
unchanged; this source edit does not itself rename the provider's registered
app. An editable new connection should use the OAuth display name. The user will
perform the MacBook update in MacBook Codex after source publication; this chat
executes on the Mac mini. Reconnection acceptance follows that client update.

## Publication receipt

Implementation commit `dabeab9` was pushed successfully to `bgpslz/kb-plugins`
GitHub main on 10 November 2026. The release inventory now marks **1.4.4 published**.
Source validation remained 93 setup tests, 8 collector regressions and passing
canonical/package/whitespace checks. The previous unreleased-source statements
record the state before this authorised publication.

The user will update KBs on the MacBook through its supported plugin manager,
verify installed 1.4.4 and use a fresh chat for the setup trial. No MacBook update
or OAuth reconnection is claimed here. The provider-side registered app display
name and live system-wiki deployment are separate pending operations.
