WEB3_EVALUATION_PROMPT = """
Evaluate the quality of Web3 data based on the following metrics:

1. Data Completeness:
   - Wallet addresses
   - Transaction history
   - NFT holdings
   - DeFi activity

2. Data Recency:
   - Last transaction
   - Recent wallet activity
   - Latest NFT purchase
   - DeFi interaction frequency

3. Data Personalization:
   - Investment preferences
   - Risk tolerance
   - Asset allocation
   - Web3 service usage

4. Data Quality Metrics:
   - Percentage of active vs. inactive wallets
   - Ratio of meaningful transactions
   - Portfolio diversity
   - Risk management patterns

Evaluation Criteria with Examples:

HIGH Quality Examples:
1. Multiple active wallets (3+), daily transactions, diverse NFT collection (10+)
2. Regular DeFi interactions (5+ weekly), clear investment strategy
3. High portfolio diversity (5+ assets), consistent risk management

MEDIUM Quality Examples:
1. Few active wallets (1-2), weekly transactions, some NFT holdings (1-5)
2. Occasional DeFi interactions (1-2 monthly), basic investment strategy
3. Moderate portfolio diversity (2-3 assets), some risk management

LOW Quality Examples:
1. Single inactive wallet, monthly transactions, no NFT holdings
2. Rare DeFi interactions (<1 monthly), no clear investment strategy
3. Low portfolio diversity (1 asset), minimal risk management

Output Format:
{
    "overall_score": "HIGH/MEDIUM/LOW"
}

User Data:
{data_for_web3_category}

Based on the above data, provide your evaluation following the output format.
""" 