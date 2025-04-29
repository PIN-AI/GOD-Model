SOCIAL_EVALUATION_PROMPT = """
Evaluate the quality of social data based on the following metrics:

1. Data Completeness:
   - Twitter handle presence and activity
   - Twitter followers count and growth
   - Discord server participation
   - Telegram username and activity

2. Data Recency:
   - Last Twitter activity
   - Last Discord interaction
   - Last Telegram message
   - Social media engagement frequency

3. Data Personalization:
   - Unique social connections
   - Active communities
   - Social interaction patterns
   - Content preferences

4. Data Quality Metrics:
   - Percentage of active vs. inactive accounts
   - Ratio of meaningful interactions
   - Social network diversity
   - Engagement depth

Evaluation Criteria with Examples:

HIGH Quality Examples:
1. Active Twitter user with 10k+ followers, daily posts, and consistent engagement
2. Member of 5+ active Discord servers with regular participation
3. Telegram user with 100+ contacts and daily message activity

MEDIUM Quality Examples:
1. Twitter account with 1k followers, weekly posts, moderate engagement
2. Member of 2-3 Discord servers with occasional participation
3. Telegram user with 50+ contacts and weekly message activity

LOW Quality Examples:
1. Twitter account with <100 followers, monthly posts, minimal engagement
2. Member of 1 Discord server with rare participation
3. Telegram user with <20 contacts and monthly message activity

Output Format:
{
    "overall_score": "HIGH/MEDIUM/LOW"
}

User Data:
{data_for_social_category}

Based on the above data, provide your evaluation following the output format.
""" 