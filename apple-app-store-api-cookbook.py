"""
Apple App Store API: Thorough Examples Cookbook

A catalog of ready-to-run examples for the three-actor Apple App Store suite:

  SEARCH   johnvc/apple-app-store-search       find apps by keyword, developer, or category
  PRODUCT  johnvc/apple-app-store-product-api  full product record for an App Store ID
  REVIEWS  johnvc/apple-app-store-reviews-api  user reviews for an App Store ID

It covers every input each actor exposes, plus three multi-step workflows that
chain them: competitor analysis, review-reputation monitoring, and price
comparison across country stores.

COST NOTE: these actors bill per result (per app, per product, per review) plus
a small per-run setup fee. Every scenario here uses small inputs to stay cheap,
and the script runs ONE scenario by default. Pass a scenario name to run a
specific one, or "all" to run every single-actor scenario (each is billed):

    uv run python apple-app-store-api-cookbook.py                 # runs 'search_basic'
    uv run python apple-app-store-api-cookbook.py product_single
    uv run python apple-app-store-api-cookbook.py competitor      # a multi-step workflow
    uv run python apple-app-store-api-cookbook.py all             # every single-actor scenario (bills each)

Get your free Apify API key at: https://apify.com?fpr=9n7kx3
Set it in a .env file (see .env.example) or export APIFY_API_TOKEN.
"""

import os
import sys

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

# Well-known App Store IDs used in the examples below.
SPOTIFY = "324684580"
NETFLIX = "363590051"


def run(actor: str, run_input: dict) -> list:
    """Call an actor and return its dataset rows."""
    job = client.actor(actor).call(run_input=run_input)
    if job is None:
        raise SystemExit(f"Actor {actor} did not start. Check your API token and inputs.")
    return list(client.dataset(job.default_dataset_id).iterate_items())


# ---------------------------------------------------------------------------
# Single-actor scenarios: (actor, description, run_input, printer)
# ---------------------------------------------------------------------------
def print_apps(rows: list) -> None:
    for a in rows:
        print(
            f"  - {a.get('title')} by {a.get('developer_name')} "
            f"(rating {a.get('rating_average')}, {a.get('rating_count')} ratings) id={a.get('app_id')}"
        )


def print_products(rows: list) -> None:
    for p in rows:
        print(f"  - {p.get('title')} | {p.get('category')} | {p.get('developer_name')}")
        print(
            f"      rating {p.get('rating_average')} | {p.get('price_text')} | "
            f"{p.get('size_text')} | versions: {len(p.get('version_history') or [])} | "
            f"related: {len(p.get('you_may_also_like') or [])}"
        )


def print_reviews(rows: list) -> None:
    for r in rows:
        title = r.get("review_title") or "(no title)"
        print(f"  - {r.get('rating')}/5  {title}  by {r.get('author_name')}  ({r.get('app_country')})")


SCENARIOS = {
    # --- SEARCH ---------------------------------------------------------
    "search_basic": (
        SEARCH, "Search apps by keyword",
        {"term": "meditation", "num": 3, "max_pages": 1}, print_apps,
    ),
    "search_developer": (
        SEARCH, "Search by developer name instead of app name",
        {"term": "Spotify", "property": "developer", "num": 3}, print_apps,
    ),
    "search_category": (
        SEARCH, "Search within a category (6014 = Games)",
        {"term": "puzzle", "category_id": 6014, "num": 3}, print_apps,
    ),
    "search_country": (
        SEARCH, "Search a different country store (UK)",
        {"term": "news", "country": "gb", "num": 3}, print_apps,
    ),
    "search_no_explicit": (
        SEARCH, "Exclude apps flagged explicit",
        {"term": "dating", "disallow_explicit": True, "num": 3}, print_apps,
    ),
    # --- PRODUCT --------------------------------------------------------
    "product_single": (
        PRODUCT, "Full product record for one App Store ID",
        {"product_ids": [SPOTIFY]}, print_products,
    ),
    "product_batch": (
        PRODUCT, "Look up several apps in one run",
        {"product_ids": [SPOTIFY, NETFLIX]}, print_products,
    ),
    "product_related": (
        PRODUCT, "Include 'You May Also Like' and 'More By This Developer'",
        {"product_ids": [SPOTIFY], "include_related_apps": True}, print_products,
    ),
    "product_country": (
        PRODUCT, "Same app, Japanese store (localized price and text)",
        {"product_ids": [SPOTIFY], "country": "jp"}, print_products,
    ),
    # --- REVIEWS --------------------------------------------------------
    "reviews_by_id": (
        REVIEWS, "Most recent reviews for an App Store ID",
        {"product_ids": [SPOTIFY], "sort": "mostrecent", "max_reviews": 5}, print_reviews,
    ),
    "reviews_by_name": (
        REVIEWS, "Resolve an app by name, then pull reviews",
        {"app_name": "spotify", "max_reviews": 5}, print_reviews,
    ),
    "reviews_critical": (
        REVIEWS, "Most critical reviews (triage negative feedback)",
        {"product_ids": [SPOTIFY], "sort": "mostcritical", "max_reviews": 5}, print_reviews,
    ),
    "reviews_country": (
        REVIEWS, "Reviews from a different country store (UK)",
        {"product_ids": [SPOTIFY], "country": "gb", "max_reviews": 5}, print_reviews,
    ),
}


