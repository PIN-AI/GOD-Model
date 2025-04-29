FINANCE_EVALUATION_PROMPT = """
Evaluate the quality of finance data based on the following metrics:

1. Data Completeness:
   - Broker receipts
   - Crypto transaction history
   - Investment patterns
   - Financial activity

2. Data Recency:
   - Last broker transaction
   - Recent crypto activity
   - Latest investment
   - Trading frequency

3. Data Personalization:
   - Investment strategy
   - Risk profile
   - Asset preferences
   - Financial goals

4. Data Quality Metrics:
   - Percentage of active vs. inactive accounts
   - Ratio of meaningful transactions
   - Portfolio diversity
   - Risk management patterns

Evaluation Criteria with Examples:

HIGH Quality Examples:
1. Multiple active broker accounts (2+), daily trading, diverse crypto portfolio
2. Regular investment activity (5+ trades weekly), clear investment strategy
3. High portfolio diversity (5+ assets), consistent risk management

MEDIUM Quality Examples:
1. Single active broker account, weekly trading, some crypto holdings
2. Occasional investment activity (1-2 trades monthly), basic investment strategy
3. Moderate portfolio diversity (2-3 assets), some risk management

LOW Quality Examples:
1. Inactive broker account, monthly trading, minimal crypto holdings
2. Rare investment activity (<1 monthly), no clear investment strategy
3. Low portfolio diversity (1 asset), minimal risk management

Output Format:
{
    "overall_score": "HIGH/MEDIUM/LOW"
}

User Data:
{data_for_finance_category}

Based on the above data, provide your evaluation following the output format.
""" 