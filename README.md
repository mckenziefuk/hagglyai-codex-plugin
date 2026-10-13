# Haggly for Codex

Find and compare agent API providers using listed prices, availability, latency and usage evidence. This package includes the `haggly:compare` skill and Haggly’s hosted read-only MCP server at `https://hagglyai.com/mcp`.

Haggly queries require no account, API key, OAuth setup or payment. Provider fees and accounts are separate. Comparisons do not execute paid provider requests, fund wallets or make payments.

## Install locally

With a current Codex client that supports plugins, run:

```sh
codex plugin marketplace add /home/fraser/Work/haggly-codex-plugin
codex plugin add haggly@haggly-codex-plugins
```

Replace the absolute path if you move this folder. Start a fresh Codex session, select the installed comparison skill, or ask:

> Use Haggly to find web-search APIs under $0.01 per call and explain the tradeoffs.

Other examples:

- Compare weather API providers using listed prices and recent reliability.
- List the API categories Haggly covers.
- Check the listed price and recent checks for https://stableenrich.dev/api/exa/search.

Avoid enabling a duplicate Haggly MCP connection if you already configured one manually. Client plugin support and installation controls vary by surface and workspace policy.

## Install from the private review repository

With GitHub access to [mckenziefuk/haggly-codex-plugin](https://github.com/mckenziefuk/haggly-codex-plugin), run:

```sh
codex plugin marketplace add mckenziefuk/haggly-codex-plugin
codex plugin add haggly@haggly-codex-plugins
```

Your Git client must already be authenticated to GitHub. Only users with access to the private repository can install from it.

## Package contents

- `plugin.json` and `mcp.json`: portable Agent Plugins manifest and Streamable HTTP configuration.
- `.codex-plugin/plugin.json` and `.mcp.json`: Codex compatibility package with presentation fields and explicit component paths.
- `.agents/plugins/marketplace.json`: local marketplace for testing and private distribution.
- `skills/compare/`: comparison workflow and HTTP fallback reference.
- `assets/icon.png`: Haggly icon used in the composer and listing.

Both package formats use the same identity, version, metadata, skill and public server. The OpenAI extension in the portable manifest is authoritative when a host supports that format; the compatibility files support Codex clients using its existing package format.

## Tools and data

| Tool | Purpose |
| --- | --- |
| `find_best` | Find providers for a task, optionally within a per-call budget |
| `compare_category` | Compare providers in a named category |
| `check_endpoint` | Read stored evidence for an exact tracked URL |
| `list_categories` | List supported categories and pricing summaries |

All tools read catalogue data. Task descriptions, endpoint URLs and filters supplied to the tools are sent to `hagglyai.com`. Unpaid checks do not prove paid-response quality. Apify can have additional usage fees, and MCP alternatives can have unpublished pricing.

See [Privacy Policy](https://hagglyai.com/privacy), [Terms of Service](https://hagglyai.com/terms), [methodology](https://hagglyai.com/how-we-test) and the [maintained OpenAPI contract](https://hagglyai.com/openapi.json).

## Validation and publication

See [docs/REVIEW.md](docs/REVIEW.md) for access instructions, validation evidence and remaining review work. This is a local draft; the package has not been submitted to OpenAI.

The manifests include five positive and three negative review scenarios. These are reviewer expectations, not a claim that every scenario has been exercised through a Codex conversation.

Official references: [Package your plugin](https://developers.openai.com/plugins/build/plugins), [Submit your plugin](https://developers.openai.com/plugins/deploy/submission).

## License and support

Plugin files are [MIT licensed](LICENSE). Haggly’s name and logo identify the service and do not grant trademark rights. Support: [hello@hagglyai.com](mailto:hello@hagglyai.com).