def run_scenario(key: str) -> None:
    actor, description, run_input, printer = SCENARIOS[key]
    print(f"\n=== {key}: {description} ===")
    print(f"Input: {run_input}")
    printer(run(actor, run_input))


# ---------------------------------------------------------------------------
# Multi-step workflows
# ---------------------------------------------------------------------------
def workflow_competitor(term: str = "habit tracker", top_n: int = 3) -> None:
    """Search a niche, then pull full details for the top apps and compare them."""
    print(f"\n=== competitor: top {top_n} apps for '{term}' ===")
    apps = run(SEARCH, {"term": term, "num": top_n, "max_pages": 1})
    ids = [str(a.get("app_id")) for a in apps if a.get("app_id")][:top_n]
    products = run(PRODUCT, {"product_ids": ids}) if ids else []
    print(f"{'App':<34}{'Developer':<22}{'Rating':<8}{'Price':<10}{'Size'}")
    for p in products:
        print(
            f"{(p.get('title') or '')[:33]:<34}"
            f"{(p.get('developer_name') or '')[:21]:<22}"
            f"{str(p.get('rating_average') or ''):<8}"
            f"{(p.get('price_text') or '')[:9]:<10}"
            f"{p.get('size_text') or ''}"
        )


def workflow_reputation(app_name: str = "spotify") -> None:
    """Pull recent and critical reviews for an app and summarize the rating mix."""
    print(f"\n=== reputation: review snapshot for '{app_name}' ===")
    recent = run(REVIEWS, {"app_name": app_name, "sort": "mostrecent", "max_reviews": 10})
    if not recent:
        print("  No reviews returned.")
        return
    stars = [r.get("rating") for r in recent if isinstance(r.get("rating"), int)]
    avg = sum(stars) / len(stars) if stars else 0
    print(f"  {len(recent)} recent reviews, average {avg:.1f}/5")
    print("  Most critical of the batch:")
    for r in sorted(recent, key=lambda r: r.get("rating") or 5)[:3]:
        print(f"    - {r.get('rating')}/5  {r.get('review_title') or '(no title)'}")


def workflow_price_by_country(app_id: str = SPOTIFY, countries=("us", "gb", "jp", "in")) -> None:
    """Compare an app's localized price and category across country stores."""
    print(f"\n=== price_by_country: id={app_id} across {', '.join(countries)} ===")
    for country in countries:
        rows = run(PRODUCT, {"product_ids": [app_id], "country": country})
        if rows:
            p = rows[0]
            print(f"  {country}: {p.get('title')} | {p.get('price_text')} | {p.get('category')}")


WORKFLOWS = {
    "competitor": workflow_competitor,
    "reputation": workflow_reputation,
    "price_by_country": workflow_price_by_country,
}


def main() -> None:
    arg = sys.argv[1] if len(sys.argv) > 1 else "search_basic"
    if arg == "all":
        print("Running ALL single-actor scenarios. Each one is billed.")
        for key in SCENARIOS:
            run_scenario(key)
    elif arg in SCENARIOS:
        run_scenario(arg)
    elif arg in WORKFLOWS:
        WORKFLOWS[arg]()
    else:
        print(f"Unknown example: {arg!r}\n")
        print("Single-actor scenarios:", ", ".join(SCENARIOS))
        print("Multi-step workflows:  ", ", ".join(WORKFLOWS))
        print('\nRun one by name, or "all". Example:')
        print("  uv run python apple-app-store-api-cookbook.py reviews_critical")


if __name__ == "__main__":
    main()
