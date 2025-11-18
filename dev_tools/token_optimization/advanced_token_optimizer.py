#!/usr/bin/env python3
"""
Advanced Token Optimizer - 2025 Industry Standards

Implements cutting-edge token reduction and optimization techniques:
1. Context-aware filtering and compression
2. Semantic code analysis for relevance scoring
3. Intelligent caching and memoization
4. Token budget management and allocation
5. Real-time usage analytics and monitoring
"""

import json
import re
import time
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from collections import defaultdict, OrderedDict
import ast
import tokenize
import io


@dataclass
class TokenMetrics:
    """Token usage metrics for optimization analysis"""
    total_tokens: int = 0
    optimized_tokens: int = 0
    savings_percentage: float = 0.0
    processing_time_ms: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    compression_ratio: float = 1.0


@dataclass
class CodeContext:
    """Structured code context with metadata"""
    file_path: str
    content: str
    language: str
    importance_score: float
    token_count: int
    dependencies: set[str]
    exports: set[str]
    complexity_score: float
    last_modified: float


class TokenCache:
    """Intelligent LRU cache for token optimization results"""

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.hit_count = 0
        self.miss_count = 0

    def _is_expired(self, timestamp: float) -> bool:
        """Check if cache entry has expired"""
        return time.time() - timestamp > self.ttl_seconds

    def get(self, key: str) -> Any | None:
        """Get cached value if not expired"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if self._is_expired(timestamp):
                del self.cache[key]
                self.miss_count += 1
                return None
            self.cache.move_to_end(key)  # LRU update
            self.hit_count += 1
            return value
        self.miss_count += 1
        return None

    def put(self, key: str, value: Any) -> None:
        """Store value in cache with timestamp"""
        current_time = time.time()

        # Remove expired entries
        expired_keys = [
            k for k, (_, ts) in self.cache.items()
            if self._is_expired(ts)
        ]
        for k in expired_keys:
            del self.cache[k]

        # LRU eviction if needed
        if len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)

        self.cache[key] = (value, current_time)

    def get_hit_rate(self) -> float:
        """Calculate cache hit rate"""
        total = self.hit_count + self.miss_count
        return self.hit_count / total if total > 0 else 0.0


class SemanticCodeAnalyzer:
    """Advanced semantic analysis for intelligent token reduction"""

    def __init__(self):
        self.importance_keywords = {
            'class', 'def', 'import', 'from', 'async', 'await', 'yield',
            'raise', 'try', 'except', 'finally', 'with', 'contextmanager',
            '__init__', '__call__', '__enter__', '__exit__', '__str__',
            '__repr__', 'property', 'staticmethod', 'classmethod'
        }
        self.low_importance_patterns = {
            r'^\s*#.*$',  # Comments
            r'^\s*$',    # Empty lines
            r'^\s*(pass|ellipsis|\.\.\.)\s*$',  # Minimal statements
            r'docstring\s*=.*',  # Docstring assignments
            r'__all__\s*=.*',  # Exports
        }

    def analyze_importance(self, content: str, file_path: str) -> float:
        """Calculate importance score (0.0 to 1.0) for code content"""
        if not content.strip():
            return 0.0

        score = 0.0
        lines = content.split('\n')

        # Base score for non-empty content
        score += 0.1

        # Keyword density scoring
        keyword_count = sum(
            len(re.findall(rf'\b{kw}\b', content, re.IGNORECASE))
            for kw in self.importance_keywords
        )
        score += min(keyword_count / len(lines), 0.4)

        # Function and class density
        func_class_count = len(re.findall(r'\b(def|class)\s+\w+', content))
        score += min(func_class_count / max(len(lines) / 10, 1), 0.3)

        # Reduce score for boilerplate and comments
        low_importance_lines = sum(
            len(re.findall(pattern, content, re.MULTILINE))
            for pattern in self.low_importance_patterns
        )
        score -= min(low_importance_lines / len(lines), 0.2)

        # File path importance
        path_importance = self._get_path_importance(file_path)
        score += path_importance

        return max(0.0, min(1.0, score))

    def _get_path_importance(self, file_path: str) -> float:
        """Get importance score based on file path patterns"""
        path = Path(file_path)

        # High importance paths
        if any(pattern in str(path) for pattern in ['__init__', 'main', 'core', 'api']):
            return 0.3

        # Medium importance paths
        if any(part in ['src', 'lib', 'models'] for part in path.parts):
            return 0.2

        # Low importance paths
        if any(part in ['test', 'docs', 'examples'] for part in path.parts):
            return 0.1

        return 0.15

    def extract_dependencies(self, content: str) -> set[str]:
        """Extract import dependencies from code"""
        imports = set()

        # Extract from import statements
        for match in re.finditer(r'from\s+([^\s]+)\s+import', content):
            imports.add(match.group(1))

        # Extract direct imports
        for match in re.finditer(r'import\s+([^\s]+)', content):
            imports.add(match.group(1))

        return imports

    def extract_exports(self, content: str) -> set[str]:
        """Extract exported symbols from code"""
        exports = set()

        # __all__ assignments
        for match in re.finditer(r'__all__\s*=\s*\[(.*?)\]', content, re.DOTALL):
            exports.update(
                name.strip().strip('"\'')
                for name in match.group(1).split(',')
                if name.strip()
            )

        # Class and function definitions
        for match in re.finditer(r'^(def|class)\s+(\w+)', content, re.MULTILINE):
            exports.add(match.group(2))

        return exports

    def calculate_complexity(self, content: str) -> float:
        """Calculate cyclomatic complexity score"""
        try:
            tree = ast.parse(content)
            complexity = 1  # Base complexity

            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                    complexity += 1
                elif isinstance(node, (ast.ExceptHandler, ast.With, ast.AsyncWith)):
                    complexity += 1
                elif isinstance(node, ast.BoolOp):
                    complexity += len(node.values) - 1
                elif isinstance(node, ast.ListComp):
                    complexity += 1
                elif isinstance(node, ast.DictComp):
                    complexity += 1

            return float(complexity)
        except:
            return 1.0


class TokenCompressor:
    """Advanced token compression using semantic analysis"""

    def __init__(self):
        self.compression_strategies = {
            'whitespace': self._compress_whitespace,
            'comments': self._compress_comments,
            'imports': self._compress_imports,
            'strings': self._compress_strings,
            'docstrings': self._compress_docstrings,
        }

    def compress_content(self, content: str, strategies: list[str] | None = None) -> str:
        """Apply compression strategies to reduce token count"""
        if not content:
            return content

        strategies = strategies or list(self.compression_strategies.keys())
        compressed = content

        for strategy in strategies:
            if strategy in self.compression_strategies:
                compressed = self.compression_strategies[strategy](compressed)

        return compressed

    def _compress_whitespace(self, content: str) -> str:
        """Compress whitespace while preserving structure"""
        # Remove excessive blank lines
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

        # Remove trailing whitespace
        content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)

        # Compress multiple spaces to single (preserve indentation)
        lines = content.split('\n')
        compressed_lines = []

        for line in lines:
            # Preserve leading indentation
            leading_ws = re.match(r'^[ \t]*', line).group()
            stripped = line[leading_ws.count(' '):]

            # Compress internal spaces
            stripped = re.sub(r'  +', ' ', stripped)

            compressed_lines.append(leading_ws + stripped)

        return '\n'.join(compressed_lines)

    def _compress_comments(self, content: str) -> str:
        """Compress or remove less important comments"""
        lines = content.split('\n')
        filtered_lines = []

        for line in lines:
            stripped = line.strip()

            # Keep docstring markers and important comments
            if (stripped.startswith('"""') or stripped.startswith("'''") or
                stripped.startswith('# TODO') or stripped.startswith('# FIXME') or
                stripped.startswith('# NOTE') or stripped.startswith('# WARNING')):
                filtered_lines.append(line)
            # Remove simple comments
            elif stripped.startswith('#') and len(stripped) < 20:
                continue
            else:
                filtered_lines.append(line)

        return '\n'.join(filtered_lines)

    def _compress_imports(self, content: str) -> str:
        """Optimize import statements for token efficiency"""
        # Group similar imports
        import_lines = []
        other_lines = []

        for line in content.split('\n'):
            if re.match(r'^(from|import)\s+', line.strip()):
                import_lines.append(line.strip())
            else:
                other_lines.append(line)

        # Sort imports and remove duplicates
        unique_imports = sorted(set(import_lines))

        # Rebuild content
        if unique_imports:
            return '\n'.join(unique_imports + [''] + other_lines)
        return content

    def _compress_strings(self, content: str) -> str:
        """Compress string literals where safe"""
        # This is conservative to preserve functionality
        lines = content.split('\n')
        compressed_lines = []

        for line in lines:
            # Compress long string literals that appear to be data
            if re.search(r'["\'][^"\']{100,}["\']', line):
                # Truncate very long data strings with indicator
                line = re.sub(
                    r'(["\'])([^"\']{80,100})[^"\']*?\1',
                    r'\1\2...[truncated]\1',
                    line
                )
            compressed_lines.append(line)

        return '\n'.join(compressed_lines)

    def _compress_docstrings(self, content: str) -> str:
        """Compress docstrings while preserving essential info"""
        # Find and compress long docstrings
        def compress_docstring(match):
            docstring = match.group()
            lines = docstring.split('\n')

            if len(lines) <= 3:
                return docstring

            # Keep first and last lines, summarize middle
            first = lines[0] if lines else ''
            last = lines[-1] if len(lines) > 1 else ''

            return f"{first}\n    ...[docstring compressed]...\n{last}"

        # Compress triple-quoted strings (likely docstrings)
        content = re.sub(
            r'("""[^"]*?"""|\'\'\'[^\']*?\'\'\')',
            compress_docstring,
            content,
            flags=re.DOTALL
        )

        return content


