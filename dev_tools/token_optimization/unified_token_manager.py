#!/usr/bin/env python3
"""Unified Token Manager - Industry-Standard Token Optimization System

Integrates HAL preprocessing and Token-Sage optimization with advanced
caching, analytics, and real-time monitoring. Implements 2025 industry
standards for maximum token efficiency.
"""

import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# Import our advanced components
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "agent_controls"))

from advanced_token_optimizer import AdvancedTokenOptimizer, TokenMetrics
from enhanced_hal_agent import AnalysisResult, filter_repository


@dataclass
class OptimizationSession:
    """Complete optimization session with all metrics"""

    session_id: str
    timestamp: datetime
    goal: str
    pattern: str | None
    hal_result: AnalysisResult
    token_result: TokenMetrics
    total_processing_time_ms: float
    total_savings_percentage: float
    recommendations: list[str]
    cache_status: dict[str, Any]


@dataclass
class TokenBudget:
    """Token budget management and allocation"""

    daily_limit: int
    per_request_limit: int
    used_today: int
    requests_today: int
    last_reset: datetime

    def is_within_limits(self, requested: int) -> bool:
        """Check if requested tokens are within budget limits"""
        return (
            self.used_today + requested <= self.daily_limit and requested <= self.per_request_limit
        )

    def allocate_tokens(self, requested: int) -> bool:
        """Allocate tokens from budget"""
        if not self.is_within_limits(requested):
            return False

        self.used_today += requested
        self.requests_today += 1
        return True

    def reset_if_needed(self):
        """Reset daily budget if needed"""
        now = datetime.now()
        if (now - self.last_reset).days >= 1:
            self.used_today = 0
            self.requests_today = 0
            self.last_reset = now


class TokenAnalytics:
    """Comprehensive analytics and monitoring system"""

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.sessions_file = storage_path / "sessions.json"
        self.metrics_file = storage_path / "metrics.json"

    def record_session(self, session: OptimizationSession) -> None:
        """Record optimization session"""
        session_data = asdict(session)
        session_data["timestamp"] = session.timestamp.isoformat()

        # Convert sets to lists for JSON serialization
        hal_result = asdict(session.hal_result)
        hal_result["relevance_distribution"] = dict(hal_result["relevance_distribution"])

        # Convert FileInfo objects' sets to lists
        file_details = []
        for file_info in hal_result.get("files", []):
            file_copy = file_info.copy()
            file_copy["dependencies"] = list(file_copy.get("dependencies", []))
            file_copy["exports"] = list(file_copy.get("exports", []))
            file_details.append(file_copy)
        hal_result["files"] = file_details

        session_data["hal_result"] = hal_result

        session_data["token_result"] = asdict(session.token_result)

        # Load existing sessions
        sessions = self._load_sessions()
        sessions.append(session_data)

        # Keep only last 1000 sessions
        if len(sessions) > 1000:
            sessions = sessions[-1000:]

        # Save sessions
        with open(self.sessions_file, "w") as f:
            json.dump(sessions, f, indent=2)

    def _load_sessions(self) -> list[dict]:
        """Load existing sessions"""
        if not self.sessions_file.exists():
            return []

        try:
            with open(self.sessions_file) as f:
                return json.load(f)
        except:
            return []

    def get_metrics(self, days: int = 7) -> dict[str, Any]:
        """Get analytics metrics for specified period"""
        sessions = self._load_sessions()

        # Filter by date
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_sessions = [
            s for s in sessions if datetime.fromisoformat(s["timestamp"]) >= cutoff_date
        ]

        if not recent_sessions:
            return {
                "total_sessions": 0,
                "total_tokens_saved": 0,
                "average_savings_percentage": 0,
                "total_processing_time_ms": 0,
                "cache_hit_rate": 0,
            }

        # Calculate metrics
        total_sessions = len(recent_sessions)
        total_tokens_saved = sum(s["token_result"]["optimized_tokens"] for s in recent_sessions)
        total_original_tokens = sum(
            s["token_result"]["total_tokens"] + s["token_result"]["optimized_tokens"]
            for s in recent_sessions
        )
        avg_savings = (
            (total_tokens_saved / total_original_tokens * 100) if total_original_tokens > 0 else 0
        )
        total_processing_time = sum(s["total_processing_time_ms"] for s in recent_sessions)
        cache_hits = sum(s.get("cache_status", {}).get("hits", 0) for s in recent_sessions)
        cache_requests = cache_hits + sum(
            s.get("cache_status", {}).get("misses", 0) for s in recent_sessions
        )
        cache_hit_rate = (cache_hits / cache_requests * 100) if cache_requests > 0 else 0

        return {
            "total_sessions": total_sessions,
            "total_tokens_saved": total_tokens_saved,
            "average_savings_percentage": avg_savings,
            "total_processing_time_ms": total_processing_time,
            "cache_hit_rate": cache_hit_rate,
            "sessions_per_day": total_sessions / days,
            "tokens_saved_per_session": total_tokens_saved / total_sessions
            if total_sessions > 0
            else 0,
        }

    def get_top_goals(self, days: int = 7, limit: int = 10) -> list[dict[str, Any]]:
        """Get most common goals and their performance"""
        sessions = self._load_sessions()

        cutoff_date = datetime.now() - timedelta(days=days)
        recent_sessions = [
            s for s in sessions if datetime.fromisoformat(s["timestamp"]) >= cutoff_date
        ]

        goal_stats = {}
        for session in recent_sessions:
            goal = session["goal"]
            if goal not in goal_stats:
                goal_stats[goal] = {
                    "count": 0,
                    "total_savings": 0,
                    "total_tokens": 0,
                    "avg_savings": 0,
                }

            goal_stats[goal]["count"] += 1
            goal_stats[goal]["total_savings"] += session["token_result"]["optimized_tokens"]
            goal_stats[goal]["total_tokens"] += session["token_result"]["total_tokens"]

        # Calculate averages and sort
        for stats in goal_stats.values():
            stats["avg_savings"] = (
                (stats["total_savings"] / stats["total_tokens"] * 100)
                if stats["total_tokens"] > 0
                else 0
            )

        sorted_goals = sorted(
            goal_stats.items(), key=lambda x: (x[1]["count"], x[1]["total_savings"]), reverse=True
        )

        return [{"goal": goal, **stats} for goal, stats in sorted_goals[:limit]]


