PRODUCTIVITY_EVALUATION_PROMPT = """
Evaluate the productivity-data sample against the metrics below, decide an overall
quality tier (HIGH / MEDIUM / LOW), and answer five binary questions.

────────────────────────────────────────────────────────────────────────
METRICS (use for overall_score)
────────────────────────────────────────────────────────────────────────
1.  Data Completeness:
    - Email activity and patterns (sent/received, thread participation).
    - Calendar event coverage (meetings, appointments, deadlines).
    - Task management data (todos, projects, deadlines).
    - Meeting frequency and types.

2.  Data Recency:
    - Freshness of recent emails, calendar events, and tasks.
    - Frequency of productivity tool usage.
    - Last activity timestamps across all productivity tools.
    - Recent meeting patterns and task completion rates.

3.  Data Personalization:
    - Work schedule patterns and preferences.
    - Meeting preferences and communication styles.
    - Task organization and prioritization patterns.
    - Productivity habits and routines.

4.  Data Quality:
    - Ratio of meaningful vs. routine communications.
    - Task completion efficiency and patterns.
    - Meeting effectiveness indicators.
    - Work-life balance indicators.

────────────────────────────────────────────────────────────────────────
QUALITY TIERS & EXAMPLES
────────────────────────────────────────────────────────────────────────
HIGH:
    - Email: Daily activity (50+ emails), high thread participation, clear communication patterns.
    - Calendar: 5+ events daily, well-structured meetings, consistent scheduling.
    - Tasks: 10+ active tasks, 90% completion rate, clear prioritization.
    - Overall: High completeness, recency, personalization, and quality across all tools.

MEDIUM:
    - Email: Weekly activity (20+ emails), moderate thread participation.
    - Calendar: 2-3 events daily, some meeting structure.
    - Tasks: 5+ active tasks, 70% completion rate.
    - Overall: Decent activity across tools, but lacks the depth or consistency of HIGH.

LOW:
    - Email: Monthly activity (<10 emails), minimal thread participation.
    - Calendar: 0-1 events daily, unstructured meetings.
    - Tasks: <5 active tasks, <50% completion rate.
    - Overall: Minimal activity, outdated information, or inconsistent usage patterns.

────────────────────────────────────────────────────────────────────────
BINARY QUESTIONS (strict "yes" / "no" answers only)
────────────────────────────────────────────────────────────────────────
Q1  Updated within the last 14 days? (Based on the most recent activity timestamp across tools)
Q2  Record count ≥ 50? (Refers to meaningful data points like emails, calendar events, tasks, etc.)
Q3  Data directly reflects user preferences / behaviour? (e.g., meeting patterns, task organization)
Q4  Contains explicit or inferable time context? (e.g., timestamps on emails, calendar events)
Q5  Shows clear work patterns? (e.g., consistent meeting times, regular task completion patterns)

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
{data_for_productivity_category}

Return the JSON object only.
""" 