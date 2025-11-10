// Shared TypeScript types for ToDoWrite web frontend and backend communication

export type NodeLayer =
  | "Goal"
  | "Concept"
  | "Context"
  | "Constraints"
  | "Requirements"
  | "AcceptanceCriteria"
  | "InterfaceContract"
  | "Phase"
  | "Step"
  | "Task"
  | "SubTask"
  | "Command";

export type NodeStatus =
  | "planned"
  | "in_progress"
  | "completed"
  | "blocked"
  | "cancelled";

export type Severity =
  | "low"
  | "med"
  | "medium"
  | "high"
  | "critical";

export type WorkType =
  | "architecture"
  | "spec"
  | "interface"
  | "validation"
  | "implementation"
  | "development"
  | "docs"
  | "ops"
  | "refactor"
  | "chore"
  | "test";

export interface NodeMetadata {
  owner?: string;
  labels?: string[];
  severity?: Severity;
  work_type?: WorkType;
  assignee?: string;
  [key: string]: any;
}

export interface CommandRun {
  shell: string;
  workdir?: string;
  env?: Record<string, string>;
}

export interface Command {
  ac_ref: string;
  run: CommandRun;
  artifacts?: string[];
}

export interface NodeLinks {
  parents: string[];
  children: string[];
}

export interface Node {
  id: string;
  layer: NodeLayer;
  title: string;
  description: string;
  status?: NodeStatus;
  metadata?: NodeMetadata;
  progress?: number; // 0-100
  started_date?: string; // ISO datetime
  completion_date?: string; // ISO datetime
  assignee?: string;
  links: NodeLinks;
  command?: Command; // Only for Command layer nodes
  [key: string]: any;
}

// API request/response types
export interface CreateNodeRequest {
  layer: NodeLayer;
  title: string;
  description: string;
  status?: NodeStatus;
  metadata?: NodeMetadata;
  assignee?: string;
  parent_ids?: string[];
  command?: Command;
}

export interface UpdateNodeRequest {
  title?: string;
  description?: string;
  status?: NodeStatus;
  metadata?: NodeMetadata;
  progress?: number;
  started_date?: string;
  completion_date?: string;
  assignee?: string;
  command?: Command;
}

export interface NodeResponse {
  node: Node;
  children?: Node[];
  parents?: Node[];
}

export interface NodeListResponse {
  nodes: Node[];
  total: number;
  page: number;
  page_size: number;
}

export interface SearchRequest {
  query: string;
  layer?: NodeLayer;
  status?: NodeStatus;
  assignee?: string;
  labels?: string[];
  limit?: number;
  offset?: number;
}

export interface SearchResponse {
  nodes: Node[];
  total: number;
  query: string;
}

export interface ErrorResponse {
  error: string;
  message: string;
  details?: any;
}

// Project-level simplified types
export interface Project {
  id: string;
  title: string;
  description: string;
  status: NodeStatus;
  progress: number;
  node_count: number;
  completed_count: number;
  last_updated: string;
}

export interface ProjectListResponse {
  projects: Project[];
  total: number;
}

// API endpoint paths
export const API_PATHS = {
  NODES: '/api/v1/nodes',
  NODE: '/api/v1/nodes/:id',
  PROJECTS: '/api/v1/projects',
  SEARCH: '/api/v1/search',
  HEALTH: '/api/v1/health',
} as const;

// WebSocket message types
export interface WebSocketMessage {
  type: 'node_created' | 'node_updated' | 'node_deleted' | 'error';
  data: any;
  timestamp: string;
}

export interface NodeSubscription {
  node_ids?: string[];
  layer?: NodeLayer;
  project_id?: string;
}
