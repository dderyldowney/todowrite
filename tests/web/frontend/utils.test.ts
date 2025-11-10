/**
 * Comprehensive tests for shared utilities using real implementations.
 * No mocking allowed - all tests use actual implementations.
 */

import {
  isValidNodeId,
  getLayerPrefix,
  generateNodeId,
  getStatusColor,
  getNextStatus,
  calculateProgress,
  getNodeDepth,
  getRootNodes,
  getLeafNodes,
  buildHierarchy,
  filterNodesByLayer,
  filterNodesByStatus,
  filterNodesByAssignee,
  searchNodes,
  formatDate,
  formatDateTime,
  isOverdue,
  validateNode,
  exportToJSON,
  exportToCSV,
  createNodeUrl,
  createSearchUrl,
} from '../index';
import {
  Node,
  NodeLayer,
  NodeStatus,
  NodeMetadata,
  NodeLinks,
  Command,
  CommandRun,
} from '../../types';

describe('Utils Tests - Real Implementations Only', () => {

  // Helper function to create test nodes
  const createTestNode = (
    id: string,
    layer: NodeLayer = NodeLayer.Task,
    status: NodeStatus = NodeStatus.Planned,
    title: string = 'Test Node',
    description: string = 'Test description',
    assignee?: string,
    labels?: string[],
    progress?: number
  ): Node => {
    const metadata: NodeMetadata = {};
    if (assignee) metadata.assignee = assignee;
    if (labels) metadata.labels = labels;

    return {
      id,
      layer,
      title,
      description,
      status,
      metadata: Object.keys(metadata).length > 0 ? metadata : undefined,
      progress,
      assignee,
      links: { parents: [], children: [] }
    };
  };

  describe('Node ID Utilities', () => {
    test('isValidNodeId should validate correct formats', () => {
      expect(isValidNodeId('GOAL-TEST123')).toBe(true);
      expect(isValidNodeId('CON-ABC_DEF')).toBe(true);
      expect(isValidNodeId('CMD-123456789')).toBe(true);
      expect(isValidNodeId('TSK-simple_test')).toBe(true);
    });

    test('isValidNodeId should reject incorrect formats', () => {
      expect(isValidNodeId('INVALID-ID')).toBe(false);
      expect(isValidNodeId('goal-test123')).toBe(false); // lowercase
      expect(isValidNodeId('GOAL')).toBe(false); // no suffix
      expect(isValidNodeId('')).toBe(false); // empty
      expect(isValidNodeId('GOAL-TEST-INVALID')).toBe(true); // actually valid format
    });

    test('getLayerPrefix should return correct prefixes', () => {
      expect(getLayerPrefix(NodeLayer.Goal)).toBe('GOAL');
      expect(getLayerPrefix(NodeLayer.Concept)).toBe('CON');
      expect(getLayerPrefix(NodeLayer.Command)).toBe('CMD');
      expect(getLayerPrefix(NodeLayer.Requirements)).toBe('R');
    });

    test('generateNodeId should create valid IDs', () => {
      const nodeId = generateNodeId(NodeLayer.Task);
      expect(nodeId).toStartWith('TSK-');
      expect(isValidNodeId(nodeId)).toBe(true);
      expect(nodeId.length).toBeGreaterThan(10);
    });

    test('generateNodeId should use custom suffix', () => {
      const customId = generateNodeId(NodeLayer.Goal, 'CUSTOM123');
      expect(customId).toBe('GOAL-CUSTOM123');
    });
  });

  describe('Status Utilities', () => {
    test('getStatusColor should return correct colors', () => {
      expect(getStatusColor(NodeStatus.Planned)).toBe('#6B7280');
      expect(getStatusColor(NodeStatus.InProgress)).toBe('#3B82F6');
      expect(getStatusColor(NodeStatus.Completed)).toBe('#10B981');
      expect(getStatusColor(NodeStatus.Blocked)).toBe('#EF4444');
      expect(getStatusColor(NodeStatus.Cancelled)).toBe('#9CA3AF');
    });

    test('getNextStatus should follow workflow', () => {
      expect(getNextStatus(NodeStatus.Planned)).toBe(NodeStatus.InProgress);
      expect(getNextStatus(NodeStatus.InProgress)).toBe(NodeStatus.Completed);
      expect(getNextStatus(NodeStatus.Completed)).toBe(NodeStatus.Completed);
      expect(getNextStatus(NodeStatus.Blocked)).toBe(NodeStatus.Planned);
      expect(getNextStatus(NodeStatus.Cancelled)).toBe(NodeStatus.Planned);
    });
  });

  describe('Progress Utilities', () => {
    test('calculateProgress should handle empty list', () => {
      expect(calculateProgress([])).toBe(0);
    });

    test('calculateProgress should calculate correctly', () => {
      const nodes = [
        createTestNode('TSK-1', NodeLayer.Task, NodeStatus.Completed),
        createTestNode('TSK-2', NodeLayer.Task, NodeStatus.Completed),
        createTestNode('TSK-3', NodeLayer.Task, NodeStatus.Planned),
        createTestNode('TSK-4', NodeLayer.Task, NodeStatus.InProgress),
      ];
      expect(calculateProgress(nodes)).toBe(50); // 2 out of 4 completed
    });

    test('calculateProgress should handle all completed', () => {
      const nodes = [
        createTestNode('TSK-1', NodeLayer.Task, NodeStatus.Completed),
        createTestNode('TSK-2', NodeLayer.Task, NodeStatus.Completed),
        createTestNode('TSK-3', NodeLayer.Task, NodeStatus.Completed),
      ];
      expect(calculateProgress(nodes)).toBe(100);
    });

    test('calculateProgress should handle none completed', () => {
      const nodes = [
        createTestNode('TSK-1', NodeLayer.Task, NodeStatus.Planned),
        createTestNode('TSK-2', NodeLayer.Task, NodeStatus.InProgress),
      ];
      expect(calculateProgress(nodes)).toBe(0);
    });
  });

  describe('Hierarchy Utilities', () => {
    test('getNodeDepth should calculate correct depth', () => {
      const root = createTestNode('GOAL-ROOT', NodeLayer.Goal);
      const child = createTestNode('TSK-CHILD', NodeLayer.Task);
      const grandchild = createTestNode('SUBTASK-GRANDCHILD', NodeLayer.SubTask);

      // Set up relationships
      root.links.children = ['TSK-CHILD'];
      child.links.parents = ['GOAL-ROOT'];
      child.links.children = ['SUBTASK-GRANDCHILD'];
      grandchild.links.parents = ['TSK-CHILD'];

      const allNodes = new Map([
        ['GOAL-ROOT', root],
        ['TSK-CHILD', child],
        ['SUBTASK-GRANDCHILD', grandchild],
      ]);

      expect(getNodeDepth(root, allNodes)).toBe(0);
      expect(getNodeDepth(child, allNodes)).toBe(1);
      expect(getNodeDepth(grandchild, allNodes)).toBe(2);
    });

    test('getRootNodes should identify root nodes', () => {
      const root1 = createTestNode('GOAL-ROOT1', NodeLayer.Goal);
      const root2 = createTestNode('GOAL-ROOT2', NodeLayer.Goal);
      const child = createTestNode('TSK-CHILD', NodeLayer.Task);
      child.links.parents = ['GOAL-ROOT1'];

      const nodes = [root1, root2, child];
      const roots = getRootNodes(nodes);

      expect(roots).toHaveLength(2);
      expect(roots).toContain(root1);
      expect(roots).toContain(root2);
      expect(roots).not.toContain(child);
    });

    test('getLeafNodes should identify leaf nodes', () => {
      const root = createTestNode('GOAL-ROOT', NodeLayer.Goal);
      const child1 = createTestNode('TSK-CHILD1', NodeLayer.Task);
      const child2 = createTestNode('TSK-CHILD2', NodeLayer.Task);
      const grandchild = createTestNode('SUBTASK-GRANDCHILD', NodeLayer.SubTask);

      // Set up relationships
      root.links.children = ['TSK-CHILD1', 'TSK-CHILD2'];
      child1.links.parents = ['GOAL-ROOT'];
      child2.links.parents = ['GOAL-ROOT'];
      child2.links.children = ['SUBTASK-GRANDCHILD'];
      grandchild.links.parents = ['TSK-CHILD2'];

      const nodes = [root, child1, child2, grandchild];
      const leaves = getLeafNodes(nodes);

      expect(leaves).toHaveLength(2);
      expect(leaves).toContain(child1);
      expect(leaves).toContain(grandchild);
      expect(leaves).not.toContain(root);
      expect(leaves).not.toContain(child2);
    });

    test('buildHierarchy should create correct mapping', () => {
      const parent = createTestNode('GOAL-PARENT', NodeLayer.Goal);
      const child1 = createTestNode('TSK-CHILD1', NodeLayer.Task);
      const child2 = createTestNode('TSK-CHILD2', NodeLayer.Task);

      // Set up relationships
      parent.links.children = ['TSK-CHILD1', 'TSK-CHILD2'];
      child1.links.parents = ['GOAL-PARENT'];
      child2.links.parents = ['GOAL-PARENT'];

      const nodes = [parent, child1, child2];
      const hierarchy = buildHierarchy(nodes);

      expect(hierarchy.get('GOAL-PARENT')).toHaveLength(2);
      expect(hierarchy.get('GOAL-PARENT')).toContain(child1);
      expect(hierarchy.get('GOAL-PARENT')).toContain(child2);
    });
  });

  describe('Filter Utilities', () => {
    test('filterNodesByLayer should filter correctly', () => {
      const nodes = [
        createTestNode('GOAL-1', NodeLayer.Goal),
        createTestNode('TSK-1', NodeLayer.Task),
        createTestNode('GOAL-2', NodeLayer.Goal),
        createTestNode('CON-1', NodeLayer.Concept),
      ];

      const goals = filterNodesByLayer(nodes, [NodeLayer.Goal]);
      expect(goals).toHaveLength(2);
      expect(goals.every(node => node.layer === NodeLayer.Goal)).toBe(true);

      const tasksAndConcepts = filterNodesByLayer(nodes, [NodeLayer.Task, NodeLayer.Concept]);
      expect(tasksAndConcepts).toHaveLength(2);
    });

    test('filterNodesByStatus should filter correctly', () => {
      const nodes = [
        createTestNode('TSK-1', NodeLayer.Task, NodeStatus.Planned),
        createTestNode('TSK-2', NodeLayer.Task, NodeStatus.Completed),
        createTestNode('TSK-3', NodeLayer.Task, NodeStatus.InProgress),
        createTestNode('TSK-4', NodeLayer.Task, NodeStatus.Completed),
      ];

      const completed = filterNodesByStatus(nodes, [NodeStatus.Completed]);
      expect(completed).toHaveLength(2);
      expect(completed.every(node => node.status === NodeStatus.Completed)).toBe(true);

      const plannedAndInProgress = filterNodesByStatus(
        nodes,
        [NodeStatus.Planned, NodeStatus.InProgress]
      );
      expect(plannedAndInProgress).toHaveLength(2);
    });

    test('filterNodesByAssignee should filter correctly', () => {
      const nodes = [
        createTestNode('TSK-1', NodeLayer.Task, NodeStatus.Planned, 'Task 1', 'Desc', 'alice'),
        createTestNode('TSK-2', NodeLayer.Task, NodeStatus.Completed, 'Task 2', 'Desc', 'bob'),
        createTestNode('TSK-3', NodeLayer.Task, NodeStatus.Planned, 'Task 3', 'Desc'), // No assignee
        createTestNode('TSK-4', NodeLayer.Task, NodeStatus.InProgress, 'Task 4', 'Desc', 'alice'),
      ];

      const aliceTasks = filterNodesByAssignee(nodes, 'alice');
      expect(aliceTasks).toHaveLength(2);
      expect(aliceTasks.every(node => node.assignee === 'alice')).toBe(true);
    });
  });

  describe('Search Utilities', () => {
    test('searchNodes should search by title', () => {
      const nodes = [
        createTestNode('GOAL-SEARCH1', NodeLayer.Goal, NodeStatus.Planned, 'Build web application'),
        createTestNode('TSK-SEARCH2', NodeLayer.Task, NodeStatus.Planned, 'Implement search functionality'),
        createTestNode('CON-SEARCH3', NodeLayer.Concept, NodeStatus.Planned, 'User interface design'),
      ];

      const webResults = searchNodes(nodes, 'web');
      expect(webResults).toHaveLength(1);
      expect(webResults[0].title).toContain('web');

      const searchResults = searchNodes(nodes, 'search');
      expect(searchResults).toHaveLength(1);
      expect(searchResults[0].title).toContain('search');
    });

    test('searchNodes should search by description', () => {
      const nodes = [
        createTestNode('GOAL-DESC1', NodeLayer.Goal, NodeStatus.Planned, 'Goal 1', 'Build amazing web features'),
        createTestNode('TSK-DESC2', NodeLayer.Task, NodeStatus.Planned, 'Task 2', 'Implement search functionality'),
      ];

      const featureResults = searchNodes(nodes, 'amazing');
      expect(featureResults).toHaveLength(1);
      expect(featureResults[0].description).toContain('amazing');

      const searchResults = searchNodes(nodes, 'search');
      expect(searchResults).toHaveLength(1);
      expect(searchResults[0].description).toContain('search');
    });

    test('searchNodes should search by ID', () => {
      const nodes = [
        createTestNode('GOAL-UNIQUE123', NodeLayer.Goal),
        createTestNode('TSK-UNIQUE456', NodeLayer.Task),
      ];

      const goalResults = searchNodes(nodes, 'GOAL-UNIQUE123');
      expect(goalResults).toHaveLength(1);
      expect(goalResults[0].id).toBe('GOAL-UNIQUE123');

      const partialResults = searchNodes(nodes, 'UNIQUE456');
      expect(partialResults).toHaveLength(1);
      expect(partialResults[0].id).toBe('TSK-UNIQUE456');
    });

    test('searchNodes should be case insensitive', () => {
      const nodes = [
        createTestNode('GOAL-CASE1', NodeLayer.Goal, NodeStatus.Planned, 'User Interface Design'),
        createTestNode('TSK-CASE2', NodeLayer.Task, NodeStatus.Planned, 'Database Schema'),
      ];

      const upperResults = searchNodes(nodes, 'INTERFACE');
      expect(upperResults).toHaveLength(1);

      const lowerResults = searchNodes(nodes, 'interface');
      expect(lowerResults).toHaveLength(1);

      const mixedResults = searchNodes(nodes, 'InTeRfAcE');
      expect(mixedResults).toHaveLength(1);
    });
  });

  describe('Date Utilities', () => {
    test('formatDate should format dates correctly', () => {
      const testDate = new Date('2023-12-25T14:30:00Z');
      expect(formatDate(testDate.toISOString())).toBe('12/25/2023');
      expect(formatDate('')).toBe('');
      expect(formatDate(undefined as any)).toBe('');
    });

    test('formatDateTime should format datetimes correctly', () => {
      const testDateTime = new Date('2023-12-25T14:30:45Z');
      const formatted = formatDateTime(testDateTime.toISOString());
      expect(formatted).toContain('12/25/2023');
      expect(formatted).toContain('2:30:45'); // Time format may vary by locale

      expect(formatDateTime('')).toBe('');
      expect(formatDateTime(undefined as any)).toBe('');
    });

    test('isOverdue should detect overdue nodes correctly', () => {
      // Not started node
      const notStarted = createTestNode('TSK-NOTSTARTED');
      expect(isOverdue(notStarted)).toBe(false);

      // Completed node
      const completed = createTestNode('TSK-COMPLETED', NodeLayer.Task, NodeStatus.Completed);
      (completed as any).started_date = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(); // 1 day ago
      expect(isOverdue(completed)).toBe(false);

      // Overdue node (started in past, not completed)
      const overdue = createTestNode('TSK-OVERDUE', NodeLayer.Task, NodeStatus.InProgress);
      (overdue as any).started_date = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(); // 1 day ago
      expect(isOverdue(overdue)).toBe(true);

      // Not overdue node (started today)
      const notOverdue = createTestNode('TSK-NOTOVERDUE', NodeLayer.Task, NodeStatus.InProgress);
      (notOverdue as any).started_date = new Date().toISOString();
      expect(isOverdue(notOverdue)).toBe(false);
    });
  });

  describe('Validation Utilities', () => {
    test('validateNode should validate correct nodes', () => {
      const validNode: Partial<Node> = {
        id: 'GOAL-VALID123',
        layer: NodeLayer.Goal,
        title: 'Valid Goal',
        description: 'A valid goal node',
        progress: 50
      };

      const result = validateNode(validNode);
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    test('validateNode should detect invalid ID', () => {
      const invalidNode: Partial<Node> = {
        id: 'INVALID-ID',
        layer: NodeLayer.Goal,
        title: 'Invalid Goal',
        description: 'Has invalid ID'
      };

      const result = validateNode(invalidNode);
      expect(result.valid).toBe(false);
      expect(result.errors.some(error => error.includes('Invalid node ID format'))).toBe(true);
    });

    test('validateNode should detect missing required fields', () => {
      const incompleteNode: Partial<Node> = {
        id: 'GOAL-INCOMPLETE123',
        layer: NodeLayer.Goal
        // Missing title and description
      };

      const result = validateNode(incompleteNode);
      expect(result.valid).toBe(false);
      expect(result.errors.some(error => error.includes('Title is required'))).toBe(true);
      expect(result.errors.some(error => error.includes('Description is required'))).toBe(true);
    });

    test('validateNode should detect invalid progress', () => {
      const invalidProgressNode: Partial<Node> = {
        id: 'TSK-INVALID123',
        layer: NodeLayer.Task,
        title: 'Invalid Progress',
        description: 'Has invalid progress',
        progress: 150 // Over 100
      };

      const result = validateNode(invalidProgressNode);
      expect(result.valid).toBe(false);
      expect(result.errors.some(error => error.includes('Progress must be between 0 and 100'))).toBe(true);
    });

    test('validateNode should validate command requirements', () => {
      // Command node without command
      const commandWithoutCommand: Partial<Node> = {
        id: 'CMD-INVALID123',
        layer: NodeLayer.Command,
        title: 'Invalid Command',
        description: 'Missing command'
      };

      let result = validateNode(commandWithoutCommand);
      expect(result.valid).toBe(false);
      expect(result.errors.some(error => error.includes('Command layer nodes must have a command'))).toBe(true);

      // Non-command node with command
      const command: Command = {
        ac_ref: 'AC-TEST123',
        run: { shell: 'echo test' } as CommandRun
      };

      const goalWithCommand: Partial<Node> = {
        id: 'GOAL-INVALID456',
        layer: NodeLayer.Goal,
        title: 'Invalid Goal',
        description: 'Should not have command',
        command
      };

      result = validateNode(goalWithCommand);
      expect(result.valid).toBe(false);
      expect(result.errors.some(error => error.includes('Only Command layer nodes can have a command'))).toBe(true);
    });
  });

  describe('Export Utilities', () => {
    test('exportToJSON should export nodes correctly', () => {
      const nodes = [
        createTestNode('GOAL-EXPORT1', NodeLayer.Goal, NodeStatus.Planned, 'Export Test Goal 1'),
        createTestNode('TSK-EXPORT2', NodeLayer.Task, NodeStatus.Planned, 'Export Test Task 2'),
      ];

      const jsonStr = exportToJSON(nodes);
      const exportedData = JSON.parse(jsonStr);

      expect(exportedData).toHaveLength(2);
      expect(exportedData[0].id).toBe('GOAL-EXPORT1');
      expect(exportedData[1].id).toBe('TSK-EXPORT2');
    });

    test('exportToCSV should export nodes correctly', () => {
      const nodes = [
        createTestNode('GOAL-CSV1', NodeLayer.Goal, NodeStatus.Completed, 'CSV Test Goal', 'Testing CSV export', 'test_user', ['important'], 100),
      ];

      const csvStr = exportToCSV(nodes);
      const lines = csvStr.split('\n');

      // Check header
      expect(lines[0]).toContain('ID');
      expect(lines[0]).toContain('Title');
      expect(lines[0]).toContain('Description');

      // Check data row
      expect(lines[1]).toContain('GOAL-CSV1');
      expect(lines[1]).toContain('CSV Test Goal');
    });
  });

  describe('URL Utilities', () => {
    test('createNodeUrl should create correct URLs', () => {
      expect(createNodeUrl('GOAL-TEST123')).toBe('/nodes/GOAL-TEST123');
      expect(createNodeUrl('TSK-ABC456')).toBe('/nodes/TSK-ABC456');
    });

    test('createProjectUrl should create correct URLs', () => {
      expect(createProjectUrl('PROJ-TEST123')).toBe('/projects/PROJ-TEST123');
    });

    test('createSearchUrl should create correct URLs', () => {
      const simpleUrl = createSearchUrl('test query');
      expect(simpleUrl).toContain('/search?q=test+query');

      const filteredUrl = createSearchUrl('test query', { layer: 'Task', status: 'completed' });
      expect(filteredUrl).toContain('/search?q=test+query');
      expect(filteredUrl).toContain('layer=Task');
      expect(filteredUrl).toContain('status=completed');
    });
  });

  describe('Integration Tests', () => {
    test('should handle complex workflow with real data', () => {
      // Create a realistic project structure
      const goal = createTestNode('GOAL-PROJECT', NodeLayer.Goal, NodeStatus.InProgress, 'Build Web App', 'Complete web application', 'project-manager', ['feature']);
      const phase1 = createTestNode('PH-DESIGN', NodeLayer.Phase, NodeStatus.Completed, 'Design Phase', 'Complete design work');
      const phase2 = createTestNode('PH-DEVELOP', NodeLayer.Phase, NodeStatus.InProgress, 'Development Phase', 'Implementation phase');
      const task1 = createTestNode('TSK-UI', NodeLayer.Task, NodeStatus.Completed, 'Build UI', 'User interface implementation', 'frontend-dev');
      const task2 = createTestNode('TSK-API', NodeLayer.Task, NodeStatus.InProgress, 'Build API', 'Backend API implementation', 'backend-dev');

      // Set up relationships
      goal.links.children = ['PH-DESIGN', 'PH-DEVELOP'];
      phase1.links.parents = ['GOAL-PROJECT'];
      phase1.links.children = ['TSK-UI'];
      phase2.links.parents = ['GOAL-PROJECT'];
      phase2.links.children = ['TSK-API'];
      task1.links.parents = ['PH-DESIGN'];
      task2.links.parents = ['PH-DEVELOP'];

      const allNodes = [goal, phase1, phase2, task1, task2];
      const nodeMap = new Map(allNodes.map(node => [node.id, node]));

      // Test hierarchy calculations
      expect(getNodeDepth(goal, nodeMap)).toBe(0);
      expect(getNodeDepth(phase1, nodeMap)).toBe(1);
      expect(getNodeDepth(task1, nodeMap)).toBe(2);

      // Test filtering
      const completedNodes = filterNodesByStatus(allNodes, [NodeStatus.Completed]);
      expect(completedNodes).toHaveLength(2);

      const tasks = filterNodesByLayer(allNodes, [NodeLayer.Task]);
      expect(tasks).toHaveLength(2);

      // Test search
      const apiResults = searchNodes(allNodes, 'API');
      expect(apiResults).toHaveLength(1);
      expect(apiResults[0].id).toBe('TSK-API');

      // Test progress calculation
      const projectProgress = calculateProgress(allNodes);
      expect(projectProgress).toBe(40); // 2 out of 5 completed

      // Test validation
      task2.title = '';
      const validation = validateNode(task2);
      expect(validation.valid).toBe(false);
      expect(validation.errors).toContain('Title is required');
    });
  });
});
