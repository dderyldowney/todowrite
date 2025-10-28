# ToDoWrite Integration Guide

## Overview

This guide demonstrates real-world integration scenarios for the ToDoWrite 12-layer declarative planning framework, showing how to structure complex projects from Goal to Command execution.

## Core Concepts

### The 12-Layer Framework

ToDoWrite organizes project planning into 12 hierarchical layers:

**Strategic & High-Level Planning (Layers 1-4):**
1. **Goal** - Ultimate outcome and business value
2. **Concept** - Big-picture architectural approach
3. **Context** - Environment, actors, and assumptions
4. **Constraints** - Standards, safety, budget, and legal limits

**Specification & Definition (Layers 5-7):**
5. **Requirements** - Atomic, testable statements
6. **Acceptance Criteria** - Objective pass/fail conditions
7. **Interface Contract** - APIs, schemas, and protocols

**Work Breakdown & Granular Units (Layers 8-11):**
8. **Phase** - Major delivery slices
9. **Step** - Single-concern work units
10. **Task** - Contributor work assignments
11. **SubTask** - Smallest planning granules

**Execution (Layer 12):**
12. **Command** - **ONLY** executable layer with scripts/CLI

### Key Principles

- **Separation of Concerns**: Layers 1-11 are purely declarative YAML
- **Traceability**: Complete forward/backward linking from Goal to Command
- **Build-time Validation**: Schema validation and SoC linting
- **Command Generation**: Automated stub creation from Acceptance Criteria

## Scenario 1: Agricultural Automation Project

### Project Overview

Implement autonomous coordination for multiple agricultural tractors in a field operation.

### Step 1: Create the Planning Hierarchy

```bash
# Initialize the system
make tw-deps
make tw-init

# Create Goal layer
cat > configs/plans/goals/GOAL-FARM-AUTOMATION.yaml << EOF
id: GOAL-FARM-AUTOMATION
layer: Goal
title: Autonomous Multi-Tractor Field Coordination
description: >
  Enable multiple autonomous tractors to coordinate field operations
  safely and efficiently, reducing overlap and optimizing coverage
  while maintaining safety standards for agricultural environments.
metadata:
  owner: agricultural-team
  labels: [agriculture, autonomous, safety-critical, coordination]
  severity: high
  work_type: architecture
links:
  parents: []
  children: []
EOF

# Create Concept layer
cat > configs/plans/concepts/CON-FLEET-COORDINATION.yaml << EOF
id: CON-FLEET-COORDINATION
layer: Concept
title: Distributed Fleet Coordination Architecture
description: >
  Implement a distributed coordination system where tractors
  communicate via mesh network to share position, task assignments,
  and safety status. Central coordination node provides oversight
  and conflict resolution.
metadata:
  owner: system-architect
  labels: [distributed-systems, mesh-network, coordination]
  severity: high
  work_type: architecture
links:
  parents: [GOAL-FARM-AUTOMATION]
  children: []
EOF

# Create Context layer
cat > configs/plans/contexts/CTX-FARM-ENVIRONMENT.yaml << EOF
id: CTX-FARM-ENVIRONMENT
layer: Context
title: Agricultural Field Operation Environment
description: >
  Operating environment consists of 5-50 acre fields with varying
  terrain, multiple John Deere autonomous tractors (up to 8 units),
  GPS/RTK positioning system, cellular/satellite connectivity,
  weather monitoring, and human oversight station.
metadata:
  owner: field-operations
  labels: [environment, field-ops, gps, connectivity]
  severity: med
  work_type: architecture
links:
  parents: [CON-FLEET-COORDINATION]
  children: []
EOF
```

### Step 2: Define Constraints and Requirements

