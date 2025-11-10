/**
 * Comprehensive tests for TypeScript types using real implementations.
 * Tests type definitions, interfaces, and type guards.
 */

import {
  Node,
  NodeLayer,
  NodeStatus,
  Severity,
  WorkType,
  NodeMetadata,
  Command,
  CommandRun,
  NodeLinks,
  CreateNodeRequest,
  UpdateNodeRequest,
  NodeResponse,
  NodeListResponse,
  SearchRequest,
  SearchResponse,
  ErrorResponse,
  Project,
  WebSocketMessage,
  NodeSubscription,
  API_PATHS,
} from '../index';

describe('Type Definitions Tests - Real Implementations Only', () => {

  describe('Node Types', () => {
    test('should create valid Node with minimal fields', () => {
      const node: Node = {
        id: 'GOAL-TEST123',
        layer: NodeLayer.Goal,
        title: 'Test Goal',
        description: 'A test goal',
        links: { parents: [], children: [] }
      };

      expect(node.id).toBe('GOAL-TEST123');
      expect(node.layer).toBe(NodeLayer.Goal);
      expect(node.title).toBe('Test Goal');
      expect(node.description).toBe('A test goal');
      expect(node.links.parents).toEqual([]);
      expect(node.links.children).toEqual([]);
      expect(node.status).toBeUndefined(); // Optional field
    });

    test('should create complete Node with all fields', () => {
      const startedDate = '2023-12-25T10:00:00Z';
      const command: Command = {
        ac_ref: 'AC-TEST123',
        run: { shell: 'echo hello', workdir: '/tmp' }
      };

      const node: Node = {
        id: 'TSK-COMPLETE456',
        layer: NodeLayer.Task,
        title: 'Complete Task',
        description: 'A complete task with all fields',
        status: NodeStatus.InProgress,
        metadata: {
          owner: 'test_owner',
          labels: ['important', 'urgent'],
          severity: Severity.High,
          work_type: WorkType.Development,
          assignee: 'developer'
        },
        progress: 75,
        started_date: startedDate,
        assignee: 'developer',
        links: {
          parents: ['GOAL-PARENT'],
          children: ['SUBTASK-CHILD']
        }
      };

      expect(node.id).toBe('TSK-COMPLETE456');
      expect(node.layer).toBe(NodeLayer.Task);
      expect(node.status).toBe(NodeStatus.InProgress);
      expect(node.metadata?.owner).toBe('test_owner');
      expect(node.metadata?.labels).toEqual(['important', 'urgent']);
      expect(node.progress).toBe(75);
      expect(node.started_date).toBe(startedDate);
    });

    test('should create Command Node correctly', () => {
      const command: Command = {
        ac_ref: 'AC-COMMAND123',
        run: {
          shell: 'npm test',
          workdir: '/app',
          env: { NODE_ENV: 'test' }
        },
        artifacts: ['test-results.xml', 'coverage-report.html']
      };

      const commandNode: Node = {
        id: 'CMD-TEST123',
        layer: NodeLayer.Command,
        title: 'Test Command',
        description: 'Run test suite',
        status: NodeStatus.Planned,
        links: { parents: [], children: [] },
        command
      };

      expect(commandNode.command?.ac_ref).toBe('AC-COMMAND123');
      expect(commandNode.command?.run.shell).toBe('npm test');
      expect(commandNode.command?.run.workdir).toBe('/app');
      expect(commandNode.command?.run.env?.NODE_ENV).toBe('test');
      expect(commandNode.command?.artifacts).toEqual(['test-results.xml', 'coverage-report.html']);
    });
  });

  describe('NodeMetadata Types', () => {
    test('should create empty metadata', () => {
      const metadata: NodeMetadata = {};
      expect(Object.keys(metadata)).toHaveLength(0);
    });

    test('should create metadata with all fields', () => {
      const metadata: NodeMetadata = {
        owner: 'project_manager',
        labels: ['feature', 'high-priority'],
        severity: Severity.Critical,
        work_type: WorkType.Architecture,
        assignee: 'lead_developer',
        custom_field: 'custom_value' // Additional properties allowed
      };

      expect(metadata.owner).toBe('project_manager');
      expect(metadata.labels).toEqual(['feature', 'high-priority']);
      expect(metadata.severity).toBe(Severity.Critical);
      expect(metadata.work_type).toBe(WorkType.Architecture);
      expect(metadata.assignee).toBe('lead_developer');
      expect((metadata as any).custom_field).toBe('custom_value');
    });
  });

  describe('Command Types', () => {
    test('should create minimal command', () => {
      const command: Command = {
        ac_ref: 'AC-MINIMAL123',
        run: { shell: 'echo "hello world"' }
      };

      expect(command.ac_ref).toBe('AC-MINIMAL123');
      expect(command.run.shell).toBe('echo "hello world"');
      expect(command.run.workdir).toBeUndefined();
      expect(command.artifacts).toBeUndefined();
    });

    test('should create full command', () => {
      const command: Command = {
        ac_ref: 'AC-FULL456',
        run: {
          shell: 'make build && make test',
          workdir: '/project',
          env: {
            'NODE_ENV': 'production',
            'DEBUG': 'true'
          }
        },
        artifacts: ['build.log', 'test-results.json', 'coverage.lcov']
      };

      expect(command.run.shell).toBe('make build && make test');
      expect(command.run.workdir).toBe('/project');
      expect(command.run.env?.NODE_ENV).toBe('production');
      expect(command.run.env?.DEBUG).toBe('true');
      expect(command.artifacts).toHaveLength(3);
    });
  });

  describe('API Request Types', () => {
    test('should create CreateNodeRequest', () => {
      const request: CreateNodeRequest = {
        layer: NodeLayer.Concept,
        title: 'New Concept',
        description: 'A new concept for the project',
        status: NodeStatus.Planned,
        parent_ids: ['GOAL-PARENT1', 'GOAL-PARENT2']
      };

      expect(request.layer).toBe(NodeLayer.Concept);
      expect(request.title).toBe('New Concept');
      expect(request.status).toBe(NodeStatus.Planned);
      expect(request.parent_ids).toEqual(['GOAL-PARENT1', 'GOAL-PARENT2']);
    });

    test('should create UpdateNodeRequest with partial data', () => {
      const request: UpdateNodeRequest = {
        title: 'Updated Title',
        status: NodeStatus.Completed,
        progress: 100
      };

      expect(request.title).toBe('Updated Title');
      expect(request.status).toBe(NodeStatus.Completed);
      expect(request.progress).toBe(100);
      expect(request.description).toBeUndefined();
    });
  });

  describe('API Response Types', () => {
    test('should create NodeResponse', () => {
      const node: Node = {
        id: 'GOAL-RESPONSE123',
        layer: NodeLayer.Goal,
        title: 'Response Goal',
        description: 'Goal for response test',
        links: { parents: [], children: [] }
      };

      const response: NodeResponse = {
        node,
        children: [],
        parents: []
      };

      expect(response.node.id).toBe('GOAL-RESPONSE123');
      expect(response.children).toEqual([]);
      expect(response.parents).toEqual([]);
    });

    test('should create NodeListResponse', () => {
      const nodes: Node[] = [
        {
          id: 'TSK-LIST1',
          layer: NodeLayer.Task,
          title: 'Task 1',
          description: 'First task',
          links: { parents: [], children: [] }
        },
        {
          id: 'TSK-LIST2',
          layer: NodeLayer.Task,
          title: 'Task 2',
          description: 'Second task',
          links: { parents: [], children: [] }
        }
      ];

      const response: NodeListResponse = {
        nodes,
        total: 2,
        page: 1,
        page_size: 10
      };

      expect(response.nodes).toHaveLength(2);
      expect(response.total).toBe(2);
      expect(response.page).toBe(1);
      expect(response.page_size).toBe(10);
    });

    test('should create SearchResponse', () => {
      const nodes: Node[] = [
        {
          id: 'GOAL-SEARCH1',
          layer: NodeLayer.Goal,
          title: 'Search Result Goal',
          description: 'Found in search',
          links: { parents: [], children: [] }
        }
      ];

      const response: SearchResponse = {
        nodes,
        total: 1,
        query: 'search term'
      };

      expect(response.nodes).toHaveLength(1);
      expect(response.total).toBe(1);
      expect(response.query).toBe('search term');
    });

    test('should create ErrorResponse', () => {
      const response: ErrorResponse = {
        error: 'ValidationError',
        message: 'Invalid input data',
        details: {
          field: 'title',
          issue: 'Title is required'
        }
      };

      expect(response.error).toBe('ValidationError');
      expect(response.message).toBe('Invalid input data');
      expect(response.details?.field).toBe('title');
    });
  });

  describe('Project Types', () => {
    test('should create Project', () => {
      const lastUpdated = '2023-12-25T15:30:00Z';
      const project: Project = {
        id: 'PROJ-PROJECT123',
        title: 'Test Project',
        description: 'A test project',
        status: NodeStatus.InProgress,
        progress: 65,
        node_count: 15,
        completed_count: 10,
        last_updated: lastUpdated
      };

      expect(project.id).toBe('PROJ-PROJECT123');
      expect(project.title).toBe('Test Project');
      expect(project.status).toBe(NodeStatus.InProgress);
      expect(project.progress).toBe(65);
      expect(project.node_count).toBe(15);
      expect(project.completed_count).toBe(10);
      expect(project.last_updated).toBe(lastUpdated);
    });
  });

  describe('WebSocket Types', () => {
    test('should create WebSocketMessage', () => {
      const message: WebSocketMessage = {
        type: 'node_created',
        data: {
          node: {
            id: 'GOAL-WS123',
            layer: NodeLayer.Goal,
            title: 'WebSocket Goal',
            description: 'Created via WebSocket',
            links: { parents: [], children: [] }
          }
        },
        timestamp: '2023-12-25T16:45:00Z'
      };

      expect(message.type).toBe('node_created');
      expect(message.data.node.id).toBe('GOAL-WS123');
      expect(message.timestamp).toBe('2023-12-25T16:45:00Z');
    });

    test('should create NodeSubscription', () => {
      const subscription: NodeSubscription = {
        node_ids: ['GOAL-SUB1', 'GOAL-SUB2'],
        layer: NodeLayer.Goal,
        project_id: 'PROJ-PROJECT123'
      };

      expect(subscription.node_ids).toEqual(['GOAL-SUB1', 'GOAL-SUB2']);
      expect(subscription.layer).toBe(NodeLayer.Goal);
      expect(subscription.project_id).toBe('PROJ-PROJECT123');
    });
  });

  describe('Constants', () => {
    test('should have correct API paths', () => {
      expect(API_PATHS.NODES).toBe('/api/v1/nodes');
      expect(API_PATHS.NODE).toBe('/api/v1/nodes/:id');
      expect(API_PATHS.PROJECTS).toBe('/api/v1/projects');
      expect(API_PATHS.SEARCH).toBe('/api/v1/search');
      expect(API_PATHS.HEALTH).toBe('/api/v1/health');
    });
  });

  describe('Type Safety Tests', () => {
    test('should enforce NodeLayer enum values', () => {
      const validLayers: NodeLayer[] = [
        NodeLayer.Goal,
        NodeLayer.Concept,
        NodeLayer.Context,
        NodeLayer.Constraints,
        NodeLayer.Requirements,
        NodeLayer.AcceptanceCriteria,
        NodeLayer.InterfaceContract,
        NodeLayer.Phase,
        NodeLayer.Step,
        NodeLayer.Task,
        NodeLayer.SubTask,
        NodeLayer.Command
      ];

      expect(validLayers).toHaveLength(12);

      // Test that each layer has expected string value
      expect(NodeLayer.Goal).toBe('Goal');
      expect(NodeLayer.Command).toBe('Command');
      expect(NodeLayer.Requirements).toBe('Requirements');
    });

    test('should enforce NodeStatus enum values', () => {
      const validStatuses: NodeStatus[] = [
        NodeStatus.Planned,
        NodeStatus.InProgress,
        NodeStatus.Completed,
        NodeStatus.Blocked,
        NodeStatus.Cancelled
      ];

      expect(validStatuses).toHaveLength(5);
      expect(NodeStatus.Planned).toBe('planned');
      expect(NodeStatus.Completed).toBe('completed');
    });

    test('should enforce Severity enum values', () => {
      const validSeverities: Severity[] = [
        Severity.Low,
        Severity.Med,
        Severity.Medium,
        Severity.High,
        Severity.Critical
      ];

      expect(validSeverities).toHaveLength(5);
      expect(Severity.Critical).toBe('critical');
      expect(Severity.Low).toBe('low');
    });

    test('should enforce WorkType enum values', () => {
      const validWorkTypes: WorkType[] = [
        WorkType.Architecture,
        WorkType.Spec,
        WorkType.Interface,
        WorkType.Validation,
        WorkType.Implementation,
        WorkType.Development,
        WorkType.Docs,
        WorkType.Ops,
        WorkType.Refactor,
        WorkType.Chore,
        WorkType.Test
      ];

      expect(validWorkTypes).toHaveLength(11);
      expect(WorkType.Development).toBe('development');
      expect(WorkType.Test).toBe('test');
    });
  });

  describe('Type Compatibility Tests', () => {
    test('should allow additional properties on Node', () => {
      const node: Node = {
        id: 'GOAL-EXTRA123',
        layer: NodeLayer.Goal,
        title: 'Goal with extras',
        description: 'Has additional properties',
        links: { parents: [], children: [] },
        custom_field: 'custom value',
        another_field: 42
      } as Node;

      expect((node as any).custom_field).toBe('custom value');
      expect((node as any).another_field).toBe(42);
    });

    test('should allow additional properties on NodeMetadata', () => {
      const metadata: NodeMetadata = {
        owner: 'test_owner',
        custom_property: 'custom value',
        numeric_property: 123
      };

      expect(metadata.owner).toBe('test_owner');
      expect((metadata as any).custom_property).toBe('custom value');
      expect((metadata as any).numeric_property).toBe(123);
    });
  });

  describe('Search Request Types', () => {
    test('should create SearchRequest with filters', () => {
      const searchRequest: SearchRequest = {
        query: 'important tasks',
        layer: NodeLayer.Task,
        status: NodeStatus.InProgress,
        assignee: 'developer',
        labels: ['urgent', 'bug'],
        limit: 50,
        offset: 0
      };

      expect(searchRequest.query).toBe('important tasks');
      expect(searchRequest.layer).toBe(NodeLayer.Task);
      expect(searchRequest.status).toBe(NodeStatus.InProgress);
      expect(searchRequest.assignee).toBe('developer');
      expect(searchRequest.labels).toEqual(['urgent', 'bug']);
      expect(searchRequest.limit).toBe(50);
      expect(searchRequest.offset).toBe(0);
    });

    test('should create minimal SearchRequest', () => {
      const searchRequest: SearchRequest = {
        query: 'test'
      };

      expect(searchRequest.query).toBe('test');
      expect(searchRequest.layer).toBeUndefined();
      expect(searchRequest.status).toBeUndefined();
      expect(searchRequest.limit).toBeUndefined();
      expect(searchRequest.offset).toBeUndefined();
    });
  });

  describe('Real-world Integration Tests', () => {
    test('should handle complete workflow with all types', () => {
      // Create a complete project structure using all types
      const goal: Node = {
        id: 'GOAL-WORKFLOW123',
        layer: NodeLayer.Goal,
        title: 'Complete Web Application',
        description: 'Build a complete web application with all features',
        status: NodeStatus.InProgress,
        metadata: {
          owner: 'product_manager',
          labels: ['feature', 'high-priority'],
          severity: Severity.High,
          work_type: WorkType.Development
        },
        progress: 45,
        links: { parents: [], children: ['PH-DESIGN', 'PH-DEVELOP'] }
      };

      const createRequest: CreateNodeRequest = {
        layer: NodeLayer.Task,
        title: 'Implement User Authentication',
        description: 'Add login and registration functionality',
        status: NodeStatus.Planned,
        metadata: {
          assignee: 'backend_developer',
          work_type: WorkType.Implementation
        },
        parent_ids: ['PH-DEVELOP']
      };

      const updateRequest: UpdateNodeRequest = {
        status: NodeStatus.InProgress,
        progress: 25,
        started_date: new Date().toISOString()
      };

      const searchRequest: SearchRequest = {
        query: 'authentication',
        layer: NodeLayer.Task,
        status: NodeStatus.InProgress
      };

      const searchResponse: SearchResponse = {
        nodes: [goal],
        total: 1,
        query: 'authentication'
      };

      const project: Project = {
        id: 'PROJ-WEBAPP123',
        title: 'Web Application Project',
        description: 'Complete web application development',
        status: NodeStatus.InProgress,
        progress: 45,
        node_count: 25,
        completed_count: 11,
        last_updated: new Date().toISOString()
      };

      const wsMessage: WebSocketMessage = {
        type: 'node_updated',
        data: {
          node_id: goal.id,
          changes: updateRequest
        },
        timestamp: new Date().toISOString()
      };

      // Verify all types are working together correctly
      expect(goal.id).toStartWith('GOAL-');
      expect(createRequest.layer).toBe(NodeLayer.Task);
      expect(updateRequest.status).toBe(NodeStatus.InProgress);
      expect(searchRequest.query).toBe('authentication');
      expect(searchResponse.nodes).toHaveLength(1);
      expect(project.progress).toBe(45);
      expect(wsMessage.type).toBe('node_updated');
      expect(wsMessage.data.node_id).toBe(goal.id);
    });
  });
});