class UnifiedTokenManager:
    """Main unified token optimization manager"""

    def __init__(self, config_path: Path | None = None):
        self.config_path = config_path or Path.home() / ".token_optimizer"
        self.config_path.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.optimizer = AdvancedTokenOptimizer(
            cache_size=1000,
            cache_ttl=7200,  # 2 hours
        )
        self.analytics = TokenAnalytics(self.config_path / "analytics")

        # Load or create budget
        self.budget = self._load_budget()

        # Session counter
        self.session_counter = 0

    def _load_budget(self) -> TokenBudget:
        """Load token budget from config"""
        budget_file = self.config_path / "budget.json"

        if budget_file.exists():
            try:
                with open(budget_file) as f:
                    data = json.load(f)
                budget = TokenBudget(**data)
                budget.reset_if_needed()
                return budget
            except:
                pass

        # Default budget
        return TokenBudget(
            daily_limit=100000,  # 100K tokens per day
            per_request_limit=8000,  # 8K tokens per request
            used_today=0,
            requests_today=0,
            last_reset=datetime.now(),
        )

    def _save_budget(self) -> None:
        """Save token budget to config"""
        budget_file = self.config_path / "budget.json"
        with open(budget_file, "w") as f:
            json.dump(asdict(self.budget), f, indent=2, default=str)

    def optimize(
        self,
        goal: str,
        pattern: str | None = None,
        roots: list[str] | None = None,
        include: list[str] | None = None,
        exclude: list[str] | None = None,
        chars: int | None = None,
        max_files: int | None = None,
        token_budget: int | None = None,
        use_cache: bool = True,
        verbose: bool = False,
    ) -> OptimizationSession:
        """Perform complete token optimization"""
        start_time = time.time()
        self.session_counter += 1

        if verbose:
            print(f"🚀 Starting optimization session #{self.session_counter}")
            print(f"🎯 Goal: {goal}")
            if pattern:
                print(f"🔍 Pattern: {pattern}")

        # Step 1: HAL preprocessing (0 API tokens)
        if verbose:
            print("\n📋 Step 1: HAL Preprocessing (0 tokens)")

        hal_start = time.time()
        hal_result = filter_repository(
            goal=goal,
            pattern=pattern,
            roots=roots,
            include=include,
            exclude=exclude,
            chars=chars or 2000,
            max_files=max_files or 50,
            verbose=verbose,
        )
        hal_time = (time.time() - hal_start) * 1000

        if not hal_result.selected_files:
            if verbose:
                print("⚠️  No files selected by HAL analysis")
            # Create empty session
            session = OptimizationSession(
                session_id=f"session_{self.session_counter}",
                timestamp=datetime.now(),
                goal=goal,
                pattern=pattern,
                hal_result=hal_result,
                token_result=TokenMetrics(),
                total_processing_time_ms=hal_time,
                total_savings_percentage=0.0,
                recommendations=["No files found for optimization"],
                cache_status={},
            )
            self.analytics.record_session(session)
            return session

        # Step 2: Token optimization
        if verbose:
            print(f"📋 Step 2: Token Optimization ({hal_result.token_estimate:,} estimated tokens)")

        # Check budget
        estimated_tokens = hal_result.token_estimate
        if not self.budget.is_within_limits(estimated_tokens):
            if verbose:
                print(
                    f"❌ Token budget exceeded: {estimated_tokens:,} requested, {self.budget.per_request_limit:,} limit"
                )
            # Still proceed but with reduced scope
            estimated_tokens = self.budget.per_request_limit

        # Perform optimization
        optimized_content, token_metrics = self.optimizer.optimize_for_context(
            files=hal_result.selected_files,
            goal=goal,
            pattern=pattern,
            token_budget=token_budget or self.budget.per_request_limit,
        )

        # Update budget
        self.budget.allocate_tokens(token_metrics.total_tokens)
        self._save_budget()

        # Calculate total metrics
        total_time = (time.time() - start_time) * 1000
        total_savings = token_metrics.savings_percentage

        # Combine recommendations
        all_recommendations = hal_result.recommendations.copy()
        if total_savings < 10:
            all_recommendations.append("💡 Consider refining goal for better token savings")
        elif total_savings > 50:
            all_recommendations.append("🎉 Excellent token savings achieved!")

        # Get cache status
        cache_status = {
            "hits": token_metrics.cache_hits,
            "misses": token_metrics.cache_misses,
            "hit_rate": self.optimizer.cache.get_hit_rate() * 100,
        }

        # Create session
        session = OptimizationSession(
            session_id=f"session_{self.session_counter}",
            timestamp=datetime.now(),
            goal=goal,
            pattern=pattern,
            hal_result=hal_result,
            token_result=token_metrics,
            total_processing_time_ms=total_time,
            total_savings_percentage=total_savings,
            recommendations=all_recommendations,
            cache_status=cache_status,
        )

        # Record session
        self.analytics.record_session(session)

        if verbose:
            print("✅ Optimization complete!")
            print(f"💰 Total savings: {total_savings:.1f}%")
            print(f"⏱️  Total time: {total_time:.1f}ms")
            print(f"📊 Cache hit rate: {cache_status['hit_rate']:.1f}%")

        return session

    def get_analytics(self, days: int = 7) -> dict[str, Any]:
        """Get comprehensive analytics"""
        metrics = self.analytics.get_metrics(days)
        top_goals = self.analytics.get_top_goals(days)

        return {
            "metrics": metrics,
            "top_goals": top_goals,
            "budget": {
                "daily_limit": self.budget.daily_limit,
                "used_today": self.budget.used_today,
                "remaining_today": self.budget.daily_limit - self.budget.used_today,
                "requests_today": self.budget.requests_today,
            },
            "cache_performance": self.optimizer.get_analytics()["cache_performance"],
        }

    def reset_cache(self) -> None:
        """Reset optimization cache"""
        self.optimizer.cache.cache.clear()
        if self.optimizer.cache.hit_count > 0:
            old_hits = self.optimizer.cache.hit_count
            self.optimizer.cache.hit_count = 0
            self.optimizer.cache.miss_count = 0
            print(f"🧹 Cache reset (had {old_hits} entries)")

    def set_budget(self, daily_limit: int, per_request_limit: int) -> None:
        """Update token budget limits"""
        self.budget.daily_limit = daily_limit
        self.budget.per_request_limit = per_request_limit
        self._save_budget()
        print(f"💰 Budget updated: {daily_limit:,}/day, {per_request_limit:,}/request")


