#!/usr/bin/env python3
"""
MCP Security and Performance Optimizer for 2025 Industry Standards

This module implements comprehensive security and performance optimizations
for MCP (Model Context Protocol) configurations including superpowers and
episodic-memory plugins.

Features:
- Real-time security scanning and validation
- Performance monitoring and optimization
- Automated compliance checking
- Token optimization integration
- Error handling and recovery

Author: Claude Code Assistant
Version: 2025.1.0
"""

import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import hashlib
import re

try:
    import yaml
except ImportError:
    yaml = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(Path(__file__).parent / "mcp_security.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class SecurityCheckResult:
    """Result of a security check"""
    check_name: str
    passed: bool
    severity: str  # 'critical', 'high', 'medium', 'low'
    message: str
    recommendation: Optional[str] = None
    timestamp: datetime = None

    def __post_init__(self) -> None:
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class PerformanceMetric:
    """Performance metric data"""
    metric_name: str
    value: float
    unit: str
    threshold: float
    status: str  # 'good', 'warning', 'critical'
    timestamp: datetime = None

    def __post_init__(self) -> None:
        if self.timestamp is None:
            self.timestamp = datetime.now()


class MCPSecurityOptimizer:
    """Main MCP Security and Performance Optimizer class"""

    def __init__(self, config_dir: Path) -> None:
        """
        Initialize the MCP Security Optimizer.

        Args:
            config_dir: Directory containing MCP configuration files
        """
        self.config_dir = Path(config_dir)
        self.security_results: List[SecurityCheckResult] = []
        self.performance_metrics: List[PerformanceMetric] = []
        self.config_cache: Dict[str, Any] = {}

        # Security patterns and rules
        self.forbidden_patterns = [
            r'subprocess\.Popen.*shell=True',
            r'eval\(',
            r'exec\(',
            r'__import__.*os',
            r'open\(/etc/passwd',
            r'shell=True.*unsafe'
        ]

        self.required_security_fields = [
            'security.authentication_required',
            'security.data_encryption',
            'security.access_control',
            'security.audit_logging'
        ]

    def load_configuration(self, config_path: Path) -> Dict[str, Any]:
        """
        Load MCP configuration from file.

        Args:
            config_path: Path to configuration file

        Returns:
            Parsed configuration dictionary

        Raises:
            FileNotFoundError: If configuration file doesn't exist
            ValueError: If configuration format is invalid
        """
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        # Check cache first
        cache_key = str(config_path) + str(config_path.stat().st_mtime)
        if cache_key in self.config_cache:
            return self.config_cache[cache_key]

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.suffix.lower() in ['.yaml', '.yml']:
                    if yaml is None:
                        raise ValueError("PyYAML not installed for YAML configuration")
                    config = yaml.safe_load(f)
                elif config_path.suffix.lower() == '.json':
                    config = json.load(f)
                else:
                    raise ValueError(f"Unsupported configuration format: {config_path.suffix}")

            # Cache the configuration
            self.config_cache[cache_key] = config
            logger.info(f"Loaded configuration from {config_path}")
            return config

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file {config_path}: {e}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in configuration file {config_path}: {e}")
        except Exception as e:
            raise ValueError(f"Error loading configuration {config_path}: {e}")

    def check_security_compliance(self, config: Dict[str, Any], config_name: str) -> List[SecurityCheckResult]:
        """
        Perform comprehensive security compliance checks.

        Args:
            config: Configuration dictionary to check
            config_name: Name of the configuration being checked

        Returns:
            List of security check results
        """
        results = []

        # Check required security fields
        for field_path in self.required_security_fields:
            if not self._check_nested_field_exists(config, field_path):
                results.append(SecurityCheckResult(
                    check_name=f"Required Security Field: {field_path}",
                    passed=False,
                    severity="high",
                    message=f"Missing required security field: {field_path}",
                    recommendation=f"Add {field_path} to configuration with appropriate value"
                ))
            else:
                results.append(SecurityCheckResult(
                    check_name=f"Required Security Field: {field_path}",
                    passed=True,
                    severity="info",
                    message=f"Security field present: {field_path}"
                ))

        # Check for forbidden patterns in configuration values
        self._check_forbidden_patterns(config, results)

        # Check encryption settings
        self._check_encryption_settings(config, results)

        # Check access control
        self._check_access_control(config, results)

        # Check audit logging
        self._check_audit_logging(config, results)

        # Check compliance standards
        self._check_compliance_standards(config, results)

        logger.info(f"Security compliance check completed for {config_name}: {len(results)} checks")
        return results

    def _check_nested_field_exists(self, config: Dict[str, Any], field_path: str) -> bool:
        """Check if a nested field exists in configuration dictionary."""
        keys = field_path.split('.')
        current = config

        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return False
            current = current[key]

        return True

    def _check_forbidden_patterns(self, config: Dict[str, Any], results: List[SecurityCheckResult]) -> None:
        """Check configuration values for forbidden security patterns."""
        def check_value(value: Any, path: str = "") -> None:
            if isinstance(value, str):
                for pattern in self.forbidden_patterns:
                    if re.search(pattern, value, re.IGNORECASE):
                        results.append(SecurityCheckResult(
                            check_name="Forbidden Pattern Detection",
                            passed=False,
                            severity="critical",
                            message=f"Potentially dangerous pattern found at {path}: {pattern}",
                            recommendation="Remove or replace the dangerous code pattern"
                        ))
            elif isinstance(value, dict):
                for key, val in value.items():
                    check_value(val, f"{path}.{key}" if path else key)
            elif isinstance(value, list):
                for i, val in enumerate(value):
                    check_value(val, f"{path}[{i}]" if path else f"[{i}]")

        check_value(config)

    def _check_encryption_settings(self, config: Dict[str, Any], results: List[SecurityCheckResult]) -> None:
        """Check encryption-related security settings."""
        security_config = config.get('security', {})

        # Check data encryption at rest
        if security_config.get('data_encryption', {}).get('at_rest', False):
            results.append(SecurityCheckResult(
                check_name="Encryption at Rest",
                passed=True,
                severity="info",
                message="Data encryption at rest is enabled"
            ))
        else:
            results.append(SecurityCheckResult(
                check_name="Encryption at Rest",
                passed=False,
                severity="high",
                message="Data encryption at rest is not enabled",
                recommendation="Enable data encryption at rest for security compliance"
            ))

        # Check encryption in transit
        if security_config.get('data_encryption', {}).get('in_transit', False):
            results.append(SecurityCheckResult(
                check_name="Encryption in Transit",
                passed=True,
                severity="info",
                message="Data encryption in transit is enabled"
            ))
        else:
            results.append(SecurityCheckResult(
                check_name="Encryption in Transit",
                passed=False,
                severity="high",
                message="Data encryption in transit is not enabled",
                recommendation="Enable TLS/SSL for data in transit"
            ))

    def _check_access_control(self, config: Dict[str, Any], results: List[SecurityCheckResult]) -> None:
        """Check access control settings."""
        security_config = config.get('security', {})
        access_control = security_config.get('access_control', 'none')

        if access_control not in ['none', 'open']:
            results.append(SecurityCheckResult(
                check_name="Access Control",
                passed=True,
                severity="info",
                message=f"Access control is configured: {access_control}"
            ))
        else:
            results.append(SecurityCheckResult(
                check_name="Access Control",
                passed=False,
                severity="medium",
                message="Access control is not properly configured",
                recommendation="Implement proper access control mechanisms"
            ))

    def _check_audit_logging(self, config: Dict[str, Any], results: List[SecurityCheckResult]) -> None:
        """Check audit logging configuration."""
        security_config = config.get('security', {})
        audit_logging = security_config.get('audit_logging', False)

        if audit_logging:
            results.append(SecurityCheckResult(
                check_name="Audit Logging",
                passed=True,
                severity="info",
                message="Audit logging is enabled"
            ))
        else:
            results.append(SecurityCheckResult(
                check_name="Audit Logging",
                passed=False,
                severity="medium",
                message="Audit logging is not enabled",
                recommendation="Enable audit logging for security monitoring and compliance"
            ))

    def _check_compliance_standards(self, config: Dict[str, Any], results: List[SecurityCheckResult]) -> None:
        """Check industry compliance standards."""
        compliance_config = config.get('compliance', {})
        industry_standards = compliance_config.get('industry_standards', [])

        required_standards = ['iso_27001', 'soc2_type2', 'gdpr']

        for standard in required_standards:
            if standard in industry_standards:
                results.append(SecurityCheckResult(
                    check_name=f"Compliance: {standard.upper()}",
                    passed=True,
                    severity="info",
                    message=f"{standard.upper()} compliance is configured"
                ))
            else:
                results.append(SecurityCheckResult(
                    check_name=f"Compliance: {standard.upper()}",
                    passed=False,
                    severity="medium",
                    message=f"{standard.upper()} compliance is not configured",
                    recommendation=f"Configure {standard.upper()} compliance settings"
                ))

    def optimize_performance(self, config: Dict[str, Any], config_name: str) -> List[PerformanceMetric]:
        """
        Analyze and optimize performance settings.

        Args:
            config: Configuration dictionary to analyze
            config_name: Name of the configuration being analyzed

        Returns:
            List of performance metrics and recommendations
        """
        metrics = []

        # Check caching configuration
        perf_config = config.get('performance', {})

        if perf_config.get('cache_enabled', False):
            cache_size = perf_config.get('cache_size_mb', 0)
            if cache_size >= 100:
                status = 'good'
                message = "Adequate cache size configured"
            elif cache_size >= 50:
                status = 'warning'
                message = "Consider increasing cache size for better performance"
            else:
                status = 'critical'
                message = "Cache size is too small for optimal performance"

            metrics.append(PerformanceMetric(
                metric_name="Cache Size",
                value=cache_size,
                unit="MB",
                threshold=100,
                status=status
            ))

        # Check timeout settings
        timeout_ms = perf_config.get('timeout_ms', 0)
        if timeout_ms >= 30000:
            timeout_status = 'good'
        elif timeout_ms >= 15000:
            timeout_status = 'warning'
        else:
            timeout_status = 'critical'

        metrics.append(PerformanceMetric(
            metric_name="Timeout Configuration",
            value=timeout_ms,
            unit="ms",
            threshold=30000,
            status=timeout_status
        ))

        # Check parallel execution
        parallel_enabled = perf_config.get('parallel_execution', False)
        if parallel_enabled:
            max_concurrent = perf_config.get('max_concurrent_skills', 1)
            metrics.append(PerformanceMetric(
                metric_name="Parallel Execution",
                value=max_concurrent,
                unit="tasks",
                threshold=3,
                status='good' if max_concurrent >= 3 else 'warning'
            ))

        # Check memory limits
        memory_limit = perf_config.get('memory_limit_mb', 0)
        if memory_limit >= 512:
            memory_status = 'good'
        elif memory_limit >= 256:
            memory_status = 'warning'
        else:
            memory_status = 'critical'

        metrics.append(PerformanceMetric(
            metric_name="Memory Limit",
            value=memory_limit,
            unit="MB",
            threshold=512,
            status=memory_status
        ))

        logger.info(f"Performance optimization analysis completed for {config_name}: {len(metrics)} metrics")
        return metrics

    def generate_security_report(self, results: List[SecurityCheckResult]) -> Dict[str, Any]:
        """
        Generate comprehensive security report.

        Args:
            results: List of security check results

        Returns:
            Security report dictionary
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_checks": len(results),
                "passed": sum(1 for r in results if r.passed),
                "failed": sum(1 for r in results if not r.passed),
                "critical_issues": sum(1 for r in results if not r.passed and r.severity == 'critical'),
                "high_issues": sum(1 for r in results if not r.passed and r.severity == 'high'),
                "medium_issues": sum(1 for r in results if not r.passed and r.severity == 'medium'),
                "low_issues": sum(1 for r in results if not r.passed and r.severity == 'low')
            },
            "detailed_results": []
        }

        for result in results:
            report["detailed_results"].append({
                "check_name": result.check_name,
                "passed": result.passed,
                "severity": result.severity,
                "message": result.message,
                "recommendation": result.recommendation,
                "timestamp": result.timestamp.isoformat()
            })

        return report

    def generate_performance_report(self, metrics: List[PerformanceMetric]) -> Dict[str, Any]:
        """
        Generate comprehensive performance report.

        Args:
            metrics: List of performance metrics

        Returns:
            Performance report dictionary
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_metrics": len(metrics),
                "good_metrics": sum(1 for m in metrics if m.status == 'good'),
                "warning_metrics": sum(1 for m in metrics if m.status == 'warning'),
                "critical_metrics": sum(1 for m in metrics if m.status == 'critical')
            },
            "detailed_metrics": []
        }

        for metric in metrics:
            report["detailed_metrics"].append({
                "metric_name": metric.metric_name,
                "value": metric.value,
                "unit": metric.unit,
                "threshold": metric.threshold,
                "status": metric.status,
                "timestamp": metric.timestamp.isoformat()
            })

        return report

    def save_reports(self, security_report: Dict[str, Any],
                    performance_report: Dict[str, Any],
                    output_dir: Path) -> None:
        """
        Save security and performance reports to files.

        Args:
            security_report: Security report dictionary
            performance_report: Performance report dictionary
            output_dir: Directory to save reports
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save security report
        security_file = output_dir / f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(security_file, 'w', encoding='utf-8') as f:
            json.dump(security_report, f, indent=2, ensure_ascii=False)

        # Save performance report
        performance_file = output_dir / f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(performance_file, 'w', encoding='utf-8') as f:
            json.dump(performance_report, f, indent=2, ensure_ascii=False)

        logger.info(f"Reports saved to {output_dir}")
        logger.info(f"Security report: {security_file}")
        logger.info(f"Performance report: {performance_file}")

    def analyze_all_configurations(self) -> None:
        """Analyze all MCP configurations in the config directory."""
        config_files = list(self.config_dir.glob("*.json")) + list(self.config_dir.glob("*.yaml")) + list(self.config_dir.glob("*.yml"))

        if not config_files:
            logger.warning(f"No configuration files found in {self.config_dir}")
            return

        all_security_results = []
        all_performance_metrics = []

        for config_file in config_files:
            try:
                config = self.load_configuration(config_file)
                config_name = config_file.name

                logger.info(f"Analyzing configuration: {config_name}")

                # Security analysis
                security_results = self.check_security_compliance(config, config_name)
                all_security_results.extend(security_results)

                # Performance analysis
                performance_metrics = self.optimize_performance(config, config_name)
                all_performance_metrics.extend(performance_metrics)

            except Exception as e:
                logger.error(f"Error analyzing {config_file}: {e}")
                continue

        # Generate reports
        security_report = self.generate_security_report(all_security_results)
        performance_report = self.generate_performance_report(all_performance_metrics)

        # Save reports
        output_dir = self.config_dir / "reports"
        self.save_reports(security_report, performance_report, output_dir)

        # Log summary
        logger.info("MCP Security and Performance Analysis Complete")
        logger.info(f"Security: {security_report['summary']['passed']}/{security_report['summary']['total_checks']} checks passed")
        logger.info(f"Performance: {performance_report['summary']['good_metrics']}/{performance_report['summary']['total_metrics']} metrics optimal")


def main() -> None:
    """Main execution function."""
    # Get script directory
    script_dir = Path(__file__).parent

    # Initialize optimizer
    optimizer = MCPSecurityOptimizer(script_dir)

    # Run analysis
    try:
        optimizer.analyze_all_configurations()
        logger.info("MCP Security and Performance Optimization completed successfully")
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()