#!/usr/bin/env python3
"""Check the package and, with --live, its public read-only service. No dependencies."""

import argparse
import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import struct
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://hagglyai.com"
CHECKS = []


def check(name, action):
    try:
        details = action()
        CHECKS.append({"name": name, "status": "passed", "details": details})
    except Exception as error:
        CHECKS.append({"name": name, "status": "failed", "details": str(error)})


def require(condition, message):
    if not condition:
        raise ValueError(message)


def package():
    portable = json.loads((ROOT / "plugin.json").read_text())
    native = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
    ext = portable["extensions"]["com.openai"]
    require(ext["interface"] == native["interface"], "Listing metadata differs between manifests")
    require(ext["review"] == native["extensions"]["com.openai"]["review"], "Review materials differ")
    require(ext["publication"] == native["extensions"]["com.openai"]["publication"], "Publication metadata differs")
    for key in ("name", "version", "description", "author", "homepage", "repository"):
        require(portable[key] == native[key], f"Manifest mismatch: {key}")
    interface = native["interface"]
    for field, maximum in [("displayName", 30), ("shortDescription", 30), ("longDescription", 4000), ("developerName", 80)]:
        value = interface[field]
        require(isinstance(value, str) and 0 < len(value) <= maximum, f"Invalid {field}")
        require(field == "longDescription" or "\n" not in value, f"Multiline {field}")
    prompts = interface["defaultPrompt"]
    require(len(prompts) <= 3 and len(set(prompts)) == len(prompts), "Invalid starter prompts")
    require(all(0 < len(p) <= 128 and "\n" not in p and "@" not in p for p in prompts), "Invalid starter prompt")
    for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        value = interface[field]
        parsed = urllib.parse.urlsplit(value)
        require(parsed.scheme == "https" and parsed.hostname and not parsed.username and len(value) <= 1024, f"Invalid {field}")
    review = ext["review"]["test_cases"]
    require(len(review["positive"]) == 5 and len(review["negative"]) == 3, "MCP review needs exactly five positive and three negative cases")
    for case in review["positive"] + review["negative"]:
        require(all(case.get(field) for field in ("description", "prompt", "expected_behavior")), "Incomplete review case")
    require(all(case.get("tools_triggered") for case in review["positive"]), "Positive case needs tools_triggered")
    for field in ("logo", "composerIcon"):
        image = ROOT / interface[field]
        data = image.read_bytes()
        require(data[:8] == b"\x89PNG\r\n\x1a\n", "Expected a PNG asset")
        width, height = struct.unpack(">II", data[16:24])
        require(width == height and 256 <= width <= 4096 and len(data) <= 5 * 1024 * 1024, f"Invalid {field} dimensions or size")
    servers = json.loads((ROOT / "mcp.json").read_text())["mcpServers"]
    compat = json.loads((ROOT / ".mcp.json").read_text())["mcpServers"]
    require(list(servers) == list(compat) == ["hagglyai"], "Expected exactly one bundled server")
    require(servers["hagglyai"]["url"] == compat["hagglyai"]["url"] == BASE + "/mcp", "Unexpected server URL")
    return {"version": native["version"], "positiveCases": 5, "negativeCases": 3, "iconPixels": [width, height]}


def fetch(path, payload=None):
    headers = {"User-Agent": "hagglyai-plugin-submission-validation (+https://hagglyai.com/for-agents)"}
    data = None
    if payload is not None:
        headers.update({"Content-Type": "application/json", "Accept": "application/json, text/event-stream"})
        data = json.dumps(payload).encode()
    with urllib.request.urlopen(urllib.request.Request(BASE + path, data=data, headers=headers), timeout=30) as response:
        require(response.status == 200, f"HTTP {response.status}")
        require(urllib.parse.urlsplit(response.url).hostname == "hagglyai.com", "Unexpected redirect host")
        return response.read()


