PRODUCTIVITY_EVALUATION_PROMPT = """
Evaluate the quality of productivity data based on the following metrics:

1. Data Completeness:
   - Email activity and patterns
   - Calendar event coverage
   - Meeting frequency and types
   - Task management data

2. Data Recency:
   - Last email activity
   - Most recent calendar event
   - Recent meeting patterns
   - Task completion rates

3. Data Personalization:
   - Work schedule patterns
   - Meeting preferences
   - Communication styles
   - Productivity habits

4. Data Quality Metrics:
   - Percentage of meaningful vs. routine emails
   - Ratio of scheduled vs. ad-hoc meetings
   - Task completion efficiency
   - Work-life balance indicators

Evaluation Criteria with Examples:

HIGH Quality Examples:
1. Daily email activity (50+ emails), 5+ calendar events per day, 90% task completion
2. Regular meeting schedule (3+ meetings daily), consistent work hours (9-5)
3. High task management activity (10+ tasks daily), 95% completion rate

MEDIUM Quality Examples:
1. Weekly email activity (20+ emails), 2-3 calendar events per day, 70% task completion
2. Occasional meetings (1-2 daily), flexible work hours
3. Moderate task management (5+ tasks daily), 75% completion rate

LOW Quality Examples:
1. Monthly email activity (<10 emails), 0-1 calendar events per day, <50% task completion
2. Rare meetings (<1 weekly), irregular work hours
3. Minimal task management (<5 tasks weekly), <50% completion rate

Output Format:
{
    "overall_score": "HIGH/MEDIUM/LOW"
}

User Data:
{data_for_productivity_category}

Based on the above data, provide your evaluation following the output format.
""" 