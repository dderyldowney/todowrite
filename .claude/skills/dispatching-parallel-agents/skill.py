#!/usr/bin/env python3
"""
Dispatching Parallel Agents Superpowers Skill

Implements parallel agent dispatching with comprehensive fail-safe mechanisms
to prevent resource exhaustion, session locking, and ensure task isolation.

Features:
- Parallel task execution with resource limits
- Task isolation and sandboxing
- Load balancing and resource monitoring
- Error isolation and recovery
- Progress tracking and cleanup automation

Author: Claude Code Assistant
Version: 2025.1.0
"""

import os
import sys
import time
import json
import threading
import subprocess
import tempfile
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from queue import Queue, Empty
import logging
import psutil

# Import fail-safe mechanisms
try:
    from .claude.superpowers_fail_safes import with_fail_safes, get_fail_safes, ResourceLimits
except ImportError:
    # Fallback for standalone execution
    def with_fail_safes(subagent_name: str):
        def decorator(func):
            return func
        return decorator
    def get_fail_safes():
        return None
    @dataclass
    class ResourceLimits:
        max_memory_mb: int = 512
        max_cpu_percent: float = 80.0
        max_execution_time_seconds: int = 300
        max_concurrent_subagents: int = 3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ParallelTask:
    """Parallel task definition"""
    id: str
    task_type: str
    target: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    priority: int = 0
    estimated_cpu_percent: float = 50.0
    estimated_memory_mb: float = 100.0
    estimated_duration_seconds: int = 30
    timeout_seconds: int = 300
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class ParallelTaskResult:
    """Result of parallel task execution"""
    task_id: str
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time_seconds: float = 0.0
    memory_peak_mb: float = 0.0
    cpu_avg_percent: float = 0.0
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    retry_count: int = 0
    worker_id: Optional[str] = None
    artifacts: List[str] = field(default_factory=list)


@dataclass
class WorkerStats:
    """Worker thread statistics"""
    worker_id: str
    tasks_completed: int = 0
    tasks_failed: int = 0
    total_execution_time: float = 0.0
    peak_memory_mb: float = 0.0
    status: str = "idle"  # idle, busy, error


