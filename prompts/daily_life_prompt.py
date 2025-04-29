DAILY_LIFE_EVALUATION_PROMPT = """
Evaluate the daily-life data sample against the metrics below, decide an overall
quality tier (HIGH / MEDIUM / LOW), and answer five binary questions.

────────────────────────────────────────────────────────────────────────
METRICS (use for overall_score)
────────────────────────────────────────────────────────────────────────
1.  Data Completeness:
    - Ride-sharing activity and patterns (Uber, Lyft, etc.).
    - Food delivery history (DoorDash, UberEats, etc.).
    - Fresh grocery orders and frequency.
    - Daily routine data and patterns.

2.  Data Recency:
    - Freshness of recent transportation and delivery activities.
    - Frequency of service usage across platforms.
    - Last activity timestamps for each service type.
    - Recent ordering patterns and preferences.

3.  Data Personalization:
    - Transportation preferences and patterns.
    - Food preferences and ordering habits.
    - Shopping frequency and timing patterns.
    - Daily schedule and routine preferences.

4.  Data Quality:
    - Ratio of regular vs. one-time service usage.
    - Consistency in service preferences.
    - Frequency of service utilization.
    - Lifestyle pattern indicators.

────────────────────────────────────────────────────────────────────────
QUALITY TIERS & EXAMPLES
────────────────────────────────────────────────────────────────────────
HIGH:
    - Transportation: Daily ride-sharing (2+ trips), consistent routes, preferred services.
    - Food Delivery: Weekly orders (3+), clear food preferences, regular delivery times.
    - Grocery: Bi-weekly orders, consistent shopping patterns, clear preferences.
    - Overall: High completeness, recency, personalization, and quality across all services.

MEDIUM:
    - Transportation: Weekly ride-sharing (1-2 trips), some route patterns.
    - Food Delivery: Monthly orders (1-2), occasional preferences.
    - Grocery: Monthly orders, some shopping patterns.
    - Overall: Decent activity across services, but lacks the consistency of HIGH.

LOW:
    - Transportation: Monthly ride-sharing (<1 trip), random routes.
    - Food Delivery: Quarterly orders, no clear preferences.
    - Grocery: Rare orders, inconsistent patterns.
    - Overall: Minimal activity, outdated information, or inconsistent usage patterns.

────────────────────────────────────────────────────────────────────────
BINARY QUESTIONS (strict "yes" / "no" answers only)
────────────────────────────────────────────────────────────────────────
Q1  Updated within the last 14 days? (Based on the most recent activity timestamp across services)
Q2  Record count ≥ 50? (Refers to meaningful data points like rides, deliveries, orders, etc.)
Q3  Data directly reflects user preferences / behaviour? (e.g., regular routes, food choices)
Q4  Contains explicit or inferable time context? (e.g., timestamps on rides, deliveries)
Q5  Shows consistent lifestyle patterns? (e.g., regular service usage times, consistent preferences)

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
{data_for_daily_life_category}

Return the JSON object only.
""" 