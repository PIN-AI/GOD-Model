FINANCE_EVALUATION_PROMPT = """
Evaluate the finance-data sample against the metrics below, decide an overall
quality tier (HIGH / MEDIUM / LOW), and answer five binary questions.

────────────────────────────────────────────────────────────────────────
METRICS (use for overall_score)
────────────────────────────────────────────────────────────────────────
1.  Data Completeness:
    - Broker receipts and transaction history.
    - Crypto transaction patterns and history.
    - Investment activity and types.
    - Financial service usage patterns.

2.  Data Recency:
    - Freshness of recent transactions and trades.
    - Frequency of financial activity.
    - Last activity timestamps for each service.
    - Recent investment patterns and preferences.

3.  Data Personalization:
    - Investment strategy and preferences.
    - Risk profile indicators.
    - Asset allocation patterns.
    - Financial goal indicators.

4.  Data Quality:
    - Ratio of active vs. inactive accounts.
    - Transaction meaningfulness and patterns.
    - Portfolio diversity and management.
    - Risk management indicators.

────────────────────────────────────────────────────────────────────────
QUALITY TIERS & EXAMPLES
────────────────────────────────────────────────────────────────────────
HIGH:
    - Broker: Multiple active accounts (2+), daily trading activity.
    - Crypto: Regular transactions (5+ weekly), diverse portfolio.
    - Investment: Clear strategy, regular activity, diverse assets.
    - Overall: High completeness, recency, personalization, and quality across all financial activities.

MEDIUM:
    - Broker: Single active account, weekly trading.
    - Crypto: Occasional transactions (1-2 monthly).
    - Investment: Basic strategy, some activity.
    - Overall: Decent activity across platforms, but lacks the depth of HIGH.

LOW:
    - Broker: Inactive account, monthly trading.
    - Crypto: Rare transactions (<1 monthly).
    - Investment: No clear strategy, minimal activity.
    - Overall: Minimal activity, outdated information, or inconsistent patterns.

────────────────────────────────────────────────────────────────────────
BINARY QUESTIONS (strict "yes" / "no" answers only)
────────────────────────────────────────────────────────────────────────
Q1  Updated within the last 14 days? (Based on the most recent transaction timestamp)
Q2  Record count ≥ 50? (Refers to meaningful data points like trades, transactions, etc.)
Q3  Data directly reflects user preferences / behaviour? (e.g., investment choices, risk tolerance)
Q4  Contains explicit or inferable time context? (e.g., timestamps on transactions)
Q5  Shows consistent financial patterns? (e.g., regular trading times, stable investment strategy)

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
{data_for_finance_category}

Return the JSON object only.
""" 