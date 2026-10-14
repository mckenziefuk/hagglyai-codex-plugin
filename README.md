# hagglyai for Codex

Find and compare agent API providers using listed prices, availability, latency and usage evidence, with platform and task sub-category filters. This package includes the `hagglyai:compare` skill and hagglyai’s hosted read-only MCP server at `https://hagglyai.com/mcp`.

hagglyai queries require no account, API key, OAuth setup or payment. Provider fees and accounts are separate. Comparisons do not execute paid provider requests, fund wallets or make payments.

## Install locally

With a current Codex client that supports plugins, run:

```sh
codex plugin marketplace add /home/fraser/Work/hagglyai-codex-plugin
codex plugin add hagglyai@hagglyai-codex-plugins
```

Replace the absolute path if you move this folder. Start a fresh Codex session, select the installed comparison skill, or ask:

> Use hagglyai to find web-search APIs under $0.01 per call and explain the tradeoffs.

Other examples:

- Compare weather API providers using listed prices and recent reliability.
- List the API categories hagglyai covers.
- Check the listed price and recent checks for https://stableenrich.dev/api/exa/search.
- Compare Instagram comment providers, limited to x402-labelled endpoints.
- Find YouTube transcript providers and explain which platform and task filters were applied.

Avoid enabling a duplicate hagglyai MCP connection if you already configured one manually. Client plugin support and installation controls vary by surface and workspace policy.

## Install from GitHub

From [mckenziefuk/hagglyai-codex-plugin](https://github.com/mckenziefuk/hagglyai-codex-plugin), run:

```sh
codex plugin marketplace add mckenziefuk/hagglyai-codex-plugin
codex plugin add hagglyai@hagglyai-codex-plugins
```

The repository is public and can be installed without a GitHub account.

## Package contents

- `plugin.json` and `mcp.json`: portable Agent Plugins manifest and Streamable HTTP configuration.
- `.codex-plugin/plugin.json` and `.mcp.json`: Codex compatibility package with presentation fields and explicit component paths.
- `.agents/plugins/marketplace.json`: marketplace for testing and distribution.
- `skills/compare/`: comparison workflow and HTTP fallback reference.
- `assets/icon.png`: hagglyai icon used in the composer and listing.

Both package formats use the same identity, version, metadata, skill and public server. The OpenAI extension in the portable manifest is authoritative when a host supports that format; the compatibility files support Codex clients using its existing package format.

## Tools and data

| Tool | Purpose |
| --- | --- |
| `find_best` | Infer a category and sub-categories from a task, optionally within a per-call budget |
| `compare_category` | Compare a category with optional platform, task and paid-rail filters |
| `check_endpoint` | Read stored evidence for an exact tracked URL |
| `list_categories` | Discover categories, pricing summaries and available platform/task IDs |

## Sub-category comparisons

Discover current platform and task IDs with `list_categories`, then pass arrays to `compare_category`. For example, `platform: ["instagram", "tiktok"]` with `task: ["comments"]` matches comments on either platform. Platform and task restrictions combine; each array can match any of its values. The platform facet may be labelled Model, Chain, Search engine or another category-specific name, while the tool parameter remains `platform`.

`rail: ["x402"]` and `rail: ["apify"]` select the paid provider rail; omit it to include both. These filters apply to paid rows, while separately listed MCP alternatives remain category-wide. `find_best` infers sub-categories from request text and can widen an empty result, so the skill checks what was actually applied and preserves explicit user restrictions.

Sub-category support also requires the updated backend to be deployed at the configured MCP URL. Older servers expose the original schema. The skill checks availability and reports missing filter support instead of treating broader results as matching a restriction. See [the API reference](skills/compare/references/api.md) for filter formats and result fields.

All tools read catalogue data. Task descriptions, endpoint URLs and filters supplied to the tools are sent to `hagglyai.com`. Unpaid checks do not prove paid-response quality. Apify can have additional usage fees, and MCP alternatives can have unpublished pricing.

See [Privacy Policy](https://hagglyai.com/privacy), [Terms of Service](https://hagglyai.com/terms), [methodology](https://hagglyai.com/how-we-test) and the [maintained OpenAPI contract](https://hagglyai.com/openapi.json).

## Validation and publication

See [docs/REVIEW.md](docs/REVIEW.md) for access instructions, validation evidence and remaining review work. This is a local draft; the package has not been submitted to OpenAI.

The manifests include eight positive and five negative review scenarios, including sub-category discovery, combined filters and unsupported IDs. These are reviewer expectations, not a claim that every scenario has been exercised through a Codex conversation.

Official references: [Package your plugin](https://developers.openai.com/plugins/build/plugins), [Submit your plugin](https://developers.openai.com/plugins/deploy/submission).

## License and support

Plugin files are [MIT licensed](LICENSE). hagglyai’s name and logo identify the service and do not grant trademark rights. Support: [hello@hagglyai.com](mailto:hello@hagglyai.com).