def rpc(method, params):
    body = fetch("/mcp", {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).decode()
    if body.lstrip().startswith("{"):
        reply = json.loads(body)
    else:
        reply = json.loads(next(line[6:] for line in body.splitlines() if line.startswith("data: ")))
    require("error" not in reply, str(reply.get("error")))
    return reply["result"]


def call(name, arguments):
    result = rpc("tools/call", {"name": name, "arguments": arguments})
    require(not result.get("isError"), f"{name} returned a tool error")
    text = "\n".join(c.get("text", "") for c in result.get("content", []))
    require(bool(text.strip()), f"Empty response: {name}")
    return text


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.ignored = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.ignored += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.ignored -= 1

    def handle_data(self, data):
        if not self.ignored:
            self.parts.append(data)


def page(path, expected):
    body = fetch(path)
    parser = VisibleText()
    parser.feed(body.decode())
    text = " ".join(parser.parts)
    require(all(value.lower() in text.lower() for value in expected), "Expected page content missing")
    return {"url": BASE + path, "httpStatus": 200, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "contentChecks": expected}


def live_filters():
    tools = {t["name"]: t for t in rpc("tools/list", {})["tools"]}
    require(set(tools) == {"find_best", "compare_category", "check_endpoint", "list_categories"}, "Unexpected tool list")
    fields = tools["compare_category"]["inputSchema"]["properties"]
    require(all(f in fields for f in ("platform", "task", "rail")), "Production filter schema is missing")
    spec = json.loads(fetch("/openapi.json"))
    params = {p["name"] for p in spec["paths"]["/categories/{id}"]["get"]["parameters"]}
    require({"platform", "task", "rail"} <= params, "OpenAPI filter parameters missing")
    categories = json.loads(fetch("/api/v1/categories"))["categories"]
    social = next(c for c in categories if c["id"] == "social-media")
    facets = {f["facet"]: {v["id"] for v in f["values"]} for f in social["subcategories"]}
    require({"instagram", "tiktok"} <= facets["platform"] and "comments" in facets["task"], "Example IDs no longer discoverable")
    discovery = call("list_categories", {})
    require("instagram" in discovery and "comments" in discovery, "MCP facet discovery missing")
    comparisons = []
    for rail in ("x402", "apify"):
        query = urllib.parse.urlencode({"platform": "instagram,tiktok", "task": "comments", "rail": rail, "limit": 5})
        result = json.loads(fetch("/api/v1/categories/social-media?" + query))
        require(set(result["selected"]["platforms"]) == {"instagram", "tiktok"} and result["selected"]["tasks"] == ["comments"], "HTTP selected filters differ")
        require(bool(result["rows"]), f"No rows to verify for {rail}")
        for row in result["rows"]:
            require(row["rail"] == rail and set(row["platforms"]) & {"instagram", "tiktok"} and "comments" in row["tasks"], "A row violates the requested filters")
        markdown = call("compare_category", {"category": "social-media", "platform": ["instagram", "tiktok"], "task": ["comments"], "rail": [rail], "limit": 3})
        require(all(word in markdown.lower() for word in ("instagram", "tiktok", "comments", rail)), "MCP comparison omits applied filters")
        comparisons.append({"rail": rail, "rowsVerified": len(result["rows"]), "mcpResponseSha256": hashlib.sha256(markdown.encode()).hexdigest()})
    best = call("find_best", {"task": "web search", "max_price_usd": 0.01})
    endpoint = call("check_endpoint", {"url": "https://stableenrich.dev/api/exa/search"})
    require("does not track" not in endpoint.lower(), "Review endpoint no longer tracked")
    missing = {name: [key for key in ("readOnlyHint", "openWorldHint", "destructiveHint") if key not in tool.get("annotations", {})] for name, tool in tools.items()}
    missing = {name: keys for name, keys in missing.items() if keys}
    if missing:
        CHECKS.append({"name": "Production tool annotations", "status": "needs_action", "details": missing})
    return {"toolsCalled": list(tools), "comparisons": comparisons, "bestResponseSha256": hashlib.sha256(best.encode()).hexdigest(), "endpointResponseSha256": hashlib.sha256(endpoint.encode()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Make public read-only HTTP and MCP requests")
    parser.add_argument("--output", type=Path, help="Write timestamped JSON evidence")
    args = parser.parse_args()
    check("Package metadata and assets", package)
    if args.live:
        for path, expected in [("/", ["Haggly", "API"]), ("/for-agents", ["MCP", "Sub-categories"]), ("/privacy", ["Privacy Policy", "Fraser McKenzie", "hello@hagglyai.com", "/mcp"]), ("/terms", ["Terms of Service", "Fraser McKenzie", "hello@hagglyai.com", "/mcp"])]:
            check("Listing page " + path, lambda p=path, e=expected: page(p, e))
        check("Production MCP and HTTP filters", live_filters)
    report = {"checkedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(), "scope": "Package and direct protocol checks; does not verify model behavior, publisher identity, domain ownership, portal scans or demo video", "checks": CHECKS}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return int(any(c["status"] == "failed" for c in CHECKS))


if __name__ == "__main__":
    raise SystemExit(main())
