SHOPPING_EVALUATION_PROMPT = """
Evaluate the shopping-data sample against the metrics below, decide an overall
quality tier (HIGH / MEDIUM / LOW), and answer five binary questions.

────────────────────────────────────────────────────────────────────────
METRICS (use for overall_score)
────────────────────────────────────────────────────────────────────────
1.  Data Completeness:
    - Shopping receipt history and patterns.
    - Purchase frequency across different categories.
    - Discount usage and preferences.
    - Shopping platform preferences.

2.  Data Recency:
    - Freshness of recent purchases and transactions.
    - Frequency of shopping activity.
    - Last activity timestamps for each platform.
    - Recent purchase patterns and preferences.

3.  Data Personalization:
    - Product preferences and categories.
    - Brand loyalty and preferences.
    - Price sensitivity and patterns.
    - Shopping timing preferences.

4.  Data Quality:
    - Ratio of regular vs. one-time purchases.
    - Consistency in shopping patterns.
    - Frequency of platform usage.
    - Price range and category diversity.

────────────────────────────────────────────────────────────────────────
QUALITY TIERS & EXAMPLES
────────────────────────────────────────────────────────────────────────
HIGH:
    - Frequency: Weekly shopping (5+ transactions), consistent categories.
    - Preferences: Clear brand loyalty, stable price ranges, regular discount usage.
    - Categories: 3+ active shopping categories, diverse product types.
    - Overall: High completeness, recency, personalization, and quality across all platforms.

MEDIUM:
    - Frequency: Monthly shopping (2-3 transactions), some category patterns.
    - Preferences: Some brand preferences, variable price ranges.
    - Categories: 1-2 active shopping categories.
    - Overall: Decent activity across platforms, but lacks the consistency of HIGH.

LOW:
    - Frequency: Quarterly shopping (<1 transaction), random categories.
    - Preferences: No clear brand preferences, highly variable price ranges.
    - Categories: No clear category preferences.
    - Overall: Minimal activity, outdated information, or inconsistent patterns.

────────────────────────────────────────────────────────────────────────
BINARY QUESTIONS (strict "yes" / "no" answers only)
────────────────────────────────────────────────────────────────────────
Q1  Updated within the last 14 days? (Based on the most recent purchase timestamp)
Q2  Record count ≥ 50? (Refers to meaningful data points like purchases, receipts, etc.)
Q3  Data directly reflects user preferences / behaviour? (e.g., brand choices, price ranges)
Q4  Contains explicit or inferable time context? (e.g., timestamps on purchases)
Q5  Shows consistent shopping patterns? (e.g., regular purchase times, stable price ranges)

────────────────────────────────────────────────────────────────────────
OUTPUT FORMAT (strict JSON, no extra keys, no comments)
────────────────────────────────────────────────────────────────────────
{
  "overall_score": "HIGH|MEDIUM|LOW",
  "Q1": "yes|no",
  "Q2": "yes|no",
  "Q3": "yes|no",
  "Q4": "yes|no",
  "Q5": "yes|no"
}

────────────────────────────────────────────────────────────────────────
USER DATA
────────────────────────────────────────────────────────────────────────
{data_for_shopping_category}

Return the JSON object only.
""" 