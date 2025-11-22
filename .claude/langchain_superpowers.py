#!/usr/bin/env python3
"""
LangChain Superpowers Framework
Industry-standard AI agent system replacing superpowers plugin
Built on LangChain - the production standard used by thousands of companies
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# LangChain imports - industry standard
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain.tools import Tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI


class LangChainSuperpowers:
    """Production-ready AI agent framework using LangChain"""

    def __init__(self, model_name: str = "gpt-4", temperature: float = 0.1):
        """Initialize LangChain superpowers with industry-standard model"""
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.memory = ConversationBufferWindowMemory(
            k=10,  # Remember last 10 interactions
            memory_key="chat_history",
            return_messages=True,
        )

    def brainstorm(self, topic: str, context: str = "") -> str:
        """Industry-standard brainstorming using LangChain"""
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an expert brainstorming facilitator using the SCAMPER method:
            - Substitute: What can be replaced?
            - Combine: What can be merged?
            - Adapt: What can be adapted?
            - Modify: What can be changed?
            - Put to another use: Alternative applications?
            - Eliminate: What can be removed?
            - Reverse: What can be reversed?

            Generate diverse, creative ideas that push boundaries while remaining practical.""",
                ),
                (
                    "human",
                    "Topic: {topic}\nContext: {context}\n\nGenerate creative ideas using SCAMPER methodology:",
                ),
            ]
        )

        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"topic": topic, "context": context})

    def plan_project(self, objective: str, constraints: str = "") -> str:
        """Strategic project planning using LangChain chains"""
        planning_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a senior project manager with 15+ years experience in enterprise software development.

            Create comprehensive project plans that include:
            1. **Phase-based breakdown** with clear milestones
            2. **Task decomposition** with dependencies
            3. **Risk assessment** with mitigation strategies
            4. **Resource requirements** and timeline estimates
            5. **Success criteria** and deliverables

            Use industry-standard project management methodologies (Agile, Waterfall, Hybrid where appropriate).""",
                ),
                (
                    "human",
                    "Project Objective: {objective}\nConstraints: {constraints}\n\nCreate a detailed project plan:",
                ),
            ]
        )

        chain = planning_prompt | self.llm | StrOutputParser()
        return chain.invoke({"objective": objective, "constraints": constraints})

    def enforce_tdd_workflow(self, feature_description: str) -> str:
        """Test-Driven Development enforcement using LangChain"""
        tdd_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a TDD expert and senior software engineer. Follow strict TDD methodology:

            1. **Red Phase**: Write failing test first
            2. **Green Phase**: Write minimal code to pass
            3. **Refactor Phase**: Improve code while tests pass

            For each feature, provide:
            - Test cases (unit, integration, edge cases)
            - Implementation steps in TDD order
            - Refactoring opportunities
            - Code review checklist

            Emphasize test coverage, clean code principles, and SOLID design.""",
                ),
                (
                    "human",
                    "Feature to implement: {feature_description}\n\nProvide TDD workflow and implementation plan:",
                ),
            ]
        )

        chain = tdd_prompt | self.llm | StrOutputParser()
        return chain.invoke({"feature_description": feature_description})

    def focus_implementation(self, task: str, current_context: str = "") -> str:
        """Implementation focus and guidance using LangChain"""
        focus_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a senior software architect and implementation specialist.

            Provide clear, actionable implementation guidance:
            1. **Architecture decisions** with rationale
            2. **Implementation steps** in logical order
            3. **Best practices** for the specific technology stack
            4. **Common pitfalls** and how to avoid them
            5. **Code quality standards** and review points

            Focus on production-ready, maintainable code solutions.""",
                ),
                (
                    "human",
                    "Implementation task: {task}\nCurrent context: {current_context}\n\nProvide detailed implementation guidance:",
                ),
            ]
        )

        chain = focus_prompt | self.llm | StrOutputParser()
        return chain.invoke({"task": task, "current_context": current_context})

    def create_agent_with_tools(self, tools: list[Tool], task: str) -> str:
        """Create a LangChain agent with custom tools for complex workflows"""
        agent_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an expert software development assistant with access to specialized tools.

            Use tools when they can help provide better, more accurate answers.
            Think step-by-step and explain your reasoning.
            Focus on practical, production-ready solutions.""",
                ),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        agent = create_openai_tools_agent(self.llm, tools, agent_prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        return agent_executor.invoke({"input": task})

    def code_review_simulation(self, code: str, review_focus: str = "") -> str:
        """Automated code review using LangChain"""
        review_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a senior engineer conducting a thorough code review.

            Review for:
            - Code quality and readability
            - Performance considerations
            - Security vulnerabilities
            - Best practices adherence
            - Testing requirements
            - Documentation needs

            Provide constructive feedback with specific, actionable suggestions.""",
                ),
                (
                    "human",
                    "Code to review:\n{code}\nReview focus: {review_focus}\n\nConduct comprehensive code review:",
                ),
            ]
        )

        chain = review_prompt | self.llm | StrOutputParser()
        return chain.invoke({"code": code, "review_focus": review_focus})


class SuperpowersCommands:
    """Command interface for LangChain superpowers"""

    def __init__(self):
        self.superpowers = LangChainSuperpowers()

    def brainstorm_command(self, topic: str, context: str = "") -> str:
        """Execute brainstorming command"""
        print(f"🧠 Brainstorming: {topic}")
        result = self.superpowers.brainstorm(topic, context)
        print("💡 Ideas Generated:")
        return result

    def plan_command(self, objective: str, constraints: str = "") -> str:
        """Execute planning command"""
        print(f"📋 Planning: {objective}")
        result = self.superpowers.plan_project(objective, constraints)
        print("📈 Project Plan Created:")
        return result

    def tdd_command(self, feature: str) -> str:
        """Execute TDD workflow command"""
        print(f"🧪 TDD Workflow: {feature}")
        result = self.superpowers.enforce_tdd_workflow(feature)
        print("✅ TDD Plan Generated:")
        return result

    def implement_command(self, task: str, context: str = "") -> str:
        """Execute implementation focus command"""
        print(f"⚙️ Implementation: {task}")
        result = self.superpowers.focus_implementation(task, context)
        print("🔧 Implementation Guidance:")
        return result

    def review_command(self, code: str, focus: str = "") -> str:
        """Execute code review command"""
        print("👁️ Code Review")
        result = self.superpowers.code_review_simulation(code, focus)
        print("📝 Review Results:")
        return result


# CLI Interface
def main():
    """Command line interface for LangChain superpowers"""
    import argparse

    parser = argparse.ArgumentParser(
        description="LangChain Superpowers - Industry-standard AI agent framework"
    )
    parser.add_argument(
        "command",
        choices=["brainstorm", "plan", "tdd", "implement", "review"],
        help="Superpower command to execute",
    )
    parser.add_argument("input", help="Input for the command")
    parser.add_argument("--context", default="", help="Additional context")
    parser.add_argument("--focus", default="", help="Specific focus area (for review)")

    args = parser.parse_args()

    # Initialize environment
    os.environ["PYTHONPATH"] = f"{PROJECT_ROOT}/lib_package/src:{PROJECT_ROOT}/cli_package/src"

    commands = SuperpowersCommands()

    if args.command == "brainstorm":
        result = commands.brainstorm_command(args.input, args.context)
    elif args.command == "plan":
        result = commands.plan_command(args.input, args.context)
    elif args.command == "tdd":
        result = commands.tdd_command(args.input)
    elif args.command == "implement":
        result = commands.implement_command(args.input, args.context)
    elif args.command == "review":
        result = commands.review_command(args.input, args.focus)

    print(result)


if __name__ == "__main__":
    main()
