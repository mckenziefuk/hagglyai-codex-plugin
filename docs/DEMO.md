# Record the submission walkthrough

A real reviewer-accessible recording is still required. This guide is a recording plan, not a video or evidence that the scenarios passed. Do not add a placeholder URL to either manifest.

## Prepare the conversation

Install this package using the README, then start a fresh Codex conversation. Also test it in ChatGPT if that is a supported submission surface. Confirm the installed version is 0.2.1 and only one Haggly MCP connection is enabled. Show the plugin and its available tools. Queries are free; no login or reviewer credentials are needed.

Record the client window with its real prompts, tool calls and answers visible. Keep unrelated windows and account settings out of the recording. A terminal-only HTTP test establishes protocol behavior; it does not replace the conversation walkthrough.

## Walk through the five positive cases

Use the exact prompts in `extensions.com.openai.review.test_cases.positive` in either manifest. Show:

1. Category discovery, including current platform/task IDs and seller counts.
2. Web-search discovery under $0.01 per call and an endpoint check. Distinguish per-call prices, unit prices and additional fees.
3. A three-provider web-search comparison using stored price and reliability evidence.
4. An exact tracked endpoint check. Explain that it reads stored probes and does not execute the paid endpoint.
5. Instagram or TikTok comments, limited to x402. Show discovery followed by arrays for platform, task and rail. Verify the filters shown in the answer; separately listed MCP alternatives are category-wide.

The walkthrough should show all four tools: `list_categories`, `find_best`, `compare_category` and `check_endpoint`. Rankings and endpoint counts can change; inspect actual evidence rather than rehearsing a fixed answer. If a case fails, fix it and repeat that case before recording it as passed.

## Walk through the three negative cases

Use the exact negative prompts in the manifests:

1. Deleting providers: the plugin cannot mutate the catalogue.
2. Paying for and running a search: the plugin has no payment or provider-execution tool.
3. Requiring an unknown task ID: report the unsupported requirement rather than treating broader results as matches.

`docs/additional-review-cases.json` retains the other proposed scenarios for additional coverage. These are not imported into the five/three submission lists.

## Publish the recording and link it

Upload the actual recording to your chosen video host, enable access without a reviewer account or invitation, and open the link in a signed-out browser. Do not publish local paths, a draft share link or an invented URL.

Set `extensions.com.openai.review.demo_recording_url` to that real HTTPS URL in both `plugin.json` and `.codex-plugin/plugin.json`. Alternatively, leave that optional ZIP field absent and enter the recording in the dashboard if it is editable there. Rebuild the ZIP after changing the manifests.

Record the date, client versions, conversation links or transcript locations, actual outcomes and recording URL in the submission notes. No conversation results have been marked as passed by this package update.
