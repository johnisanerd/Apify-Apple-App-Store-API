"""
Example: call the Apple App Store API Apify Actors from Python.

This is a suite of three actors that chain together:

  1. apple-app-store-search      -> find apps by keyword, developer, or category
  2. apple-app-store-product-api -> full details for an App Store ID
  3. apple-app-store-reviews-api -> user reviews for an App Store ID

This script runs the full chain: it searches for an app, takes the top result's
App Store ID, then fetches that app's full product record and a few of its
latest reviews. Inputs are kept small so your first run stays inexpensive.

For a catalog of every input and many more use cases (competitor analysis,
review monitoring, price comparison across countries, and more), see
apple-app-store-api-cookbook.py.

Get your free Apify API key at: https://apify.com?fpr=9n7kx3
Set it in a .env file (see .env.example) or export APIFY_API_TOKEN.
"""

import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
if not APIFY_API_TOKEN:
    raise SystemExit(
        "APIFY_API_TOKEN is not set. Copy .env.example to .env and add your key, "
        "or run: export APIFY_API_TOKEN=your_api_key_here"
    )

client = ApifyClient(APIFY_API_TOKEN)

SEARCH = "johnvc/apple-app-store-search"
PRODUCT = "johnvc/apple-app-store-product-api"
REVIEWS = "johnvc/apple-app-store-reviews-api"

# ---------------------------------------------------------------------------
# 1. SEARCH: find apps for a keyword. Each result row is one app, already rich
#    with metadata. Inputs are kept small (num=3, one page) to keep cost low;
#    each app returned is billed.
# ---------------------------------------------------------------------------
search_input = {"term": "meditation", "num": 3, "max_pages": 1, "country": "us"}
print(f"1. Searching the App Store for: {search_input['term']}")
search_run = client.actor(SEARCH).call(run_input=search_input)
if search_run is None:
    raise SystemExit("The search Actor did not start. Check your API token and inputs.")

apps = list(client.dataset(search_run.default_dataset_id).iterate_items())
print(f"   Found {len(apps)} apps:")
for app in apps:
    print(
        f"   - {app.get('title')} by {app.get('developer_name')} "
        f"(rating {app.get('rating_average')}, {app.get('rating_count')} ratings) "
        f"id={app.get('app_id')}"
    )

first_id = apps[0].get("app_id") if apps else None
if first_id is None:
    raise SystemExit("No apps returned, nothing to enrich.")
print(f"\n   Enriching the top result (id={first_id})...\n")

# ---------------------------------------------------------------------------
# 2. PRODUCT DETAILS: the full record for that App Store ID. Pass a list of IDs
#    (or App Store URLs) to look up several apps in one run.
# ---------------------------------------------------------------------------
print("2. Fetching the full product record...")
product_run = client.actor(PRODUCT).call(
    run_input={"product_ids": [str(first_id)], "country": "us", "include_reviews_sample": True}
)
products = list(client.dataset(product_run.default_dataset_id).iterate_items())
if products:
    p = products[0]
    print(f"   {p.get('title')} | {p.get('category')} | {p.get('developer_name')}")
    print(
        f"   rating {p.get('rating_average')} | {p.get('price_text')} | "
        f"{p.get('size_text')} | {p.get('age_rating')}"
    )
    print(f"   version history entries: {len(p.get('version_history') or [])}")
    print(f"   sample reviews on the product page: {len(p.get('review_examples') or [])}")
    print(f"   App Store link: {p.get('link')}\n")

# ---------------------------------------------------------------------------
# 3. REVIEWS: the most recent user reviews for that same app. max_reviews is
#    kept small to keep the run cheap; each review returned is billed.
# ---------------------------------------------------------------------------
print("3. Fetching the most recent reviews...")
reviews_run = client.actor(REVIEWS).call(
    run_input={"product_ids": [str(first_id)], "sort": "mostrecent", "max_reviews": 5}
)
reviews = list(client.dataset(reviews_run.default_dataset_id).iterate_items())
print(f"   Got {len(reviews)} reviews. The latest few:")
for r in reviews[:5]:
    title = r.get("review_title") or "(no title)"
    author = r.get("author_name") or "(anonymous)"
    print(f"   - {r.get('rating')}/5  {title}  by {author}")
