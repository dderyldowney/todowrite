from graphviz import Digraph

uml = Digraph("UML_Diagram", format="png")
uml.attr(rankdir="TB")

# Define MasterStation class
uml.node(
    "MasterStation",
    """\
MasterStation
------------------------
- station_id: int
- system: str
------------------------
+ activate(): str
+ deactivate(): str
""",
    shape="rectangle",
)

# Define derived classes
uml.node(
    "DiagnosticsStation",
    """\
DiagnosticsStation
------------------------
- diagnostic_tools: list[str]
------------------------
+ run_diagnostics(): str
""",
    shape="rectangle",
)

uml.node(
    "DroidDispatchStation",
    """\
DroidDispatchStation
------------------------
- droid_count: int
------------------------
+ deploy_droid(): str
""",
    shape="rectangle",
)

uml.node(
    "ServiceDispatchStation",
    """\
ServiceDispatchStation
------------------------
- active_tasks: int
------------------------
+ assign_task(): str
""",
    shape="rectangle",
)

uml.node(
    "RepairStation",
    """\
RepairStation
------------------------
- repair_capacity: int
------------------------
+ perform_repair(): str
""",
    shape="rectangle",
)

# Define inheritance relationships
uml.edge("MasterStation", "DiagnosticsStation", arrowhead="empty")
uml.edge("MasterStation", "DroidDispatchStation", arrowhead="empty")
uml.edge("MasterStation", "ServiceDispatchStation", arrowhead="empty")
uml.edge("MasterStation", "RepairStation", arrowhead="empty")

# Render the diagram
uml.render("uml_masterstation", format="png", cleanup=True)
