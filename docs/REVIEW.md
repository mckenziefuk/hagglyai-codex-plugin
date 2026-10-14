# Reviewer access and validation

## Access instructions for the review form

Connect to `https://hagglyai.com/mcp` using Streamable HTTP. No signup, account, credentials, OAuth, client ID, API key, wallet or payment is required. The full public catalogue is available immediately. All four tools are read-only and return stored evidence; `check_endpoint` does not call the supplied provider URL.

Call `list_categories` with `{}`. Call `find_best` with `{"task":"web search","max_price_usd":0.01}`. Call `compare_category` with `{"category":"web-search","limit":3}`. Call `check_endpoint` using an exact URL from those results, for example `{"url":"https://stableenrich.dev/api/exa/search"}`.

For sub-category coverage, first verify that `compare_category` advertises `platform`, `task` and `rail`. Discover the `social-media` IDs with `list_categories`, then try `{"category":"social-media","platform":["instagram"],"task":["comments"],"rail":["x402"],"limit":3}` when those values are offered. Also try `find_best` with `{"task":"YouTube transcripts"}` and check the matched category and any automatic widening.

Catalogue entries and observed prices can change. Assess results by their field semantics and evidence, rather than expecting fixed rankings or counts.

## Checks completed

On 13 October 2026:

- Codex CLI 0.162.1’s app-server `plugin/read` successfully read the local marketplace and plugin, discovered `hagglyai:compare`, resolved the image paths and recognized the `hagglyai` MCP server.
- The skill-creator validator passed for `skills/compare`.
- MCP initialization and tool discovery succeeded without credentials. All four advertised tools returned populated responses without tool errors in direct protocol calls.
- A weather category comparison returned populated results. An unknown category returned the expected tool error, and an untracked endpoint returned the expected coverage message.

On 14 October 2026, for the 0.2.0 update:

- The native Codex app-server `plugin/read` resolved the local marketplace, discovered the updated `hagglyai:compare` skill and recognized the bundled `hagglyai` MCP server.
- The skill-creator validator and Git whitespace checks passed.
- Haggly's feature checkout passed TypeScript checking and all seven existing `test/integration/subcategories.test.ts` tests. These test tagging, discovery thresholds, filter combinations, automatic narrowing and response formats against local test data, with remote bindings disabled.

## Sub-category rollout

The 0.2.0 package follows the sub-category contract in Haggly's `worktree-more-sources` checkout at commit `6230538`: category discovery, `compare_category` platform/task/rail arrays, automatic `find_best` narrowing, and the corresponding JSON formats.

On 14 October 2026, the production `https://hagglyai.com/mcp` tool list still exposed the older `compare_category` schema without `platform`, `task` or `rail`. The backend feature must be deployed before this package can exercise those filters against production. Packaging changes do not deploy or change the server. Refresh MCP discovery in a new client session after the deployment, then repeat the filtered comparisons and review scenarios.

## Checks before directory submission

Install the package and exercise its eight positive and five negative scenarios through actual Codex or ChatGPT conversations. Check both a fresh session and installation during an existing session. The manifest scenarios are proposed review cases; direct MCP tests do not establish model behavior, such as refusing an unsupported payment or deletion request.

Record an accessible video walkthrough and enter its real URL as `extensions.com.openai.review.demo_recording_url` in both manifests. No demonstration video has been recorded or linked yet.

Upload the ZIP through the OpenAI plugin submission dashboard using the MCP workflow. Select the correct publisher organization and project, resolve automated validation findings, enter the access instructions above in the secure review form, and complete the dashboard’s ownership verification and submission fields. No reviewer credentials are needed for hagglyai. Public submission has not been performed.

Review the MIT license, publisher details, listing category, support link and policy URLs before publication. The public repository is https://github.com/mckenziefuk/hagglyai-codex-plugin. Both manifests include its URL.

The package uses an existing 180 × 180 square PNG for its listing logo and composer icon. It has no hooks, installation scripts, dependencies or local server.

Official sources: https://developers.openai.com/plugins/build/plugins and https://developers.openai.com/plugins/deploy/submission.
