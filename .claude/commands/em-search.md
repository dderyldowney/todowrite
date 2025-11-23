# Episodic Memory Search Command

Search through your conversation history using PostgreSQL full-text search with similarity scoring.

## Usage
/em-search "your search query"

## Examples
/em-search "PostgreSQL database"
/em-search "agent framework"
/em-search "API design patterns"

## Options
- Limit results to 10 by default
- Supports natural language queries
- Returns ranked results with similarity scores

## Example Output
```
🔍 Searching for: 'PostgreSQL database'
Found 8 results:

1. [ASSISTANT] agent-47652f29
   Project: -Users-dderyldowney
   Score: 0.892
   Time: 2025-11-21T15:30:22Z
   Content: I'll help you implement a PostgreSQL backend system with full-text search capabilities...

2. [USER] agent-47652f29
   Score: 0.856
   Time: 2025-11-21T15:28:45Z
   Content: Can we migrate the episodic memory to PostgreSQL for better performance?
```
