QUESTION_GENERATION_PROMPT = """
Data Formatting, Background, and Task Instructions

1. Overview of Data Processing
	* Data is pulled from OAuth-based streaming connectors and data dumps, processed using two JSON parsers.
	* A Personal Memory Table is maintained for each data connector (e.g., Gmail Memory Table.json, Amazon Shopping History.json).
	* Memory tables are updated in real-time and categorized into seven groups:
		1. Productivity
		2. Social
		3. Shopping
		4. Web2 Finance
		5. Web3 Onchain
		6. Gaming
		7. AI Native

2. Short-Term vs. Long-Term Memory
	* Short-term memory cache stores temporary facts (recent events, logs) and refreshes weekly.
	* Long-term memory tables store stable, factual data from summarized historical records.
	* A policy GOD model verifies data consistency across sources like X, Meta, Gsuite (Gmail, Gcal), penalizing inconsistencies.

3. Special Data Tokens
	* NE (Non-Exist): Indicates missing personal data after verification.
	* NA (Not Available): Due to system errors (e.g., parser failure, LLM failure).

Task: Generating Personalization Questions

The questions should be:
 1. Easy to Grade → Can be verified automatically by a TEE (Intel SGX) compute engine.
 2. Useful for AI Recommendations → Predictive of future user transactions.
 3. Impressive to the User → Makes the AI feel like a loyal executive assistant that “knows them well.”

Data Sources & Example Questions

1. Social
	* Data sources: Twitter, Discord, Telegram, Facebook (via Gmail receipts).
	* Example Questions:
		1. Number of Discord servers joined?
		2. Do we know the Telegram username?
		3. Twitter handle?
		4. Number of followers on Twitter as of yesterday?
		5. List of accounts the user follows on Twitter?

2. Productivity
	* Data sources: Gmail, Google Calendar.
	* Example Questions:
		1. Total emails sent in the last 7 days?
		2. Number of Google Calendar events in the last 7 days?
		3. Number of emails received in the last 7 days?

3. Daily Life
	* Data sources: Ride-sharing, food delivery, fresh grocery services (via Gmail receipts).
	* Example Questions:
		1. Number of Uber rides taken in the last 30 days?
		2. Number of DoorDash food deliveries in the last 90 days?
		3. Last Amazon Fresh order date?

4. Shopping
	* Data sources: Amazon, Shopify, Shein, Macy’s, Lululemon (via Gmail receipts).
	* Example Questions:
		1. Number of Amazon purchases in the last 60 days?
		2. Last Shein order date?
		3. Number of Lululemon purchases in the last year?

5. Web3
	* Data sources: MetaMask, Phantom, WalletConnect, on-chain data (via 3rd-party APIs).
	* Example Questions:
		1. Does the user have an Ethereum wallet connected?
		2. Total on-chain transactions in the last 6 months?
		3. Last NFT purchase date?

6. Finance
	* Data sources: Robinhood, IB, Coinbase, Binance, Kraken, OKX (via Gmail receipts).
	* Example Questions:
		1. Number of crypto exchange transactions in the last 30 days?
		2. Number of stock trades on Robinhood in the last 90 days?
		3. Last deposit amount into Binance?

7. AI Native Chat History
	* Data sources: ChatGPT, Gemini, DeepSeek, Perplexity, Character AI.
	* Example Questions:
		1. Number of queries sent to ChatGPT in the last month?
		2. Last Gemini AI conversation topic?
		3. Most-used AI chatbot in the last 30 days?

Final Task: Best Question Selection

For each data connector type, generate 20 candidate questions.
Then, select 8 best questions per category based on:
* Relevance (important for user personalization).
* Diversity (well-representing all data sources).
* Scalability (can be automated for grading).

Only output results in the following JSON format:
{"domain": "Social", "questions": ["<question1>", "<question2>", "<question3>"]}
{"domain": "Productivity", "questions": ["<question1>", "<question2>", "<question3>"]}
...

"""
