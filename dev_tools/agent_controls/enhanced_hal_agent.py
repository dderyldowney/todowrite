#!/usr/bin/env python3
"""
Enhanced HAL Agent - Industry-Standard Local Preprocessing

Advanced HAL (Human-Aware Language) preprocessing system for zero-token
local operations before AI interaction. Implements 2025 industry standards
for semantic code analysis, intelligent filtering, and context optimization.
"""

import ast
import os
import re
import sys
import json
import time
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict
import hashlib


@dataclass
class FileInfo:
    """Structured information about analyzed files"""
    path: str
    size: int
    language: str
    relevance_score: float
    complexity: float
    dependencies: set[str]
    exports: set[str]
    last_modified: float
    content_hash: str


@dataclass
class AnalysisResult:
    """Results from HAL preprocessing analysis"""
    files: list[FileInfo]
    total_files_analyzed: int
    selected_files: list[str]
    analysis_time_ms: float
    token_estimate: int
    relevance_distribution: dict[str, int]
    recommendations: list[str]


class SemanticAnalyzer:
    """Advanced semantic analysis for intelligent file selection"""

    def __init__(self):
        self.importance_indicators = {
            # Core structural elements
            'class', 'def', 'interface', 'protocol', 'abstract', 'override',

            # Python-specific important keywords
            'async', 'await', 'yield', 'generator', 'coroutine', 'contextlib',
            'property', 'staticmethod', 'classmethod', '__init__', '__call__',
            '__enter__', '__exit__', '__str__', '__repr__', '__iter__',

            # Control flow
            'if', 'elif', 'else', 'try', 'except', 'finally', 'with', 'for', 'while',

            # Data definitions
            'dataclass', 'namedtuple', 'TypedDict', 'Protocol', 'Union', 'Optional',
            'List', 'Dict', 'Set', 'Tuple', 'Callable', 'Iterator', 'Generator',

            # Testing and validation
            'test', 'spec', 'describe', 'it', 'should', 'expect', 'assert',
            'pytest', 'unittest', 'fixture',
        }

        self.file_importance_patterns = {
            # Core files
            r'.*__init__\.py$': 0.9,
            r'.*main\.py$': 0.9,
            r'.*app\.py$': 0.8,
            r'.*config\.py$': 0.8,
            r'.*settings\.py$': 0.8,

            # Core modules
            r'.*/core/.*\.py$': 0.8,
            r'.*/api/.*\.py$': 0.8,
            r'.*/models/.*\.py$': 0.7,
            r'.*/services/.*\.py$': 0.7,
            r'.*/utils/.*\.py$': 0.6,

            # CLI and entry points
            r'.*/cli/.*\.py$': 0.7,
            r'.*/bin/.*': 0.7,

            # Lower priority
            r'.*/test_.*\.py$': 0.4,
            r'.*/.*_test\.py$': 0.4,
            r'.*/tests/.*\.py$': 0.3,
            r'.*/conftest\.py$': 0.3,
        }

    def analyze_file_relevance(self, file_path: str, content: str, goal: str, pattern: str | None = None) -> float:
        """Analyze file relevance to the given goal and pattern"""
        if not content.strip():
            return 0.0

        relevance = 0.0

        # Base path importance
        path_importance = self._get_path_importance(file_path)
        relevance += path_importance

        # Content analysis
        content_lower = content.lower()
        goal_lower = goal.lower()

        # Direct keyword matching
        goal_keywords = self._extract_keywords(goal_lower)
        content_keywords = self._extract_keywords(content_lower)

        keyword_overlap = len(goal_keywords.intersection(content_keywords))
        if goal_keywords:
            relevance += (keyword_overlap / len(goal_keywords)) * 0.3

        # Pattern matching
        if pattern and pattern.lower() in content_lower:
            relevance += 0.4

        # Structural importance
        structural_score = self._calculate_structural_importance(content)
        relevance += structural_score * 0.2

        # Code density (signals of meaningful content)
        code_density = self._calculate_code_density(content)
        relevance += code_density * 0.1

        # Recent modifications (more likely to be relevant)
        try:
            mtime = Path(file_path).stat().st_mtime
            days_old = (time.time() - mtime) / 86400
            recency_boost = max(0, (30 - days_old) / 30) * 0.1  # Boost for files < 30 days old
            relevance += recency_boost
        except:
            pass

        return min(1.0, relevance)

    def _get_path_importance(self, file_path: str) -> float:
        """Get importance score based on file path patterns"""
        for pattern, importance in self.file_importance_patterns.items():
            if re.match(pattern, file_path):
                return importance

        # Default importance based on directory
        path = Path(file_path)
        parts = path.parts

        if 'src' in parts:
            return 0.6
        elif 'lib' in parts:
            return 0.6
        elif 'test' in parts:
            return 0.3
        elif 'docs' in parts:
            return 0.2
        elif 'examples' in parts:
            return 0.2

        return 0.4  # Default

    def _extract_keywords(self, text: str) -> set[str]:
        """Extract meaningful keywords from text"""
        # Remove common stop words and extract meaningful terms
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you',
            'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when',
            'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
            'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
            'same', 'so', 'than', 'too', 'very', 'just', 'now',
        }

        # Extract words (technical terms, identifiers, etc.)
        words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', text.lower())
        return {word for word in words if len(word) > 2 and word not in stop_words}

    def _calculate_structural_importance(self, content: str) -> float:
        """Calculate importance based on code structure"""
        try:
            tree = ast.parse(content)

            importance_metrics = {
                'classes': 0,
                'functions': 0,
                'imports': 0,
                'decorators': 0,
                'complexity': 0,
            }

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    importance_metrics['classes'] += 1
                elif isinstance(node, ast.FunctionDef):
                    importance_metrics['functions'] += 1
                    if node.decorators:
                        importance_metrics['decorators'] += len(node.decorators)
                elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    importance_metrics['imports'] += 1
                elif isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                    importance_metrics['complexity'] += 1

            # Calculate weighted score
            score = (
                importance_metrics['classes'] * 0.3 +
                importance_metrics['functions'] * 0.2 +
                importance_metrics['imports'] * 0.1 +
                importance_metrics['decorators'] * 0.2 +
                importance_metrics['complexity'] * 0.2
            )

            return min(1.0, score / 10)  # Normalize to 0-1

        except:
            return 0.3  # Default if parsing fails

    def _calculate_code_density(self, content: str) -> float:
        """Calculate code density (ratio of meaningful code to total content)"""
        lines = content.split('\n')

        if not lines:
            return 0.0

        code_lines = 0
        comment_lines = 0
        empty_lines = 0

        for line in lines:
            stripped = line.strip()
            if not stripped:
                empty_lines += 1
            elif stripped.startswith('#'):
                comment_lines += 1
            elif not (stripped.startswith('"""') or stripped.startswith("'''")):
                code_lines += 1

        total_lines = len(lines)
        if total_lines == 0:
            return 0.0

        density = code_lines / total_lines
        return density

    def extract_dependencies(self, content: str) -> set[str]:
        """Extract import dependencies from code"""
        dependencies = set()

        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        dependencies.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        dependencies.add(node.module)
        except:
            # Fallback to regex-based extraction
            import_patterns = [
                r'from\s+([^\s]+)\s+import',
                r'import\s+([^\s]+)',
            ]
            for pattern in import_patterns:
                matches = re.findall(pattern, content)
                dependencies.update(matches)

        return dependencies

    def extract_exports(self, content: str) -> set[str]:
        """Extract exported symbols"""
        exports = set()

        # __all__ assignments
        for match in re.finditer(r'__all__\s*=\s*\[(.*?)\]', content, re.DOTALL):
            exports.update(
                name.strip().strip('"\'')
                for name in match.group(1).split(',')
                if name.strip()
            )

        # Class and function definitions
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    exports.add(node.name)
                elif isinstance(node, ast.FunctionDef):
                    exports.add(node.name)
        except:
            # Fallback to regex
            for match in re.finditer(r'^(def|class)\s+(\w+)', content, re.MULTILINE):
                exports.add(match.group(2))

        return exports


