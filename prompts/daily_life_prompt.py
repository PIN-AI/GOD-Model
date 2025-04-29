DAILY_LIFE_EVALUATION_PROMPT = """
Evaluate the quality of daily life data based on the following metrics:

1. Data Completeness:
   - Ride-sharing activity
   - Food delivery patterns
   - Fresh grocery orders
   - Daily routine data

2. Data Recency:
   - Last ride-sharing trip
   - Most recent food delivery
   - Latest grocery order
   - Daily activity patterns

3. Data Personalization:
   - Transportation preferences
   - Food preferences
   - Shopping habits
   - Daily schedule patterns

4. Data Quality Metrics:
   - Percentage of regular vs. one-time services
   - Ratio of essential vs. luxury purchases
   - Service usage frequency
   - Lifestyle consistency

Evaluation Criteria with Examples:

HIGH Quality Examples:
1. Daily ride-sharing (2+ trips), weekly food delivery (3+ orders), bi-weekly grocery orders
2. Consistent transportation patterns (same routes), regular food preferences
3. High service usage (10+ transactions monthly), stable lifestyle patterns

MEDIUM Quality Examples:
1. Weekly ride-sharing (1-2 trips), monthly food delivery (1-2 orders), monthly grocery orders
2. Some transportation patterns, occasional food preferences
3. Moderate service usage (5+ transactions monthly), somewhat consistent lifestyle

LOW Quality Examples:
1. Monthly ride-sharing (<1 trip), quarterly food delivery, rare grocery orders
2. Irregular transportation, random food choices
3. Minimal service usage (<5 transactions monthly), inconsistent lifestyle

Output Format:
{
    "overall_score": "HIGH/MEDIUM/LOW"
}

User Data:
{data_for_daily_life_category}

Based on the above data, provide your evaluation following the output format.
""" 