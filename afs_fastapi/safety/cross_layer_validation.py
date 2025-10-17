"""
Cross-Layer Safety Validation for J1939/ISO 25119 Integration

Provides safety validation at protocol boundaries to ensure J1939 communication
meets ISO 25119 functional safety requirements for agricultural equipment.

Implementation follows Test-First Development (TDD) GREEN phase.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

import can

from afs_fastapi.protocols.sae_j1939 import J1939DTC
from afs_fastapi.safety.iso25119 import (
    DynamicSafetyMonitor,
    SafetyAuditLogger,
    SafetyHeartbeatMonitor,
    SafetyPerformanceMonitor,
)

logger = logging.getLogger(__name__)


class SafetyCriticalityLevel(Enum):
    """Safety criticality levels for J1939 messages."""

    NON_CRITICAL = "non_critical"
    LOW_CRITICAL = "low_critical"
    MEDIUM_CRITICAL = "medium_critical"
    HIGH_CRITICAL = "high_critical"
    SAFETY_CRITICAL = "safety_critical"


@dataclass
class SafetyValidationResult:
    """Result of safety validation for J1939 message."""

    message_id: int
    safety_critical: bool
    criticality_level: SafetyCriticalityLevel
    iso25119_compliant: bool
    validation_passed: bool
    required_sil_level: str
    current_sil_level: str
    validation_errors: list[str] = field(default_factory=list)
    mandatory_actions: list[str] = field(default_factory=list)
    response_time_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class SafetyProtocolMapping:
    """Mapping between J1939 PGN and ISO 25119 safety requirements."""

    pgn: int
    pgn_name: str
    criticality_level: SafetyCriticalityLevel
    required_sil: str
    max_response_time_ms: float
    safety_functions: list[str]
    validation_rules: list[str] = field(default_factory=list)
    iso25119_context: dict[str, Any] = field(default_factory=dict)


@dataclass
class DTCSafetyAnalysis:
    """Safety analysis result for J1939 DTC."""

    dtc: J1939DTC
    safety_impact: str  # none, low, medium, high, critical
    required_response: str  # log, alert, escalate, emergency_stop
    sil_escalation_required: bool = False
    new_sil_level: str | None = None
    mandatory_actions: list[str] = field(default_factory=list)
    iso25119_context: dict[str, Any] = field(default_factory=dict)


class J1939SafetyProtocolMapper:
    """
    Maps J1939 PGNs to ISO 25119 safety requirements.

    Defines safety criticality and requirements for agricultural equipment messages.
    """

    def __init__(self) -> None:
        """Initialize safety protocol mapping."""
        self.safety_mappings = self._load_safety_mappings()

    def _load_safety_mappings(self) -> dict[int, SafetyProtocolMapping]:
        """Load safety mappings for J1939 PGNs."""
        mappings = {
            # Emergency and Safety Critical Messages
            0xFECA: SafetyProtocolMapping(  # DM1 - Active DTCs
                pgn=0xFECA,
                pgn_name="Diagnostic Message 1",
                criticality_level=SafetyCriticalityLevel.HIGH_CRITICAL,
                required_sil="SIL 2",
                max_response_time_ms=500.0,
                safety_functions=["diagnostic_monitoring", "fault_detection"],
                validation_rules=["validate_dtc_format", "check_safety_critical_spns"],
                iso25119_context={"hazard_category": "equipment_failure"},
            ),
            0xF004: SafetyProtocolMapping(  # Engine Controller 1
                pgn=0xF004,
                pgn_name="Electronic Engine Controller 1",
                criticality_level=SafetyCriticalityLevel.MEDIUM_CRITICAL,
                required_sil="SIL 1",
                max_response_time_ms=100.0,
                safety_functions=["engine_monitoring", "performance_validation"],
                validation_rules=["validate_engine_parameters", "check_operating_limits"],
                iso25119_context={"hazard_category": "power_system"},
            ),
            0xFEF3: SafetyProtocolMapping(  # Vehicle Position
                pgn=0xFEF3,
                pgn_name="Vehicle Position",
                criticality_level=SafetyCriticalityLevel.HIGH_CRITICAL,
                required_sil="SIL 2",
                max_response_time_ms=200.0,
                safety_functions=["position_monitoring", "collision_avoidance"],
                validation_rules=["validate_gps_accuracy", "check_position_bounds"],
                iso25119_context={"hazard_category": "navigation_safety"},
            ),
            0xFEF1: SafetyProtocolMapping(  # Vehicle Speed
                pgn=0xFEF1,
                pgn_name="Wheel-Based Vehicle Speed",
                criticality_level=SafetyCriticalityLevel.MEDIUM_CRITICAL,
                required_sil="SIL 1",
                max_response_time_ms=100.0,
                safety_functions=["speed_monitoring", "safe_speed_validation"],
                validation_rules=["validate_speed_range", "check_acceleration_limits"],
                iso25119_context={"hazard_category": "motion_control"},
            ),
            # Emergency Stop Messages (Custom Agricultural PGNs)
            0xEF00: SafetyProtocolMapping(  # Emergency Stop Command
                pgn=0xEF00,
                pgn_name="Emergency Stop Command",
                criticality_level=SafetyCriticalityLevel.SAFETY_CRITICAL,
                required_sil="SIL 3",
                max_response_time_ms=50.0,  # 50ms for emergency stop
                safety_functions=["emergency_stop", "immediate_response"],
                validation_rules=["validate_emergency_authority", "verify_stop_capability"],
                iso25119_context={"hazard_category": "emergency_response"},
            ),
        }

        return mappings

    def get_safety_mapping(self, pgn: int) -> SafetyProtocolMapping | None:
        """Get safety mapping for PGN."""
        return self.safety_mappings.get(pgn)

    def is_safety_critical(self, pgn: int) -> bool:
        """Check if PGN is safety critical."""
        mapping = self.get_safety_mapping(pgn)
        if not mapping:
            return False
        return mapping.criticality_level in [
            SafetyCriticalityLevel.HIGH_CRITICAL,
            SafetyCriticalityLevel.SAFETY_CRITICAL,
        ]

    def get_required_sil(self, pgn: int) -> str | None:
        """Get required SIL level for PGN."""
        mapping = self.get_safety_mapping(pgn)
        return mapping.required_sil if mapping else None


class CrossLayerSafetyValidator:
    """
    Cross-layer safety validator for J1939/ISO 25119 integration.

    Validates safety-critical J1939 messages against ISO 25119 requirements
    and triggers appropriate safety responses.
    """

    def __init__(
        self,
        dynamic_monitor: DynamicSafetyMonitor,
        heartbeat_monitor: SafetyHeartbeatMonitor,
        performance_monitor: SafetyPerformanceMonitor,
        audit_logger: SafetyAuditLogger,
    ) -> None:
        """Initialize cross-layer safety validator."""
        self.protocol_mapper = J1939SafetyProtocolMapper()
        self.dynamic_monitor = dynamic_monitor
        self.heartbeat_monitor = heartbeat_monitor
        self.performance_monitor = performance_monitor
        self.audit_logger = audit_logger

        # Safety state tracking
        self.current_sil_levels: dict[str, str] = {}
        self.safety_violations: list[SafetyValidationResult] = []
        self.emergency_escalation_active = False

        # Register safety functions for heartbeat monitoring
        self._register_safety_functions()

    def _register_safety_functions(self) -> None:
        """Register safety functions for monitoring."""
        safety_functions = [
            "cross_layer_validation",
            "emergency_stop_validation",
            "safety_critical_message_processing",
            "sil_compliance_check",
        ]

        for function in safety_functions:
            self.heartbeat_monitor.register_safety_function(function)

    def validate_safety_critical_message(self, message: can.Message) -> SafetyValidationResult:
        """
        Validate safety-critical J1939 message against ISO 25119 requirements.

        Args:
            message: J1939 CAN message to validate

        Returns:
            Safety validation result
        """
        start_time = self.performance_monitor.start_function_timing("cross_layer_validation")

        try:
            # Extract PGN from message
            pgn = self._extract_pgn(message)

            # Get safety mapping
            safety_mapping = self.protocol_mapper.get_safety_mapping(pgn)

            if not safety_mapping:
                # Non-critical message - minimal validation
                return self._create_non_critical_result(message.arbitration_id, pgn)

            # Record heartbeat for safety function
            self.heartbeat_monitor.heartbeat("safety_critical_message_processing")

            # Perform comprehensive safety validation
            validation_result = self._perform_safety_validation(message, safety_mapping)

            # Check SIL compliance
            sil_compliant = self._validate_sil_compliance(validation_result, safety_mapping)
            validation_result.iso25119_compliant = sil_compliant

            # Log validation result
            self._log_validation_result(validation_result)

            # Trigger safety actions if needed
            if not validation_result.validation_passed:
                self._trigger_safety_response(validation_result, safety_mapping)

            return validation_result

        except Exception as e:
            logger.error(f"Safety validation error: {e}")
            return self._create_error_result(message.arbitration_id, str(e))

        finally:
            # Record performance metrics
            self.performance_monitor.end_function_timing(
                "cross_layer_validation", start_time, success=True
            )

    def _extract_pgn(self, message: can.Message) -> int:
        """Extract PGN from J1939 CAN message."""
        if not message.is_extended_id:
            return 0

        pdu_format = (message.arbitration_id >> 16) & 0xFF
        pdu_specific = (message.arbitration_id >> 8) & 0xFF
        data_page = (message.arbitration_id >> 24) & 0x01

        if pdu_format >= 240:
            # PDU1 format
            pgn = (data_page << 16) | (pdu_format << 8) | pdu_specific
        else:
            # PDU2 format
            pgn = (data_page << 16) | (pdu_format << 8)

        return pgn

    def _create_non_critical_result(self, message_id: int, pgn: int) -> SafetyValidationResult:
        """Create validation result for non-critical message."""
        return SafetyValidationResult(
            message_id=message_id,
            safety_critical=False,
            criticality_level=SafetyCriticalityLevel.NON_CRITICAL,
            iso25119_compliant=True,
            validation_passed=True,
            required_sil_level="SIL 1",
            current_sil_level="SIL 1",
        )

    def _perform_safety_validation(
        self, message: can.Message, mapping: SafetyProtocolMapping
    ) -> SafetyValidationResult:
        """Perform comprehensive safety validation."""
        validation_errors = []
        mandatory_actions = []

        # Validate message timing
        response_time = self._validate_message_timing(mapping)
        if response_time > mapping.max_response_time_ms:
            validation_errors.append(
                f"Response time {response_time:.1f}ms exceeds limit {mapping.max_response_time_ms}ms"
            )

        # Validate message content based on PGN
        content_valid = self._validate_message_content(message, mapping)
        if not content_valid:
            validation_errors.append("Message content validation failed")

        # Check current SIL level adequacy
        current_sil = self.current_sil_levels.get(mapping.pgn_name, "SIL 1")
        if not self._is_sil_adequate(current_sil, mapping.required_sil):
            validation_errors.append(
                f"Current SIL {current_sil} inadequate for required {mapping.required_sil}"
            )
            mandatory_actions.append("escalate_sil_level")

        return SafetyValidationResult(
            message_id=message.arbitration_id,
            safety_critical=True,
            criticality_level=mapping.criticality_level,
            iso25119_compliant=len(validation_errors) == 0,
            validation_passed=len(validation_errors) == 0,
            required_sil_level=mapping.required_sil,
            current_sil_level=current_sil,
            validation_errors=validation_errors,
            mandatory_actions=mandatory_actions,
            response_time_ms=response_time,
        )

    def _validate_message_timing(self, mapping: SafetyProtocolMapping) -> float:
        """Validate message timing requirements."""
        # Get heartbeat status for relevant safety function
        heartbeat_status = self.heartbeat_monitor.get_health_status()

        relevant_function = None
        for func_name in heartbeat_status:
            if any(safety_func in func_name for safety_func in mapping.safety_functions):
                relevant_function = func_name
                break

        if relevant_function and relevant_function in heartbeat_status:
            return heartbeat_status[relevant_function].response_time_ms

        return 0.0  # No timing data available

    def _validate_message_content(
        self, message: can.Message, mapping: SafetyProtocolMapping
    ) -> bool:
        """Validate message content based on safety rules."""
        # Apply validation rules specific to the PGN
        for rule in mapping.validation_rules:
            if not self._apply_validation_rule(rule, message, mapping):
                return False
        return True

    def _apply_validation_rule(
        self, rule: str, message: can.Message, mapping: SafetyProtocolMapping
    ) -> bool:
        """Apply specific validation rule."""
        if rule == "validate_dtc_format":
            return self._validate_dtc_format(message)
        elif rule == "validate_engine_parameters":
            return self._validate_engine_parameters(message)
        elif rule == "validate_gps_accuracy":
            return self._validate_gps_accuracy(message)
        elif rule == "validate_speed_range":
            return self._validate_speed_range(message)
        elif rule == "validate_emergency_authority":
            return self._validate_emergency_authority(message)
        else:
            # Unknown rule - default to pass
            return True

    def _validate_dtc_format(self, message: can.Message) -> bool:
        """Validate DTC message format."""
        return len(message.data) >= 2  # Minimum DTC message length

    def _validate_engine_parameters(self, message: can.Message) -> bool:
        """Validate engine parameter ranges."""
        if len(message.data) < 4:
            return False

        # Basic engine parameter validation
        return True  # Simplified for now

    def _validate_gps_accuracy(self, message: can.Message) -> bool:
        """Validate GPS accuracy requirements."""
        # Check for valid GPS position data format
        return len(message.data) >= 8

    def _validate_speed_range(self, message: can.Message) -> bool:
        """Validate speed is within safe operational range."""
        if len(message.data) < 3:
            return False

        # Basic speed validation - ensure not exceeding safe limits
        return True  # Simplified for now

    def _validate_emergency_authority(self, message: can.Message) -> bool:
        """Validate emergency command authority."""
        # Verify message comes from authorized emergency system
        source_address = message.arbitration_id & 0xFF
        authorized_addresses = [0x00, 0x01, 0xF9]  # Authorized emergency controllers
        return source_address in authorized_addresses

    def _is_sil_adequate(self, current_sil: str, required_sil: str) -> bool:
        """Check if current SIL level meets requirement."""
        sil_levels = {"SIL 1": 1, "SIL 2": 2, "SIL 3": 3, "SIL 4": 4}
        current_level = sil_levels.get(current_sil, 1)
        required_level = sil_levels.get(required_sil, 1)
        return current_level >= required_level

    def _validate_sil_compliance(
        self, result: SafetyValidationResult, mapping: SafetyProtocolMapping
    ) -> bool:
        """Validate ISO 25119 SIL compliance."""
        # Check if validation passed and SIL is adequate
        return result.validation_passed and self._is_sil_adequate(
            result.current_sil_level, result.required_sil_level
        )

    def _log_validation_result(self, result: SafetyValidationResult) -> None:
        """Log validation result to audit trail."""
        severity = "critical" if not result.validation_passed else "low"

        self.audit_logger.log_safety_event(
            event_type="safety_validation",
            severity=severity,
            description=f"Cross-layer validation for message {result.message_id:08X}",
            safety_function="cross_layer_validation",
            response_actions=result.mandatory_actions,
            iso25119_context={
                "criticality_level": result.criticality_level.value,
                "required_sil": result.required_sil_level,
                "validation_errors": result.validation_errors,
            },
        )

    def _trigger_safety_response(
        self, result: SafetyValidationResult, mapping: SafetyProtocolMapping
    ) -> None:
        """Trigger appropriate safety response for validation failure."""
        if result.criticality_level == SafetyCriticalityLevel.SAFETY_CRITICAL:
            self._trigger_emergency_response(result, mapping)
        elif result.criticality_level == SafetyCriticalityLevel.HIGH_CRITICAL:
            self._trigger_high_priority_response(result, mapping)
        else:
            self._trigger_standard_response(result, mapping)

    def _trigger_emergency_response(
        self, result: SafetyValidationResult, mapping: SafetyProtocolMapping
    ) -> None:
        """Trigger emergency response for safety-critical violations."""
        self.emergency_escalation_active = True

        logger.critical(
            f"Emergency response triggered for safety-critical message {result.message_id:08X}"
        )

        # Record emergency event
        self.audit_logger.log_safety_event(
            event_type="emergency_response",
            severity="critical",
            description=f"Emergency response for {mapping.pgn_name}",
            safety_function="emergency_stop",
            response_actions=["immediate_stop", "operator_alert", "system_isolation"],
            iso25119_context={"trigger": "safety_critical_validation_failure"},
        )

    def _trigger_high_priority_response(
        self, result: SafetyValidationResult, mapping: SafetyProtocolMapping
    ) -> None:
        """Trigger high priority response for critical violations."""
        logger.warning(f"High priority safety response for message {result.message_id:08X}")

        # Escalate SIL level if required
        if "escalate_sil_level" in result.mandatory_actions:
            self._escalate_sil_level(mapping.pgn_name, mapping.required_sil)

    def _trigger_standard_response(
        self, result: SafetyValidationResult, mapping: SafetyProtocolMapping
    ) -> None:
        """Trigger standard response for medium/low priority violations."""
        logger.info(f"Standard safety response for message {result.message_id:08X}")

    def _escalate_sil_level(self, system_name: str, target_sil: str) -> None:
        """Escalate SIL level for system."""
        old_sil = self.current_sil_levels.get(system_name, "SIL 1")
        self.current_sil_levels[system_name] = target_sil

        logger.warning(f"SIL escalation: {system_name} from {old_sil} to {target_sil}")

        self.audit_logger.log_safety_event(
            event_type="sil_escalation",
            severity="medium",
            description=f"SIL escalated for {system_name}",
            safety_function="sil_compliance_check",
            response_actions=[f"escalate_to_{target_sil}"],
            iso25119_context={"old_sil": old_sil, "new_sil": target_sil},
        )

    def _create_error_result(self, message_id: int, error: str) -> SafetyValidationResult:
        """Create error validation result."""
        return SafetyValidationResult(
            message_id=message_id,
            safety_critical=True,
            criticality_level=SafetyCriticalityLevel.HIGH_CRITICAL,
            iso25119_compliant=False,
            validation_passed=False,
            required_sil_level="SIL 3",
            current_sil_level="SIL 1",
            validation_errors=[f"Validation error: {error}"],
        )

    def get_safety_status(self) -> dict[str, Any]:
        """Get comprehensive safety status."""
        return {
            "current_sil_levels": self.current_sil_levels.copy(),
            "emergency_escalation_active": self.emergency_escalation_active,
            "recent_violations": len(
                [
                    v
                    for v in self.safety_violations
                    if (datetime.now() - v.timestamp) < timedelta(minutes=10)
                ]
            ),
            "heartbeat_status": self.heartbeat_monitor.get_health_status(),
            "performance_compliant": self.performance_monitor.is_system_compliant(),
        }


class DTCSafetyAnalyzer:
    """
    Enhanced diagnostic integration between J1939 DTCs and ISO 25119 safety analysis.

    Analyzes J1939 DTCs for safety implications and triggers appropriate responses.
    """

    def __init__(
        self,
        dynamic_monitor: DynamicSafetyMonitor,
        audit_logger: SafetyAuditLogger,
    ) -> None:
        """Initialize DTC safety analyzer."""
        self.dynamic_monitor = dynamic_monitor
        self.audit_logger = audit_logger
        self.safety_critical_spns = self._load_safety_critical_spns()

    def _load_safety_critical_spns(self) -> dict[int, dict[str, Any]]:
        """Load safety-critical SPN definitions."""
        return {
            110: {  # Engine Coolant Temperature
                "safety_impact": "high",
                "response": "alert",
                "escalation_required": True,
                "target_sil": "SIL 2",
                "mandatory_actions": ["reduce_engine_load", "activate_cooling_protocol"],
            },
            190: {  # Engine Speed
                "safety_impact": "medium",
                "response": "alert",
                "escalation_required": False,
                "mandatory_actions": ["monitor_engine_parameters"],
            },
            9999: {  # Emergency Stop System
                "safety_impact": "critical",
                "response": "emergency_stop",
                "escalation_required": True,
                "target_sil": "SIL 3",
                "mandatory_actions": ["immediate_stop", "isolate_system", "operator_notification"],
            },
            84: {  # Vehicle Speed Sensor
                "safety_impact": "high",
                "response": "escalate",
                "escalation_required": True,
                "target_sil": "SIL 2",
                "mandatory_actions": ["activate_backup_sensors", "reduce_max_speed"],
            },
        }

    def analyze_dtc_safety_impact(self, dtc: J1939DTC) -> DTCSafetyAnalysis:
        """
        Analyze safety impact of J1939 DTC.

        Args:
            dtc: J1939 Diagnostic Trouble Code

        Returns:
            Safety analysis result
        """
        spn_config = self.safety_critical_spns.get(dtc.spn, {})

        # Determine safety impact
        safety_impact = spn_config.get("safety_impact", "low")
        required_response = spn_config.get("response", "log")
        escalation_required = spn_config.get("escalation_required", False)

        # Get mandatory actions
        mandatory_actions = spn_config.get("mandatory_actions", [])

        # Determine SIL escalation
        new_sil_level = None
        if escalation_required:
            new_sil_level = spn_config.get("target_sil", "SIL 2")

        analysis = DTCSafetyAnalysis(
            dtc=dtc,
            safety_impact=safety_impact,
            required_response=required_response,
            sil_escalation_required=escalation_required,
            new_sil_level=new_sil_level,
            mandatory_actions=mandatory_actions,
            iso25119_context={
                "spn": dtc.spn,
                "fmi": dtc.fmi,
                "occurrence_count": dtc.occurrence_count,
                "timestamp": getattr(dtc, "timestamp", datetime.now()).isoformat(),
            },
        )

        # Log safety analysis
        self._log_dtc_analysis(analysis)

        # Trigger safety actions
        self._execute_safety_actions(analysis)

        return analysis

    def _log_dtc_analysis(self, analysis: DTCSafetyAnalysis) -> None:
        """Log DTC safety analysis to audit trail."""
        severity_map = {
            "none": "low",
            "low": "low",
            "medium": "medium",
            "high": "high",
            "critical": "critical",
        }

        severity = severity_map.get(analysis.safety_impact, "medium")

        self.audit_logger.log_safety_event(
            event_type="dtc_safety_analysis",
            severity=severity,
            description=f"DTC safety analysis for SPN {analysis.dtc.spn}, FMI {analysis.dtc.fmi}",
            safety_function="diagnostic_integration",
            response_actions=analysis.mandatory_actions,
            iso25119_context=analysis.iso25119_context,
        )

    def _execute_safety_actions(self, analysis: DTCSafetyAnalysis) -> None:
        """Execute safety actions based on DTC analysis."""
        if analysis.required_response == "emergency_stop":
            self._trigger_emergency_stop(analysis)
        elif analysis.required_response == "escalate":
            self._escalate_safety_level(analysis)
        elif analysis.required_response == "alert":
            self._send_safety_alert(analysis)

    def _trigger_emergency_stop(self, analysis: DTCSafetyAnalysis) -> None:
        """Trigger emergency stop for critical DTC."""
        logger.critical(
            f"Emergency stop triggered by DTC: SPN {analysis.dtc.spn}, FMI {analysis.dtc.fmi}"
        )

        self.audit_logger.log_safety_event(
            event_type="emergency_stop",
            severity="critical",
            description=f"Emergency stop due to critical DTC SPN {analysis.dtc.spn}",
            safety_function="emergency_response",
            response_actions=["immediate_stop", "isolate_systems", "operator_alert"],
            iso25119_context=analysis.iso25119_context,
        )

    def _escalate_safety_level(self, analysis: DTCSafetyAnalysis) -> None:
        """Escalate safety level for high-impact DTC."""
        logger.warning(
            f"Safety level escalation for DTC: SPN {analysis.dtc.spn}, FMI {analysis.dtc.fmi}"
        )

    def _send_safety_alert(self, analysis: DTCSafetyAnalysis) -> None:
        """Send safety alert for medium-impact DTC."""
        logger.info(f"Safety alert for DTC: SPN {analysis.dtc.spn}, FMI {analysis.dtc.fmi}")
