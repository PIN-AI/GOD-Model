SOCIAL_EVALUATION_PROMPT = """
Evaluate the social-data sample against the metrics below, decide an overall
quality tier (HIGH / MEDIUM / LOW), and answer five binary questions.

────────────────────────────────────────────────────────────────────────
METRICS (use for overall_score)
────────────────────────────────────────────────────────────────────────
1.  Data Completeness:
    - Presence and activity on platforms like Twitter, Discord, Telegram.
    - Follower/contact counts and growth (e.g., Twitter followers, Telegram contacts).
    - Participation in relevant communities (e.g., Discord servers).

2.  Data Recency:
    - Freshness of recent posts, messages, or interactions (e.g., last Twitter post, last Discord message, last Telegram activity).
    - Frequency of engagement across platforms.

3.  Data Personalization:
    - Evidence of unique social connections and interaction patterns.
    - Indication of active participation in specific communities.
    - Reflection of user's content preferences or interests through interactions.

4.  Data Quality:
    - Ratio of active vs. inactive accounts or connections.
    - Depth and meaningfulness of interactions (beyond simple likes/follows).
    - Diversity of social networks used.
    - Overall engagement depth.

────────────────────────────────────────────────────────────────────────
QUALITY TIERS & EXAMPLES
────────────────────────────────────────────────────────────────────────
HIGH:
    - Twitter: Active user with 10k+ followers, daily posts, consistent engagement.
    - Discord: Member of 5+ active servers with regular, meaningful participation.
    - Telegram: User with 100+ contacts and daily message activity.
    - Overall: High completeness, recency, personalization, and quality across multiple platforms.

MEDIUM:
    - Twitter: Account with ~1k followers, weekly posts, moderate engagement.
    - Discord: Member of 2-3 servers with moderate or occasional participation.
    - Telegram: User with 50+ contacts and weekly message activity.
    - Overall: Decent presence on some platforms, but lacks the depth, breadth, or recency of HIGH.

LOW:
    - Twitter: Account with <100 followers, infrequent (e.g., monthly) posts, minimal engagement.
    - Discord: Member of 0-1 servers with rare participation.
    - Telegram: User with <20 contacts and infrequent (e.g., monthly) message activity.
    - Overall: Minimal presence, outdated information, low engagement, or activity limited to a single, inactive platform.

────────────────────────────────────────────────────────────────────────
BINARY QUESTIONS (strict "yes" / "no" answers only)
────────────────────────────────────────────────────────────────────────
Q1  Updated within the last 14 days? (Based on the most recent activity timestamp across platforms)
Q2  Record count ≥ 50? (Refers to meaningful data points like posts, messages, significant connections, server memberships etc., not just raw follower count)
Q3  Data directly reflects user preferences / behaviour? (e.g., joining specific groups, commenting on certain topics)
Q4  Contains explicit or inferable time context? (e.g., timestamps on posts/messages, activity logs)
Q5  Shows consistent engagement patterns? (e.g., regular posting times, consistent interaction frequency)

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
{data_for_social_category}

Return the JSON object only.
""" 