```bash
# Create Constraints
cat > configs/plans/constraints/CST-SAFETY-REGULATIONS.yaml << EOF
id: CST-SAFETY-REGULATIONS
layer: Constraints
title: Agricultural Safety and Regulatory Constraints
description: >
  MANDATORY: ISO 25119 functional safety compliance (ASIL B).
  Maximum 30km/h operating speed. 5-meter minimum separation between
  vehicles. Emergency stop within 2 seconds. Human oversight required
  within 500m. Weather operation limits (wind < 25km/h, no precipitation).
metadata:
  owner: safety-engineer
  labels: [safety, iso25119, regulations, emergency-stop]
  severity: high
  work_type: validation
links:
  parents: [CTX-FARM-ENVIRONMENT]
  children: []
EOF

# Create Functional Requirements
cat > configs/plans/requirements/R-POSITION-TRACKING.yaml << EOF
id: R-POSITION-TRACKING
layer: Requirements
title: Real-time Position Tracking System
description: >
  The system SHALL track position of all tractors with ±10cm accuracy
  using RTK-GPS, update positions every 100ms, and broadcast position
  data to all fleet members within 200ms latency.
metadata:
  owner: positioning-engineer
  labels: [gps, rtk, real-time, accuracy]
  severity: high
  work_type: implementation
links:
  parents: [CST-SAFETY-REGULATIONS]
  children: []
EOF

cat > configs/plans/requirements/R-COLLISION-AVOIDANCE.yaml << EOF
id: R-COLLISION-AVOIDANCE
layer: Requirements
title: Active Collision Avoidance System
description: >
  The system SHALL detect potential collisions 10 seconds in advance,
  automatically adjust paths to maintain 5-meter minimum separation,
  and execute emergency stop if separation drops below 3 meters.
metadata:
  owner: safety-engineer
  labels: [collision-avoidance, safety, emergency-stop]
  severity: high
  work_type: implementation
links:
  parents: [CST-SAFETY-REGULATIONS]
  children: []
EOF
```

### Step 3: Create Acceptance Criteria

```bash
# Acceptance Criteria for Position Tracking
cat > configs/plans/acceptance_criteria/AC-POSITION-ACCURACY-VERIFIED.yaml << EOF
id: AC-POSITION-ACCURACY-VERIFIED
layer: AcceptanceCriteria
title: Position tracking achieves required accuracy and latency
description: >
  PASS: GPS tracking demonstrates ±10cm accuracy over 1000 position
  samples, position updates occur every 100ms ±5ms, and broadcast
  latency is consistently under 200ms in field testing.
  FAIL: Any measurement exceeds specified tolerances.
metadata:
  owner: positioning-engineer
  labels: [testing, accuracy, latency, field-test]
  severity: high
  work_type: validation
links:
  parents: [R-POSITION-TRACKING]
  children: []
EOF

# Acceptance Criteria for Collision Avoidance
cat > configs/plans/acceptance_criteria/AC-COLLISION-PREVENTION-TESTED.yaml << EOF
id: AC-COLLISION-PREVENTION-TESTED
layer: AcceptanceCriteria
title: Collision avoidance prevents all dangerous situations
description: >
  PASS: System successfully prevents collisions in 100 simulated
  scenarios including sudden stops, communication loss, and adverse
  weather. Emergency stops complete within 2 seconds. No separation
  violations below 5 meters occur during normal operation.
  FAIL: Any collision occurs or emergency stop exceeds 2 seconds.
metadata:
  owner: safety-engineer
  labels: [safety-testing, collision-avoidance, emergency-stop]
  severity: high
  work_type: validation
links:
  parents: [R-COLLISION-AVOIDANCE]
  children: []
EOF
```

### Step 4: Generate and Execute Commands

```bash
# Validate the planning hierarchy
todowrite todowrite validate-plan --strict
todowrite todowrite trace-links

# Generate command stubs from Acceptance Criteria
todowrite todowrite generate-commands

# Review generated commands
ls configs/commands/
# Should show: CMD-POSITION-ACCURACY-VERIFIED.yaml, CMD-COLLISION-PREVENTION-TESTED.yaml

# Execute validation commands
todowrite todowrite execute-commands --all --dry-run  # Review first
todowrite todowrite execute-commands --all            # Execute tests
```

## Scenario 2: Web Application Development

### Project Structure for E-commerce Platform