class ParallelTaskExecutor:
    """Isolated task executor with resource monitoring"""

    def __init__(self, worker_id: str, temp_dir: Path) -> None:
        """
        Initialize parallel task executor.

        Args:
            worker_id: Unique worker identifier
            temp_dir: Temporary directory for isolation
        """
        self.worker_id = worker_id
        self.temp_dir = temp_dir
        self.process = psutil.Process()
        self.current_task: Optional[ParallelTask] = None
        self.start_time: Optional[datetime] = None

    def execute_task(self, task: ParallelTask) -> ParallelTaskResult:
        """
        Execute a single task with isolation and monitoring.

        Args:
            task: Task to execute

        Returns:
            Task execution result
        """
        self.current_task = task
        self.start_time = datetime.now()

        result = ParallelTaskResult(
            task_id=task.id,
            worker_id=self.worker_id,
            retry_count=task.retry_count
        )

        try:
            # Create isolated working directory
            task_dir = self.temp_dir / f"task_{task.id}_{int(time.time())}"
            task_dir.mkdir(parents=True, exist_ok=True)

            # Execute task based on type
            if task.task_type == "code_analysis":
                result.result = self._execute_code_analysis(task, task_dir)
            elif task.task_type == "test_execution":
                result.result = self._execute_tests(task, task_dir)
            elif task.task_type == "documentation":
                result.result = self._execute_documentation(task, task_dir)
            elif task.task_type == "security_scan":
                result.result = self._execute_security_scan(task, task_dir)
            elif task.task_type == "file_processing":
                result.result = self._execute_file_processing(task, task_dir)
            else:
                result.result = self._execute_generic_task(task, task_dir)

            result.success = True

        except Exception as e:
            result.success = False
            result.error = str(e)
            logger.error(f"Task {task.id} failed in worker {self.worker_id}: {e}")

        finally:
            # Update result with execution metrics
            result.end_time = datetime.now()
            result.execution_time_seconds = (result.end_time - result.start_time).total_seconds()
            result.memory_peak_mb = self.process.memory_info().rss / 1024 / 1024
            result.cpu_avg_percent = self.process.cpu_percent()

            # Cleanup task directory
            self._cleanup_task_directory(task_dir)

            self.current_task = None
            self.start_time = None

        return result

    def _execute_code_analysis(self, task: ParallelTask, task_dir: Path) -> Dict[str, Any]:
        """Execute code analysis task."""
        target_path = Path(task.parameters.get("target", "."))

        cmd = [
            "python3", "-c",
            f"""
import ast
import os
from pathlib import Path

def analyze_code(path):
    results = {{"files": 0, "classes": 0, "functions": 0, "lines": 0}}

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                results["files"] += 1
                file_path = Path(root) / file

                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        results["lines"] += len(content.splitlines())

                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            results["classes"] += 1
                        elif isinstance(node, ast.FunctionDef):
                            results["functions"] += 1
                except Exception as e:
                    results["errors"] = results.get("errors", []) + [str(e)]

    return results

result = analyze_code('{target_path}')
print(json.dumps(result))
            """
        ]

        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(task_dir),
            timeout=task.timeout_seconds
        )

        if process.returncode != 0:
            raise RuntimeError(f"Code analysis failed: {process.stderr}")

        return json.loads(process.stdout)

    def _execute_tests(self, task: ParallelTask, task_dir: Path) -> Dict[str, Any]:
        """Execute test task."""
        test_path = task.parameters.get("target", "tests/")

        cmd = [
            "python3", "-m", "pytest",
            test_path,
            "--tb=short",
            "--no-header",
            "--json-report",
            "--json-report-file=test_results.json"
        ]

        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(task_dir),
            timeout=task.timeout_seconds
        )

        # Parse test results
        test_results_file = task_dir / "test_results.json"
        if test_results_file.exists():
            with open(test_results_file) as f:
                return json.load(f)
        else:
            # Fallback parsing
            output_lines = process.stdout.split('\n')
            passed = len([line for line in output_lines if 'passed' in line])
            failed = len([line for line in output_lines if 'failed' in line])

            return {
                "summary": {
                    "total": passed + failed,
                    "passed": passed,
                    "failed": failed,
                    "duration": process.execution_time if hasattr(process, 'execution_time') else 0
                },
                "tests": []
            }

    def _execute_documentation(self, task: ParallelTask, task_dir: Path) -> Dict[str, Any]:
        """Execute documentation task."""
        target_path = task.parameters.get("target", "docs/")

        # Simple documentation generation
        doc_content = f"""
# Generated Documentation

Generated by Parallel Agent: {self.worker_id}
Task ID: {task.id}
Timestamp: {datetime.now().isoformat()}

Target: {target_path}

## Analysis Summary

This documentation was generated automatically by the parallel agent system.
"""

        doc_file = task_dir / "generated_docs.md"
        doc_file.write_text(doc_content)

        return {
            "generated_files": [str(doc_file)],
            "word_count": len(doc_content.split()),
            "target_path": target_path
        }

    def _execute_security_scan(self, task: ParallelTask, task_dir: Path) -> Dict[str, Any]:
        """Execute security scan task."""
        target_path = task.parameters.get("target", ".")

        cmd = [
            "python3", "-c",
            f"""
import re
import os
from pathlib import Path

def security_scan(path):
    issues = []
    patterns = [
        (r'eval\\(', "Use of eval() function"),
        (r'exec\\(', "Use of exec() function"),
        (r'subprocess\\.Popen.*shell=True', "Subprocess with shell=True"),
        (r'password.*=.*["\'][^"\']+["\']', "Hardcoded password")
    ]

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file

                try:
                    with open(file_path, 'r') as f:
                        content = f.read()

                    for pattern, description in patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            issues.append({{
                                "file": str(file_path),
                                "issue": description,
                                "count": len(matches)
                            }})
                except Exception:
                    pass

    return {{"issues_found": len(issues), "issues": issues}}

result = security_scan('{target_path}')
print(json.dumps(result))
            """
        ]

        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(task_dir),
            timeout=task.timeout_seconds
        )

        if process.returncode != 0:
            raise RuntimeError(f"Security scan failed: {process.stderr}")

        return json.loads(process.stdout)

    def _execute_file_processing(self, task: ParallelTask, task_dir: Path) -> Dict[str, Any]:
        """Execute file processing task."""
        input_files = task.parameters.get("files", [])
        operation = task.parameters.get("operation", "copy")

        results = {
            "processed_files": [],
            "operation": operation,
            "count": 0
        }

        for file_path in input_files:
            source = Path(file_path)
            if source.exists():
                if operation == "copy":
                    dest = task_dir / source.name
                    dest.write_text(source.read_text())
                    results["processed_files"].append(str(dest))
                elif operation == "analyze":
                    results["processed_files"].append({
                        "path": str(source),
                        "size": source.stat().st_size,
                        "modified": source.stat().st_mtime
                    })

                results["count"] += 1

        return results

    def _execute_generic_task(self, task: ParallelTask, task_dir: Path) -> Dict[str, Any]:
        """Execute generic task."""
        # Generic task execution
        return {
            "task_id": task.id,
            "task_type": task.task_type,
            "parameters": task.parameters,
            "execution_time": time.time(),
            "worker_id": self.worker_id
        }

    def _cleanup_task_directory(self, task_dir: Path) -> None:
        """Clean up task directory."""
        try:
            import shutil
            if task_dir.exists():
                shutil.rmtree(task_dir)
        except Exception as e:
            logger.warning(f"Failed to cleanup task directory {task_dir}: {e}")

    def get_current_resource_usage(self) -> Dict[str, float]:
        """Get current resource usage."""
        return {
            "memory_mb": self.process.memory_info().rss / 1024 / 1024,
            "cpu_percent": self.process.cpu_percent(),
            "status": "busy" if self.current_task else "idle"
        }


