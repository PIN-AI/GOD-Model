SHOPPING_EVALUATION_PROMPT = """
Evaluate the quality of shopping data based on the following metrics:

1. Data Completeness:
   - Shopping receipt history
   - Purchase patterns
   - Discount usage
   - Shopping preferences

2. Data Recency:
   - Last shopping activity
   - Recent purchase patterns
   - Latest discount usage
   - Shopping frequency

3. Data Personalization:
   - Product preferences
   - Brand loyalty
   - Price sensitivity
   - Shopping categories

4. Data Quality Metrics:
   - Percentage of regular vs. one-time purchases
   - Ratio of essential vs. luxury items
   - Shopping frequency consistency
   - Price range patterns

Evaluation Criteria with Examples:

HIGH Quality Examples:
1. Weekly shopping (5+ transactions), consistent brand preferences, regular discount usage
2. Clear product categories (3+ categories), stable price ranges, high brand loyalty
3. Active shopping history (20+ transactions monthly), 80% regular purchases

MEDIUM Quality Examples:
1. Monthly shopping (2-3 transactions), some brand preferences, occasional discount usage
2. Few product categories (1-2), variable price ranges, moderate brand loyalty
3. Moderate shopping history (5+ transactions monthly), 50% regular purchases

LOW Quality Examples:
1. Quarterly shopping (<1 transaction), random brand choices, rare discount usage
2. No clear product categories, highly variable price ranges, low brand loyalty
3. Minimal shopping history (<5 transactions monthly), <30% regular purchases

Output Format:
{
    "overall_score": "HIGH/MEDIUM/LOW"
}

User Data:
{data_for_shopping_category}

Based on the above data, provide your evaluation following the output format.
""" 