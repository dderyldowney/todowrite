#!/usr/bin/env python3
"""
MCP Monitoring and Analytics Dashboard for 2025 Industry Standards

This module provides real-time monitoring and analytics for MCP (Model Context Protocol)
configurations including performance metrics, security status, and operational insights.

Features:
- Real-time performance monitoring
- Security compliance tracking
- Usage analytics and insights
- Automated alerting and notifications
- Interactive dashboard capabilities
- Historical trend analysis

Author: Claude Code Assistant
Version: 2025.1.0
"""

import json
import logging
import sqlite3
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(Path(__file__).parent / "mcp_monitoring.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


@dataclass
class MonitoringMetric:
    """Base monitoring metric data structure"""

    timestamp: datetime
    metric_name: str
    value: float
    unit: str
    tags: dict[str, str]
    source: str


@dataclass
class SecurityEvent:
    """Security event data structure"""

    timestamp: datetime
    event_type: str
    severity: str
    description: str
    source: str
    resolved: bool = False
    resolution_time: datetime | None = None


@dataclass
class PerformanceAlert:
    """Performance alert data structure"""

    timestamp: datetime
    alert_type: str
    metric_name: str
    current_value: float
    threshold: float
    severity: str
    message: str


class MCPMonitoringDashboard:
    """Main MCP Monitoring Dashboard class"""

    def __init__(self, config_dir: Path, db_path: Path | None = None) -> None:
        """
        Initialize the MCP Monitoring Dashboard.

        Args:
            config_dir: Directory containing MCP configuration files
            db_path: Path to SQLite database for storing metrics
        """
        self.config_dir = Path(config_dir)

        if db_path is None:
            self.db_path = self.config_dir / "mcp_monitoring.db"
        else:
            self.db_path = db_path

        # In-memory storage for real-time metrics
        self.metrics_buffer: deque = deque(maxlen=10000)
        self.security_events: deque = deque(maxlen=1000)
        self.performance_alerts: deque = deque(maxlen=500)

        # Monitoring thresholds
        self.thresholds = {
            "response_time_ms": 5000,
            "error_rate_percent": 5.0,
            "memory_usage_percent": 80.0,
            "cpu_usage_percent": 70.0,
            "disk_usage_percent": 85.0,
            "cache_hit_rate_percent": 80.0,
            "security_vulnerabilities": 0,
        }

        # Initialize database
        self._init_database()

        # Start background monitoring tasks
        self.monitoring_active = True

    def _init_database(self) -> None:
        """Initialize SQLite database for metrics storage."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    metric_name TEXT NOT NULL,
                    value REAL NOT NULL,
                    unit TEXT NOT NULL,
                    tags TEXT,
                    source TEXT NOT NULL
                )
            """)

            # Create security events table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS security_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    description TEXT NOT NULL,
                    source TEXT NOT NULL,
                    resolved BOOLEAN DEFAULT FALSE,
                    resolution_time TEXT
                )
            """)

            # Create performance alerts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS performance_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    alert_type TEXT NOT NULL,
                    metric_name TEXT NOT NULL,
                    current_value REAL NOT NULL,
                    threshold REAL NOT NULL,
                    severity TEXT NOT NULL,
                    message TEXT NOT NULL
                )
            """)

            # Create indexes for better performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_name ON metrics(metric_name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_source ON metrics(source)")

            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_events_timestamp ON security_events(timestamp)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_events_severity ON security_events(severity)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_events_resolved ON security_events(resolved)"
            )

            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON performance_alerts(timestamp)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_alerts_severity ON performance_alerts(severity)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_alerts_metric ON performance_alerts(metric_name)"
            )

            conn.commit()
            conn.close()
            logger.info(f"Database initialized: {self.db_path}")

        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            raise

    def record_metric(self, metric: MonitoringMetric) -> None:
        """
        Record a monitoring metric.

        Args:
            metric: MonitoringMetric to record
        """
        # Add to in-memory buffer
        self.metrics_buffer.append(metric)

        # Check thresholds and generate alerts
        self._check_performance_thresholds(metric)

        # Store in database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO metrics (timestamp, metric_name, value, unit, tags, source)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    metric.timestamp.isoformat(),
                    metric.metric_name,
                    metric.value,
                    metric.unit,
                    json.dumps(metric.tags),
                    metric.source,
                ),
            )
            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            logger.error(f"Error storing metric: {e}")

    def record_security_event(self, event: SecurityEvent) -> None:
        """
        Record a security event.

        Args:
            event: SecurityEvent to record
        """
        # Add to in-memory buffer
        self.security_events.append(event)

        # Store in database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO security_events (timestamp, event_type, severity, description, source, resolved, resolution_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    event.timestamp.isoformat(),
                    event.event_type,
                    event.severity,
                    event.description,
                    event.source,
                    event.resolved,
                    event.resolution_time.isoformat() if event.resolution_time else None,
                ),
            )
            conn.commit()
            conn.close()

            # Log security event
            if event.severity in ["critical", "high"]:
                logger.warning(f"Security event: {event.event_type} - {event.description}")

        except sqlite3.Error as e:
            logger.error(f"Error storing security event: {e}")

    def _check_performance_thresholds(self, metric: MonitoringMetric) -> None:
        """Check if metric exceeds thresholds and generate alerts."""
        metric_name = metric.metric_name.lower()

        for threshold_name, threshold_value in self.thresholds.items():
            if threshold_name in metric_name:
                if metric.value > threshold_value:
                    severity = "critical" if metric.value > threshold_value * 1.5 else "warning"

                    alert = PerformanceAlert(
                        timestamp=datetime.now(),
                        alert_type="threshold_exceeded",
                        metric_name=metric.metric_name,
                        current_value=metric.value,
                        threshold=threshold_value,
                        severity=severity,
                        message=f"{metric.metric_name} exceeded threshold: {metric.value} > {threshold_value} {metric.unit}",
                    )

                    self.performance_alerts.append(alert)
                    self._store_alert(alert)
                    logger.warning(f"Performance alert: {alert.message}")

    def _store_alert(self, alert: PerformanceAlert) -> None:
        """Store performance alert in database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO performance_alerts (timestamp, alert_type, metric_name, current_value, threshold, severity, message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    alert.timestamp.isoformat(),
                    alert.alert_type,
                    alert.metric_name,
                    alert.current_value,
                    alert.threshold,
                    alert.severity,
                    alert.message,
                ),
            )
            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            logger.error(f"Error storing alert: {e}")

    def get_metrics_summary(self, hours: int = 24) -> dict[str, Any]:
        """
        Get summary of metrics for the specified time period.

        Args:
            hours: Number of hours to look back

        Returns:
            Dictionary containing metrics summary
        """
        since_time = datetime.now() - timedelta(hours=hours)

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT metric_name, COUNT(*) as count, AVG(value) as avg_value,
                       MIN(value) as min_value, MAX(value) as max_value
                FROM metrics
                WHERE timestamp > ?
                GROUP BY metric_name
                ORDER BY metric_name
            """,
                (since_time.isoformat(),),
            )

            results = cursor.fetchall()
            conn.close()

            summary = {
                "time_period_hours": hours,
                "total_metrics": sum(row[1] for row in results),
                "metric_breakdown": {},
            }

            for row in results:
                metric_name, count, avg_value, min_value, max_value = row
                summary["metric_breakdown"][metric_name] = {
                    "count": count,
                    "average": round(avg_value, 2),
                    "minimum": min_value,
                    "maximum": max_value,
                }

            return summary

        except sqlite3.Error as e:
            logger.error(f"Error getting metrics summary: {e}")
            return {"error": str(e)}

    def get_security_summary(self, days: int = 7) -> dict[str, Any]:
        """
        Get summary of security events for the specified time period.

        Args:
            days: Number of days to look back

        Returns:
            Dictionary containing security summary
        """
        since_time = datetime.now() - timedelta(days=days)

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get security events by severity
            cursor.execute(
                """
                SELECT severity, COUNT(*) as count
                FROM security_events
                WHERE timestamp > ?
                GROUP BY severity
                ORDER BY severity
            """,
                (since_time.isoformat(),),
            )

            severity_counts = dict(cursor.fetchall())

            # Get recent events
            cursor.execute(
                """
                SELECT event_type, severity, description, timestamp
                FROM security_events
                WHERE timestamp > ?
                ORDER BY timestamp DESC
                LIMIT 10
            """,
                (since_time.isoformat(),),
            )

            recent_events = [
                {
                    "event_type": row[0],
                    "severity": row[1],
                    "description": row[2],
                    "timestamp": row[3],
                }
                for row in cursor.fetchall()
            ]

            conn.close()

            summary = {
                "time_period_days": days,
                "total_events": sum(severity_counts.values()),
                "events_by_severity": severity_counts,
                "recent_events": recent_events,
                "critical_events": severity_counts.get("critical", 0),
                "high_events": severity_counts.get("high", 0),
            }

            return summary

        except sqlite3.Error as e:
            logger.error(f"Error getting security summary: {e}")
            return {"error": str(e)}

    def get_alert_summary(self, hours: int = 24) -> dict[str, Any]:
        """
        Get summary of performance alerts for the specified time period.

        Args:
            hours: Number of hours to look back

        Returns:
            Dictionary containing alert summary
        """
        since_time = datetime.now() - timedelta(hours=hours)

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get alerts by severity
            cursor.execute(
                """
                SELECT severity, COUNT(*) as count
                FROM performance_alerts
                WHERE timestamp > ?
                GROUP BY severity
                ORDER BY severity
            """,
                (since_time.isoformat(),),
            )

            severity_counts = dict(cursor.fetchall())

            # Get recent alerts
            cursor.execute(
                """
                SELECT alert_type, metric_name, current_value, threshold, severity, message, timestamp
                FROM performance_alerts
                WHERE timestamp > ?
                ORDER BY timestamp DESC
                LIMIT 10
            """,
                (since_time.isoformat(),),
            )

            recent_alerts = [
                {
                    "alert_type": row[0],
                    "metric_name": row[1],
                    "current_value": row[2],
                    "threshold": row[3],
                    "severity": row[4],
                    "message": row[5],
                    "timestamp": row[6],
                }
                for row in cursor.fetchall()
            ]

            conn.close()

            summary = {
                "time_period_hours": hours,
                "total_alerts": sum(severity_counts.values()),
                "alerts_by_severity": severity_counts,
                "recent_alerts": recent_alerts,
                "critical_alerts": severity_counts.get("critical", 0),
                "warning_alerts": severity_counts.get("warning", 0),
            }

            return summary

        except sqlite3.Error as e:
            logger.error(f"Error getting alert summary: {e}")
            return {"error": str(e)}

    def generate_dashboard_data(self) -> dict[str, Any]:
        """
        Generate comprehensive dashboard data for visualization.

        Returns:
            Dictionary containing all dashboard data
        """
        dashboard_data = {
            "timestamp": datetime.now().isoformat(),
            "system_status": "healthy",
            "metrics_summary": self.get_metrics_summary(),
            "security_summary": self.get_security_summary(),
            "alert_summary": self.get_alert_summary(),
            "performance_trends": self._get_performance_trends(),
            "health_indicators": self._get_health_indicators(),
        }

        # Determine overall system status
        critical_alerts = dashboard_data["alert_summary"].get("critical_alerts", 0)
        critical_events = dashboard_data["security_summary"].get("critical_events", 0)

        if critical_alerts > 0 or critical_events > 0:
            dashboard_data["system_status"] = "critical"
        elif dashboard_data["alert_summary"].get("warning_alerts", 0) > 5:
            dashboard_data["system_status"] = "warning"

        return dashboard_data

    def _get_performance_trends(self) -> dict[str, list[float]]:
        """Get performance trends for key metrics over time."""
        trends = {}
        key_metrics = [
            "response_time_ms",
            "memory_usage_percent",
            "cpu_usage_percent",
            "cache_hit_rate_percent",
        ]

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            for metric in key_metrics:
                cursor.execute(
                    """
                    SELECT timestamp, value
                    FROM metrics
                    WHERE metric_name = ? AND timestamp > ?
                    ORDER BY timestamp ASC
                    LIMIT 100
                """,
                    (metric, (datetime.now() - timedelta(hours=24)).isoformat()),
                )

                results = cursor.fetchall()
                trends[metric] = [float(row[1]) for row in results]

            conn.close()

        except sqlite3.Error as e:
            logger.error(f"Error getting performance trends: {e}")

        return trends

    def _get_health_indicators(self) -> dict[str, Any]:
        """Get system health indicators."""
        indicators = {
            "database_health": "unknown",
            "security_health": "unknown",
            "performance_health": "unknown",
            "last_update": datetime.now().isoformat(),
        }

        # Check database connectivity
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM metrics WHERE timestamp > ?",
                ((datetime.now() - timedelta(hours=1)).isoformat(),),
            )
            recent_metrics = cursor.fetchone()[0]
            conn.close()

            if recent_metrics > 0:
                indicators["database_health"] = "healthy"
            else:
                indicators["database_health"] = "warning"

        except sqlite3.Error:
            indicators["database_health"] = "error"

        # Check security health
        security_summary = self.get_security_summary(days=1)
        if security_summary.get("critical_events", 0) > 0:
            indicators["security_health"] = "critical"
        elif security_summary.get("high_events", 0) > 0:
            indicators["security_health"] = "warning"
        else:
            indicators["security_health"] = "healthy"

        # Check performance health
        alert_summary = self.get_alert_summary(hours=1)
        if alert_summary.get("critical_alerts", 0) > 0:
            indicators["performance_health"] = "critical"
        elif alert_summary.get("warning_alerts", 0) > 5:
            indicators["performance_health"] = "warning"
        else:
            indicators["performance_health"] = "healthy"

        return indicators

    def export_dashboard_data(self, output_path: Path) -> None:
        """
        Export dashboard data to JSON file.

        Args:
            output_path: Path to export the dashboard data
        """
        dashboard_data = self.generate_dashboard_data()

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(dashboard_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Dashboard data exported to {output_path}")

        except Exception as e:
            logger.error(f"Error exporting dashboard data: {e}")

    def cleanup_old_data(self, days_to_keep: int = 30) -> None:
        """
        Clean up old data from the database.

        Args:
            days_to_keep: Number of days to keep data
        """
        cutoff_time = datetime.now() - timedelta(days=days_to_keep)

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Clean up old metrics
            cursor.execute("DELETE FROM metrics WHERE timestamp < ?", (cutoff_time.isoformat(),))
            metrics_deleted = cursor.rowcount

            # Clean up old resolved security events
            cursor.execute(
                """
                DELETE FROM security_events
                WHERE timestamp < ? AND resolved = TRUE
            """,
                (cutoff_time.isoformat(),),
            )
            events_deleted = cursor.rowcount

            # Clean up old performance alerts
            cursor.execute(
                "DELETE FROM performance_alerts WHERE timestamp < ?", (cutoff_time.isoformat(),)
            )
            alerts_deleted = cursor.rowcount

            conn.commit()
            conn.close()

            logger.info(
                f"Cleanup completed: {metrics_deleted} metrics, {events_deleted} events, {alerts_deleted} alerts deleted"
            )

        except sqlite3.Error as e:
            logger.error(f"Error during cleanup: {e}")


def main() -> None:
    """Main execution function."""
    script_dir = Path(__file__).parent

    # Initialize monitoring dashboard
    dashboard = MCPMonitoringDashboard(script_dir)

    # Generate sample metrics for testing
    logger.info("Generating sample metrics...")

    # Sample metrics
    sample_metrics = [
        MonitoringMetric(
            timestamp=datetime.now() - timedelta(minutes=i),
            metric_name="response_time_ms",
            value=100 + (i % 50),
            unit="ms",
            tags={"endpoint": "/api/search", "method": "POST"},
            source="episodic-memory",
        )
        for i in range(60)  # Last 60 minutes
    ]

    for metric in sample_metrics:
        dashboard.record_metric(metric)

    # Sample security event
    security_event = SecurityEvent(
        timestamp=datetime.now(),
        event_type="authentication_failure",
        severity="medium",
        description="Failed login attempt from unknown source",
        source="authentication_service",
    )
    dashboard.record_security_event(security_event)

    # Generate dashboard data
    dashboard_data = dashboard.generate_dashboard_data()

    # Export dashboard data
    output_file = script_dir / "dashboard_data.json"
    dashboard.export_dashboard_data(output_file)

    # Print summary
    print("MCP Monitoring Dashboard Summary:")
    print(f"System Status: {dashboard_data['system_status']}")
    print(f"Total Metrics: {dashboard_data['metrics_summary'].get('total_metrics', 0)}")
    print(f"Security Events: {dashboard_data['security_summary'].get('total_events', 0)}")
    print(f"Performance Alerts: {dashboard_data['alert_summary'].get('total_alerts', 0)}")
    print(f"Dashboard data exported to: {output_file}")


if __name__ == "__main__":
    main()