```bash
# Goal: Modern e-commerce platform
cat > configs/plans/goals/GOAL-ECOMMERCE-PLATFORM.yaml << EOF
id: GOAL-ECOMMERCE-PLATFORM
layer: Goal
title: Next-Generation E-commerce Platform
description: >
  Build a scalable, secure e-commerce platform supporting 10,000+
  concurrent users, real-time inventory, mobile-first design,
  and integrated payment processing with 99.9% uptime.
metadata:
  owner: product-manager
  labels: [ecommerce, scalable, mobile-first, payments]
  severity: high
  work_type: architecture
links:
  parents: []
  children: []
EOF

# Concept: Microservices architecture
cat > configs/plans/concepts/CON-MICROSERVICES-ARCH.yaml << EOF
id: CON-MICROSERVICES-ARCH
layer: Concept
title: Cloud-Native Microservices Architecture
description: >
  Implement containerized microservices with API Gateway,
  event-driven communication, auto-scaling, and observability.
  Use Kubernetes for orchestration and service mesh for communication.
metadata:
  owner: solution-architect
  labels: [microservices, kubernetes, api-gateway, cloud-native]
  severity: high
  work_type: architecture
links:
  parents: [GOAL-ECOMMERCE-PLATFORM]
  children: []
EOF

# Requirements with specific acceptance criteria
cat > configs/plans/requirements/R-API-PERFORMANCE.yaml << EOF
id: R-API-PERFORMANCE
layer: Requirements
title: API Response Time Performance
description: >
  All API endpoints SHALL respond within 200ms for 95th percentile
  under normal load (1000 req/sec) and within 500ms for 99th
  percentile under peak load (5000 req/sec).
metadata:
  owner: backend-team
  labels: [performance, api, latency, load-testing]
  severity: high
  work_type: implementation
links:
  parents: [CON-MICROSERVICES-ARCH]
  children: []
EOF

cat > configs/plans/acceptance_criteria/AC-LOAD-TEST-PASSED.yaml << EOF
id: AC-LOAD-TEST-PASSED
layer: AcceptanceCriteria
title: Load testing confirms API performance requirements
description: >
  PASS: Load tests with k6 demonstrate 95th percentile < 200ms
  and 99th percentile < 500ms over 30-minute test duration.
  Error rate remains below 0.1%. CPU and memory usage stay
  within allocated resource limits.
  FAIL: Any performance metric exceeds specified thresholds.
metadata:
  owner: performance-engineer
  labels: [load-testing, k6, performance-validation]
  severity: high
  work_type: validation
links:
  parents: [R-API-PERFORMANCE]
  children: []
EOF
```

## Scenario 3: DevOps Pipeline Implementation

### CI/CD Pipeline with Security and Compliance

```bash
# Goal: Secure automated deployment pipeline
cat > configs/plans/goals/GOAL-SECURE-CICD.yaml << EOF
id: GOAL-SECURE-CICD
layer: Goal
title: Zero-Trust DevOps Pipeline
description: >
  Implement fully automated, secure CI/CD pipeline with security
  scanning, compliance validation, automated testing, and
  zero-downtime deployments across multiple environments.
metadata:
  owner: devops-lead
  labels: [cicd, security, zero-trust, automation]
  severity: high
  work_type: ops
links:
  parents: []
  children: []
EOF

# Requirements with security constraints
cat > configs/plans/constraints/CST-SECURITY-COMPLIANCE.yaml << EOF
id: CST-SECURITY-COMPLIANCE
layer: Constraints
title: Security and Compliance Requirements
description: >
  MANDATORY: SOC 2 Type II compliance. SAST/DAST scanning required.
  Container vulnerability scanning (no HIGH/CRITICAL). Secrets
  encrypted at rest and in transit. Audit logging for all deployments.
  Zero-trust network policies. Signed container images only.
metadata:
  owner: security-team
  labels: [security, compliance, soc2, scanning, zero-trust]
  severity: high
  work_type: validation
links:
  parents: [GOAL-SECURE-CICD]
  children: []
EOF

cat > configs/plans/acceptance_criteria/AC-SECURITY-GATES-ENFORCED.yaml << EOF
id: AC-SECURITY-GATES-ENFORCED
layer: AcceptanceCriteria
title: All security gates prevent vulnerable deployments
description: >
  PASS: Pipeline blocks deployments with HIGH/CRITICAL vulnerabilities,
  SAST scan passes with zero violations, secrets detection prevents
  commits with exposed credentials, and container images are signed
  and verified. SOC 2 compliance validated through automated checks.
  FAIL: Any security violation bypasses gates or compliance check fails.
metadata:
  owner: security-engineer
  labels: [security-gates, vulnerability-scanning, compliance]
  severity: high
  work_type: validation
links:
  parents: [CST-SECURITY-COMPLIANCE]
  children: []
EOF
```

