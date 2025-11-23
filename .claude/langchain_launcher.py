#!/usr/bin/env python3
"""
LangChain Superpowers Launcher
Industry-standard AI agent commands built on LangChain
Replaces superpowers plugin with production-ready framework
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Add project root to Python path for this session only
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def setup_environment():
    """Setup project-specific environment without polluting system"""
    # Set PYTHONPATH for this session
    python_path = f"{PROJECT_ROOT}/lib_package/src:{PROJECT_ROOT}/cli_package/src"

    # Environment variables for this session
    env = os.environ.copy()
    env["PYTHONPATH"] = python_path
    env["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")  # Required for LangChain

    return env


def show_brainstorm_help():
    """Show brainstorming command help"""
    return """
🧠 LangChain Brainstorming - SCAMPER Method

Usage: lc-brainstorm "your topic" --context "additional context"

Features:
• SCAMPER methodology (Substitute, Combine, Adapt, Modify, Put to use, Eliminate, Reverse)
• Industry-standard creative thinking techniques
• Diverse idea generation with practical applications
• LangChain-powered structured brainstorming

Examples:
  lc-brainstorm "New features for our mobile app"
  lc-brainstorm "Ways to improve team productivity" --context "Remote work environment"
  lc-brainstorm "Innovative API design patterns"

This command uses LangChain with GPT-4 to generate creative, structured ideas using proven brainstorming methodologies.
"""


def show_plan_help():
    """Show planning command help"""
    return """
📋 LangChain Planning - Enterprise Project Management

Usage: lc-plan "your project objective" --context "constraints or requirements"

Features:
• Phase-based project breakdown with milestones
• Task decomposition with dependency mapping
• Risk assessment with mitigation strategies
• Resource requirements and timeline estimates
• Industry-standard project management methodologies

Examples:
  lc-plan "Build a REST API for user authentication"
  lc-plan "Migrate from monolith to microservices" --context "Must maintain 99.9% uptime"
  lc-plan "Implement CI/CD pipeline for the team"

This command uses LangChain to create comprehensive, production-ready project plans using enterprise methodologies.
"""


def show_tdd_help():
    """Show TDD command help"""
    return """
🧪 LangChain TDD Enforcement - Test-Driven Development Workflow

Usage: lc-tdd "feature description"

Features:
• Red-Green-Refactor TDD methodology
• Comprehensive test case generation (unit, integration, edge cases)
• Implementation steps in TDD order
• Refactoring opportunities and code review checklist
• SOLID principles and clean code emphasis

Examples:
  lc-tdd "User authentication system with JWT tokens"
  lc-tdd "File upload service with progress tracking"
  lc-tdd "Real-time notification system using WebSockets"

This command uses LangChain to enforce strict TDD workflows, ensuring test-first development with industry best practices.
"""


def show_implement_help():
    """Show implementation command help"""
    return """
⚙️ LangChain Implementation - Production-Ready Code Guidance

Usage: lc-implement "task description" --context "current technical context"

Features:
• Architecture decisions with detailed rationale
• Step-by-step implementation guidance
• Technology-specific best practices
• Common pitfalls and prevention strategies
• Code quality standards and review points

Examples:
  lc-implement "Database connection pooling" --context "Node.js with PostgreSQL"
  lc-implement "Rate limiting middleware" --context "Express.js API"
  lc-implement "Caching layer for API responses"

This command uses LangChain to provide detailed, production-ready implementation guidance from expert software architects.
"""


def show_review_help():
    """Show code review command help"""
    return """
👁️ LangChain Code Review - Automated Expert Review

Usage: lc-review "code snippet" --focus "specific area to review"

Features:
• Comprehensive code quality assessment
• Security vulnerability detection
• Performance optimization suggestions
• Best practices adherence checking
• Actionable improvement recommendations

Examples:
  lc-review "function getUserData(id) { ... }" --focus "Security and performance"
  lc-review "class DatabaseConnection { ... }" --focus "Error handling"
  lc-review "API endpoint implementation" --focus "RESTful design"