class AdvancedTokenOptimizer:
    """Main optimizer implementing industry-standard techniques"""

    def __init__(self, cache_size: int = 1000, cache_ttl: int = 3600):
        self.cache = TokenCache(cache_size, cache_ttl)
        self.analyzer = SemanticCodeAnalyzer()
        self.compressor = TokenCompressor()
        self.metrics = TokenMetrics()
        self.budget_limits = {
            'max_context_tokens': 8000,  # GPT-4 limit
            'max_snippet_chars': 2000,
            'max_files': 50,
        }

    def optimize_for_context(
        self,
        files: list[str],
        goal: str,
        pattern: str | None = None,
        token_budget: int | None = None
    ) -> tuple[str, TokenMetrics]:
        """Optimize code context for minimal token usage"""
        start_time = time.time()

        # Generate cache key
        cache_key = self._generate_cache_key(files, goal, pattern, token_budget)

        # Check cache first
        cached_result = self.cache.get(cache_key)
        if cached_result:
            self.metrics.cache_hits += 1
            return cached_result[0], cached_result[1]

        self.metrics.cache_misses += 1

        # Analyze and score files
        code_contexts = self._analyze_files(files, goal, pattern)

        # Apply budget-aware selection
        selected_contexts = self._select_contexts_by_budget(
            code_contexts,
            token_budget or self.budget_limits['max_context_tokens']
        )

        # Compress selected content
        optimized_content = self._compress_and_format(selected_contexts, goal)

        # Update metrics
        self.metrics.total_tokens = self._estimate_tokens(optimized_content)
        original_tokens = sum(ctx.token_count for ctx in code_contexts)
        self.metrics.optimized_tokens = original_tokens - self.metrics.total_tokens
        self.metrics.savings_percentage = (self.metrics.optimized_tokens / original_tokens * 100) if original_tokens > 0 else 0
        self.metrics.processing_time_ms = (time.time() - start_time) * 1000
        self.metrics.compression_ratio = original_tokens / self.metrics.total_tokens if self.metrics.total_tokens > 0 else 1.0

        # Cache result
        result_data = (optimized_content, self.metrics)
        self.cache.put(cache_key, result_data)

        return optimized_content, self.metrics

    def _analyze_files(self, files: list[str], goal: str, pattern: str | None) -> list[CodeContext]:
        """Analyze files and create context objects"""
        contexts = []

        for file_path in files:
            try:
                path = Path(file_path)
                if not path.exists():
                    continue

                content = path.read_text(encoding='utf-8')
                if not content.strip():
                    continue

                # Calculate metrics
                importance = self.analyzer.analyze_importance(content, file_path)
                token_count = self._estimate_tokens(content)
                dependencies = self.analyzer.extract_dependencies(content)
                exports = self.analyzer.extract_exports(content)
                complexity = self.analyzer.calculate_complexity(content)
                last_modified = path.stat().st_mtime

                # Boost importance based on goal relevance
                relevance_boost = self._calculate_relevance_boost(content, goal, pattern)
                importance = min(1.0, importance + relevance_boost)

                context = CodeContext(
                    file_path=str(path),
                    content=content,
                    language=self._detect_language(file_path),
                    importance_score=importance,
                    token_count=token_count,
                    dependencies=dependencies,
                    exports=exports,
                    complexity_score=complexity,
                    last_modified=last_modified
                )

                contexts.append(context)

            except Exception as e:
                # Log error but continue processing
                print(f"Warning: Could not analyze {file_path}: {e}")
                continue

        return contexts

    def _calculate_relevance_boost(self, content: str, goal: str, pattern: str | None) -> float:
        """Calculate relevance boost based on goal and pattern matching"""
        boost = 0.0

        # Pattern matching boost
        if pattern and pattern.lower() in content.lower():
            boost += 0.3

        # Goal keyword matching
        goal_words = set(goal.lower().split())
        content_lower = content.lower()

        word_matches = sum(1 for word in goal_words if word in content_lower)
        if goal_words:
            boost += (word_matches / len(goal_words)) * 0.2

        return boost

    def _select_contexts_by_budget(self, contexts: list[CodeContext], token_budget: int) -> list[CodeContext]:
        """Select contexts based on importance within token budget"""
        # Sort by importance score (descending)
        sorted_contexts = sorted(contexts, key=lambda c: c.importance_score, reverse=True)

        selected = []
        used_tokens = 0

        for context in sorted_contexts:
            if used_tokens + context.token_count <= token_budget:
                selected.append(context)
                used_tokens += context.token_count
            elif not selected:  # Always include at least the most important file
                # Truncate content to fit budget
                max_chars = int((token_budget - used_tokens) * 0.75)  # Rough estimate
                if max_chars > 100:
                    truncated_content = context.content[:max_chars] + "\n...[truncated for token budget]..."
                    context.content = truncated_content
                    context.token_count = self._estimate_tokens(truncated_content)
                    selected.append(context)
                    used_tokens += context.token_count
                break

        return selected

    def _compress_and_format(self, contexts: list[CodeContext], goal: str) -> str:
        """Compress and format selected contexts"""
        if not contexts:
            return "# No relevant context found"

        sections = [f"# Optimized Context for Goal: {goal}\n"]

        for context in contexts:
            # Apply compression
            compressed_content = self.compressor.compress_content(
                context.content,
                strategies=['whitespace', 'comments', 'docstrings']
            )

            sections.append(f"## File: {context.file_path}")
            sections.append(f"# Importance: {context.importance_score:.2f}, Complexity: {context.complexity_score:.0f}")
            sections.append(f"# Dependencies: {', '.join(list(context.dependencies)[:5])}")
            sections.append("")
            sections.append(compressed_content)
            sections.append("\n" + "=" * 50 + "\n")

        return "\n".join(sections)

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count using industry-standard approximation"""
        if not text:
            return 0

        # Use multiple estimation methods for accuracy
        # Method 1: Character-based (roughly 4 chars per token)
        char_estimate = len(text) / 4

        # Method 2: Word-based (roughly 1.3 words per token)
        word_estimate = len(text.split()) / 1.3

        # Method 3: Python-specific for code
        try:
            tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
            token_estimate = len(tokens)
        except:
            token_estimate = char_estimate

        # Use the most conservative estimate
        return max(1, int(min(char_estimate, word_estimate, token_estimate)))

    def _generate_cache_key(self, files: list[str], goal: str, pattern: str | None, budget: int | None) -> str:
        """Generate cache key for optimization results"""
        key_data = {
            'files': sorted(files),
            'goal': goal,
            'pattern': pattern,
            'budget': budget,
        }

        key_json = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_json.encode()).hexdigest()[:16]

    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        suffix = Path(file_path).suffix.lower()
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
        }
        return language_map.get(suffix, 'text')

    def get_analytics(self) -> dict[str, Any]:
        """Get comprehensive analytics and performance metrics"""
        return {
            'metrics': asdict(self.metrics),
            'cache_performance': {
                'hit_rate': self.cache.get_hit_rate(),
                'total_entries': len(self.cache.cache),
                'max_entries': self.cache.max_size,
            },
            'configuration': {
                'budget_limits': self.budget_limits,
                'cache_ttl': self.cache.ttl_seconds,
            },
            'optimization_strategies': list(self.compressor.compression_strategies.keys()),
        }


def main():
    """CLI interface for token optimization"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Advanced Token Optimizer - 2025 Industry Standards"
    )
    parser.add_argument(
        "goal",
        help="Goal for token optimization (e.g., 'analyze database models')"
    )
    parser.add_argument(
        "--pattern",
        help="Search pattern for focused optimization"
    )
    parser.add_argument(
        "--files",
        nargs="*",
        help="Specific files to optimize"
    )
    parser.add_argument(
        "--budget",
        type=int,
        help="Token budget limit"
    )
    parser.add_argument(
        "--output",
        help="Output file for optimized content"
    )
    parser.add_argument(
        "--analytics",
        action="store_true",
        help="Show detailed analytics"
    )

    args = parser.parse_args()

    optimizer = AdvancedTokenOptimizer()

    # Get files (default to current directory Python files)
    if args.files:
        files = args.files
    else:
        files = [str(p) for p in Path('.').rglob('*.py') if p.is_file()]

    if not files:
        print("No files found for optimization")
        return 1

    # Perform optimization
    optimized_content, metrics = optimizer.optimize_for_context(
        files, args.goal, args.pattern, args.budget
    )

    # Output results
    if args.output:
        Path(args.output).write_text(optimized_content)
        print(f"Optimized content written to {args.output}")
    else:
        print("OPTIMIZED CONTENT:")
        print("=" * 50)
        print(optimized_content)
        print("=" * 50)

    # Show metrics
    print(f"\nTOKEN OPTIMIZATION METRICS:")
    print(f"Total tokens: {metrics.total_tokens:,}")
    print(f"Optimized tokens: {metrics.optimized_tokens:,}")
    print(f"Savings: {metrics.savings_percentage:.1f}%")
    print(f"Processing time: {metrics.processing_time_ms:.1f}ms")
    print(f"Compression ratio: {metrics.compression_ratio:.2f}x")

    if args.analytics:
        analytics = optimizer.get_analytics()
        print(f"\nDETAILED ANALYTICS:")
        print(json.dumps(analytics, indent=2))

    return 0


if __name__ == "__main__":
    exit(main())