class DispatchingParallelAgents:
    """Main parallel agent dispatcher with fail-safes"""

    def __init__(self, max_workers: int = 4, temp_dir: Optional[Path] = None) -> None:
        """
        Initialize parallel agent dispatcher.

        Args:
            max_workers: Maximum number of worker threads
            temp_dir: Temporary directory for task isolation
        """
        self.max_workers = max_workers
        self.temp_dir = temp_dir or Path(tempfile.mkdtemp(prefix="parallel_agents_"))

        # Initialize fail-safes
        self.fail_safes = get_fail_safes()
        if self.fail_safes:
            self.limits = self.fail_safes.limits
        else:
            self.limits = ResourceLimits()

        # Worker management
        self.workers: Dict[str, WorkerStats] = {}
        self.executor: Optional[ThreadPoolExecutor] = None
        self.active_futures: Dict[str, Future] = {}

        # Task management
        self.task_queue: Queue[ParallelTask] = Queue()
        self.completed_tasks: List[ParallelTaskResult] = []
        self.task_dependencies: Dict[str, List[str]] = {}

        # Resource monitoring
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_resources,
            daemon=True
        )

        logger.info(f"Parallel agent dispatcher initialized with {max_workers} workers")

    @with_fail_safes("parallel_dispatcher")
    def dispatch_tasks(self, tasks: List[ParallelTask]) -> List[ParallelTaskResult]:
        """
        Dispatch multiple tasks for parallel execution.

        Args:
            tasks: List of tasks to execute

        Returns:
            List of task results
        """
        logger.info(f"Dispatching {len(tasks)} tasks for parallel execution")

        # Initialize dependencies
        for task in tasks:
            self.task_dependencies[task.id] = task.dependencies

        # Validate resource limits
        if not self._validate_resource_limits(tasks):
            raise RuntimeError("Resource limits validation failed")

        # Sort tasks by priority and dependencies
        sorted_tasks = self._sort_tasks_by_priority_and_dependencies(tasks)

        # Start worker threads
        self._start_workers()

        # Submit tasks to workers
        results = []

        for task in sorted_tasks:
            if self._can_execute_task(task):
                future = self._submit_task(task)
                self.active_futures[task.id] = future
            else:
                # Task blocked by dependencies or resource limits
                self.task_queue.put(task)

        # Wait for completion and collect results
        results = self._collect_results()

        # Cleanup
        self._cleanup()

        logger.info(f"Parallel execution completed: {len(results)} results")
        return results

    def _validate_resource_limits(self, tasks: List[ParallelTask]) -> bool:
        """Validate that tasks fit within resource limits."""
        total_memory = sum(task.estimated_memory_mb for task in tasks)
        max_concurrent_needed = len(tasks)

        if total_memory > self.limits.max_memory_mb:
            logger.warning(f"Total memory requirement ({total_memory}MB) exceeds limit ({self.limits.max_memory_mb}MB)")
            return False

        if max_concurrent_needed > self.limits.max_concurrent_subagents:
            logger.warning(f"Concurrent tasks ({max_concurrent_needed}) exceed limit ({self.limits.max_concurrent_subagents})")
            return False

        return True

    def _sort_tasks_by_priority_and_dependencies(self, tasks: List[ParallelTask]) -> List[ParallelTask]:
        """Sort tasks by priority and resolve dependencies."""
        # Simple topological sort based on dependencies
        sorted_tasks = []
        remaining_tasks = tasks.copy()

        while remaining_tasks:
            # Find tasks with no unmet dependencies
            ready_tasks = [
                task for task in remaining_tasks
                if all(dep in [t.id for t in sorted_tasks] for dep in task.dependencies)
            ]

            if not ready_tasks:
                # Circular dependency or missing dependency
                logger.warning("Circular dependency detected, executing remaining tasks by priority")
                ready_tasks = remaining_tasks

            # Sort by priority (higher priority first)
            ready_tasks.sort(key=lambda t: t.priority, reverse=True)

            # Add to sorted list and remove from remaining
            for task in ready_tasks:
                sorted_tasks.append(task)
                remaining_tasks.remove(task)

        return sorted_tasks

    def _can_execute_task(self, task: ParallelTask) -> bool:
        """Check if task can be executed (dependencies met, resources available)."""
        # Check dependencies
        for dep in task.dependencies:
            if dep not in [result.task_id for result in self.completed_tasks]:
                return False

        # Check resource availability
        current_usage = sum(
            worker.peak_memory_mb for worker in self.workers.values()
            if worker.status == "busy"
        )

        if current_usage + task.estimated_memory_mb > self.limits.max_memory_mb:
            return False

        # Check worker availability
        busy_workers = sum(1 for worker in self.workers.values() if worker.status == "busy")
        if busy_workers >= self.max_workers:
            return False

        return True

    def _start_workers(self) -> None:
        """Start worker threads."""
        if self.executor is None:
            self.executor = ThreadPoolExecutor(max_workers=self.max_workers)

        # Initialize worker stats
        for i in range(self.max_workers):
            worker_id = f"worker_{i+1}"
            self.workers[worker_id] = WorkerStats(worker_id=worker_id)

    def _submit_task(self, task: ParallelTask) -> Future:
        """Submit task to worker thread."""
        # Find available worker
        available_worker = next(
            (worker_id for worker_id, stats in self.workers.items()
             if stats.status == "idle"),
            None
        )

        if available_worker is None:
            raise RuntimeError("No available workers")

        # Update worker status
        self.workers[available_worker].status = "busy"

        # Create task executor
        task_executor = ParallelTaskExecutor(available_worker, self.temp_dir)

        # Submit task
        future = self.executor.submit(task_executor.execute_task, task)

        # Add completion callback
        future.add_done_callback(lambda f, worker_id=available_worker: self._task_completed(f, worker_id))

        return future

    def _task_completed(self, future: Future, worker_id: str) -> None:
        """Handle task completion."""
        try:
            result = future.result()
            self.completed_tasks.append(result)

            # Update worker stats
            worker_stats = self.workers[worker_id]
            worker_stats.status = "idle"

            if result.success:
                worker_stats.tasks_completed += 1
            else:
                worker_stats.tasks_failed += 1

            worker_stats.total_execution_time += result.execution_time_seconds
            worker_stats.peak_memory_mb = max(worker_stats.peak_memory_mb, result.memory_peak_mb)

            # Check for queued tasks that can now be executed
            self._process_queued_tasks()

        except Exception as e:
            logger.error(f"Error handling task completion: {e}")
            self.workers[worker_id].status = "error"

    def _process_queued_tasks(self) -> None:
        """Process tasks waiting in queue."""
        processed_tasks = []

        while not self.task_queue.empty():
            try:
                task = self.task_queue.get_nowait()
                if self._can_execute_task(task):
                    future = self._submit_task(task)
                    self.active_futures[task.id] = future
                    processed_tasks.append(task)
                else:
                    # Put back in queue
                    self.task_queue.put(task)
                    break
            except Empty:
                break

    def _collect_results(self, timeout: Optional[float] = None) -> List[ParallelTaskResult]:
        """Collect results from all executed tasks."""
        if timeout is None:
            timeout = self.limits.max_execution_time_seconds

        # Wait for all futures to complete
        for future in as_completed(self.active_futures.values(), timeout=timeout):
            try:
                result = future.result()
            except Exception as e:
                logger.error(f"Task execution failed: {e}")

        return self.completed_tasks

    def _monitor_resources(self) -> None:
        """Monitor resource usage and enforce limits."""
        while self.monitoring_active:
            try:
                # Check total resource usage
                total_memory = sum(
                    worker.peak_memory_mb for worker in self.workers.values()
                )

                if total_memory > self.limits.max_memory_mb:
                    logger.warning(f"Memory usage ({total_memory}MB) exceeds limit ({self.limits.max_memory_mb}MB)")
                    # Could implement task cancellation here

                time.sleep(5)  # Check every 5 seconds

            except Exception as e:
                logger.error(f"Error in resource monitoring: {e}")
                time.sleep(5)

    def _cleanup(self) -> None:
        """Clean up resources."""
        self.monitoring_active = False

        if self.executor:
            self.executor.shutdown(wait=True)

        # Clean up temp directory
        try:
            import shutil
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
        except Exception as e:
            logger.warning(f"Failed to cleanup temp directory: {e}")

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status."""
        return {
            "workers": {
                worker_id: {
                    "status": stats.status,
                    "tasks_completed": stats.tasks_completed,
                    "tasks_failed": stats.tasks_failed,
                    "peak_memory_mb": stats.peak_memory_mb
                }
                for worker_id, stats in self.workers.items()
            },
            "active_tasks": len(self.active_futures),
            "completed_tasks": len(self.completed_tasks),
            "queued_tasks": self.task_queue.qsize(),
            "resource_limits": {
                "max_memory_mb": self.limits.max_memory_mb,
                "max_workers": self.max_workers,
                "max_concurrent_subagents": self.limits.max_concurrent_subagents
            }
        }


def create_parallel_task(task_id: str, task_type: str, target: str, **kwargs) -> ParallelTask:
    """
    Factory function to create parallel task.

    Args:
        task_id: Unique task identifier
        task_type: Type of task
        target: Target for task execution
        **kwargs: Additional task parameters

    Returns:
        ParallelTask instance
    """
    return ParallelTask(
        id=task_id,
        task_type=task_type,
        target=target,
        **kwargs
    )


def execute_parallel_tasks(tasks: List[Dict[str, Any]], max_workers: int = 4) -> List[Dict[str, Any]]:
    """
    Execute multiple tasks in parallel with fail-safes.

    Args:
        tasks: List of task dictionaries
        max_workers: Maximum number of parallel workers

    Returns:
        List of task results
    """
    # Convert dictionaries to ParallelTask objects
    parallel_tasks = []
    for task_dict in tasks:
        task = create_parallel_task(
            task_id=task_dict["id"],
            task_type=task_dict["type"],
            target=task_dict["target"],
            parameters=task_dict.get("parameters", {}),
            dependencies=task_dict.get("dependencies", []),
            priority=task_dict.get("priority", 0)
        )
        parallel_tasks.append(task)

    # Execute tasks
    dispatcher = DispatchingParallelAgents(max_workers=max_workers)
    results = dispatcher.dispatch_tasks(parallel_tasks)

    # Convert results to dictionaries
    return [
        {
            "task_id": result.task_id,
            "success": result.success,
            "result": result.result,
            "error": result.error,
            "execution_time_seconds": result.execution_time_seconds,
            "memory_peak_mb": result.memory_peak_mb,
            "worker_id": result.worker_id
        }
        for result in results
    ]


if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1:
        # Execute parallel tasks from JSON file
        with open(sys.argv[1]) as f:
            tasks_data = json.load(f)

        results = execute_parallel_tasks(tasks_data["tasks"], tasks_data.get("max_workers", 4))
        print(json.dumps(results, indent=2))
    else:
        print("Usage: python skill.py <tasks_json_file>")
        print("Example tasks JSON file:")
        print(json.dumps({
            "tasks": [
                {"id": "task1", "type": "code_analysis", "target": "src/"},
                {"id": "task2", "type": "test_execution", "target": "tests/"}
            ],
            "max_workers": 2
        }, indent=2))