class ContentProcessor:
    """Advanced content processing for token optimization"""

    def __init__(self):
        self.max_snippet_chars = 2000
        self.max_files = 50

    def process_files(
        self,
        files: list[str],
        goal: str,
        pattern: str | None = None,
        max_chars: int | None = None,
        max_files: int | None = None
    ) -> AnalysisResult:
        """Process files and return optimized content"""
        start_time = time.time()
        analyzer = SemanticAnalyzer()

        max_chars = max_chars or self.max_snippet_chars
        max_files = max_files or self.max_files

        # Analyze all files
        file_infos = []
        for file_path in files:
            try:
                file_info = self._analyze_file(file_path, analyzer, goal, pattern)
                if file_info:
                    file_infos.append(file_info)
            except Exception as e:
                print(f"Warning: Could not process {file_path}: {e}", file=sys.stderr)
                continue

        # Sort by relevance
        file_infos.sort(key=lambda f: f.relevance_score, reverse=True)

        # Select top files within limits
        selected_files = []
        used_chars = 0
        relevance_dist = defaultdict(int)

        for file_info in file_infos[:max_files]:
            if used_chars + file_info.size <= max_chars:
                selected_files.append(file_info.path)
                used_chars += file_info.size

                # Track relevance distribution
                if file_info.relevance_score > 0.7:
                    relevance_dist['high'] += 1
                elif file_info.relevance_score > 0.4:
                    relevance_dist['medium'] += 1
                else:
                    relevance_dist['low'] += 1

        # Generate recommendations
        recommendations = self._generate_recommendations(file_infos, selected_files, goal, pattern)

        processing_time = (time.time() - start_time) * 1000
        token_estimate = self._estimate_tokens(used_chars)

        return AnalysisResult(
            files=file_infos,
            total_files_analyzed=len(file_infos),
            selected_files=selected_files,
            analysis_time_ms=processing_time,
            token_estimate=token_estimate,
            relevance_distribution=dict(relevance_dist),
            recommendations=recommendations
        )

    def _analyze_file(self, file_path: str, analyzer: SemanticAnalyzer, goal: str, pattern: str | None) -> FileInfo | None:
        """Analyze individual file"""
        try:
            path = Path(file_path)
            if not path.exists() or not path.is_file():
                return None

            content = path.read_text(encoding='utf-8')
            if not content.strip():
                return None

            # Calculate metrics
            relevance = analyzer.analyze_file_relevance(file_path, content, goal, pattern)
            complexity = analyzer._calculate_structural_importance(content)
            dependencies = analyzer.extract_dependencies(content)
            exports = analyzer.extract_exports(content)
            content_hash = hashlib.md5(content.encode()).hexdigest()

            return FileInfo(
                path=str(path),
                size=len(content),
                language=self._detect_language(file_path),
                relevance_score=relevance,
                complexity=complexity,
                dependencies=dependencies,
                exports=exports,
                last_modified=path.stat().st_mtime,
                content_hash=content_hash
            )

        except Exception:
            return None

    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file path"""
        suffix = Path(file_path).suffix.lower()
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'react',
            '.tsx': 'react-typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'c-header',
            '.hpp': 'cpp-header',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.sh': 'shell',
            '.bash': 'bash',
            '.zsh': 'zsh',
            '.sql': 'sql',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.less': 'less',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.xml': 'xml',
            '.md': 'markdown',
            '.txt': 'text',
            '.toml': 'toml',
            '.ini': 'ini',
        }
        return language_map.get(suffix, 'unknown')

    def _generate_recommendations(
        self,
        all_files: list[FileInfo],
        selected_files: list[str],
        goal: str,
        pattern: str | None
    ) -> list[str]:
        """Generate optimization recommendations"""
        recommendations = []

        # Analyze selection quality
        selected_paths = set(selected_files)
        selected_count = len(selected_files)
        total_count = len(all_files)

        if selected_count == 0:
            recommendations.append("⚠️  No files selected - consider broadening search criteria")
        elif selected_count < total_count * 0.1:
            recommendations.append(f"🔍 High selectivity: Only {selected_count}/{total_count} files selected")
        elif selected_count > total_count * 0.8:
            recommendations.append(f"📊 Low selectivity: {selected_count}/{total_count} files selected - consider refining goal")

        # Check for high-relevance missed files
        high_relevance_missed = [
            f for f in all_files
            if f.path not in selected_paths and f.relevance_score > 0.7
        ]

        if high_relevance_missed:
            recommendations.append(
                f"⚡ {len(high_relevance_missed)} high-relevance files missed - increase token budget"
            )

        # Language distribution analysis
        lang_counts = defaultdict(int)
        for file_info in selected_files:
            if isinstance(file_info, FileInfo):
                lang_counts[file_info.language] += 1
            else:
                # Handle case where selected_files contains just paths
                lang = self._detect_language(file_info)
                lang_counts[lang] += 1

        if len(lang_counts) > 3:
            recommendations.append(f"🌐 Multiple languages detected: {', '.join(lang_counts.keys())}")

        # Pattern matching effectiveness
        if pattern:
            pattern_matches = sum(1 for f in selected_files if pattern.lower() in Path(f).name.lower())
            if pattern_matches == 0:
                recommendations.append("🔍 Pattern didn't match any selected files - consider refining pattern")
            else:
                recommendations.append(f"✅ Pattern matched {pattern_matches} selected files")

        # Complexity analysis
        if selected_files:
            complexities = []
            for item in selected_files:
                if isinstance(item, FileInfo):
                    complexities.append(item.complexity)
            avg_complexity = sum(complexities) / len(complexities) if complexities else 0
            if avg_complexity > 0.7:
                recommendations.append(f"🧠 High complexity content detected (avg: {avg_complexity:.2f})")

        return recommendations

    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file path"""
        suffix = Path(file_path).suffix.lower()
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'react',
            '.tsx': 'react-typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'c-header',
            '.hpp': 'cpp-header',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.sh': 'shell',
            '.bash': 'bash',
            '.zsh': 'zsh',
            '.sql': 'sql',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.less': 'less',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.xml': 'xml',
            '.md': 'markdown',
            '.txt': 'text',
            '.toml': 'toml',
            '.ini': 'ini',
        }
        return language_map.get(suffix, 'unknown')

    def _estimate_tokens(self, char_count: int) -> int:
        """Estimate token count from character count"""
        # Industry-standard approximation: ~4 characters per token
        return max(1, char_count // 4)


def filter_repository(
    goal: str,
    pattern: str | None = None,
    roots: list[str] | None = None,
    include: list[str] | None = None,
    exclude: list[str] | None = None,
    chars: int | None = None,
    max_files: int | None = None,
    context_lines: int = 0,
    verbose: bool = False
) -> AnalysisResult:
    """Main function for repository filtering and analysis"""

    processor = ContentProcessor()

    # Find files
    roots = roots or ['.']
    include = include or ['*.py']
    exclude = exclude or []

    files = []
    for root in roots:
        root_path = Path(root)
        if not root_path.exists():
            continue

        for pattern in include:
            for file_path in root_path.rglob(pattern):
                if file_path.is_file():
                    # Check exclusions
                    file_str = str(file_path)
                    if not any(excl in file_str for excl in exclude):
                        files.append(file_str)

    if not files:
        if verbose:
            print("No files found matching criteria")
        return AnalysisResult(
            files=[], total_files_analyzed=0, selected_files=[],
            analysis_time_ms=0, token_estimate=0,
            relevance_distribution={}, recommendations=["No files found"]
        )

    if verbose:
        print(f"Found {len(files)} files to analyze")

    # Process files
    result = processor.process_files(files, goal, pattern, chars, max_files)

    if verbose:
        print(f"Processed {result.total_files_analyzed} files in {result.analysis_time_ms:.1f}ms")
        print(f"Selected {len(result.selected_files)} files (~{result.token_estimate:,} tokens)")

        if result.recommendations:
            print("\nRecommendations:")
            for rec in result.recommendations:
                print(f"  {rec}")

    return result


def main():
    """CLI interface for enhanced HAL agent"""
    parser = argparse.ArgumentParser(
        description="Enhanced HAL Agent - Industry-Standard Local Preprocessing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze authentication-related code
  python enhanced_hal_agent.py --goal "analyze authentication system" --roots src/ lib/

  # Search for database models
  python enhanced_hal_agent.py --goal "database models" --pattern "class.*Model" --include "*.py"

  # Quick analysis with token limits
  python enhanced_hal_agent.py --goal "API endpoints" --chars 1500 --max-files 10
        """
    )

    parser.add_argument(
        "--goal",
        required=True,
        help="Analysis goal (required)"
    )

    parser.add_argument(
        "--pattern",
        help="Regex pattern for focused analysis"
    )

    parser.add_argument(
        "--roots",
        nargs="*",
        default=["."],
        help="Root directories to search (default: .)"
    )

    parser.add_argument(
        "--include",
        nargs="*",
        default=["*.py"],
        help="File patterns to include (default: *.py)"
    )

    parser.add_argument(
        "--exclude",
        nargs="*",
        default=[".git", "__pycache__", ".pytest_cache", "node_modules", ".venv"],
        help="File/directory patterns to exclude"
    )

    parser.add_argument(
        "--chars",
        type=int,
        default=2000,
        help="Maximum characters for output (default: 2000)"
    )

    parser.add_argument(
        "--max-files",
        type=int,
        default=50,
        help="Maximum number of files to process (default: 50)"
    )

    parser.add_argument(
        "--context",
        type=int,
        default=0,
        help="Context lines around matches"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    # Perform analysis
    result = filter_repository(
        goal=args.goal,
        pattern=args.pattern,
        roots=args.roots,
        include=args.include,
        exclude=args.exclude,
        chars=args.chars,
        max_files=args.max_files,
        context_lines=args.context,
        verbose=args.verbose
    )

    # Output results
    if args.json:
        output_data = {
            'selected_files': result.selected_files,
            'total_analyzed': result.total_files_analyzed,
            'token_estimate': result.token_estimate,
            'processing_time_ms': result.analysis_time_ms,
            'relevance_distribution': result.relevance_distribution,
            'recommendations': result.recommendations,
            'file_details': [
                {
                    'path': f.path,
                    'relevance_score': f.relevance_score,
                    'complexity': f.complexity,
                    'language': f.language,
                    'size': f.size,
                    'dependencies': list(f.dependencies),
                    'exports': list(f.exports)
                }
                for f in result.files
            ]
        }
        print(json.dumps(output_data, indent=2))
    else:
        print(f"\n🎯 HAL Analysis Results for: {args.goal}")
        print("=" * 50)
        print(f"Files analyzed: {result.total_files_analyzed}")
        print(f"Files selected: {len(result.selected_files)}")
        print(f"Estimated tokens: {result.token_estimate:,}")
        print(f"Processing time: {result.analysis_time_ms:.1f}ms")

        if result.relevance_distribution:
            print(f"\nRelevance Distribution:")
            for level, count in result.relevance_distribution.items():
                print(f"  {level.capitalize()}: {count}")

        if result.selected_files:
            print(f"\nSelected Files:")
            for file_path in result.selected_files:
                print(f"  {file_path}")

        if result.recommendations:
            print(f"\nRecommendations:")
            for rec in result.recommendations:
                print(f"  {rec}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
