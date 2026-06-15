# 🍏 Apple App Store API: Search, Product Details & Reviews (Python + MCP)

> The efficient, reliable, and developer-friendly way to use the Apple App Store API on Apify, from Python or as an MCP tool in Claude and Cursor.

This is a quick-start for a three-part Apple App Store API suite. The actors chain together: search the store for apps, then pull full product details and user reviews for any result.

**App Store Search API:** [apify.com/johnvc/apple-app-store-search](https://apify.com/johnvc/apple-app-store-search?fpr=9n7kx3) - find apps by keyword, developer, or category.
**App Store Product API:** [apify.com/johnvc/apple-app-store-product-api](https://apify.com/johnvc/apple-app-store-product-api?fpr=9n7kx3) - full product record for an App Store ID.
**App Store Reviews API:** [apify.com/johnvc/apple-app-store-reviews-api](https://apify.com/johnvc/apple-app-store-reviews-api?fpr=9n7kx3) - user reviews for an App Store ID.

Each returns clean, structured JSON. Search results carry the `app_id` you feed into the Product and Reviews APIs to enrich any app. No HTML parsing, no captchas, predictable pay-per-event pricing. Built for App Store Optimization (ASO), competitor analysis, market research, review monitoring, and AI agent workflows.

## Video Walkthrough

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/maxresdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

## Quick Start

### Prerequisites
- Python 3.11 or higher
- An Apify account and API key ([get a free key here](https://apify.com?fpr=9n7kx3))

1. **Clone the repository**
   ```bash
   git clone https://github.com/johnisanerd/Apify-Apple-App-Store-API.git
   cd Apify-Apple-App-Store-API
   ```

2. **Install dependencies with UV**
   ```bash
   # Install UV if you do not have it:
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install project dependencies:
   uv sync
   ```

3. **Configure your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your Apify API key
   # Get your free API key at: https://apify.com?fpr=9n7kx3
   ```

4. **Run the example**
   ```bash
   uv run python apple-app-store-api-example.py
   ```

The example runs the full chain: it searches for meditation apps, takes the top result's `app_id`, then fetches that app's full product record and its latest reviews. Inputs are kept small so your first run stays inexpensive.

### Run the cookbook
A second script, `apple-app-store-api-cookbook.py`, is a catalog of every input plus multi-step workflows (competitor comparison, review-reputation snapshot, price across country stores). It runs one cheap scenario by default:

```bash
uv run python apple-app-store-api-cookbook.py                # search_basic
uv run python apple-app-store-api-cookbook.py reviews_critical
uv run python apple-app-store-api-cookbook.py competitor     # a multi-step workflow
```

### Alternative: set the API key directly
```bash
export APIFY_API_TOKEN="your_api_key_here"
uv run python apple-app-store-api-example.py
```

## Why Use This Apple App Store API?

**Three composable endpoints.** Search returns ranked apps with rich metadata; Product returns the complete app record; Reviews returns user reviews. Each is useful alone and they chain through `app_id`.

**Rich data, already structured.** Ratings, developer, price, category, size, version history, privacy cards, screenshots, supported languages, and sample reviews come back as clean JSON, with no HTML to parse.

**Search by name, developer, or category.** Scope a search to app names or developer names, filter by category and country store, and exclude explicit apps.

**Localized.** The same App Store ID returns different price, availability, and localized text per country store, so you can compare across regions.

**Reliable by design.** API-backed, not browser-driven, so there are no captchas and no layout breakage.

**Predictable pricing.** Pay-per-event billing: a search page, a product record, or a page of reviews each cost a fixed, known amount.

**Agent-ready.** All three actors are available over MCP, so Claude and Cursor can call the Apple App Store API in natural language (setup below).

## Features

### Core Capabilities
- App search by keyword, developer name, or category, across 50+ country stores
- Full product records: developer, description, price, ratings, version history, screenshots, in-app purchases, supported languages, privacy cards, and sample reviews
- User reviews with rating, title, text, author, version, dates, and helpfulness counts
- Single or batch product lookups (up to 100 IDs per run)
- Country and language targeting on every endpoint

### Data Quality
- One app per row on search, one record per ID on product, one review per row on reviews
- Stable, consistent field names across every result
- `app_id` on every search result for easy chaining
- Localized price and metadata per country store

## Usage Examples

### Search for apps
```json
{
  "term": "meditation",
  "num": 5,
  "country": "us"
}
```

### Product details for one or more apps
```json
{
  "product_ids": ["324684580", "https://apps.apple.com/us/app/netflix/id363590051"],
  "include_related_apps": true
}
```

### Reviews for an app (by ID or by name)
```json
{
  "product_ids": ["324684580"],
  "sort": "mostcritical",
  "max_reviews": 50
}
```

## Input Parameters

### App Store Search API
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `term` | `str` | YES | - | Search query (e.g. `meditation`), or a developer name when `property` is `developer`. |
| `country` | `str` | no | `us` | Two-letter country store code. |
| `lang` | `str` | no | `en-us` | Language code in `xx-yy` form, e.g. `fr-fr`, `ja-jp`. |
| `num` | `int` | no | `10` | Apps per page (1-200). Each app returned is billed. |
| `device` | `str` | no | `desktop` | Device class to emulate: `desktop`, `tablet`, `mobile`. |
| `disallow_explicit` | `bool` | no | `false` | Exclude apps flagged explicit. |
| `property` | `str` | no | (app names) | Set to `developer` to search developer names instead. |
| `category_id` | `int` | no | - | Filter by category/genre ID (e.g. `6014` Games, `6017` Education). |
| `max_pages` | `int` | no | `1` | Pages to fetch; `0` = unlimited. |

### App Store Product API
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `product_ids` | `list[str]` | YES | - | App Store IDs or full App Store URLs (1-100 per run). |
| `country` | `str` | no | `us` | Country store; the same ID returns localized price and text per country. |
| `include_reviews_sample` | `bool` | no | `true` | Include the small sample of reviews Apple shows on the product page. |
| `include_related_apps` | `bool` | no | `false` | Include `you_may_also_like` and `more_by_this_developer` lists. |

### App Store Reviews API
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `product_ids` | `list[str]` | one of | - | Numeric App Store IDs to pull reviews for. |
| `app_name` | `str` | one of | - | Resolve an app by name when you do not have the ID. |
| `country` | `str` | no | `us` | Country store (drives review locale). |
| `sort` | `str` | no | `mostrecent` | `mostrecent`, `mosthelpful`, `mostfavorable`, `mostcritical` (iOS only). |
| `max_reviews` | `int` | no | `100` | Maximum reviews per app. Each review returned is billed. |
| `include_macos` | `bool` | no | `true` | Set `false` to skip macOS apps. |

## Output Format

**Search** returns one app per row (the long `description_text` and `release_notes` are present but trimmed here):
```json
{
  "position": 1,
  "app_id": 572966485,
  "title": "Mindfulness: Guided Meditation",
  "bundle_id": "com.gmeditations.audioguides",
  "developer_name": "Hector Rodriguez Fornies",
  "version": "5.14",
  "age_rating": "12+",
  "price_type": "Free",
  "rating_average": 4.67,
  "rating_count": 97,
  "genres": [{ "name": "Health & Fitness", "id": 6013, "primary": true }],
  "size_in_bytes": 135770112,
  "minimum_os_version": "15.0",
  "description_text": "<app description text>",
  "link": "https://apps.apple.com/us/app/id572966485",
  "search_timestamp": "2026-05-30T12:49:14"
}
```

**Product** returns one full record per ID (lists and long text trimmed):
```json
{
  "app_id": 324684580,
  "title": "Spotify: Music and Podcasts",
  "developer_name": "Spotify",
  "category": "Music",
  "rating_average": 4.8,
  "price_text": "Get",
  "size_text": "271.4 MB",
  "age_rating": "13+",
  "description_text": "<app description text>",
  "version_history": [ "...25 entries..." ],
  "rating_distribution": { "5": "...", "4": "...", "3": "...", "2": "...", "1": "..." },
  "review_examples": [ "...sample reviews..." ],
  "privacy_cards": [ "...data categories..." ],
  "in_app_purchases": [ "...tiers..." ],
  "link": "https://apps.apple.com/us/app/id324684580",
  "lookup_country": "us"
}
```

**Reviews** returns one review per row (the `review_text` body is present in your run):
```json
{
  "position_global": 1,
  "review_id": "6274377290",
  "review_title": "Use the App Daily",
  "rating": 5,
  "review_date": "Aug 03, 2020",
  "review_date_iso": "2020-08-03",
  "reviewed_version": "Version 4.31",
  "author_name": "C-lu1958",
  "product_id": "572966485",
  "app_platform": "ios",
  "app_country": "us",
  "sort_order": "mostrecent"
}
```

---

## Use as an MCP tool

You can load the Apple App Store API as an MCP tool so assistants call it for you. The MCP server URL preloads all three actors:

```
https://mcp.apify.com/?tools=actors,docs,johnvc/apple-app-store-search,johnvc/apple-app-store-product-api,johnvc/apple-app-store-reviews-api
```

Authenticate with OAuth in the browser when offered, or with your Apify API token (the same `APIFY_API_TOKEN` used by the Python example). Get a token at https://console.apify.com/settings/integrations and a free Apify account at https://apify.com?fpr=9n7kx3 .

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the Apple App Store API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings → Connectors** (or **Settings → Developer → Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with the three App Store actors:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/apple-app-store-search,johnvc/apple-app-store-product-api,johnvc/apple-app-store-reviews-api"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the Apple App Store API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the App Store API's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/apple-app-store-search,johnvc/apple-app-store-product-api,johnvc/apple-app-store-reviews-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/apple-app-store-search,johnvc/apple-app-store-product-api,johnvc/apple-app-store-reviews-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the Apple App Store API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable the App Store API tools.

1. Go to **Settings → Connectors → Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tools `johnvc/apple-app-store-search`, `johnvc/apple-app-store-product-api`, and `johnvc/apple-app-store-reviews-api`.
3. In any chat, open **+ → Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/apple-app-store-search,johnvc/apple-app-store-product-api,johnvc/apple-app-store-reviews-api`, using OAuth when prompted.
5. Ask Claude to run the Apple App Store API.

Open Claude on the web: https://claude.ai

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/apple-app-store-search,johnvc/apple-app-store-product-api,johnvc/apple-app-store-reviews-api"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/apple-app-store-search,johnvc/apple-app-store-product-api,johnvc/apple-app-store-reviews-api",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor → Settings → MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the Apple App Store API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/apple-app-store-search,johnvc/apple-app-store-product-api,johnvc/apple-app-store-reviews-api`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp

---

[**Made with care**](https://apify.com/johnvc?fpr=9n7kx3)

*Use the Apple App Store API to power ASO, competitor analysis, market research, and review monitoring with reliable, structured results.*

Last Updated: 2026.06.15
