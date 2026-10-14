# Reviewer access and submission status

## Access instructions for the review form

Connect to `https://hagglyai.com/mcp` using Streamable HTTP. No signup, account, credentials, OAuth, client ID, API key, wallet or payment is required. The full public catalogue is available immediately. All four tools are read-only and return stored evidence; `check_endpoint` does not call the supplied provider URL.

Call `list_categories` with `{}`. Call `find_best` with `{"task":"web search","max_price_usd":0.01}`. Call `compare_category` with `{"category":"web-search","limit":3}`. Call `check_endpoint` using an exact URL from those results, for example `{"url":"https://stableenrich.dev/api/exa/search"}`.

For sub-category coverage, discover the current `social-media` IDs with `list_categories`, then use `{"category":"social-media","platform":["instagram","tiktok"],"task":["comments"],"rail":["x402"],"limit":3}` when those values are offered. The service now advertises all three filters. Verify the applied filters in its answer. Category-wide MCP alternatives are not filtered by these restrictions.

Catalogue entries and observed prices can change. Assess results by their field semantics and evidence, rather than expecting fixed rankings or counts.

## Version 0.2.1 package corrections

- Rebuilt `assets/icon.png` as a 512 × 512 PNG from the robot mark in the original Haggly brand artwork, preserving the navy background and padding. The package uses this asset for both its logo and composer icon. This satisfies the reported 256px requirement without enlarging the old 180px export.
- Selected exactly five positive and three negative cases for initial MCP review. The other proposed cases are retained in `additional-review-cases.json`.
- Removed empty screenshot declarations. This text-only MCP server provides no custom UI, so submission screenshots are not needed.
- Added `scripts/validate_submission.py` and a recording plan in `DEMO.md`.

For this update, the native Codex app-server `plugin/read` loaded the local package, discovered `hagglyai:compare` and recognized the bundled MCP server. The skill validator, package checks and Git whitespace checks passed. The refreshed ZIP was checked for integrity and matching file contents.

The OpenAI submission documentation currently lists a 48px minimum for square icons; this package also exceeds the stricter 256px finding supplied during review.

## Production feature mismatch resolved

The earlier 14 October check saw a production tool schema without platform/task/rail filters. A fresh production check later on 14 October 2026 confirmed those fields in `compare_category`, the category-specific discovery values, and corresponding OpenAPI parameters. The old rollout blocker no longer applies.

The validation report at `validation/2026-10-14.json` records the timestamp and direct checks. Filtered JSON responses were checked row by row for matching platform, task and rail. Both x402 and Apify comparisons and all four MCP tools were exercised. These are protocol checks, not evidence of a model following the skill in a conversation.

## Listing URLs checked

On 14 October 2026, all four listing URLs returned HTTP 200 from this environment:

| Listing field | URL | Content checked |
| --- | --- | --- |
| Website | https://hagglyai.com | Haggly API comparison product |
| Support | https://hagglyai.com/for-agents | Integration guide with MCP and filter instructions; contact link to hello@hagglyai.com |
| Privacy | https://hagglyai.com/privacy | Hagglyai Privacy Policy, covering the public API and MCP, identifying Fraser McKenzie trading as Hagglyai, with a privacy contact |
| Terms | https://hagglyai.com/terms | Hagglyai Terms of Service, covering the public API and MCP, identifying the same operator and contact |

The report includes response hashes and content checks. Reachability and relevant content were confirmed; this is not a legal compliance assessment or a guarantee that another crawler can reach the pages. Re-run before uploading if the service changes.

## Remaining server annotation work

The production tool list has `readOnlyHint: true` and `openWorldHint: false`, but all four tools omit an explicit `destructiveHint`. Current OpenAI MCP review rules require all three hints and a justification for each in the submission workflow.

In the Haggly backend, the shared helper in `src/mcp/server.ts` can explicitly declare the existing behavior:

```ts
const readOnly = (title: string) => ({
  title,
  readOnlyHint: true,
  openWorldHint: false,
  destructiveHint: false,
});
```

Deploy that server change, refresh the portal's production scan, and confirm the annotation values there. Updating this plugin ZIP does not change hosted tool annotations. Do not invent a custom MCP annotation field for the portal justifications; enter the explanations where the portal requests them.

Suggested explanations to check against actual behavior:

- Read-only: each tool reads Haggly's stored catalogue, comparison or probe evidence and cannot mutate provider records or user resources.
- Closed-world: tool requests operate on Haggly's indexed records. An endpoint URL is a lookup key; `check_endpoint` does not fetch or execute it. Provider links in results are data.
- Non-destructive: no tool can delete resources, modify records, fund a wallet, process payments or execute paid provider requests.

## Publisher and publication settings

The package identity is `hagglyai`; the draft `author.name` and `interface.developerName` also say `hagglyai`. This is branding metadata, not proof of a verified publisher. The portal sets the public developer name from the selected verified individual or business identity, regardless of the name in the ZIP.

Confirm the exact verified public name and select the owning organization and project in the portal. If publishing as an individual, use the name actually verified there. If publishing as a business, verify that business first. The site's legal pages identify Fraser McKenzie trading as Hagglyai; that does not establish which identity is verified in the OpenAI portal. Align package metadata with the selected identity once confirmed.

Publication country restrictions and translations are omitted; this preserves existing portal targeting on updates. Confirm intended countries, category, listing URLs and policy attestations in the portal. No acceptance of terms, submission or publication has been performed by this update.

## Conversation testing and recording still required

Install the package and exercise the five positive and three negative submission cases through actual Codex and supported ChatGPT conversations. Check both a fresh session and installation during an existing session. Save the real conversation outcomes. Manifest scenarios and direct MCP tests do not establish model behavior, including how it handles unsupported payment or deletion requests.

Follow `DEMO.md` to record the walkthrough. No actual client walkthrough has been recorded or linked. Add its real, reviewer-accessible URL as `extensions.com.openai.review.demo_recording_url` in both manifests, or enter it in the portal when that field is editable. The field is intentionally absent until a real recording exists.

## Upload and portal-only checks

Use the OpenAI plugin submission dashboard's **With MCP** workflow. Select the verified publisher and ownership settings, upload the refreshed ZIP, and wait for metadata and skill checks. Complete the exact domain-verification challenge supplied by the portal; no verification token is present in this repository. Run a current MCP scan after any server changes and resolve its findings, including the annotation justifications. This public server needs no demo credentials.

Review the MIT license, publisher details, listing category, support link and policy URLs before publication. The public repository is https://github.com/mckenziefuk/hagglyai-codex-plugin. Both manifests include its URL.

## Earlier validation

On 13 October 2026, Codex CLI 0.162.1's native app-server `plugin/read` read the local marketplace, discovered `hagglyai:compare`, resolved its images and recognized its MCP server. Skill validation and direct calls to all four tools passed; unknown-category and untracked-endpoint coverage messages were checked.

On 14 October 2026, the 0.2.0 skill validation and native package read passed. The Haggly feature checkout passed TypeScript checking and all seven existing sub-category integration tests using local test data with remote bindings disabled. These checks are historical context, separate from the 0.2.1 live report.

Official references: [Upload and submit your plugin](https://developers.openai.com/plugins/deploy/submission), [submission error reference](https://developers.openai.com/plugins/deploy/submission-errors), and [package your plugin](https://developers.openai.com/plugins/build/plugins).