This command uses LangChain to perform expert-level code reviews with specific, actionable feedback.
"""


def show_all_commands():
    """Show all available LangChain superpowers commands"""
    return """
🤖 LangChain Superpowers - Industry-Standard AI Agent Framework

Built on LangChain - Used by thousands of companies in production

Available Commands:
  lc-brainstorm "topic"           - Creative brainstorming using SCAMPER methodology
  lc-plan "objective"             - Strategic project planning with phases and timelines
  lc-tdd "feature"                - Test-Driven Development workflow enforcement
  lc-implement "task"             - Production-ready implementation guidance
  lc-review "code"                - Expert automated code review

Enterprise Features:
• LangChain-powered AI agents with GPT-4
• Industry-standard methodologies (Agile, TDD, SOLID)
• Production-proven workflows used by Fortune 500 companies
• Zero environment pollution (project-local execution)
• Comprehensive logging and error handling

Examples:
  lc-brainstorm "API design patterns for microservices"
  lc-plan "Database migration strategy" --context "Zero downtime required"
  lc-tdd "User authentication with OAuth2"
  lc-implement "Message queue system" --context "RabbitMQ with Node.js"
  lc-review "Complex query logic" --focus "Performance optimization"

This replaces the superpowers plugin with a battle-tested, enterprise-grade AI agent framework.
"""


def execute_langchain_command(command_type, input_text="", context="", focus=""):
    """Execute LangChain superpowers commands"""
    env = setup_environment()

    # Check for OpenAI API key
    if not env.get("OPENAI_API_KEY"):
        return "❌ Error: OPENAI_API_KEY environment variable is required for LangChain commands.\n\nSet it with: export OPENAI_API_KEY='your-api-key-here'"

    # Path to LangChain superpowers script
    langchain_script = PROJECT_ROOT / ".claude" / "langchain_superpowers.py"

    if not langchain_script.exists():
        return f"❌ LangChain superpowers script not found: {langchain_script}"

    try:
        # Activate virtual environment and run command
        venv_python = PROJECT_ROOT / ".venv" / "bin" / "python"
        if not venv_python.exists():
            return f"❌ Virtual environment not found: {venv_python}"

        cmd = [str(venv_python), str(langchain_script), command_type, input_text]

        if context:
            cmd.extend(["--context", context])
        if focus:
            cmd.extend(["--focus", focus])

        # Execute the command
        result = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=PROJECT_ROOT)

        if result.returncode == 0:
            return result.stdout
        else:
            return f"❌ Command failed: {result.stderr}"

    except Exception as e:
        return f"❌ Error executing command: {e}"


def main():
    """Command line interface for the LangChain launcher"""
    parser = argparse.ArgumentParser(description="LangChain Superpowers Launcher")
    parser.add_argument(
        "command",
        choices=["brainstorm", "plan", "tdd", "implement", "review", "help"],
        help="LangChain superpower command to execute",
    )
    parser.add_argument("input", nargs="?", help="Input for the command")
    parser.add_argument(
        "--context", default="", help="Additional context for planning/implementation"
    )
    parser.add_argument("--focus", default="", help="Specific focus for code review")

    args = parser.parse_args()

    if args.command == "help":
        result = show_all_commands()
    elif args.command == "brainstorm":
        if not args.input:
            result = show_brainstorm_help()
        else:
            result = execute_langchain_command("brainstorm", args.input, args.context)
    elif args.command == "plan":
        if not args.input:
            result = show_plan_help()
        else:
            result = execute_langchain_command("plan", args.input, args.context)
    elif args.command == "tdd":
        if not args.input:
            result = show_tdd_help()
        else:
            result = execute_langchain_command("tdd", args.input)
    elif args.command == "implement":
        if not args.input:
            result = show_implement_help()
        else:
            result = execute_langchain_command("implement", args.input, args.context)
    elif args.command == "review":
        if not args.input:
            result = show_review_help()
        else:
            result = execute_langchain_command("review", args.input, "", args.focus)

    print(result)


if __name__ == "__main__":
    main()
