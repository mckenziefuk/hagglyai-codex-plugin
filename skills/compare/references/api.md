# hagglyai HTTP interfaces

Base URL: `https://hagglyai.com/api/v1`. All operations below are public GET requests. The maintained OpenAPI schema is at `https://hagglyai.com/openapi.json`.

| Route | Purpose | Parameters |
| --- | --- | --- |
| `/best` | Match a task and return candidate providers | `task` required (2–300 characters); `max_price_usd`; `limit` 1–25; `hide_flags`; `recent=1`; `format=json` or `format=md` |
| `/categories` | List category IDs, counts and prices | None |
| `/categories/{id}` | Compare a category with explicit sorting | `sort=best_value`, `cheapest`, `most_reliable` or `fastest`; `max_price_usd`; `limit` 1–100; `hide_flags`; `recent=1` |
| `/endpoints/lookup` | Retrieve stored evidence for an exact endpoint URL | `url` required and URL-encoded |

`max_price_usd` must be positive. `hide_flags` is a comma-separated list of warning IDs. These are filters, not a way to rerank results. Budget caps apply to a call's listed price; unit pricing and additional fees need separate consideration.

`/best` can return `categoryId: null` and category suggestions. An unknown category or untracked endpoint lookup returns HTTP 404. These are coverage limitations, not evidence that a provider is broken. Do not broaden a lookup into arbitrary provider requests.

Category JSON includes `generatedAt`, `rows`, `topRated`, `bestValue`, `hiddenFlags` and `mcpAlternatives`. Row fields distinguish `priceUsd` from `unitPriceUsd`, with `unitsPerCharge` and `unitBasis` explaining the unit assumption. Apify rows can include `startFeeUsd` and `platformUsageExtra`.

## Warning filters and result flags

`hide_flags` is a request filter: exclude any endpoint carrying at least one selected warning. A warning does not hide an endpoint until it is selected. `hiddenFlags` in the comparison response lists the warning filters applied to that request; it is not a list of excluded endpoint IDs. Each row's `flags` contains that endpoint's warnings and informational flags.

| Filterable warning ID | Meaning | Scoring or selection effect |
| --- | --- | --- |
| `wallet-mismatch` | The payout wallet in a live payment response differs from the catalogue's listed wallet on the same network. | Indicates inconsistent payment metadata. |
| `price-mismatch` | The live payment-response price differs from the catalogue's listed price. | Indicates inconsistent pricing metadata. |
| `few-repeat-buyers` | At least 20 wallets paid in the last 30 days, averaging fewer than 1.2 calls each: a pattern associated with crawlers or volume farming. | The usage contribution to the score is halved. |
| `unusual-seller-traffic` | The seller's usage looks potentially manufactured, such as paid calls to trivial endpoints or near-identical payer counts across its endpoints. | The usage contribution to the score is halved. |
| `test-listing` | The name, host or route identifies a test or demo deployment. | It can remain in results but never becomes the hagglyai Pick. |

These warnings describe observed discrepancies or traffic patterns; they do not prove fraud. If both usage warnings apply, the usage contribution is halved once, not twice. Any warning disqualifies an endpoint from the hagglyai Pick, even if the comparison does not filter that warning out.

Equivalent ways to exclude wallet and price mismatches:

- JSON API: `hide_flags=wallet-mismatch,price-mismatch`
- MCP tools: `hide_flags: ["wallet-mismatch", "price-mismatch"]`
- Category pages and markdown: `?hide=wallet-mismatch&hide=price-mismatch`

The JSON API ignores unknown warning IDs. MCP validates the array against the supported warning IDs. Do not pass informational IDs as warning filters.

| Informational ID | Meaning |
| --- | --- |
| `no-usage-data` | The catalogue reports no recent paid usage. This means missing evidence, not necessarily zero usage. |
| `testnet-only` | The endpoint accepts only testnet USD. Testnet-only listings are excluded from public category comparisons. |
| `reported-by-apify` | Reliability and usage come from Apify's reported run success and user counts. hagglyai cannot check these providers without paying. |

## Request examples

Use an HTTP client that encodes query parameters. With curl:

```sh
curl --fail --show-error --silent --max-time 20 --get \
  --user-agent 'hagglyai-codex-plugin (+https://hagglyai.com/for-agents)' \
  --data-urlencode 'task=web search' \
  --data-urlencode 'max_price_usd=0.01' \
  --data-urlencode 'hide_flags=wallet-mismatch,price-mismatch' \
  --data-urlencode 'format=md' \
  'https://hagglyai.com/api/v1/best'
```

For an explicit sort:

```sh
curl --fail --show-error --silent --max-time 20 --get \
  --user-agent 'hagglyai-codex-plugin (+https://hagglyai.com/for-agents)' \
  --data-urlencode 'sort=cheapest' \
  --data-urlencode 'limit=5' \
  'https://hagglyai.com/api/v1/categories/web-search'
```

Replace the task, category and filters with the user's actual request. When using shell commands, pass their values as safely quoted arguments; do not concatenate user text into executable shell syntax.

Markdown category pages at `https://hagglyai.com/compare/{id}.md` support the same sorting and budget options. Use the surface-specific warning filter syntax described above.