def main():
    """CLI interface for unified token manager"""
    parser = argparse.ArgumentParser(
        description="Unified Token Manager - Industry-Standard Token Optimization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Optimize for database analysis
  python unified_token_manager.py "analyze database models" --roots lib_package/src

  # Quick optimization with limits
  python unified_token_manager.py "API endpoints" --chars 1500 --max-files 10

  # Show analytics
  python unified_token_manager.py --analytics

  # Set budget limits
  python unified_token_manager.py --set-budget 200000 10000
        """,
    )

    # Optimization options
    parser.add_argument("goal", nargs="?", help="Optimization goal (omit for analytics mode)")

    parser.add_argument("--pattern", help="Regex pattern for focused analysis")

    parser.add_argument(
        "--roots",
        nargs="*",
        default=["lib_package/src", "cli_package/src"],
        help="Root directories to search",
    )

    parser.add_argument("--include", nargs="*", default=["*.py"], help="File patterns to include")

    parser.add_argument(
        "--exclude",
        nargs="*",
        default=[".git", "__pycache__", ".pytest_cache", ".venv"],
        help="Patterns to exclude",
    )

    parser.add_argument("--chars", type=int, default=2000, help="Maximum characters for output")

    parser.add_argument("--max-files", type=int, default=50, help="Maximum files to process")

    parser.add_argument("--token-budget", type=int, help="Token budget limit for this request")

    # Management options
    parser.add_argument("--analytics", action="store_true", help="Show analytics dashboard")

    parser.add_argument("--days", type=int, default=7, help="Days for analytics (default: 7)")

    parser.add_argument("--reset-cache", action="store_true", help="Reset optimization cache")

    parser.add_argument(
        "--set-budget",
        nargs=2,
        type=int,
        metavar=("DAILY", "PER_REQUEST"),
        help="Set token budget limits",
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    # Initialize manager
    manager = UnifiedTokenManager()

    # Handle management commands
    if args.analytics:
        analytics = manager.get_analytics(args.days)
        if args.json:
            print(json.dumps(analytics, indent=2, default=str))
        else:
            print("📊 Token Optimization Analytics")
            print("=" * 50)
            metrics = analytics["metrics"]
            print(f"Total sessions (last {args.days} days): {metrics['total_sessions']}")
            print(f"Sessions per day: {metrics['sessions_per_day']:.1f}")
            print(f"Total tokens saved: {metrics['total_tokens_saved']:,}")
            print(f"Average savings: {metrics['average_savings_percentage']:.1f}%")
            print(f"Cache hit rate: {metrics['cache_hit_rate']:.1f}%")
            print(f"Total processing time: {metrics['total_processing_time_ms']:.1f}ms")

            budget = analytics["budget"]
            print("\n💰 Budget Status:")
            print(f"Used today: {budget['used_today']:,}/{budget['daily_limit']:,}")
            print(f"Remaining: {budget['remaining_today']:,}")
            print(f"Requests today: {budget['requests_today']}")

            top_goals = analytics["top_goals"][:5]
            if top_goals:
                print("\n🎯 Top Goals:")
                for goal_data in top_goals:
                    print(
                        f"  {goal_data['goal'][:50]}... ({goal_data['count']} uses, {goal_data['avg_savings']:.1f}% savings)"
                    )
        return 0

    if args.reset_cache:
        manager.reset_cache()
        return 0

    if args.set_budget:
        daily_limit, per_request_limit = args.set_budget
        manager.set_budget(daily_limit, per_request_limit)
        return 0

    # Require goal for optimization
    if not args.goal:
        parser.error("Goal is required for optimization (use --analytics for analytics mode)")

    # Perform optimization
    session = manager.optimize(
        goal=args.goal,
        pattern=args.pattern,
        roots=args.roots,
        include=args.include,
        exclude=args.exclude,
        chars=args.chars,
        max_files=args.max_files,
        token_budget=args.token_budget,
        verbose=args.verbose,
    )

    # Output results
    if args.json:
        output_data = {
            "session_id": session.session_id,
            "timestamp": session.timestamp.isoformat(),
            "goal": session.goal,
            "pattern": session.pattern,
            "hal_result": asdict(session.hal_result),
            "token_result": asdict(session.token_result),
            "total_processing_time_ms": session.total_processing_time_ms,
            "total_savings_percentage": session.total_savings_percentage,
            "recommendations": session.recommendations,
            "cache_status": session.cache_status,
        }
        print(json.dumps(output_data, indent=2, default=str))
    else:
        print(f"\n🎯 Optimization Results: {session.goal}")
        print("=" * 50)
        print(f"📁 Files analyzed: {session.hal_result.total_files_analyzed}")
        print(f"📄 Files selected: {len(session.hal_result.selected_files)}")
        print(f"💰 Token savings: {session.total_savings_percentage:.1f}%")
        print(f"🔤 Final tokens: {session.token_result.total_tokens:,}")
        print(f"⏱️  Processing time: {session.total_processing_time_ms:.1f}ms")
        print(f"🎯 Cache hit rate: {session.cache_status.get('hit_rate', 0):.1f}%")

        if session.recommendations:
            print("\n💡 Recommendations:")
            for rec in session.recommendations:
                print(f"  {rec}")

        if args.verbose and session.hal_result.selected_files:
            print("\n📄 Selected Files:")
            for file_path in session.hal_result.selected_files[:10]:  # Show first 10
                print(f"  {file_path}")
            if len(session.hal_result.selected_files) > 10:
                print(f"  ... and {len(session.hal_result.selected_files) - 10} more")

    return 0


if __name__ == "__main__":
    sys.exit(main())