## Best Practices

### 1. Hierarchical Linking Strategy

```yaml
# Always maintain proper parent-child relationships
links:
  parents: [PARENT-ID]  # Reference to higher layer
  children: []          # Will be populated by child nodes
```

### 2. Work-Type Tagging

Use consistent work-type labels:
- `architecture` - System design and high-level structure
- `implementation` - Code development and feature building
- `validation` - Testing, verification, and quality assurance
- `docs` - Documentation and knowledge management
- `ops` - Operations, deployment, and infrastructure

### 3. Acceptance Criteria Best Practices

```yaml
description: >
  PASS: [Specific, measurable success conditions]
  FAIL: [Clear failure conditions and thresholds]
```

### 4. Command Generation Strategy

Commands are automatically generated from Acceptance Criteria:
- Test commands for validation ACs
- Build commands for implementation ACs
- Deployment commands for ops ACs

## Validation Workflow

### Complete System Validation

```bash
# 1. Validate schema and structure
make tw-all

# 2. Check separation of concerns
todowrite todowrite check-soc

# 3. Analyze traceability
todowrite todowrite trace-links --summary

# 4. Generate and test commands
todowrite todowrite generate-commands
todowrite todowrite execute-commands --all

# 5. Final validation
make tw-check
```

### Continuous Integration Integration

```yaml
# .github/workflows/todowrite-validation.yml
name: ToDoWrite Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: make tw-deps
      - run: make tw-check
      - run: todowrite todowrite validate-plan --strict
      - run: todowrite todowrite trace-links
      - run: todowrite todowrite check-soc
```

## Migration from Legacy Systems

### From Traditional Project Management

1. **Map existing artifacts:**
   - Project charter → Goal
   - Requirements doc → Requirements layer
   - Test cases → Acceptance Criteria
   - Build scripts → Commands

2. **Use migration tool:**
   ```bash
   python todowrite/tools/migrate_todowrite.py --source legacy_project.json
   ```

3. **Validate migration:**
   ```bash
   make tw-check
   todowrite todowrite trace-links
   ```

## Troubleshooting

### Common Issues

1. **Schema Validation Errors**
   ```bash
   # Check specific file
   python todowrite/tools/tw_validate.py configs/plans/goals/GOAL-EXAMPLE.yaml
   ```

2. **Broken Traceability Links**
   ```bash
   # Analyze link issues
   todowrite todowrite trace-links --summary
   ```

3. **SoC Violations**
   ```bash
   # Check for executable content in declarative layers
   todowrite todowrite check-soc
   ```

## Advanced Features

### Custom Command Templates

Extend `tw_stub_command.py` to generate specialized commands for your domain:

```python
def _generate_custom_command(self, ac_data):
    if 'database' in ac_data.get('title', '').lower():
        return "python manage.py test --tag=database"
    elif 'security' in ac_data.get('title', '').lower():
        return "bandit -r . && safety check"
    # ... additional patterns
```

### Integration with External Tools

```bash
# Export to project management tools
todowrite todowrite show-hierarchy --format json > project_status.json

# Import traceability into monitoring
python scripts/export_traces.py trace/graph.json
```

This integration guide demonstrates how ToDoWrite's 12-layer framework scales from simple projects to complex, enterprise-level implementations while maintaining traceability and validation throughout the development lifecycle.
