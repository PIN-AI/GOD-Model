WEB3_EVALUATION_PROMPT = """
Evaluate the Web3-data sample against the metrics below, decide an overall
quality tier (HIGH / MEDIUM / LOW), and answer five binary questions.

────────────────────────────────────────────────────────────────────────
METRICS (use for overall_score)
────────────────────────────────────────────────────────────────────────
1.  Data Completeness:
    - Wallet addresses and types (MetaMask, Phantom, etc.).
    - Transaction history and patterns.
    - NFT holdings and collections.
    - DeFi activity and protocols used.

2.  Data Recency:
    - Freshness of recent transactions and interactions.
    - Frequency of wallet activity.
    - Last activity timestamps for each wallet.
    - Recent DeFi and NFT activity patterns.

3.  Data Personalization:
    - Investment preferences and strategies.
    - Risk tolerance indicators.
    - Asset allocation patterns.
    - Web3 service usage preferences.

4.  Data Quality:
    - Ratio of active vs. inactive wallets.
    - Transaction meaningfulness and patterns.
    - Portfolio diversity and management.
    - Risk management indicators.

────────────────────────────────────────────────────────────────────────
QUALITY TIERS & EXAMPLES
────────────────────────────────────────────────────────────────────────
HIGH:
    - Wallets: Multiple active wallets (3+), daily transactions.
    - NFTs: Diverse collection (10+), regular trading activity.
    - DeFi: Regular interactions (5+ weekly), clear strategy.
    - Overall: High completeness, recency, personalization, and quality across all Web3 activities.

MEDIUM:
    - Wallets: Few active wallets (1-2), weekly transactions.
    - NFTs: Some holdings (1-5), occasional trading.
    - DeFi: Occasional interactions (1-2 monthly).
    - Overall: Decent activity across platforms, but lacks the depth of HIGH.

LOW:
    - Wallets: Single inactive wallet, monthly transactions.
    - NFTs: No holdings or rare trading.
    - DeFi: Rare interactions (<1 monthly).
    - Overall: Minimal activity, outdated information, or inconsistent patterns.

────────────────────────────────────────────────────────────────────────
BINARY QUESTIONS (strict "yes" / "no" answers only)
────────────────────────────────────────────────────────────────────────
Q1  Updated within the last 14 days? (Based on the most recent transaction timestamp)
Q2  Record count ≥ 50? (Refers to meaningful data points like transactions, NFT holdings, etc.)
Q3  Data directly reflects user preferences / behaviour? (e.g., investment choices, risk tolerance)
Q4  Contains explicit or inferable time context? (e.g., timestamps on transactions)
Q5  Shows consistent investment patterns? (e.g., regular trading times, stable portfolio allocation)

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
{data_for_web3_category}

Return the JSON object only.
""" 