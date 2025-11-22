#!/usr/bin/env python3
"""
Claude Context Verification Questions
Ask Claude these questions in the IDE to verify session memory
"""

questions = [
    {
        "question": "Do you remember our work setting up the ToDoWrite PostgreSQL Backend System? What container and database configuration did we create?",
        "expected_keywords": [
            "mcp-postgres",
            "port 5433",
            "mcp_tools",
            "mcp_user",
            "auto-restart",
            "unless-stopped",
        ],
        "description": "Basic session memory check",
    },
    {
        "question": "What specific foreign key relationships and association tables did we create for the ToDoWrite hierarchy?",
        "expected_keywords": [
            "31 foreign key constraints",
            "23 tables",
            "todowrite_goal_tasks",
            "todowrite_concept_tasks",
            "association tables",
        ],
        "description": "Technical details memory check",
    },
    {
        "question": "How much data should be in our current database and what specific counts should we see?",
        "expected_keywords": [
            "5 goals",
            "12 concepts",
            "1 session",
            "23 total tables",
            "cross-association tables",
        ],
        "description": "Data memory check",
    },
    {
        "question": "Can you summarize the complete ToDoWrite PostgreSQL Backend System we built and confirm all the key components are working in this IDE session?",
        "expected_keywords": [
            "PostgreSQL container",
            "existing Models API",
            "12-layer hierarchy",
            "data persistence",
            "session continuity",
        ],
        "description": "Comprehensive memory check",
    },
]


def print_verification_guide():
    print("🧠 CLAUDE CONTEXT VERIFICATION GUIDE")
    print("=" * 50)
    print()
    print("Ask Claude these questions in the IDE to verify session memory:")
    print()

    for i, q in enumerate(questions, 1):
        print(f"Question {i}: {q['description']}")
        print(f'Ask: "{q["question"]}"')
        print(f"Expected response should mention: {', '.join(q['expected_keywords'])}")
        print()

    print("🎯 SUCCESS CRITERIA:")
    print("Claude should remember:")
    print("✅ mcp-postgres container on port 5433")
    print("✅ Database: mcp_tools with user mcp_user")
    print("✅ 23 tables with complete hierarchy")
    print("✅ 31 foreign key constraints")
    print("✅ Auto-restart policy: unless-stopped")
    print("✅ 5 goals, 12 concepts, 1 session")
    print("✅ Complete association system")
    print("✅ Existing Models API only")
    print()


def print_quick_test():
    print("⚡ QUICK CLAUDE MEMORY TEST:")
    print("Just ask: 'Summarize the ToDoWrite PostgreSQL Backend System we built'")
    print()
    print("✅ Expected comprehensive response should include:")
    print("  - Container details (mcp-postgres, port 5433)")
    print("  - Database configuration (mcp_tools, mcp_user)")
    print("  - Table structure (23 tables, complete hierarchy)")
    print("  - Data integrity (5 goals, 12 concepts)")
    print("  - Session continuity mechanisms")
    print("  - Auto-restart configuration")
    print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        print_quick_test()
    else:
        print_verification_guide()
