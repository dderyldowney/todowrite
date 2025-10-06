# `strategic-list` Command Documentation

## Purpose

The `strategic-list` command provides a clear and concise overview of all strategic objectives defined within the AFS FastAPI Dual TODO System. It displays both pending and completed strategic goals, along with their priority, ID, and category, offering a high-level view of the project's long-term direction.

## Usage

To view the list of strategic objectives, execute the `strategic-list` command from your project's root directory:

```bash
./bin/strategic-list
```

## Key Features

*   **Comprehensive Listing**: Displays all strategic objectives, regardless of their completion status.
*   **Status Indicators**: Clearly marks pending (○) and completed (●) objectives.
*   **Priority and Category**: Shows the priority (e.g., HIGH, MED) and category (e.g., docs, api, monitoring) for each objective.
*   **Completion Dates**: For completed objectives, the date of completion is provided.
*   **Summary**: Provides a quick summary of the total, pending, and completed strategic TODOs.
*   **Command Reference**: Offers guidance on how to add new strategic objectives or mark existing ones as completed.

## Agricultural Context

In the context of the AFS FastAPI Agricultural Robotics Platform, `strategic-list` is vital for:

*   **Strategic Alignment**: Ensuring that all development efforts remain aligned with the overarching strategic goals of the agricultural robotics platform.
*   **Roadmap Communication**: Clearly communicating the project roadmap to stakeholders, including agricultural engineers, robotics engineers, and AI specialists.
*   **Progress Tracking**: Monitoring progress against long-term strategic objectives, which is crucial for large-scale agricultural technology deployments.
*   **Compliance Planning**: Supporting the planning and tracking of objectives related to compliance with agricultural standards like ISO 18497 and ISO 11783.

## Example Output

```
=== AFS FastAPI Strategic TODOs ===

 1. ○ [HIGH] Create comprehensive user documentation for agricultural engineers
     ID: strategic-006 | Category: docs

 2. ○ [MED]  Implement cloud integration for agricultural data services
     ID: strategic-003 | Category: api

 3. ○ [MED]  Add IoT sensor network integration with guaranteed delivery
     ID: strategic-004 | Category: monitoring

 4. ● [HIGH] Phase 6 ISOBUS guaranteed delivery - COMPLETE (enterprise-grade reliability achieved)
     ID: strategic-001 | Category: equipment
     Completed: 2025-10-03

 ... and 8 more completed objectives

=== Summary ===
Total Strategic TODOs: 12
Pending: 3 | Completed: 9
Last Updated: 2025-10-06T15:44:26Z

Use './bin/strategic-add "Description"' to add new strategic objectives.
Use './bin/strategic-complete "Objective"' to mark objectives as completed.
```
